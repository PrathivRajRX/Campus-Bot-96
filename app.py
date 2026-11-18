
import streamlit as st
from chatbot import get_answer
from styles.theme import apply_theme, brand_header, footer
from datetime import datetime
import json
from pathlib import Path

# ==================================================
# CAMPUSBOT BY TEAM96 - STUDENT CHAT
# ==================================================

st.set_page_config(
    page_title="CampusBot | National College",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ==================================================
# WHATSAPP-INSPIRED DESIGN + MOBILE FIX
# ==================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #0b141a;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    section[data-testid="stSidebar"] {
        background: #111b21;
        border-right: 1px solid #26343d;
    }

    section[data-testid="stSidebar"] * {
        color: #e9edef;
    }

    .chat-header {
        background: #202c33;
        border: 1px solid #2a3942;
        border-radius: 16px;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 12px 0 16px;
    }

    .chat-avatar {
        background: #075e54;
        border-radius: 50%;
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 25px;
        flex-shrink: 0;
    }

    .chat-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 700;
    }

    .chat-subtitle {
        color: #cbd5e1;
        font-size: 12px;
        margin-top: 3px;
    }

    .welcome-card {
        background: #202c33;
        border: 1px solid #34434c;
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        margin: 12px auto 20px;
        max-width: 650px;
    }

    .welcome-card h3 {
        color: #ffffff !important;
    }

    .welcome-card p {
        color: #e2e8f0 !important;
        font-size: 14px;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 13px;
        padding: 12px 16px;
        margin-top: 10px;
        margin-bottom: 12px;
        max-width: 90%;
        border: none;
    }

    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: #005c4b;
        margin-left: auto;
        margin-right: 5px;
        flex-direction: row-reverse;
    }

    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: #202c33;
        margin-right: auto;
        margin-left: 5px;
        border: 1px solid #2a3942;
    }

    div[data-testid="stChatMessage"] p {
        color: #ffffff !important;
        font-size: 15px;
        line-height: 1.65;
    }

    /* CHAT INPUT */

    div[data-testid="stChatInput"] {
        background: #202c33 !important;
        border: 1px solid #526773 !important;
        border-radius: 15px !important;
    }

    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] textarea:focus,
    div[data-testid="stChatInput"] [data-baseweb="textarea"] textarea {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important;
        opacity: 1 !important;
        font-size: 16px !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #d1d5db !important;
        -webkit-text-fill-color: #d1d5db !important;
        opacity: 1 !important;
    }

    /* BUTTONS */

    div.stButton > button {
        border-radius: 12px;
        min-height: 46px;
        background: #202c33;
        border: 1px solid #526773;
        color: #ffffff !important;
    }

    div.stButton > button:hover {
        background: #075e54;
        border-color: #128c7e;
        color: #ffffff !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 10px;
            padding-right: 10px;
        }

        .chat-header {
            padding: 12px;
        }

        .chat-title {
            font-size: 16px;
        }

        div[data-testid="stChatMessage"] {
            max-width: 98%;
        }

        div[data-testid="stChatMessage"] p {
            font-size: 16px !important;
            line-height: 1.7 !important;
        }

        div[data-testid="stChatInput"] textarea,
        div[data-testid="stChatInput"] textarea:focus {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            caret-color: #ffffff !important;
            font-size: 16px !important;
        }

        div[data-testid="stChatInput"] textarea::placeholder {
            color: #d1d5db !important;
            -webkit-text-fill-color: #d1d5db !important;
            opacity: 1 !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# FAQ-BASED SUGGESTIONS
# ==================================================

def load_suggestion_faqs():
    faq_path = Path(__file__).resolve().parent / "faqs.json"

    try:
        with faq_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (OSError, json.JSONDecodeError):
        return []


def get_follow_up_suggestions(previous_question, limit=3):

    faqs = load_suggestion_faqs()
    candidates = []

    for faq in faqs:
        examples = faq.get("questions", [])

        if not examples and faq.get("question"):
            examples = [faq["question"]]

        for item in examples:
            if isinstance(item, str) and item.strip():
                candidates.append(
                    (item.strip(), faq.get("category", ""))
                )

    if not candidates:
        return []

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        texts = [item[0] for item in candidates]

        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english"
        )

        matrix = vectorizer.fit_transform(
            texts + [previous_question]
        )

        scores = cosine_similarity(
            matrix[-1],
            matrix[:-1]
        ).ravel()

        ranked = sorted(
            range(len(candidates)),
            key=lambda i: float(scores[i]),
            reverse=True
        )

        previous = previous_question.strip().lower().rstrip("?.! ")
        results = []

        for index in ranked:
            candidate = candidates[index][0]
            normalized = candidate.lower().rstrip("?.! ")

            if normalized == previous:
                continue

            if float(scores[index]) < 0.04:
                continue

            if candidate not in results:
                results.append(candidate)

            if len(results) == limit:
                break

        return results

    except (ValueError, ImportError):
        return []


# Common questions for first-time visitors
FIRST_VISIT_QUESTIONS = [
    "What courses are available?",
    "How can I get admission?",
    "Where is the college located?",
]


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    brand_header()

    st.markdown("---")

    st.markdown("### 🎓 Student Portal")
    st.caption("Your digital campus companion")

    st.markdown("---")

    st.markdown("### 💡 Quick Information")

    quick_questions = {
        "🏫 College Information": "Tell me about National College",
        "📚 Courses & Programmes": "Which courses are available?",
        "🎓 Admissions": "How can I get admission?",
        "📝 Examinations": "Tell me about examinations",
        "🏛️ Campus Facilities": "What facilities are available?",
    }

    for label, query in quick_questions.items():

        if st.button(
            label,
            key=f"quick_{label}",
            use_container_width=True
        ):
            st.session_state.pending_question = query
            st.rerun()

    st.markdown("---")

    st.markdown("**Need assistance?**")
    st.caption(
        "Use the Complaints button on the main screen "
        "to submit or track a complaint."
    )

    st.markdown("---")

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

    st.markdown("---")

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#cbd5e1;
            font-size:11px;
            padding:16px 0;
            letter-spacing:1px;
        ">
            CAMPUSBOT<br>
            POWERED BY TEAM96
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# MAIN CHAT HEADER
# ==================================================

st.markdown(
    """
    <div class="chat-header">
        <div class="chat-avatar">🎓</div>
        <div>
            <div class="chat-title">CampusBot</div>
            <div class="chat-subtitle">
                The National College · Virtual Assistant
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# COMPLAINT NAVIGATION
# ==================================================

st.markdown("### Student Support")

st.page_link(
    "pages/2_Complaints.py",
    label="📝 Submit or Track a Complaint",
    icon="📝",
    use_container_width=True
)

st.caption(
    "Submit a new complaint or check its status "
    "using your complaint reference ID."
)

st.divider()


# ==================================================
# WELCOME MESSAGE
# ==================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome-card">
            <h3>👋 Welcome to CampusBot!</h3>
            <p>
                Your digital campus companion for
                The National College, Basavanagudi.
            </p>
            <p>
                Ask me about courses, admissions,
                examinations, college facilities and more.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    role = message["role"]
    avatar = "👤" if role == "user" else "🎓"

    with st.chat_message(role, avatar=avatar):

        st.markdown(message["content"])

        if message.get("timestamp"):
            st.caption(message["timestamp"])


# ==================================================
# DYNAMIC SUGGESTED QUESTIONS
# ==================================================

if st.session_state.messages:

    latest_user_question = next(
        (
            message["content"]
            for message in reversed(st.session_state.messages)
            if message.get("role") == "user"
        ),
        ""
    )

    suggested_questions = get_follow_up_suggestions(
        latest_user_question,
        limit=3
    )

else:
    suggested_questions = FIRST_VISIT_QUESTIONS


if suggested_questions:

    st.markdown(
        """
        <div style="
            color:#dbeafe;
            font-weight:700;
            margin:8px 0 6px;
        ">
            💡 You can also ask
        </div>
        """,
        unsafe_allow_html=True
    )

    suggestion_columns = st.columns(
        len(suggested_questions)
    )

    for index, suggestion in enumerate(suggested_questions):

        with suggestion_columns[index]:

            if st.button(
                suggestion,
                key=f"followup_{len(st.session_state.messages)}_{index}",
                use_container_width=True
            ):
                st.session_state.pending_question = suggestion
                st.rerun()


# ==================================================
# CHAT INPUT
# ==================================================

question = st.chat_input("Message CampusBot...")

if st.session_state.pending_question:

    question = st.session_state.pending_question
    st.session_state.pending_question = None


# ==================================================
# PROCESS QUESTION
# ==================================================

if question:

    question = question.strip()

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question,
            "timestamp": datetime.now().strftime("%I:%M %p")
        })

        try:

            with st.spinner("CampusBot is typing..."):
                answer = get_answer(question)

            if not answer:
                answer = (
                    "Sorry, I couldn't find an answer. "
                    "Please contact the college administration."
                )

        except Exception as error:

            answer = (
                "Sorry, something went wrong while processing "
                "your question. Please try again."
            )

            print("Chatbot Error:", error)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "timestamp": datetime.now().strftime("%I:%M %p")
        })

        st.rerun()


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")
footer()
