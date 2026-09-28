import streamlit as st
from dotenv import load_dotenv

# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Nexora",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# THEME + SIDEBAR
# =========================================================

from ui.theme import (
    apply_nexora_theme,
    render_sidebar
)

apply_nexora_theme()


# =========================================================
# SERVICES
# =========================================================

from services.document_engine import DocumentEngine


# =========================================================
# PAGE IMPORTS
# =========================================================

from views.dashboard import render_dashboard
from views.competencies import render_competencies
from views.learning import render_learning
from views.ai_assistant import render_ai_assistant
from views.assessments import render_assessments
from views.analytics import render_analytics
from views.organization import render_organization
from views.admin import render_admin
from views.settings import render_settings


# =========================================================
# SESSION STATE
# =========================================================

def initialize_session_state():

    # -----------------------------------------------------
    # Navigation
    # -----------------------------------------------------

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"


    # -----------------------------------------------------
    # Document / RAG
    # -----------------------------------------------------

    if "document_engine" not in st.session_state:
        st.session_state.document_engine = DocumentEngine()

    if "document_processed" not in st.session_state:
        st.session_state.document_processed = False

    if "document_info" not in st.session_state:
        st.session_state.document_info = None


    # -----------------------------------------------------
    # Assessment
    # -----------------------------------------------------

    if "assessment_questions" not in st.session_state:
        st.session_state.assessment_questions = None

    if "assessment_submitted" not in st.session_state:
        st.session_state.assessment_submitted = False

    if "assessment_result" not in st.session_state:
        st.session_state.assessment_result = None


    # -----------------------------------------------------
    # Adaptive learning
    # -----------------------------------------------------

    if "adaptive_result" not in st.session_state:
        st.session_state.adaptive_result = None


    # -----------------------------------------------------
    # Learning activity
    # -----------------------------------------------------

    if "learning_hours" not in st.session_state:
        st.session_state.learning_hours = 0.0


    # -----------------------------------------------------
    # Competency analysis
    # -----------------------------------------------------

    if "gap_df" not in st.session_state:
        st.session_state.gap_df = None

    if "priority_gaps" not in st.session_state:
        st.session_state.priority_gaps = None

    if "competency_score" not in st.session_state:
        st.session_state.competency_score = None


    # -----------------------------------------------------
    # Competency levels
    # -----------------------------------------------------

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
# INITIALIZE
# =========================================================

initialize_session_state()


# =========================================================
# SIDEBAR
# =========================================================

selected_page = render_sidebar()


# =========================================================
# PAGE ROUTER
# =========================================================

if selected_page == "Dashboard":

    render_dashboard()


elif selected_page == "Competencies":

    render_competencies()


elif selected_page == "Learning":

    render_learning()


elif selected_page == "AI Assistant":

    render_ai_assistant()


elif selected_page == "Assessments":

    render_assessments()


elif selected_page == "Analytics":

    render_analytics()


elif selected_page == "Organization":

    render_organization()


elif selected_page == "Admin":

    render_admin()


elif selected_page == "Settings":

    render_settings()


else:

    st.session_state.current_page = "Dashboard"
    st.rerun()