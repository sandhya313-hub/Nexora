import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class AssessmentEngine:

    def __init__(self, api_key=None):

        self.api_key = (
            api_key
            or os.getenv("GOOGLE_API_KEY")
        )

        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

        # -------------------------------------------------
        # Models that are actually available in your API
        # -------------------------------------------------
        self.models = [
            "gemini-3.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-3.1-flash-lite",
            "gemini-2.5-flash-lite",
            "gemini-flash-lite-latest",
        ]


    # =====================================================
    # GENERATE QUESTIONS
    # =====================================================

    def generate_questions(
        self,
        context,
        num_questions=5,
        difficulty="Intermediate"
    ):

        # -------------------------------------------------
        # Validate question count
        # -------------------------------------------------

        try:
            num_questions = int(num_questions)
        except Exception:
            num_questions = 5

        num_questions = max(
            1,
            min(num_questions, 20)
        )

        # -------------------------------------------------
        # Validate context
        # -------------------------------------------------

        if not context or not str(context).strip():

            raise ValueError(
                "No learning material was provided."
            )

        context = str(context)

        # Prevent excessively large prompt
        max_context_length = 30000

        if len(context) > max_context_length:

            context = context[
                :max_context_length
            ]

        # -------------------------------------------------
        # JSON SCHEMA
        # -------------------------------------------------

        question_schema = {
            "type": "array",
            "minItems": num_questions,
            "maxItems": num_questions,
            "items": {
                "type": "object",
                "properties": {

                    "question": {
                        "type": "string"
                    },

                    "options": {
                        "type": "array",
                        "minItems": 4,
                        "maxItems": 4,
                        "items": {
                            "type": "string"
                        }
                    },

                    "answer": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 3
                    }
                },

                "required": [
                    "question",
                    "options",
                    "answer"
                ]
            }
        }

        # -------------------------------------------------
        # PROMPT
        # -------------------------------------------------

        prompt = f"""
You are Nexora, an expert AI educational assessment generator.

Generate EXACTLY {num_questions} multiple-choice questions
from the learning material provided below.

Difficulty level:
{difficulty}

STRICT REQUIREMENTS:

1. Generate exactly {num_questions} questions.
2. Every question must be based ONLY on the learning material.
3. Every question must have exactly 4 options.
4. Every question must have exactly ONE correct answer.
5. The answer field must contain:
   0 for option 1
   1 for option 2
   2 for option 3
   3 for option 4
6. Do not repeat questions.
7. Questions should test understanding of the material.
8. Do not invent information outside the material.
9. Return only the requested JSON structure.
10. Do not include explanations.
11. Do not include Markdown.
12. Do not generate fewer than {num_questions} questions.

LEARNING MATERIAL:

{context}
"""

        errors = []

        # -------------------------------------------------
        # TRY AVAILABLE MODELS
        # -------------------------------------------------

        for model_name in self.models:

            # Retry temporary 503 / 429 failures
            for attempt in range(2):

                try:

                    response = (
                        self.client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                response_schema=question_schema
                            )
                        )
                    )

                    text = getattr(
                        response,
                        "text",
                        ""
                    )

                    if not text:
                        raise ValueError(
                            "Model returned an empty response."
                        )

                    questions = self._parse_questions(
                        text
                    )

                    questions = self._validate_questions(
                        questions
                    )

                    # -------------------------------------------------
                    # SUCCESS
                    # -------------------------------------------------

                    if len(questions) >= num_questions:

                        return questions[
                            :num_questions
                        ]

                    errors.append(
                        f"{model_name}: generated "
                        f"{len(questions)} instead of "
                        f"{num_questions}"
                    )

                    break

                except Exception as error:

                    error_text = str(error)

                    errors.append(
                        f"{model_name}: {error_text}"
                    )

                    # Temporary service errors
                    if (
                        "503" in error_text
                        or "UNAVAILABLE" in error_text
                        or "429" in error_text
                        or "RESOURCE_EXHAUSTED" in error_text
                    ):

                        if attempt == 0:

                            time.sleep(2)

                            continue

                    # Model unavailable / not found
                    # immediately move to next model
                    break

        # -------------------------------------------------
        # ALL MODELS FAILED
        # -------------------------------------------------

        error_summary = " | ".join(
            errors
        )

        raise RuntimeError(
            "Assessment AI generation failed.\n\n"
            + error_summary
        )


    # =====================================================
    # PARSE QUESTIONS
    # =====================================================

    def _parse_questions(
        self,
        text
    ):

        if not text:
            return []

        text = text.strip()

        # -------------------------------------------------
        # Remove accidental Markdown fences
        # -------------------------------------------------

        if text.startswith("```"):

            text = text.replace(
                "```json",
                "",
                1
            )

            text = text.replace(
                "```",
                ""
            )

            text = text.strip()

        # -------------------------------------------------
        # Parse JSON
        # -------------------------------------------------

        try:

            data = json.loads(
                text
            )

            if isinstance(
                data,
                list
            ):

                return data

        except Exception:

            pass

        # -------------------------------------------------
        # Try extracting JSON array
        # -------------------------------------------------

        start = text.find("[")
        end = text.rfind("]")

        if start != -1 and end != -1:

            try:

                data = json.loads(
                    text[
                        start:end + 1
                    ]
                )

                if isinstance(
                    data,
                    list
                ):

                    return data

            except Exception:

                pass

        return []


    # =====================================================
    # VALIDATE QUESTIONS
    # =====================================================

    def _validate_questions(
        self,
        questions
    ):

        valid_questions = []

        if not isinstance(
            questions,
            list
        ):

            return []

        for question in questions:

            if not isinstance(
                question,
                dict
            ):

                continue

            question_text = question.get(
                "question"
            )

            options = question.get(
                "options"
            )

            answer = question.get(
                "answer"
            )

            # -------------------------------------------------
            # Validate question text
            # -------------------------------------------------

            if not question_text:
                continue

            # -------------------------------------------------
            # Validate options
            # -------------------------------------------------

            if not isinstance(
                options,
                list
            ):

                continue

            if len(options) != 4:
                continue

            if any(
                not str(option).strip()
                for option in options
            ):

                continue

            # -------------------------------------------------
            # Validate answer
            # -------------------------------------------------

            if isinstance(
                answer,
                bool
            ):

                continue

            if not isinstance(
                answer,
                int
            ):

                continue

            if answer < 0 or answer > 3:
                continue

            # -------------------------------------------------
            # Create clean question
            # -------------------------------------------------

            clean_question = {

                "question":
                    str(
                        question_text
                    ).strip(),

                "options": [
                    str(option).strip()
                    for option in options
                ],

                "answer":
                    answer
            }

            valid_questions.append(
                clean_question
            )

        return valid_questions


    # =====================================================
    # EVALUATE ASSESSMENT
    # =====================================================

    def evaluate(
        self,
        questions,
        answers
    ):

        total = len(
            questions
        )

        correct = 0

        results = []

        for index, question in enumerate(
            questions
        ):

            correct_answer = question[
                "answer"
            ]

            user_answer = answers.get(
                index
            )

            is_correct = (
                user_answer == correct_answer
            )

            if is_correct:
                correct += 1

            results.append({

                "is_correct":
                    is_correct,

                "question":
                    question[
                        "question"
                    ],

                "correct_answer":
                    question[
                        "options"
                    ][correct_answer],

                "explanation":
                    (
                        "Correct answer."
                        if is_correct
                        else
                        "Review this concept "
                        "in the learning material."
                    )
            })

        score = 0

        if total > 0:

            score = round(
                (
                    correct / total
                ) * 100
            )

        return {

            "score":
                score,

            "correct":
                correct,

            "total":
                total,

            "results":
                results
        }