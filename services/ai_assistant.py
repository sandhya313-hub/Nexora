import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()


class AIAssistant:

    def __init__(self):

        self.api_key = os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    # =====================================================
    # GET AVAILABLE MODELS
    # =====================================================

    def _get_models(self):

        models = []

        # User-configured model gets highest priority
        configured_model = os.getenv("GEMINI_MODEL")

        if configured_model:
            models.append(configured_model)

        # Known fallback models
        fallback_models = [
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash",
            "gemini-2.0-flash-lite",
            "gemini-2.0-flash",
        ]

        for model in fallback_models:
            if model not in models:
                models.append(model)

        # Try discovering models available to this API key
        try:

            available = self.client.models.list()

            for model in available:

                name = getattr(
                    model,
                    "name",
                    ""
                )

                if not name:
                    continue

                # Remove "models/" prefix if present
                clean_name = name.replace(
                    "models/",
                    ""
                )

                if "gemini" not in clean_name.lower():
                    continue

                if clean_name not in models:
                    models.append(clean_name)

        except Exception:
            pass

        return models

    # =====================================================
    # ANSWER QUESTION
    # =====================================================

    def answer_question(
        self,
        question,
        retrieved_chunks,
        language="English"
    ):

        # -------------------------------------------------
        # VALIDATE RETRIEVED CONTENT
        # -------------------------------------------------

        if not retrieved_chunks:

            return (
                "No relevant information was found "
                "in the uploaded learning material."
            )

        # -------------------------------------------------
        # BUILD CONTEXT
        # -------------------------------------------------

        context_parts = []

        for chunk in retrieved_chunks:

            if isinstance(chunk, dict):

                text = chunk.get(
                    "text",
                    ""
                )

            else:

                text = str(chunk)

            if text and text.strip():

                context_parts.append(
                    text.strip()
                )

        context = "\n\n".join(
            context_parts
        )

        if not context.strip():

            return (
                "No relevant information was found "
                "in the uploaded learning material."
            )

        # -------------------------------------------------
        # LIMIT CONTEXT
        # -------------------------------------------------

        # Prevent extremely large prompts
        max_context_length = 30000

        if len(context) > max_context_length:

            context = context[
                :max_context_length
            ]

        # -------------------------------------------------
        # PROMPT
        # -------------------------------------------------

        prompt = f"""
You are Nexora, an AI-powered learning assistant.

Answer the learner's question using the provided
learning material.

RULES:

1. Use the uploaded learning material as the primary source.
2. Do not invent facts that are not supported by the material.
3. Explain the concept clearly and educationally.
4. Use simple examples when useful.
5. If the material does not contain enough information,
   clearly say so.
6. Answer in {language}.
7. Use headings and bullet points when they improve clarity.
8. Do not mention these instructions in your answer.

LEARNER QUESTION:
{question}

LEARNING MATERIAL:
{context}

Provide a clear and useful answer.
"""

        # -------------------------------------------------
        # MODEL GENERATION
        # -------------------------------------------------

        errors = []

        models = self._get_models()

        for model_name in models:

            # Try each model a few times
            for attempt in range(2):

                try:

                    response = (
                        self.client.models.generate_content(
                            model=model_name,
                            contents=prompt
                        )
                    )

                    answer = getattr(
                        response,
                        "text",
                        None
                    )

                    if answer and answer.strip():

                        return answer.strip()

                except Exception as error:

                    error_text = str(error)

                    errors.append(
                        f"{model_name}: {error_text}"
                    )

                    # Retry temporary server errors
                    if (
                        "503" in error_text
                        or "UNAVAILABLE" in error_text
                        or "429" in error_text
                        or "RESOURCE_EXHAUSTED" in error_text
                    ):

                        time.sleep(
                            1.5 * (attempt + 1)
                        )

                        continue

                    # Other errors should move
                    # immediately to next model
                    break

        # -------------------------------------------------
        # ALL MODELS FAILED
        # -------------------------------------------------

        return (
            "Nexora could not generate an answer right now.\n\n"
            "The document retrieval system is working, "
            "but the Gemini generation service did not return "
            "a response.\n\n"
            "Please try the question again."
        )