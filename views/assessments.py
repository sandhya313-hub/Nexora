import streamlit as st

from services.assessment_engine import AssessmentEngine


# =========================================================
# ASSESSMENT PAGE
# =========================================================

def render_assessments():
    """
    Render the Nexora AI Assessment page.
    """

    st.title("AI Assessment")

    st.caption(
        "Evaluate your knowledge and measure your learning progress."
    )

    st.divider()


    # =====================================================
    # SESSION STATE
    # =====================================================

    if "assessment_generated" not in st.session_state:
        st.session_state.assessment_generated = False

    if "assessment_questions" not in st.session_state:
        st.session_state.assessment_questions = []

    if "assessment_score" not in st.session_state:
        st.session_state.assessment_score = None

    if "assessment_completed" not in st.session_state:
        st.session_state.assessment_completed = False

    if "assessment_result" not in st.session_state:
        st.session_state.assessment_result = None


    # =====================================================
    # ASSESSMENT OVERVIEW
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Assessments Completed",
            "3"
        )

    with col2:

        st.metric(
            "Average Score",
            "78%"
        )

    with col3:

        latest_score = st.session_state.get(
            "assessment_score"
        )

        if latest_score is not None:

            display_score = f"{latest_score}%"

        else:

            display_score = "84%"

        st.metric(
            "Latest Score",
            display_score
        )


    st.divider()


    # =====================================================
    # ASSESSMENT SETUP
    # =====================================================

    st.subheader(
        "Create Assessment"
    )

    col1, col2 = st.columns(2)

    with col1:

        topic = st.selectbox(
            "Assessment Topic",
            [
                "Uploaded Learning Material",
                "Python",
                "Statistics",
                "SQL",
                "AI and Machine Learning",
                "Data Visualization"
            ]
        )

    with col2:

        num_questions = st.selectbox(
            "Number of Questions",
            [5, 10, 15, 20],
            index=0
        )


    difficulty = st.selectbox(
        "Difficulty Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


    st.write("")


    # =====================================================
    # CHECK DOCUMENT
    # =====================================================

    document_available = (
        st.session_state.get(
            "document_processed",
            False
        )
        and
        st.session_state.get(
            "document_engine"
        ) is not None
    )


    if topic == "Uploaded Learning Material":

        if document_available:

            document_info = (
                st.session_state.get(
                    "document_info"
                )
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

            st.success(
                f"Learning material ready — "
                f"{chunks} chunks · "
                f"{characters:,} characters"
            )

        else:

            st.info(
                "Go to AI Assistant, upload and process "
                "your learning material first."
            )


    # =====================================================
    # GENERATE ASSESSMENT
    # =====================================================

    if st.button(
        "Generate Assessment",
        type="primary",
        use_container_width=True
    ):

        # -------------------------------------------------
        # Require uploaded document
        # -------------------------------------------------

        if topic == "Uploaded Learning Material":

            if not document_available:

                st.error(
                    "Please upload and process learning "
                    "material before generating an assessment."
                )

                return


        try:

            with st.spinner(
                f"Generating {num_questions} questions..."
            ):

                document_engine = (
                    st.session_state.document_engine
                )

                # -------------------------------------------------
                # Retrieve material
                # -------------------------------------------------

                if topic == "Uploaded Learning Material":

                    # Search using a broad query to obtain
                    # relevant material from the document.
                    retrieved_chunks = (
                        document_engine.search(
                            "important concepts definitions "
                            "principles architecture examples",
                            top_k=10
                        )
                    )

                    context_parts = []

                    for chunk in retrieved_chunks:

                        if isinstance(
                            chunk,
                            dict
                        ):

                            text = chunk.get(
                                "text",
                                ""
                            )

                        else:

                            text = str(
                                chunk
                            )

                        if text.strip():

                            context_parts.append(
                                text.strip()
                            )

                    context = "\n\n".join(
                        context_parts
                    )

                else:

                    # -------------------------------------------------
                    # For non-uploaded topics, use available
                    # competency/context if present.
                    # -------------------------------------------------

                    context = (
                        f"Topic: {topic}\n\n"
                        f"Create educational questions about "
                        f"{topic} using standard foundational "
                        f"concepts."
                    )


                if not context.strip():

                    raise ValueError(
                        "No learning content was found "
                        "for this assessment."
                    )


                # -------------------------------------------------
                # Generate questions
                # -------------------------------------------------

                engine = AssessmentEngine()

                questions = (
                    engine.generate_questions(
                        context=context,
                        num_questions=num_questions,
                        difficulty=difficulty
                    )
                )


                # -------------------------------------------------
                # FINAL COUNT CHECK
                # -------------------------------------------------

                if len(questions) != num_questions:

                    raise ValueError(
                        f"Expected {num_questions} questions "
                        f"but received {len(questions)}."
                    )


                # -------------------------------------------------
                # Store questions
                # -------------------------------------------------

                st.session_state.assessment_questions = (
                    questions
                )

                st.session_state.assessment_generated = True

                st.session_state.assessment_completed = False

                st.session_state.assessment_score = None

                st.session_state.assessment_result = None


            st.success(
                f"Assessment generated successfully "
                f"with {len(questions)} questions."
            )

            # Refresh so generated questions appear
            st.rerun()


        except Exception as error:

            st.error(
                "Assessment generation failed."
            )

            st.caption(
                str(error)
            )

            return


    # =====================================================
    # DISPLAY GENERATED ASSESSMENT
    # =====================================================

    if not st.session_state.get(
        "assessment_generated",
        False
    ):

        return


    questions = (
        st.session_state.get(
            "assessment_questions",
            []
        )
    )


    if not questions:

        return


    st.divider()

    st.subheader(
        "Assessment"
    )

    st.caption(
        f"{len(questions)} questions · "
        f"{difficulty} difficulty"
    )


    # =====================================================
    # ANSWERS
    # =====================================================

    answers = {}


    for index, question in enumerate(
        questions
    ):

        st.markdown(
            f"### Question {index + 1}"
        )

        st.write(
            question["question"]
        )


        selected = st.radio(
            "Select your answer",
            question["options"],
            key=f"assessment_answer_{index}",
            index=None
        )


        if selected is not None:

            answers[index] = (
                question[
                    "options"
                ].index(
                    selected
                )
            )


        if index < len(questions) - 1:

            st.divider()


    # =====================================================
    # SUBMIT ASSESSMENT
    # =====================================================

    st.write("")


    if st.button(
        "Submit Assessment",
        type="primary",
        use_container_width=True
    ):

        # -------------------------------------------------
        # Check unanswered questions
        # -------------------------------------------------

        unanswered = []

        for index in range(
            len(questions)
        ):

            if index not in answers:

                unanswered.append(
                    index + 1
                )


        if unanswered:

            st.warning(
                "Please answer all questions before submitting."
            )

            st.caption(
                "Unanswered questions: "
                + ", ".join(
                    map(
                        str,
                        unanswered
                    )
                )
            )

            return


        # -------------------------------------------------
        # Evaluate
        # -------------------------------------------------

        engine = AssessmentEngine()

        result = engine.evaluate(
            questions,
            answers
        )


        st.session_state.assessment_result = (
            result
        )

        st.session_state.assessment_score = (
            result["score"]
        )

        st.session_state.assessment_completed = True


        st.success(
            "Assessment submitted successfully."
        )


    # =====================================================
    # RESULT
    # =====================================================

    result = (
        st.session_state.get(
            "assessment_result"
        )
    )


    if (
        st.session_state.get(
            "assessment_completed",
            False
        )
        and result
    ):

        st.divider()

        st.subheader(
            "Assessment Result"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Score",
                f"{result['score']}%"
            )


        with col2:

            st.metric(
                "Correct",
                result["correct"]
            )


        with col3:

            st.metric(
                "Questions",
                result["total"]
            )


        # -------------------------------------------------
        # Performance message
        # -------------------------------------------------

        score = result["score"]


        if score >= 80:

            st.success(
                "Strong performance. You have demonstrated "
                "a good understanding of the assessed concepts."
            )

        elif score >= 60:

            st.info(
                "Good progress. Review the concepts you "
                "found difficult and continue practicing."
            )

        else:

            st.warning(
                "More practice is recommended. Review the "
                "learning material and attempt another assessment."
            )


        # -------------------------------------------------
        # Detailed results
        # -------------------------------------------------

        st.subheader(
            "Question Review"
        )


        for index, item in enumerate(
            result["results"]
        ):

            if item["is_correct"]:

                st.success(
                    f"Question {index + 1}: Correct"
                )

            else:

                st.error(
                    f"Question {index + 1}: Incorrect"
                )

                st.write(
                    "Correct answer:",
                    item["correct_answer"]
                )