import streamlit as st


def render_competencies():
    """Render the competency intelligence page."""

    st.title("Competency Intelligence")

    st.caption(
        "Analyze your current skills, identify gaps, "
        "and track competency development."
    )

    st.divider()

    competencies = {
        "Statistics": 2,
        "Python": 2,
        "SQL": 1,
        "GIS": 1,
        "AI & Machine Learning": 1,
        "Data Visualization": 2,
        "Survey Design": 2,
        "Sampling": 2,
    }

    st.subheader("Current Competency Levels")

    col1, col2 = st.columns(2)

    with col1:
        for skill in list(competencies.keys())[:4]:

            level = st.slider(
                skill,
                1,
                3,
                competencies[skill],
                key=f"competency_{skill}"
            )

            st.progress(level / 3)

            st.caption(
                f"Level {level} / 3"
            )

    with col2:
        for skill in list(competencies.keys())[4:]:

            level = st.slider(
                skill,
                1,
                3,
                competencies[skill],
                key=f"competency_{skill}"
            )

            st.progress(level / 3)

            st.caption(
                f"Level {level} / 3"
            )

    st.divider()

    if st.button(
        "Analyze Competencies",
        type="primary"
    ):

        st.success(
            "Competency analysis completed."
        )

        st.subheader("Competency Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Overall Competency",
                "62%"
            )

        with col2:
            st.metric(
                "Priority Skill Gaps",
                "4"
            )

        with col3:
            st.metric(
                "Skills Tracked",
                "8"
            )

    st.subheader("Skill Gap Overview")

    gaps = [
        ("SQL", "High"),
        ("GIS", "High"),
        ("AI & Machine Learning", "Medium"),
        ("Python", "Low"),
    ]

    for skill, priority in gaps:

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(
                f"**{skill}**"
            )

        with col2:
            st.write(
                priority
            )