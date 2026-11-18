
import streamlit as st
from chatbot import get_answer
from styles.theme import apply_theme, brand_header, footer
from datetime import datetime

# ==================================================
# CAMPUSBOT BY TEAM96
# WHATSAPP-INSPIRED STUDENT CHAT
# ==================================================

st.set_page_config(
    page_title="CampusBot | National College",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

# ==================================================
# WHATSAPP-INSPIRED DARK THEME
# ==================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background: #0b141a;
}

/* Main content width */
.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111b21;
    border-right: 1px solid #26343d;
}

section[data-testid="stSidebar"] * {
    color: #e9edef;
}

/* Chat header */
.chat-header {
    background: #202c33;
    border: 1px solid #2a3942;
    border-radius: 16px 16px 0 0;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin-top: 15px;
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
    color: #e9edef;
    font-size: 18px;
    font-weight: 700;
}

.chat-subtitle {
    color: #aebac1;
    font-size: 12px;
    margin-top: 3px;
}

/* Chat background */
.chat-area {
    background-color: #0b141a;
    background-image:
        radial-gradient(#26343d 0.6px, transparent 0.6px);
    background-size: 19px 19px;
    border-left: 1px solid #26343d;
    border-right: 1px solid #26343d;
    min-height: 250px;
    padding: 14px;
}

/* Welcome card */
.welcome-card {
    background: #202c33;
    border: 1px solid #34434c;
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    margin: 20px auto;
    max-width: 600px;
}

.welcome-card h3 {
    color: #e9edef;
}

.welcome-card p {
    color: #b5c0c6;
    font-size: 14px;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    border-radius: 13px;
    padding: 12px 16px;
    margin-top: 10px;
    margin-bottom: 12px;
    max-width: 82%;
    border: none;
}

/* User message - RIGHT */
div[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: #005c4b;
    margin-left: auto;
    margin-right: 5px;
    flex-direction: row-reverse;
}

/* User message text */
div[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) [data-testid="stMarkdownContainer"] {
    color: #f1f7f5;
}

/* Assistant message - LEFT */
div[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: #202c33;
    margin-right: auto;
    margin-left: 5px;
    border: 1px solid #2a3942;
}

/* Assistant message text */
div[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) [data-testid="stMarkdownContainer"] {
    color: #e9edef;
}

/* Message text */
div[data-testid="stChatMessage"] p {
    font-size: 15px;
    line-height: 1.65;
}

/* Suggested questions */
div.stButton > button {
    border-radius: 12px;
    min-height: 48px;
    background: #202c33;
    border: 1px solid #34434c;
    color: #e9edef;
    transition: 0.2s ease;
}

div.stButton > button:hover {
    background: #075e54;
    border-color: #128c7e;
    color: white;
}

/* Chat input */
div[data-testid="stChatInput"] {
    background: #202c33;
    border: 1px solid #34434c;
    border-radius: 15px;
}

div[data-testid="stChatInput"] textarea {
    color: #e9edef;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #8696a0;
}

/* Divider */
hr {
    border-color: #26343d !important;
}

/* Section headings */
h1, h2, h3 {
    color: #e9edef !important;
}

/* Captions */
.stCaption {
    color: #aebac1;
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding-left: 10px;
        padding-right: 10px;
    }

    div[data-testid="stChatMessage"] {
        max-width: 94%;
    }

    .chat-header {
        padding: 12px;
    }

    .chat-title {
        font-size: 16px;
    }
}

</style>
""", unsafe_allow_html=True)


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

    st.markdown("**Quick Information**")

    st.markdown("""
    - College information
    - Courses and programmes
    - Admissions
    - Examinations
    - Campus facilities
    """)

    st.markdown("---")

    st.markdown("**Need assistance?**")

    st.caption(
        "Use the Complaints page in the sidebar "
        "to submit and track your complaints."
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

    st.markdown("""
    <div style="
        text-align:center;
        color:#8696a0;
        font-size:11px;
        padding:20px 0;
        letter-spacing:1px;
    ">
        CAMPUSBOT<br>
        POWERED BY TEAM96
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# MAIN CHAT HEADER
# ==================================================

st.markdown("""
<div class="chat-header">
    <div class="chat-avatar">🎓</div>
    <div>
        <div class="chat-title">CampusBot</div>
        <div class="chat-subtitle">
            The National College · Virtual Assistant
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# WELCOME MESSAGE
# ==================================================

if not st.session_state.messages:

    st.markdown("""
    <div class="chat-area">
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
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ Suggested Questions")

    suggestions = [
        "Tell me about National College",
        "Which courses are available?",
        "How can I get admission?",
        "Where is the college located?",
        "Does NCB offer BCA?",
        "What facilities are available?"
    ]

    columns = st.columns(2)

    for index, suggestion in enumerate(suggestions):

        with columns[index % 2]:

            if st.button(
                suggestion,
                key=f"suggestion_{index}",
                use_container_width=True
            ):
                st.session_state.pending_question = suggestion
                st.rerun()


# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    role = message["role"]

    avatar = "👤" if role == "user" else "🎓"

    with st.chat_message(role, avatar=avatar):

        st.markdown(message["content"])

        timestamp = message.get("timestamp", "")

        if timestamp:
            st.caption(timestamp)


# ==================================================
# CHAT INPUT
# ==================================================

question = st.chat_input(
    "Message CampusBot..."
)

if st.session_state.pending_question:

    question = st.session_state.pending_question

    st.session_state.pending_question = None


# ==================================================
# PROCESS QUESTION
# ==================================================

if question:

    question = question.strip()

    if question:

        current_time = datetime.now().strftime("%I:%M %p")

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": question,
            "timestamp": current_time
        })

        # Generate assistant response
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

        # Save assistant response
        response_time = datetime.now().strftime("%I:%M %p")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "timestamp": response_time
        })

        st.rerun()


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

footer()
