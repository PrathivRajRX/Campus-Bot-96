
import streamlit as st
from chatbot import get_answer
from styles.theme import apply_theme, brand_header, hero, footer


# ==========================================
# CAMPUSBOT BY TEAM96
# STUDENT CHATBOT APPLICATION
# ==========================================

st.set_page_config(
    page_title="CampusBot | National College",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply shared theme
apply_theme()


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ==========================================
# SIDEBAR
# ==========================================

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

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#94A3B8;
            font-size:11px;
            padding-top:25px;
        ">
            CAMPUSBOT<br>
            POWERED BY TEAM96
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# MAIN HEADER
# ==========================================

brand_header()

hero(
    "Your Campus. Connected.",
    "Welcome to CampusBot — your virtual assistant "
    "for The National College, Basavanagudi."
)

# ==========================================
# WELCOME SECTION
# ==========================================

st.markdown("## 👋 How can we help you today?")

st.markdown(
    "Ask questions about your college, courses, "
    "admissions, examinations and campus life."
)

st.markdown("")


# ==========================================
# SUGGESTED QUESTIONS
# ==========================================

st.markdown("### ✨ Suggested Questions")

suggestions = [
    "Tell me about National College",
    "Which courses are available?",
    "How can I get admission?",
    "Where is the college located?",
    "Does NCB offer BCA?",
    "What facilities are available?"
]

columns = st.columns(3)

for index, suggestion in enumerate(suggestions):

    with columns[index % 3]:

        if st.button(
            suggestion,
            key=f"suggestion_{index}",
            use_container_width=True
        ):
            st.session_state.pending_question = suggestion
            st.rerun()


st.markdown("---")


# ==========================================
# CHAT SECTION
# ==========================================

st.markdown("## 💬 CampusBot Assistant")

st.caption(
    "Your questions, answered by your virtual campus assistant."
)


# Display conversation history

if not st.session_state.messages:

    with st.container(border=True):

        st.markdown("### 🎓 Hello! I'm CampusBot.")

        st.write(
            "I'm here to make your college experience easier. "
            "Ask me anything about National College, "
            "Basavanagudi."
        )

        st.info(
            "Try asking: What courses does the college offer?"
        )


for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user", avatar="👤"):
            st.markdown(message["content"])

    else:

        with st.chat_message("assistant", avatar="🎓"):
            st.markdown(message["content"])


# ==========================================
# CHAT INPUT
# ==========================================

question = st.chat_input(
    "Ask CampusBot anything about your college..."
)

# Suggested question takes priority

if st.session_state.pending_question:

    question = st.session_state.pending_question

    st.session_state.pending_question = None


# ==========================================
# PROCESS QUESTION
# ==========================================

if question:

    question = question.strip()

    if question:

        # Save user message

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        # Generate answer

        try:

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

        # Save assistant message

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

footer()
