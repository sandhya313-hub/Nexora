import streamlit as st


# =========================================================
# NEXORA DESIGN SYSTEM
# =========================================================

NEXORA_BG = "#0B1020"
NEXORA_SURFACE = "#111827"
NEXORA_SURFACE_2 = "#151D2F"
NEXORA_BORDER = "#263247"

NEXORA_TEXT = "#F3F6FC"
NEXORA_TEXT_MUTED = "#9AA8BD"

NEXORA_PRIMARY = "#6C63FF"
NEXORA_PRIMARY_HOVER = "#8179FF"


# =========================================================
# GLOBAL THEME
# =========================================================

def apply_nexora_theme():

    st.markdown(
        f"""
        <style>

        /* =================================================
           GLOBAL
        ================================================= */

        .stApp {{
            background:
                radial-gradient(
                    circle at 85% 0%,
                    rgba(108, 99, 255, 0.10),
                    transparent 30%
                ),
                {NEXORA_BG};
        }}

        .main {{
            background: transparent;
        }}

        .block-container {{
            max-width: 1380px;
            padding-top: 2rem;
            padding-bottom: 4rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }}


        /* =================================================
           SIDEBAR
        ================================================= */

        section[data-testid="stSidebar"] {{
            background: {NEXORA_SURFACE};
            border-right: 1px solid {NEXORA_BORDER};
        }}

        section[data-testid="stSidebar"] > div {{
            background: {NEXORA_SURFACE};
        }}


        /* =================================================
           SIDEBAR TEXT
        ================================================= */

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {{
            color: {NEXORA_TEXT_MUTED};
        }}


        /* =================================================
           SIDEBAR BRAND
        ================================================= */

        .nexora-brand-container {{
            padding-top: 0.5rem;
            padding-bottom: 1.6rem;
            border-bottom: 1px solid {NEXORA_BORDER};
            margin-bottom: 1rem;
        }}

        .nexora-brand-title {{
            font-size: 1.55rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            color: {NEXORA_TEXT};
            line-height: 1.1;
        }}

        .nexora-brand-subtitle {{
            margin-top: 0.4rem;
            font-size: 0.72rem;
            font-weight: 500;
            letter-spacing: 0.03em;
            color: {NEXORA_TEXT_MUTED};
        }}


        /* =================================================
           NAVIGATION LABELS
        ================================================= */

        .nexora-nav-label {{
            font-size: 0.66rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.13em;
            color: {NEXORA_TEXT_MUTED};
            margin-top: 1.25rem;
            margin-bottom: 0.5rem;
        }}


        /* =================================================
           SIDEBAR BUTTONS
        ================================================= */

        section[data-testid="stSidebar"] .stButton {{
            width: 100%;
            margin-bottom: 0.18rem;
        }}

        section[data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            min-height: 40px;

            padding: 0.45rem 0.75rem;

            border-radius: 8px;
            border: 1px solid transparent;

            background: transparent;

            color: {NEXORA_TEXT_MUTED};

            font-size: 0.86rem;
            font-weight: 500;

            text-align: left;

            transition:
                background 0.15s ease,
                border-color 0.15s ease,
                color 0.15s ease;
        }}

        section[data-testid="stSidebar"] .stButton > button:hover {{
            background: {NEXORA_SURFACE_2};
            border-color: {NEXORA_BORDER};
            color: {NEXORA_TEXT};
        }}

        section[data-testid="stSidebar"] .stButton > button:focus {{
            outline: none;
            border-color: {NEXORA_PRIMARY};
            box-shadow: 0 0 0 1px {NEXORA_PRIMARY};
        }}


        /* =================================================
           MAIN PAGE
        ================================================= */

        .nexora-page-title {{
            font-size: 2rem;
            font-weight: 750;
            letter-spacing: -0.025em;
            color: {NEXORA_TEXT};
            margin-bottom: 0.35rem;
        }}

        .nexora-page-description {{
            font-size: 0.94rem;
            line-height: 1.6;
            color: {NEXORA_TEXT_MUTED};
            margin-bottom: 1.8rem;
        }}


        /* =================================================
           HERO
        ================================================= */

        .nexora-hero {{
            padding: 2.2rem 2.4rem;
            margin-bottom: 2rem;

            border: 1px solid {NEXORA_BORDER};
            border-radius: 18px;

            background:
                linear-gradient(
                    135deg,
                    rgba(108, 99, 255, 0.13),
                    rgba(17, 24, 39, 0.96)
                );
        }}

        .nexora-hero-title {{
            margin: 0;
            font-size: 2.35rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: {NEXORA_TEXT};
        }}

        .nexora-hero-description {{
            margin-top: 0.7rem;
            max-width: 760px;
            font-size: 0.98rem;
            line-height: 1.6;
            color: {NEXORA_TEXT_MUTED};
        }}


        /* =================================================
           CARDS
        ================================================= */

        .nexora-card {{
            padding: 1.35rem;

            border: 1px solid {NEXORA_BORDER};
            border-radius: 14px;

            background: {NEXORA_SURFACE};

            min-height: 120px;
        }}

        .nexora-card-title {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: {NEXORA_TEXT_MUTED};
        }}

        .nexora-card-value {{
            margin-top: 0.5rem;
            font-size: 2rem;
            font-weight: 750;
            color: {NEXORA_TEXT};
        }}

        .nexora-card-description {{
            margin-top: 0.4rem;
            font-size: 0.82rem;
            color: {NEXORA_TEXT_MUTED};
        }}


        /* =================================================
           METRICS
        ================================================= */

        [data-testid="stMetric"] {{
            background: {NEXORA_SURFACE};
            border: 1px solid {NEXORA_BORDER};
            border-radius: 14px;
            padding: 1.2rem;
        }}

        [data-testid="stMetricLabel"] {{
            color: {NEXORA_TEXT_MUTED} !important;
        }}

        [data-testid="stMetricValue"] {{
            color: {NEXORA_TEXT} !important;
        }}


        /* =================================================
           HEADINGS
        ================================================= */

        h1,
        h2,
        h3 {{
            color: {NEXORA_TEXT} !important;
        }}


        /* =================================================
           INPUTS
        ================================================= */

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input {{
            background: {NEXORA_SURFACE} !important;

            border: 1px solid {NEXORA_BORDER} !important;

            border-radius: 9px !important;

            color: {NEXORA_TEXT} !important;
        }}

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus {{
            border-color: {NEXORA_PRIMARY} !important;

            box-shadow:
                0 0 0 1px {NEXORA_PRIMARY} !important;
        }}


        /* =================================================
           SELECTBOX
        ================================================= */

        div[data-baseweb="select"] > div {{
            background: {NEXORA_SURFACE} !important;
            border-color: {NEXORA_BORDER} !important;
            color: {NEXORA_TEXT} !important;
            border-radius: 9px !important;
        }}


        /* =================================================
           BUTTONS
        ================================================= */

        .stButton > button {{
            min-height: 42px;

            padding: 0.55rem 1.05rem;

            border-radius: 9px;

            border: 1px solid {NEXORA_BORDER};

            background: {NEXORA_SURFACE_2};

            color: {NEXORA_TEXT};

            font-weight: 600;

            transition:
                background 0.15s ease,
                border-color 0.15s ease,
                transform 0.15s ease;
        }}

        .stButton > button:hover {{
            background: {NEXORA_PRIMARY};
            border-color: {NEXORA_PRIMARY};
            color: white;

            transform: translateY(-1px);
        }}

        .stButton > button[kind="primary"] {{
            background: {NEXORA_PRIMARY};
            border-color: {NEXORA_PRIMARY};
            color: white;
        }}

        .stButton > button[kind="primary"]:hover {{
            background: {NEXORA_PRIMARY_HOVER};
            border-color: {NEXORA_PRIMARY_HOVER};
        }}


        /* =================================================
           PROGRESS
        ================================================= */

        .stProgress > div > div > div > div {{
            background-color: {NEXORA_PRIMARY};
        }}


        /* =================================================
           DATAFRAME
        ================================================= */

        [data-testid="stDataFrame"] {{
            border: 1px solid {NEXORA_BORDER};
            border-radius: 12px;
            overflow: hidden;
        }}


        /* =================================================
           EXPANDERS
        ================================================= */

        [data-testid="stExpander"] {{
            border: 1px solid {NEXORA_BORDER};
            border-radius: 10px;
            background: {NEXORA_SURFACE};
        }}


        /* =================================================
           FILE UPLOADER
        ================================================= */

        [data-testid="stFileUploader"] {{
            background: {NEXORA_SURFACE};
            border: 1px dashed {NEXORA_BORDER};
            border-radius: 12px;
            padding: 0.7rem;
        }}


        /* =================================================
           DIVIDER
        ================================================= */

        hr {{
            border-color: {NEXORA_BORDER};
        }}


        /* =================================================
           ALERTS
        ================================================= */

        [data-testid="stAlert"] {{
            border-radius: 10px;
        }}


        /* =================================================
           STREAMLIT CLEANUP
        ================================================= */

        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}


        /* =================================================
           RESPONSIVE
        ================================================= */

        @media (max-width: 900px) {{

            .block-container {{
                padding-left: 1.2rem;
                padding-right: 1.2rem;
            }}

            .nexora-hero {{
                padding: 1.5rem;
            }}

            .nexora-hero-title {{
                font-size: 1.8rem;
            }}

        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

def render_sidebar():

    with st.sidebar:

        # =================================================
        # BRAND
        # =================================================
        #
        # IMPORTANT:
        # Native Streamlit text is intentionally used here.
        # This prevents HTML from appearing as literal text.
        #

        st.markdown(
            "## NEXORA"
        )

        st.caption(
            "Skill Intelligence Platform"
        )

        st.divider()


        # =================================================
        # WORKSPACE
        # =================================================

        st.markdown(
            "##### WORKSPACE"
        )

        navigation = [
            ("Dashboard", "Dashboard"),
            ("Competencies", "Competencies"),
            ("Learning", "Learning"),
            ("AI Assistant", "AI Assistant"),
            ("Assessments", "Assessments"),
            ("Analytics", "Analytics"),
        ]


        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"


        for label, page_name in navigation:

            if st.button(
                label,
                key=f"nav_{page_name}",
                use_container_width=True
            ):

                st.session_state.current_page = page_name
                st.rerun()


        # =================================================
        # ORGANIZATION
        # =================================================

        st.markdown(
            "##### ORGANIZATION"
        )

        organization_navigation = [
            ("Organization", "Organization"),
            ("Admin", "Admin"),
        ]


        for label, page_name in organization_navigation:

            if st.button(
                label,
                key=f"nav_{page_name}",
                use_container_width=True
            ):

                st.session_state.current_page = page_name
                st.rerun()


        # =================================================
        # SYSTEM
        # =================================================

        st.markdown(
            "##### SYSTEM"
        )

        if st.button(
            "Settings",
            key="nav_settings",
            use_container_width=True
        ):

            st.session_state.current_page = "Settings"
            st.rerun()


        # =================================================
        # SIDEBAR FOOTER
        # =================================================

        st.divider()

        st.caption(
            "NEXORA"
        )

        st.caption(
            "AI-powered learning intelligence"
        )


    return st.session_state.current_page