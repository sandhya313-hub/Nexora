import os
import streamlit as st

from dotenv import load_dotenv

from services.document_engine import DocumentEngine
from services.ai_assistant import AIAssistant


load_dotenv()


# =========================================================
# AI ASSISTANT PAGE
# =========================================================

def render_ai_assistant():

    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title("AI Assistant")

    st.caption(
        "Ask questions about your learning material "
        "and receive grounded explanations from Nexora."
    )

    st.divider()

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "document_engine" not in st.session_state:

        st.session_state.document_engine = (
            DocumentEngine()
        )

    if "document_processed" not in st.session_state:

        st.session_state.document_processed = False

    if "document_info" not in st.session_state:

        st.session_state.document_info = None

    if "last_ai_answer" not in st.session_state:

        st.session_state.last_ai_answer = None

    if "last_ai_sources" not in st.session_state:

        st.session_state.last_ai_sources = []

    # =====================================================
    # LEARNING MATERIAL
    # =====================================================

    st.subheader("Learning Material")

    uploaded_file = st.file_uploader(
        "Upload your learning material",
        type=["pdf"],
        help=(
            "Upload textbooks, notes, study material, "
            "or reference documents."
        ),
        key="learning_material_upload"
    )

    if uploaded_file is not None:

        st.caption(
            f"{uploaded_file.name} • "
            f"{uploaded_file.size / (1024 * 1024):.1f} MB"
        )

        process_button = st.button(
            "Process Learning Material",
            type="primary",
            use_container_width=False,
            key="process_learning_material"
        )

        if process_button:

            try:

                os.makedirs(
                    "uploads",
                    exist_ok=True
                )

                upload_path = os.path.join(
                    "uploads",
                    uploaded_file.name
                )

                with open(
                    upload_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

                with st.spinner(
                    "Processing learning material..."
                ):

                    document_info = (
                        st.session_state
                        .document_engine
                        .process_pdf(
                            upload_path
                        )
                    )

                st.session_state.document_processed = True

                st.session_state.document_info = (
                    document_info
                )

                st.session_state.last_ai_answer = None

                st.session_state.last_ai_sources = []

                st.success(
                    "Learning material processed successfully."
                )

            except Exception as error:

                st.error(
                    "Document processing failed."
                )

                st.caption(
                    str(error)
                )

    # =====================================================
    # DOCUMENT STATUS
    # =====================================================

    if st.session_state.document_processed:

        document_info = (
            st.session_state.document_info
            or {}
        )

        chunks = document_info.get(
            "chunks",
            0
        )

        characters = document_info.get(
            "characters",
            0
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Document Status",
                "Ready"
            )

        with col2:

            st.metric(
                "Knowledge Chunks",
                chunks
            )

        with col3:

            st.metric(
                "Characters",
                f"{characters:,}"
            )

    else:

        st.info(
            "Upload and process a learning document "
            "before asking questions."
        )

    st.divider()

    # =====================================================
    # ASK NEXORA
    # =====================================================

    st.subheader("Ask Nexora")

    language = st.selectbox(
        "Response Language",
        [
            "English",
            "Telugu",
            "Hindi",
            "Tamil",
            "Kannada"
        ],
        key="assistant_language"
    )

    question = st.text_area(
        "Your question",
        placeholder=(
            "Example: What is the Transformer "
            "architecture and how does self-attention work?"
        ),
        height=130,
        key="assistant_question"
    )

    # =====================================================
    # ASK BUTTON
    # =====================================================

    ask_button = st.button(
        "Ask Nexora",
        type="primary",
        key="ask_nexora"
    )

    if ask_button:

        # -------------------------------------------------
        # DOCUMENT CHECK
        # -------------------------------------------------

        if not st.session_state.document_processed:

            st.warning(
                "Please upload and process a learning "
                "document first."
            )

        # -------------------------------------------------
        # QUESTION CHECK
        # -------------------------------------------------

        elif not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            retrieved_chunks = []
            answer = None

            try:

                with st.spinner(
                    "Nexora is analyzing your learning material..."
                ):

                    # -------------------------------------
                    # RETRIEVE CONTENT
                    # -------------------------------------

                    retrieved_chunks = (
                        st.session_state
                        .document_engine
                        .search(
                            question,
                            top_k=3
                        )
                    )

                    if not retrieved_chunks:

                        st.warning(
                            "No relevant information was found "
                            "in the uploaded material."
                        )

                    else:

                        # ---------------------------------
                        # GENERATE ANSWER
                        # ---------------------------------

                        assistant = AIAssistant()

                        answer = (
                            assistant.answer_question(
                                question=question,
                                retrieved_chunks=retrieved_chunks,
                                language=language
                            )
                        )

                        st.session_state.last_ai_answer = (
                            answer
                        )

                        st.session_state.last_ai_sources = (
                            retrieved_chunks
                        )

                # -------------------------------------------------
                # DISPLAY ANSWER
                # -------------------------------------------------

                if answer:

                    if answer.startswith(
                        "Nexora could not generate"
                    ):

                        st.error(
                            "Nexora could not generate an answer."
                        )

                        st.caption(
                            "The document was retrieved successfully, "
                            "but the AI generation service did not "
                            "return a response. Please try again."
                        )

                    else:

                        st.success(
                            "Answer generated successfully."
                        )

                        st.subheader(
                            f"Nexora's Answer • {language}"
                        )

                        st.markdown(
                            answer
                        )

                # -------------------------------------------------
                # SOURCES
                # -------------------------------------------------

                if retrieved_chunks:

                    st.subheader(
                        "Retrieved Sources"
                    )

                    for index, chunk in enumerate(
                        retrieved_chunks,
                        start=1
                    ):

                        score = chunk.get(
                            "score",
                            0
                        )

                        with st.expander(
                            f"Source {index} • "
                            f"Similarity {score:.3f}"
                        ):

                            st.write(
                                chunk.get(
                                    "text",
                                    ""
                                )
                            )

            except Exception as error:

                st.error(
                    "The AI service could not generate "
                    "a response."
                )

                st.caption(
                    f"Technical details: {error}"
                )

    # =====================================================
    # PREVIOUS RESPONSE
    # =====================================================

    previous_answer = (
        st.session_state.last_ai_answer
    )

    if (
        previous_answer
        and not previous_answer.startswith(
            "Nexora could not generate"
        )
    ):

        st.divider()

        st.subheader(
            "Previous Response"
        )

        st.markdown(
            previous_answer
        )