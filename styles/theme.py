
import streamlit as st


BG = "#090E1B"
SIDEBAR = "#0D1525"
CARD = "#131F33"
CARD_HOVER = "#192942"
BORDER = "#26364F"

PRIMARY = "#3B82F6"
PRIMARY_HOVER = "#2563EB"

TEXT = "#F1F5F9"
MUTED = "#94A3B8"

SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"


def apply_theme():

    st.markdown(
        f"""
        <style>

        /* GLOBAL */

        .stApp {{
            background: {BG};
            color: {TEXT};
        }}

        [data-testid="stHeader"] {{
            background: {BG};
        }}

        #MainMenu, footer {{
            visibility: hidden;
        }}

        .block-container {{
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }}

        html, body, [class*="css"] {{
            font-family: Inter, -apple-system,
                         BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}

        /* TEXT */

        h1, h2, h3, h4 {{
            color: {TEXT} !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }}

        p, label, span {{
            color: inherit;
        }}

        [data-testid="stCaptionContainer"] {{
            color: #CBD5E1 !important;
        }}

        /* SIDEBAR */

        [data-testid="stSidebar"] {{
            background: {SIDEBAR};
            border-right: 1px solid {BORDER};
        }}

        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 2rem;
        }}

        [data-testid="stSidebar"] * {{
            color: {TEXT};
        }}

        [data-testid="stSidebar"] a {{
            border-radius: 10px;
        }}

        /* INPUTS */

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input {{
            background: {CARD} !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: 1px solid {BORDER} !important;
            border-radius: 10px !important;
            caret-color: #FFFFFF !important;
        }}

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {{
            color: #CBD5E1 !important;
            -webkit-text-fill-color: #CBD5E1 !important;
            opacity: 1 !important;
        }}

        .stTextInput input:focus,
        .stTextArea textarea:focus {{
            border-color: {PRIMARY} !important;
            box-shadow: 0 0 0 1px {PRIMARY} !important;
        }}

        [data-baseweb="select"] > div {{
            background: {CARD} !important;
            border-color: {BORDER} !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
        }}

        /* CHAT INPUT */

        div[data-testid="stChatInput"] {{
            background: #202C33 !important;
            border: 1px solid #526773 !important;
            border-radius: 15px !important;
        }}

        div[data-testid="stChatInput"] textarea,
        div[data-testid="stChatInput"] textarea:focus {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            caret-color: #FFFFFF !important;
            opacity: 1 !important;
            font-size: 16px !important;
        }}

        div[data-testid="stChatInput"] textarea::placeholder {{
            color: #D1D5DB !important;
            -webkit-text-fill-color: #D1D5DB !important;
            opacity: 1 !important;
        }}

        /* BUTTONS */

        .stButton button,
        .stFormSubmitButton button,
        .stDownloadButton button {{
            background: {PRIMARY};
            color: #FFFFFF !important;
            border: 1px solid {PRIMARY};
            border-radius: 10px;
            min-height: 42px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}

        .stButton button:hover,
        .stFormSubmitButton button:hover,
        .stDownloadButton button:hover {{
            background: {PRIMARY_HOVER};
            border-color: {PRIMARY_HOVER};
            transform: translateY(-1px);
        }}

        /* PAGE LINKS */

        [data-testid="stPageLink"] a {{
            background: {PRIMARY};
            color: #FFFFFF !important;
            border-radius: 10px;
            min-height: 44px;
            font-weight: 600;
        }}

        /* CARDS */

        [data-testid="stMetric"] {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 18px;
        }}

        [data-testid="stMetricLabel"] {{
            color: {MUTED} !important;
        }}

        [data-testid="stMetricValue"] {{
            color: {TEXT} !important;
        }}

        /* CONTAINERS */

        [data-testid="stVerticalBlockBorderWrapper"] {{
            border-color: {BORDER};
            border-radius: 14px;
        }}

        [data-testid="stExpander"] {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 12px;
        }}

        /* TABS */

        .stTabs [data-baseweb="tab-list"] {{
            gap: 12px;
            border-bottom: 1px solid {BORDER};
        }}

        .stTabs [data-baseweb="tab"] {{
            color: {MUTED};
            font-weight: 600;
        }}

        .stTabs [aria-selected="true"] {{
            color: {PRIMARY} !important;
        }}

        /* CHECKBOX */

        [data-testid="stCheckbox"] label {{
            color: {TEXT} !important;
        }}

        /* RADIO BUTTONS */

        [data-testid="stRadio"] label {{
            color: {TEXT} !important;
        }}

        /* ALERTS */

        [data-testid="stAlert"] {{
            border-radius: 12px;
        }}

        /* DIVIDERS */

        hr {{
            border-color: {BORDER};
        }}

        /* TABLES */

        [data-testid="stDataFrame"] {{
            border: 1px solid {BORDER};
            border-radius: 12px;
        }}

        /* BRANDING */

        .brand-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 25px;
        }}

        .brand-icon {{
            background: linear-gradient(
                135deg,
                #2563EB,
                #7C3AED
            );
            border-radius: 12px;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 25px;
        }}

        .brand-name {{
            font-size: 25px;
            font-weight: 800;
            color: {TEXT};
            line-height: 1.2;
        }}

        .brand-tag {{
            color: {MUTED};
            font-size: 10px;
            letter-spacing: 2px;
            font-weight: 700;
        }}

        .hero-card {{
            background: linear-gradient(
                135deg,
                #172B4D,
                #111B30
            );
            border: 1px solid {BORDER};
            border-radius: 18px;
            padding: 30px;
            margin-bottom: 25px;
        }}

        .hero-title {{
            color: #FFFFFF;
            font-size: 32px;
            font-weight: 800;
        }}

        .hero-subtitle {{
            color: #D1DCEB;
            font-size: 15px;
        }}

        .custom-footer {{
            text-align: center;
            color: {MUTED};
            font-size: 11px;
            padding: 25px 0 10px;
            border-top: 1px solid {BORDER};
            margin-top: 40px;
        }}

        /* MOBILE */

        @media(max-width: 768px) {{

            .block-container {{
                padding: 1rem 10px 5rem;
            }}

            .hero-title {{
                font-size: 24px;
            }}

            .brand-name {{
                font-size: 21px;
            }}

            .stApp,
            .stApp p,
            .stApp li,
            .stApp label,
            .stMarkdown,
            .stMarkdown p {{
                color: #F1F5F9 !important;
                opacity: 1 !important;
            }}

            h1, h2, h3, h4, h5 {{
                color: #FFFFFF !important;
                opacity: 1 !important;
            }}

            .stCaption,
            [data-testid="stCaptionContainer"] p {{
                color: #CBD5E1 !important;
                opacity: 1 !important;
            }}

            div[data-testid="stChatInput"] textarea,
            div[data-testid="stChatInput"] textarea:focus,
            .stTextInput input,
            .stTextArea textarea {{
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
                caret-color: #FFFFFF !important;
                font-size: 16px !important;
            }}

            div[data-testid="stChatInput"] textarea::placeholder,
            input::placeholder,
            textarea::placeholder {{
                color: #CBD5E1 !important;
                -webkit-text-fill-color: #CBD5E1 !important;
                opacity: 1 !important;
            }}

            .stButton button {{
                color: #FFFFFF !important;
                opacity: 1 !important;
                min-height: 48px;
            }}
        }}

        </style>
        """,
        unsafe_allow_html=True
    )



def brand_header():

    st.markdown(
        """
        <div class="brand-header">
            <div class="brand-icon">🎓</div>
            <div>
                <div class="brand-name">CampusBot</div>
                <div class="brand-tag">BY TEAM96</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def footer():

    st.markdown(
        """
        <div class="custom-footer">
            CAMPUSBOT BY TEAM96<br>
            J PRATHIV RAJ SHASHANK SIDDHARTH
            · NATIONAL COLLEGE, BASAVANAGUDI
        </div>
        """,
        unsafe_allow_html=True
    )


def hero(title, subtitle):

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
