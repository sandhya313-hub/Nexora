import streamlit as st


def render_learning():

    st.title("Personalized Learning")

    st.caption(
        "Your AI-generated learning path based on "
        "your competency gaps."
    )

    st.divider()

    courses = [
        ("Python for Data Analysis", "Python", 82),
        ("SQL Fundamentals", "SQL", 91),
        ("Machine Learning Foundations", "AI & ML", 76),
        ("GIS for Data Analytics", "GIS", 69),
    ]

    for title, skill, match in courses:

        with st.container():

            st.subheader(title)

            st.write(
                f"Skill focus: **{skill}**"
            )

            st.write(
                f"Nexora match: **{match}%**"
            )

            st.progress(match / 100)

            if st.button(
                "Start Learning",
                key=f"learn_{title}"
            ):
                st.success(
                    f"Learning path opened for {title}."
                )

            st.divider()