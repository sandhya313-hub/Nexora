import streamlit as st


def render_organization():
    """Render the organization intelligence page."""

    st.title("Organization Intelligence")

    st.caption(
        "Workforce competency, training performance, "
        "and organizational skill intelligence."
    )

    st.divider()

    # ---------------------------------------------------------
    # KPI SECTION
    # ---------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Learners",
            "24"
        )

    with col2:
        st.metric(
            "Average Competency",
            "68%"
        )

    with col3:
        st.metric(
            "Average Assessment",
            "74%"
        )

    with col4:
        st.metric(
            "Priority Skills",
            "5"
        )

    st.divider()

    # ---------------------------------------------------------
    # COMPETENCY DISTRIBUTION
    # ---------------------------------------------------------

    st.subheader("Workforce Competency Distribution")

    competency_data = {
        "Python": 72,
        "Statistics": 65,
        "SQL": 58,
        "AI / ML": 46,
        "GIS": 52,
        "Data Visualization": 70
    }

    st.bar_chart(competency_data)

    st.divider()

    # ---------------------------------------------------------
    # PRIORITY SKILLS
    # ---------------------------------------------------------

    st.subheader("Priority Skill Areas")

    priority_skills = [
        ("AI / Machine Learning", "High priority"),
        ("SQL", "High priority"),
        ("GIS", "Medium priority"),
        ("Statistics", "Medium priority")
    ]

    for skill, priority in priority_skills:

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"**{skill}**")

        with col2:
            st.write(priority)

    st.divider()

    # ---------------------------------------------------------
    # TRAINING EFFECTIVENESS
    # ---------------------------------------------------------

    st.subheader("Training Effectiveness")

    progress = 0.74

    st.progress(progress)

    st.write(
        "Current workforce assessment performance: **74%**"
    )

    st.info(
        "Organization intelligence can be connected to "
        "real learner records and assessment history as "
        "the platform evolves."
    )