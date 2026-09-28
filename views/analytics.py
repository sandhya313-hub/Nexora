import streamlit as st


def render_analytics():

    st.title("Learner Analytics")

    st.caption(
        "Track competency, assessment performance "
        "and learning progress."
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
            "Assessment Average",
            "78%"
        )

    with col3:
        st.metric(
            "Skill Gaps",
            "4"
        )

    with col4:
        st.metric(
            "Learning Hours",
            "12"
        )

    st.subheader(
        "Competency Development"
    )

    skills = {
        "Python": 75,
        "Statistics": 68,
        "SQL": 55,
        "AI & ML": 62,
        "GIS": 48,
    }

    for skill, value in skills.items():

        st.write(
            f"**{skill}**"
        )

        st.progress(
            value / 100
        )