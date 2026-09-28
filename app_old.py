import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from ui.theme import render_sidebar


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# NEXORA SERVICES
# =========================================================

from services.competency_engine import (
    analyze_skill_gaps,
    get_priority_gaps,
    calculate_competency_score
)

from services.recommendation_engine import (
    RecommendationEngine
)

from services.document_engine import (
    DocumentEngine
)

from services.ai_assistant import (
    AIAssistant
)

from services.assessment_engine import (
    AssessmentEngine
)

from services.adaptive_engine import (
    AdaptiveCompetencyEngine
)

from services.analytics_engine import (
    AnalyticsEngine
)

from services.admin_analytics_engine import (
    AdminAnalyticsEngine
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Nexora",
    page_icon="🧠",
    layout="wide"
)

selected_page = render_sidebar()


# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

if "document_engine" not in st.session_state:
    st.session_state.document_engine = DocumentEngine()


if "document_processed" not in st.session_state:
    st.session_state.document_processed = False


if "document_info" not in st.session_state:
    st.session_state.document_info = None


if "assessment_questions" not in st.session_state:
    st.session_state.assessment_questions = None


if "assessment_submitted" not in st.session_state:
    st.session_state.assessment_submitted = False


if "assessment_result" not in st.session_state:
    st.session_state.assessment_result = None


if "analytics_engine" not in st.session_state:
    st.session_state.analytics_engine = AnalyticsEngine()

if "admin_analytics_engine" not in st.session_state:

    st.session_state.admin_analytics_engine = (
        AdminAnalyticsEngine()
    )    


if "learning_hours" not in st.session_state:
    st.session_state.learning_hours = 0.0


if "adaptive_result" not in st.session_state:
    st.session_state.adaptive_result = None


if "gap_df" not in st.session_state:
    st.session_state.gap_df = None


if "priority_gaps" not in st.session_state:
    st.session_state.priority_gaps = None


if "competency_score" not in st.session_state:
    st.session_state.competency_score = None


# =========================================================
# PERSISTENT COMPETENCY LEVELS
# =========================================================

if "competency_levels" not in st.session_state:

    st.session_state.competency_levels = {

        "Statistics": 2,

        "Python": 2,

        "SQL": 1,

        "GIS": 1,

        "AI and Machine Learning": 1,

        "Data Visualization": 2,

        "Survey Design": 2,

        "Sampling": 2
    }


# =========================================================
# HEADER
# =========================================================

st.title("🧠 Nexora")

st.subheader(
    "AI-Powered Skill Intelligence & Personalized Learning Platform"
)

st.caption(
    "Assess skills • Identify gaps • Recommend learning • "
    "Learn with AI • Test knowledge"
)

st.divider()


# =========================================================
# USER PROFILE
# =========================================================

st.header("👤 Competency Profile")

col1, col2 = st.columns(2)


with col1:

    name = st.text_input(
        "Name",
        "Demo User"
    )


with col2:

    role = st.selectbox(
        "Job Role",
        [
            "Statistical Officer",
            "Data Analyst",
            "GIS Analyst",
            "AI/ML Specialist",
            "Project Manager"
        ]
    )


# =========================================================
# COMPETENCY LEVELS
# =========================================================

st.subheader(
    "Current Competency Levels"
)

st.caption(
    "1 = Beginner | 2 = Intermediate | 3 = Advanced"
)


competency_levels = st.session_state.competency_levels


col1, col2, col3 = st.columns(3)


with col1:

    competency_levels["Statistics"] = st.slider(
        "Statistics",
        1,
        3,
        competency_levels["Statistics"],
        key="statistics_slider"
    )

    competency_levels["Python"] = st.slider(
        "Python",
        1,
        3,
        competency_levels["Python"],
        key="python_slider"
    )

    competency_levels["SQL"] = st.slider(
        "SQL",
        1,
        3,
        competency_levels["SQL"],
        key="sql_slider"
    )


with col2:

    competency_levels["GIS"] = st.slider(
        "GIS",
        1,
        3,
        competency_levels["GIS"],
        key="gis_slider"
    )

    competency_levels["AI and Machine Learning"] = st.slider(
        "AI and Machine Learning",
        1,
        3,
        competency_levels["AI and Machine Learning"],
        key="ai_ml_slider"
    )

    competency_levels["Data Visualization"] = st.slider(
        "Data Visualization",
        1,
        3,
        competency_levels["Data Visualization"],
        key="data_visualization_slider"
    )


with col3:

    competency_levels["Survey Design"] = st.slider(
        "Survey Design",
        1,
        3,
        competency_levels["Survey Design"],
        key="survey_design_slider"
    )

    competency_levels["Sampling"] = st.slider(
        "Sampling",
        1,
        3,
        competency_levels["Sampling"],
        key="sampling_slider"
    )


# =========================================================
# COMPETENCY ANALYSIS
# =========================================================

if st.button(
    "🔍 Analyze My Competencies",
    type="primary"
):

    try:

        user_skills = dict(
            st.session_state.competency_levels
        )

        gap_df = analyze_skill_gaps(
            role,
            user_skills
        )

        if isinstance(gap_df, dict) and "error" in gap_df:

            st.error(
                gap_df["error"]
            )

        else:

            score = calculate_competency_score(
                gap_df
            )

            priority_gaps = get_priority_gaps(
                gap_df
            )

            st.session_state.gap_df = gap_df

            st.session_state.priority_gaps = priority_gaps

            st.session_state.competency_score = score

            st.success(
                "✅ Competency analysis completed successfully!"
            )

    except Exception as error:

        st.error(
            f"❌ Competency analysis failed: {error}"
        )


# =========================================================
# DISPLAY COMPETENCY RESULTS
# =========================================================

if st.session_state.gap_df is not None:

    gap_df = st.session_state.gap_df

    priority_gaps = st.session_state.priority_gaps

    score = st.session_state.competency_score


    st.divider()

    st.header(
        f"📊 {name}'s Competency Intelligence"
    )


    # -----------------------------------------------------
    # SCORE
    # -----------------------------------------------------

    score_col, gap_col = st.columns(2)


    with score_col:

        st.metric(
            "Overall Competency",
            f"{score}%"
        )


    with gap_col:

        st.metric(
            "Priority Skill Gaps",
            len(priority_gaps)
        )


    # -----------------------------------------------------
    # GAP TABLE
    # -----------------------------------------------------

    st.subheader(
        "🎯 Competency Gap Analysis"
    )


    display_df = gap_df.copy()


    display_df["Current Level"] = (
        display_df["current_level"]
    )


    display_df["Required Level"] = (
        display_df["required_level"]
    )


    display_df = display_df[
        [
            "competency",
            "Current Level",
            "Required Level",
            "gap",
            "status"
        ]
    ]


    display_df.columns = [
        "Competency",
        "Current Level",
        "Required Level",
        "Gap",
        "Status"
    ]


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    # -----------------------------------------------------
    # PRIORITY GAPS
    # -----------------------------------------------------

    st.subheader(
        "🚨 Priority Skill Gaps"
    )


    if priority_gaps.empty:

        st.success(
            "Excellent! No significant competency gaps detected."
        )

    else:

        for _, row in priority_gaps.iterrows():

            st.warning(
                f"**{row['competency']}** — "
                f"{row['status']} gap "
                f"(Gap: {row['gap']})"
            )


    # =====================================================
    # PERSONALIZED LEARNING PATH
    # =====================================================

    st.divider()

    st.header(
        "🎯 Personalized Learning Path"
    )

    st.caption(
        "Nexora uses semantic AI, explicit skill matching, "
        "and competency levels to identify relevant learning resources."
    )


    if priority_gaps.empty:

        st.info(
            "No learning recommendations are required "
            "because no competency gaps were detected."
        )

    else:

        try:

            with st.spinner(
                "🧠 Nexora is generating your personalized learning path..."
            ):

                recommendation_engine = (
                    RecommendationEngine()
                )

                recommendations = (
                    recommendation_engine
                    .recommend_for_gaps(
                        priority_gaps,
                        top_k_per_skill=2
                    )
                )


            if recommendations.empty:

                st.info(
                    "No matching learning resources found."
                )

            else:

                recommendations = (
                    recommendations
                    .sort_values(
                        "match_score",
                        ascending=False
                    )
                    .drop_duplicates(
                        subset=["course_id"]
                    )
                )


                for index, (_, course) in enumerate(
                    recommendations.iterrows(),
                    start=1
                ):

                    st.markdown(
                        f"""
### {index:02d}. {course['course_name']}

**🎯 Skill Gap:** {course['skill']}  

**📚 Level:** {course['level']}  

**⏱️ Duration:** {course['duration_hours']} hours  

**🧠 Nexora Match:** {course['match_score']}%
"""
                    )


                    st.progress(
                        min(
                            float(
                                course["match_score"]
                            ) / 100,
                            1.0
                        )
                    )


                    st.divider()


        except Exception as error:

            st.error(
                f"❌ Recommendation error: {error}"
            )


# =========================================================
# AI LEARNING ASSISTANT
# =========================================================

st.divider()

st.header(
    "📚 Nexora AI Learning Assistant"
)

st.caption(
    "Upload learning material and ask questions. "
    "Nexora retrieves relevant content and generates "
    "grounded AI explanations."
)


# =========================================================
# PDF UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "📄 Upload Learning Material",
    type=["pdf"],
    help="Upload a PDF containing learning material."
)


# =========================================================
# PROCESS DOCUMENT
# =========================================================

if uploaded_file is not None:

    if st.button(
        "⚙️ Process Learning Material"
    ):

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
                "📖 Nexora is reading your learning material..."
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


            # Count document processing as learning activity
            st.session_state.learning_hours += 1.0


            st.success(
                "✅ Learning material processed successfully!"
            )


            st.info(
                f"📚 Created "
                f"{document_info['chunks']} "
                f"knowledge chunks from "
                f"{document_info['characters']:,} "
                f"characters."
            )


        except Exception as error:

            st.error(
                f"❌ Document processing failed: {error}"
            )


# =========================================================
# DOCUMENT STATUS + AI LEARNING ASSISTANT
# =========================================================

if st.session_state.document_processed:

    st.success(
        "🟢 Learning material is ready for Nexora."
    )

    # =====================================================
    # ASK NEXORA
    # =====================================================

    st.subheader(
        "💬 Ask Nexora"
    )

    language = st.selectbox(
        "🌐 Select Learning Language",
        [
            "English",
            "Telugu",
            "Hindi",
            "Tamil",
            "Kannada"
        ],
        key="learning_language"
    )

    question = st.text_area(
        "Ask a question about your uploaded material:",
        placeholder="Example: What is UML?",
        height=100,
        key="nexora_question"
    )

    if st.button(
        "🤖 Ask Nexora",
        type="primary",
        key="ask_nexora_button"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question first."
            )

        else:

            try:

                with st.spinner(
                    "🧠 Nexora is analyzing your learning material..."
                ):

                    retrieved_chunks = (
                        st.session_state
                        .document_engine
                        .search(
                            question,
                            top_k=3
                        )
                    )

                    assistant = AIAssistant()

                    answer = assistant.answer_question(
                        question,
                        retrieved_chunks,
                        language=language
                    )

                # -------------------------------------------------
                # ANSWER
                # -------------------------------------------------

                st.subheader(
                    f"🤖 Nexora's Answer — {language}"
                )

                st.markdown(
                    answer
                )

                # -------------------------------------------------
                # SOURCES
                # -------------------------------------------------

                st.subheader(
                    "📚 Retrieved Learning Sources"
                )

                for i, chunk in enumerate(
                    retrieved_chunks,
                    start=1
                ):

                    score = chunk.get(
                        "score",
                        0
                    )

                    with st.expander(
                        f"Source {i} • Similarity: {score:.3f}"
                    ):

                        st.write(
                            chunk["text"]
                        )

            except Exception as error:

                st.error(
                    f"❌ AI assistant error: {error}"
                )

else:

    st.info(
        "📚 Upload and process learning material "
        "above to start asking Nexora questions."
    )


# =========================================================
# AI ASSESSMENT ENGINE
# =========================================================

st.divider()

st.header(
    "📝 AI-Powered Assessment"
)

st.caption(
    "Nexora generates objective assessments "
    "from your uploaded learning material."
)


# =========================================================
# ASSESSMENT GENERATION
# =========================================================

if not st.session_state.document_processed:

    st.info(
        "📚 Upload and process learning material "
        "above before generating an assessment."
    )

else:

    st.subheader(
        "🧠 Generate Assessment"
    )


    num_questions = st.slider(
        "Number of Questions",
        min_value=3,
        max_value=10,
        value=5,
        key="assessment_question_count"
    )


    if st.button(
        "🧠 Generate Assessment"
    ):

        try:

            with st.spinner(
                "🧠 Nexora is creating your assessment..."
            ):

                retrieved_chunks = (
                    st.session_state
                    .document_engine
                    .search(
                        "important concepts definitions "
                        "key topics principles",
                        top_k=6
                    )
                )


                context = "\n\n".join(
                    chunk["text"]
                    for chunk in retrieved_chunks
                )


                api_key = os.getenv(
                    "GOOGLE_API_KEY"
                )


                if not api_key:

                    raise ValueError(
                        "GOOGLE_API_KEY is not configured."
                    )


                assessment_engine = (
                    AssessmentEngine(
                        api_key
                    )
                )


                questions = (
                    assessment_engine
                    .generate_questions(
                        context,
                        num_questions
                    )
                )


            st.session_state.assessment_questions = (
                questions
            )


            st.session_state.assessment_submitted = False

            st.session_state.assessment_result = None

            st.session_state.adaptive_result = None


            st.success(
                f"✅ Generated "
                f"{len(questions)} assessment questions!"
            )


        except Exception as error:

            st.error(
                f"❌ Assessment generation failed: {error}"
            )


# =========================================================
# DISPLAY QUESTIONS
# =========================================================

if st.session_state.assessment_questions:

    st.divider()

    st.subheader(
        "📝 Your Assessment"
    )


    answers = {}


    for i, question in enumerate(
        st.session_state.assessment_questions
    ):

        st.markdown(
            f"### Question {i + 1}"
        )


        st.write(
            question["question"]
        )


        selected = st.radio(
            "Select your answer:",
            question["options"],
            key=f"assessment_question_{i}"
        )


        answers[i] = (
            question["options"].index(
                selected
            )
        )


        st.divider()


    # =====================================================
    # SUBMIT ASSESSMENT
    # =====================================================

    if st.button(
        "📊 Submit Assessment",
        type="primary"
    ):

        try:

            api_key = os.getenv(
                "GOOGLE_API_KEY"
            )


            if not api_key:

                raise ValueError(
                    "GOOGLE_API_KEY is not configured."
                )


            assessment_engine = (
                AssessmentEngine(
                    api_key
                )
            )


            result = (
                assessment_engine
                .evaluate(
                    st.session_state.assessment_questions,
                    answers
                )
            )


            # -------------------------------------------------
            # SAVE ASSESSMENT RESULT
            # -------------------------------------------------

            st.session_state.analytics_engine.add_assessment_score(
                result["score"]
            )


            st.session_state.assessment_result = result

            st.session_state.assessment_submitted = True


            st.success(
                "✅ Assessment submitted successfully!"
            )


        except Exception as error:

            st.error(
                f"❌ Assessment evaluation failed: {error}"
            )


# =========================================================
# ASSESSMENT RESULTS
# =========================================================

if st.session_state.assessment_submitted:

    result = st.session_state.assessment_result


    if result:

        st.divider()

        st.subheader(
            "📊 Assessment Results"
        )


        # -------------------------------------------------
        # SCORE CARDS
        # -------------------------------------------------

        score_col, correct_col = st.columns(2)


        with score_col:

            st.metric(
                "Assessment Score",
                f"{result['score']}%"
            )


        with correct_col:

            st.metric(
                "Correct Answers",
                f"{result['correct']} / "
                f"{result['total']}"
            )


        # -------------------------------------------------
        # FEEDBACK
        # -------------------------------------------------

        st.subheader(
            "💡 Personalized Feedback"
        )


        if result["score"] >= 80:

            st.success(
                "Excellent understanding! "
                "You have demonstrated strong understanding "
                "of this learning material."
            )

        elif result["score"] >= 60:

            st.warning(
                "Good progress! Review the incorrect "
                "questions and strengthen those concepts."
            )

        else:

            st.error(
                "This topic needs more practice. "
                "Review the learning material and "
                "try the assessment again."
            )


        # -------------------------------------------------
        # QUESTION REVIEW
        # -------------------------------------------------

        st.subheader(
            "🔎 Question Review"
        )


        for i, item in enumerate(
            result["results"]
        ):

            if item["is_correct"]:

                st.success(
                    f"Question {i + 1}: Correct"
                )

            else:

                st.error(
                    f"Question {i + 1}: Incorrect"
                )


            st.write(
                item["explanation"]
            )


        # =================================================
        # ADAPTIVE COMPETENCY UPDATE
        # =================================================

        st.divider()

        st.subheader(
            "🔄 Adaptive Competency Update"
        )

        st.caption(
            "Nexora uses your assessment performance "
            "to dynamically update your competency level."
        )


        competency_options = [
            "Statistics",
            "Python",
            "SQL",
            "GIS",
            "AI and Machine Learning",
            "Data Visualization",
            "Survey Design",
            "Sampling"
        ]


        selected_competency = st.selectbox(
            "Assessment Competency",
            competency_options,
            key="adaptive_competency"
        )


        # -------------------------------------------------
        # CURRENT LEVEL
        # -------------------------------------------------

        current_level = (
            st.session_state
            .competency_levels[
                selected_competency
            ]
        )


        st.write(
            f"Current **{selected_competency}** level: "
            f"**{current_level}/3**"
        )


        # -------------------------------------------------
        # UPDATE COMPETENCY
        # -------------------------------------------------

        if st.button(
            "🔄 Update My Competency"
        ):

            try:

                adaptive_engine = (
                    AdaptiveCompetencyEngine()
                )


                adaptive_result = (
                    adaptive_engine
                    .update_competency(
                        competency=selected_competency,
                        current_level=current_level,
                        score=result["score"]
                    )
                )


                st.session_state.adaptive_result = (
                    adaptive_result
                )


                # -----------------------------------------
                # PERSIST NEW COMPETENCY LEVEL
                # -----------------------------------------

                st.session_state.competency_levels[
                    selected_competency
                ] = adaptive_result["new_level"]


                st.success(
                    "✅ Competency level updated successfully!"
                )


            except Exception as error:

                st.error(
                    f"❌ Adaptive update failed: {error}"
                )


        # =================================================
        # DISPLAY ADAPTIVE RESULT
        # =================================================

        if st.session_state.adaptive_result:

            adaptive_result = (
                st.session_state.adaptive_result
            )


            old_level = (
                adaptive_result[
                    "old_level_name"
                ]
            )


            new_level = (
                adaptive_result[
                    "new_level_name"
                ]
            )


            assessment_score = (
                adaptive_result[
                    "score"
                ]
            )


            st.markdown(
                "### 🎯 Competency Intelligence"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Assessment Score",
                    f"{assessment_score}%"
                )


            with col2:

                st.metric(
                    "Previous Level",
                    old_level
                )


            with col3:

                st.metric(
                    "Updated Level",
                    new_level
                )


            if new_level != old_level:

                st.success(
                    adaptive_result[
                        "message"
                    ]
                )

            else:

                st.info(
                    adaptive_result[
                        "message"
                    ]
                )


            st.markdown(
                """
### 🚀 Nexora Learning Loop

**Assessment → Competency Update → Skill Gap Analysis
→ Personalized Learning Path**
"""
            )


# =========================================================
# LEARNER ANALYTICS DASHBOARD
# =========================================================

if st.session_state.gap_df is not None:

    st.divider()

    st.header(
        "📊 Learner Analytics Dashboard"
    )

    st.caption(
        "Nexora continuously tracks competency, "
        "assessment performance, skill gaps, "
        "and learning progress."
    )


    # -----------------------------------------------------
    # CURRENT COMPETENCY LEVELS
    # -----------------------------------------------------

    competency_levels = dict(
        st.session_state.competency_levels
    )


    # -----------------------------------------------------
    # APPLY ADAPTIVE UPDATE
    # -----------------------------------------------------

    if st.session_state.adaptive_result:

        adaptive_result = (
            st.session_state.adaptive_result
        )


        updated_competency = (
            adaptive_result["competency"]
        )


        updated_level = (
            adaptive_result["new_level"]
        )


        competency_levels[
            updated_competency
        ] = updated_level


    # -----------------------------------------------------
    # GENERATE ANALYTICS
    # -----------------------------------------------------

    analytics_engine = (
        st.session_state.analytics_engine
    )


    priority_gap_count = 0


    if st.session_state.priority_gaps is not None:

        priority_gap_count = len(
            st.session_state.priority_gaps
        )


    analytics_report = (
        analytics_engine.generate_report(
            competency_levels=competency_levels,
            priority_gap_count=priority_gap_count
        )
    )


    # =====================================================
    # KPI CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🧠 Overall Competency",
            f"{analytics_report['overall_competency']}%"
        )


    with col2:

        st.metric(
            "📝 Average Assessment",
            f"{analytics_report['average_assessment_score']}%"
        )


    with col3:

        st.metric(
            "🎯 Skill Gaps",
            analytics_report["skill_gaps"]
        )


    with col4:

        st.metric(
            "⏱️ Learning Hours",
            analytics_report["learning_hours"]
        )


    # =====================================================
    # LEARNING PROGRESS
    # =====================================================

    st.subheader(
        "📈 Overall Learning Progress"
    )


    progress = (
        analytics_report["learning_progress"]
        / 100
    )


    st.progress(
        min(
            max(progress, 0.0),
            1.0
        )
    )


    st.write(
        f"**Learning Progress: "
        f"{analytics_report['learning_progress']}%**"
    )


    # =====================================================
    # COMPETENCY DEVELOPMENT
    # =====================================================

    st.subheader(
        "🧠 Competency Development"
    )


    competency_percentages = (
        analytics_report[
            "competency_percentages"
        ]
    )


    for competency, percentage in (
        competency_percentages.items()
    ):

        col1, col2 = st.columns(
            [2, 5]
        )


        with col1:

            st.write(
                f"**{competency}**"
            )


        with col2:

            st.progress(
                min(
                    float(percentage) / 100,
                    1.0
                )
            )


        st.caption(
            f"{percentage}% competency level"
        )


    # =====================================================
    # ASSESSMENT SUMMARY
    # =====================================================

    st.subheader(
        "📝 Assessment Summary"
    )


    assessment_count = (
        analytics_report[
            "assessment_count"
        ]
    )


    if assessment_count == 0:

        st.info(
            "No assessments completed yet."
        )

    else:

        st.success(
            f"🎉 You have completed "
            f"**{assessment_count} assessment(s)** "
            f"with an average score of "
            f"**{analytics_report['average_assessment_score']}%**."
        )


    # =====================================================
    # LEARNING INTELLIGENCE SUMMARY
    # =====================================================

    st.subheader(
        "💡 Learning Intelligence"
    )


    if assessment_count > 0:

        average_score = (
            analytics_report[
                "average_assessment_score"
            ]
        )


        if average_score >= 80:

            st.success(
                "🚀 Your assessment performance indicates "
                "strong learning progress. Nexora can now "
                "focus your learning path on advanced topics."
            )

        elif average_score >= 60:

            st.info(
                "📈 You are making steady progress. "
                "Nexora recommends strengthening intermediate "
                "concepts before moving to advanced topics."
            )

        else:

            st.warning(
                "🎯 Your current assessment performance "
                "suggests that additional foundational practice "
                "would be useful."
            )

    else:

        st.info(
            "Complete an assessment to unlock "
            "Nexora's learning intelligence insights."
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🧠 Nexora — AI-powered skill intelligence, "
    "personalized learning and adaptive competency development."
)

# =========================================================
# ADMIN / ORGANIZATION INTELLIGENCE DASHBOARD
# =========================================================

st.divider()

st.header(
    "🏢 Nexora Organization Intelligence"
)

st.caption(
    "Organization-wide workforce competency and "
    "training intelligence for administrators."
)


admin_engine = (
    st.session_state.admin_analytics_engine
)


admin_report = (
    admin_engine.generate_report()
)


# =========================================================
# ADMIN KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👥 Total Learners",
        admin_report[
            "total_learners"
        ]
    )


with col2:

    st.metric(
        "🧠 Avg. Competency",
        f"{admin_report['average_competency']}%"
    )


with col3:

    st.metric(
        "📝 Avg. Assessment",
        f"{admin_report['average_assessment']}%"
    )


with col4:

    st.metric(
        "🎯 Priority Skills",
        len(
            admin_report[
                "priority_skills"
            ]
        )
    )


# =========================================================
# WORKFORCE COMPETENCY DISTRIBUTION
# =========================================================

st.subheader(
    "📊 Workforce Competency Distribution"
)


distribution = pd.DataFrame(
    {
        "Competency":
            list(
                admin_report[
                    "skill_distribution"
                ].keys()
            ),

        "Competency Level (%)":
            list(
                admin_report[
                    "skill_distribution"
                ].values()
            )
    }
)


st.bar_chart(
    distribution.set_index(
        "Competency"
    )
)


# =========================================================
# PRIORITY SKILLS
# =========================================================

st.subheader(
    "🔥 Organization Priority Skills"
)


priority_skills = (
    admin_report[
        "priority_skills"
    ]
)


if not priority_skills:

    st.success(
        "No major workforce skill gaps detected."
    )

else:

    st.warning(
        "The following competencies require "
        "additional workforce development:"
    )

    for skill in priority_skills:

        st.markdown(
            f"🔸 **{skill}**"
        )


# =========================================================
# WORKFORCE DATA
# =========================================================

st.subheader(
    "👥 Workforce Competency Overview"
)


workforce_data = (
    admin_engine
    .get_workforce_data()
)


display_workforce = (
    workforce_data
    .copy()
)


display_workforce.columns = [

    "Learner",

    "Role",

    "Statistics",

    "Python",

    "SQL",

    "GIS",

    "AI/ML",

    "Assessment Score"

]


st.dataframe(
    display_workforce,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# TRAINING EFFECTIVENESS
# =========================================================

st.subheader(
    "📚 Training Effectiveness"
)


assessment_average = (
    admin_report[
        "average_assessment"
    ]
)


if assessment_average >= 80:

    st.success(
        f"🎉 Workforce training performance "
        f"is currently strong with an average "
        f"assessment score of "
        f"**{assessment_average}%**."
    )

elif assessment_average >= 60:

    st.warning(
        f"⚠️ Workforce learning outcomes show "
        f"room for improvement. Current average "
        f"assessment score: "
        f"**{assessment_average}%**."
    )

else:

    st.error(
        f"🚨 Workforce training requires "
        f"additional intervention. Current "
        f"average assessment score: "
        f"**{assessment_average}%**."
    )


# =========================================================
# EMERGING SKILL REQUIREMENTS
# =========================================================

st.subheader(
    "🚀 Emerging Skill Requirements"
)

st.caption(
    "Nexora identifies competencies that require "
    "greater organizational investment."
)


emerging_skills = [
    "AI and Machine Learning",
    "Python",
    "SQL",
    "GIS",
    "Data Analytics"
]


for skill in emerging_skills:

    st.markdown(
        f"🔹 **{skill}** — "
        f"Recommended for future workforce development"
    )


# =========================================================
# ADMIN INSIGHT
# =========================================================

st.subheader(
    "💡 Nexora Workforce Insight"
)


if priority_skills:

    st.info(
        "Nexora recommends prioritizing training "
        f"in **{', '.join(priority_skills)}** "
        "based on the current competency distribution."
    )

else:

    st.success(
        "The current workforce competency profile "
        "shows no critical priority skill areas."
    )