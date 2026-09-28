import streamlit as st


def render_dashboard():
    """Render the main Nexora dashboard."""

    st.title("Dashboard")

    st.markdown(
        """
        <div class="nexora-card">
            <h2>Welcome to Nexora</h2>
            <p>
                Your AI-powered skill intelligence and
                personalized learning workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Overall Competency",
            "72%"
        )

    with col2:
        st.metric(
            "Skill Gaps",
            "4"
        )

    with col3:
        st.metric(
            "Assessments",
            "3"
        )

    with col4:
        st.metric(
            "Learning Hours",
            "12"
        )

    st.subheader("Learning Progress")

    st.progress(0.72)

    st.write(
        "Your current learning progress is 72%."
    )

    st.subheader("Competency Overview")

    competencies = {
        "Python": 75,
        "Statistics": 68,
        "SQL": 55,
        "AI & Machine Learning": 62,
        "GIS": 48,
        "Data Visualization": 70,
    }

    for skill, value in competencies.items():

        col1, col2 = st.columns([2, 5])

        with col1:
            st.write(f"**{skill}**")

        with col2:
            st.progress(value / 100)

    st.subheader("Recent Activity")

    activities = [
        "Completed AI fundamentals assessment",
        "Uploaded learning material",
        "Updated Python competency",
        "Generated personalized learning path",
    ]

    for activity in activities:
        st.write(f"• {activity}")