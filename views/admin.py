import streamlit as st


def render_admin():

    st.title("Organization Intelligence")

    st.caption(
        "Workforce competency and training intelligence."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Learners",
            "120"
        )

    with col2:
        st.metric(
            "Average Competency",
            "68%"
        )

    with col3:
        st.metric(
            "Assessment Average",
            "74%"
        )

    with col4:
        st.metric(
            "Priority Skills",
            "5"
        )

    st.subheader(
        "Workforce Competency Distribution"
    )

    data = {
        "Python": 72,
        "SQL": 61,
        "AI & ML": 58,
        "GIS": 49,
        "Statistics": 75,
    }

    st.bar_chart(data)

    st.subheader(
        "Priority Skills"
    )

    for skill in [
        "AI & Machine Learning",
        "SQL",
        "GIS"
    ]:
        st.write(
            f"• {skill}"
        )