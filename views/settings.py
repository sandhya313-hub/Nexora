import streamlit as st


def render_settings():
    """Render the Nexora settings page."""

    st.title("Settings")

    st.caption(
        "Manage your Nexora profile, learning preferences, "
        "and application configuration."
    )

    st.divider()

    # ---------------------------------------------------------
    # PROFILE SETTINGS
    # ---------------------------------------------------------

    st.subheader("Profile")

    name = st.text_input(
        "Display Name",
        value="Demo User"
    )

    role = st.selectbox(
        "Primary Role",
        [
            "Statistical Officer",
            "Data Analyst",
            "GIS Analyst",
            "AI/ML Specialist",
            "Project Manager"
        ]
    )

    st.divider()

    # ---------------------------------------------------------
    # LEARNING PREFERENCES
    # ---------------------------------------------------------

    st.subheader("Learning Preferences")

    language = st.selectbox(
        "Preferred Learning Language",
        [
            "English",
            "Telugu",
            "Hindi",
            "Tamil",
            "Kannada"
        ]
    )

    difficulty = st.selectbox(
        "Preferred Difficulty",
        [
            "Adaptive",
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    learning_mode = st.selectbox(
        "Learning Mode",
        [
            "Self-paced",
            "Assessment-focused",
            "Skill-gap focused"
        ]
    )

    st.divider()

    # ---------------------------------------------------------
    # AI SETTINGS
    # ---------------------------------------------------------

    st.subheader("AI Assistant")

    enable_ai = st.toggle(
        "Enable AI Learning Assistant",
        value=True
    )

    grounded_answers = st.toggle(
        "Use uploaded learning material for answers",
        value=True
    )

    st.divider()

    # ---------------------------------------------------------
    # SAVE SETTINGS
    # ---------------------------------------------------------

    if st.button(
        "Save Changes",
        type="primary"
    ):

        st.session_state.user_settings = {
            "name": name,
            "role": role,
            "language": language,
            "difficulty": difficulty,
            "learning_mode": learning_mode,
            "enable_ai": enable_ai,
            "grounded_answers": grounded_answers
        }

        st.success(
            "Settings saved successfully."
        )