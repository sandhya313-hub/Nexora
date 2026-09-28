import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div class="nexora-brand">
                <div class="nexora-brand-title">
                    NEXORA
                </div>

                <div class="nexora-brand-subtitle">
                    Skill Intelligence Platform
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.caption("WORKSPACE")

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Competencies",
                "Learning Path",
                "AI Learning",
                "Assessments",
                "Analytics",
                "Organization",
                "Settings"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")

        st.caption("ACCOUNT")

        st.write("Demo User")
        st.caption("Learner")

        return page