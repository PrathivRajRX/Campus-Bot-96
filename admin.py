
import os
import json
import hmac
import csv
import io
from pathlib import Path
from datetime import datetime, timezone

import streamlit as st
import pandas as pd

from styles.theme import apply_theme

# ==================================================
# CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
COMPLAINTS_FILE = BASE_DIR / "complaints.json"
FAQ_FILE = BASE_DIR / "faqs.json"

ADMIN_PASSWORD = os.environ.get("CAMPUSBOT_ADMIN_PASSWORD", "")

STATUSES = ["Submitted", "Under Review", "Resolved", "Rejected"]

DEPARTMENTS = [
    "Not Assigned",
    "Principal's Office",
    "Administration",
    "Academic Department",
    "Examination Section",
    "Accounts Department",
    "Library",
    "Infrastructure",
    "Student Welfare",
    "Anti-Ragging Committee",
    "Internal Complaints Committee",
    "Other",
]

# ==================================================
# PAGE SETUP
# ==================================================

st.set_page_config(
    page_title="CampusBot Admin | Team96",
    page_icon="🎓",
    layout="wide",
)

apply_theme()

st.markdown("""
<style>
.admin-hero {
    background: linear-gradient(120deg, #172d50, #101a30);
    border: 1px solid #263e62;
    border-radius: 18px;
    padding: 28px 32px;
    margin: 12px 0 25px 0;
}
.admin-hero h1 {
    color: white;
    font-size: 30px;
    margin: 8px 0;
}
.admin-hero p {
    color: #a9c9f4;
    margin: 8px 0 0 0;
}
.brand-small {
    color: #8bbcff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
}
.section-note {
    color: #8c9bb2;
    font-size: 14px;
}
.metric-card {
    background: #111d31;
    border: 1px solid #263a58;
    border-radius: 14px;
    padding: 18px;
    min-height: 105px;
}
.metric-label {
    color: #a8b9d1;
    font-size: 13px;
}
.metric-value {
    color: white;
    font-size: 30px;
    font-weight: 750;
    margin-top: 8px;
}
.admin-footer {
    border-top: 1px solid #26354c;
    margin-top: 40px;
    padding: 22px 0;
    text-align: center;
    color: #8294ae;
    font-size: 11px;
    letter-spacing: 1px;
}
div[data-testid="stMetric"] {
    background: #111d31;
    border: 1px solid #263a58;
    border-radius: 12px;
    padding: 16px;
}
div[data-testid="stMetric"] label {
    color: #a8b9d1 !important;
}
div[data-testid="stMetricValue"] {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA HELPERS
# ==================================================

def load_json(path, default):
    if not path.exists():
        return default

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except (json.JSONDecodeError, OSError) as error:
        st.error(f"Could not read {path.name}: {error}")
        return default


def save_json(path, data):
    temp_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        temp_path.replace(path)
        return True

    except OSError as error:
        st.error(f"Could not save {path.name}: {error}")
        return False


def load_complaints():
    data = load_json(COMPLAINTS_FILE, [])
    return data if isinstance(data, list) else []


def load_faqs():
    data = load_json(FAQ_FILE, [])
    return data if isinstance(data, list) else []


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def format_date(value):
    if not value:
        return "Not available"

    try:
        date = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return date.astimezone().strftime("%d %b %Y, %I:%M %p")
    except (ValueError, TypeError):
        return str(value)


def status_color(status):
    return {
        "Submitted": "#60a5fa",
        "Under Review": "#fbbf24",
        "Resolved": "#34d399",
        "Rejected": "#f87171",
    }.get(status, "#94a3b8")


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def find_complaint(complaints, complaint_id):
    for complaint in complaints:
        if complaint.get("id") == complaint_id:
            return complaint
    return None


def add_activity(complaint, action, details):
    history = complaint.get("activity_history", [])

    if not isinstance(history, list):
        history = []

    history.append({
        "timestamp": now_iso(),
        "actor": "Admin",
        "action": action,
        "details": details,
    })

    complaint["activity_history"] = history


def faq_questions(faq):
    questions = faq.get("questions", faq.get("question", []))

    if isinstance(questions, str):
        return [questions] if questions.strip() else []

    if isinstance(questions, list):
        return [str(q) for q in questions if str(q).strip()]

    return []


def update_faq_questions(faq, questions):
    # Preserve the existing FAQ question format where possible.
    if "questions" in faq:
        faq["questions"] = questions
    elif "question" in faq and len(questions) == 1:
        faq["question"] = questions[0]
    else:
        faq["questions"] = questions
        faq.pop("question", None)


# ==================================================
# LOGIN
# ==================================================

if not ADMIN_PASSWORD:
    st.error(
        "Admin password is not configured. "
        "Set CAMPUSBOT_ADMIN_PASSWORD before starting the app."
    )
    st.stop()

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:

    st.markdown("""
    <div class="admin-hero">
        <div class="brand-small">TEAM96 PRESENTS</div>
        <h1>🎓 CampusBot Administration</h1>
        <p>Secure administrator access · National College, Basavanagudi</p>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.2, 1])

    with center:
        with st.container(border=True):
            st.subheader("Administrator Login")

            with st.form("admin_login"):
                password = st.text_input("Admin Password", type="password")
                login = st.form_submit_button(
                    "Sign In",
                    type="primary",
                    use_container_width=True,
                )

            if login:
                if hmac.compare_digest(password, ADMIN_PASSWORD):
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password.")

    st.stop()

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown("## 🎓 CampusBot")
    st.markdown("**ADMIN CONTROL PANEL**")
    st.caption("National College, Basavanagudi")
    st.divider()

    st.markdown("### Administrator")
    st.success("Authenticated")

    if st.button("Logout", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.rerun()

    st.divider()
    st.caption("TEAM96 · CAMPUSBOT")
    st.caption("Administration Portal")

# ==================================================
# HEADER AND DATA
# ==================================================

st.markdown("""
<div class="admin-hero">
    <div class="brand-small">CAMPUSBOT · TEAM96</div>
    <h1>🎓 Admin Dashboard</h1>
    <p>Manage student grievances, monitor resolutions and maintain college FAQs.</p>
</div>
""", unsafe_allow_html=True)

complaints = load_complaints()
faqs = load_faqs()

dashboard_tab, complaints_tab, faq_tab = st.tabs([
    "📊 Dashboard",
    "📩 Manage Complaints",
    "📚 Manage FAQs",
])

# ==================================================
# DASHBOARD
# ==================================================

with dashboard_tab:

    st.subheader("Dashboard Overview")
    st.markdown(
        '<p class="section-note">Live overview of student grievance activity.</p>',
        unsafe_allow_html=True,
    )

    total = len(complaints)
    submitted = sum(c.get("status", "Submitted") == "Submitted" for c in complaints)
    under_review = sum(c.get("status") == "Under Review" for c in complaints)
    resolved = sum(c.get("status") == "Resolved" for c in complaints)
    rejected = sum(c.get("status") == "Rejected" for c in complaints)

    columns = st.columns(5)
    metrics = [
        ("Total Complaints", total),
        ("Submitted", submitted),
        ("Under Review", under_review),
        ("Resolved", resolved),
        ("Rejected", rejected),
    ]

    for column, (label, value) in zip(columns, metrics):
        with column:
            metric_card(label, value)

    st.divider()

    chart_col, stats_col = st.columns([1.2, 1])

    with chart_col:
        st.subheader("Complaint Status")

        chart_data = pd.DataFrame({
            "Status": ["Submitted", "Under Review", "Resolved", "Rejected"],
            "Complaints": [submitted, under_review, resolved, rejected],
        })

        st.bar_chart(
            chart_data,
            x="Status",
            y="Complaints",
            use_container_width=True,
        )

    with stats_col:
        st.subheader("Quick Statistics")

        resolution_rate = (resolved / total * 100) if total else 0

        st.metric("Resolution Rate", f"{resolution_rate:.1f}%")
        st.metric("Total FAQs", len(faqs))

        assigned = sum(
            bool(c.get("assigned_department"))
            and c.get("assigned_department") != "Not Assigned"
            for c in complaints
        )

        st.metric("Complaints Assigned", assigned)

    st.divider()
    st.subheader("Recent Complaints")

    if complaints:
        recent = sorted(
            complaints,
            key=lambda c: c.get("submitted_at", ""),
            reverse=True,
        )[:8]

        for complaint in recent:
            complaint_id = complaint.get("id", "Unknown")
            subject = complaint.get("subject", "No subject")
            status = complaint.get("status", "Submitted")
            color = status_color(status)

            with st.expander(f"{complaint_id} · {subject}"):
                st.write(f"**Student:** {complaint.get('name', 'N/A')}")
                st.write(f"**Category:** {complaint.get('category', 'N/A')}")
                st.write(f"**Submitted:** {format_date(complaint.get('submitted_at'))}")
                st.markdown(
                    f"**Status:** <span style='color:{color};font-weight:700'>{status}</span>",
                    unsafe_allow_html=True,
                )
                st.write(
                    f"**Department:** {complaint.get('assigned_department', 'Not Assigned')}"
                )
    else:
        st.info("No complaints have been submitted yet.")

# ==================================================
# COMPLAINT MANAGEMENT
# ==================================================

with complaints_tab:

    st.subheader("Complaint Management")
    st.caption("Search, review, assign and update student complaints.")

    if not complaints:
        st.info("There are no complaints to manage.")

    else:
        search_col, status_col, category_col = st.columns([2, 1, 1])

        with search_col:
            search_text = st.text_input(
                "Search complaints",
                placeholder="Search ID, name, email or subject...",
            ).strip().lower()

        with status_col:
            selected_status = st.selectbox(
                "Filter by status",
                ["All"] + STATUSES,
            )

        categories = sorted({
            c.get("category", "Other") for c in complaints
        })

        with category_col:
            selected_category = st.selectbox(
                "Filter by category",
                ["All"] + categories,
            )

        filtered = []

        for complaint in complaints:
            searchable = " ".join([
                str(complaint.get("id", "")),
                str(complaint.get("name", "")),
                str(complaint.get("email", "")),
                str(complaint.get("subject", "")),
            ]).lower()

            if search_text and search_text not in searchable:
                continue

            if selected_status != "All" and complaint.get("status", "Submitted") != selected_status:
                continue

            if selected_category != "All" and complaint.get("category", "Other") != selected_category:
                continue

            filtered.append(complaint)

        st.caption(f"Showing {len(filtered)} of {len(complaints)} complaints")

        for complaint in filtered:

            complaint_id = complaint.get("id", "")
            subject = complaint.get("subject", "No subject")
            current_status = complaint.get("status", "Submitted")

            with st.expander(
                f"📩 {complaint_id} | {subject} | {current_status}"
            ):

                details_col, update_col = st.columns([1, 1])

                with details_col:
                    st.markdown("### Student Details")
                    st.write(f"**Name:** {complaint.get('name', 'N/A')}")
                    st.write(f"**Email:** {complaint.get('email', 'N/A')}")
                    st.write(f"**Phone:** {complaint.get('phone', 'N/A')}")

                    st.divider()
                    st.markdown("### Complaint Details")
                    st.write(f"**ID:** {complaint_id}")
                    st.write(f"**Category:** {complaint.get('category', 'N/A')}")
                    st.write(f"**Subject:** {subject}")
                    st.write(f"**Submitted:** {format_date(complaint.get('submitted_at'))}")
                    st.markdown("**Description**")
                    st.write(complaint.get("description", "No description"))

                with update_col:
                    st.markdown("### Update Complaint")

                    if current_status not in STATUSES:
                        current_status = "Submitted"

                    current_department = complaint.get(
                        "assigned_department",
                        "Not Assigned",
                    )

                    if current_department not in DEPARTMENTS:
                        current_department = "Not Assigned"

                    with st.form(f"update_{complaint_id}"):

                        new_status = st.selectbox(
                            "Complaint Status",
                            STATUSES,
                            index=STATUSES.index(current_status),
                        )

                        new_department = st.selectbox(
                            "Assign Department",
                            DEPARTMENTS,
                            index=DEPARTMENTS.index(current_department),
                        )

                        new_remarks = st.text_area(
                            "Administration Remarks",
                            value=complaint.get("admin_remarks", ""),
                            height=120,
                            placeholder="Enter an update for the student...",
                        )

                        save_clicked = st.form_submit_button(
                            "💾 Save Changes",
                            type="primary",
                            use_container_width=True,
                        )

                    if save_clicked:
                        target = find_complaint(complaints, complaint_id)

                        if target is not None:
                            old_status = target.get("status", "Submitted")
                            old_department = target.get(
                                "assigned_department",
                                "Not Assigned",
                            )
                            old_remarks = target.get("admin_remarks", "")

                            changes = []

                            if old_status != new_status:
                                changes.append(
                                    f"Status changed from {old_status} to {new_status}"
                                )

                            if old_department != new_department:
                                changes.append(
                                    f"Department changed from {old_department} to {new_department}"
                                )

                            if old_remarks != new_remarks.strip():
                                changes.append("Administration remarks updated")

                            target["status"] = new_status
                            target["assigned_department"] = new_department
                            target["admin_remarks"] = new_remarks.strip()

                            if changes:
                                add_activity(
                                    target,
                                    "Complaint updated",
                                    "; ".join(changes),
                                )

                            if save_json(COMPLAINTS_FILE, complaints):
                                st.success("Complaint updated successfully.")
                                st.rerun()

                st.divider()
                st.markdown("### 🕒 Complaint Activity History")

                history = complaint.get("activity_history", [])

                if history:
                    for event in reversed(history):
                        st.markdown(
                            f"**{event.get('action', 'Update')}** · "
                            f"{format_date(event.get('timestamp'))}"
                        )
                        st.caption(
                            f"{event.get('actor', 'Admin')}: "
                            f"{event.get('details', '')}"
                        )
                else:
                    st.caption(
                        "No activity history recorded yet. "
                        "Changes made from this upgraded version will appear here."
                    )

        st.divider()
        st.subheader("Export Complaints")

        csv_buffer = io.StringIO()

        fieldnames = [
            "id",
            "name",
            "email",
            "phone",
            "category",
            "subject",
            "description",
            "status",
            "assigned_department",
            "admin_remarks",
            "submitted_at",
        ]

        writer = csv.DictWriter(
            csv_buffer,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(complaints)

        st.download_button(
            "⬇️ Download All Complaints (CSV)",
            data=csv_buffer.getvalue().encode("utf-8-sig"),
            file_name="campusbot_complaints.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ==================================================
# FAQ MANAGEMENT
# ==================================================

with faq_tab:

    st.subheader("FAQ Management")
    st.caption("Manage the knowledge base used by the student chatbot.")

    st.metric("Total FAQ Entries", len(faqs))

    # ADD FAQ
    with st.expander("➕ Add a New FAQ"):

        with st.form("add_faq_form"):

            new_category = st.text_input(
                "Category",
                placeholder="Example: Admissions",
            )

            new_questions = st.text_area(
                "Questions (one per line)",
                height=120,
                placeholder="How do I apply?\nWhat is the admission process?",
            )

            new_answer = st.text_area(
                "Answer",
                height=150,
                placeholder="Enter the answer...",
            )

            add_clicked = st.form_submit_button(
                "➕ Add FAQ",
                type="primary",
                use_container_width=True,
            )

        if add_clicked:
            questions = [
                q.strip()
                for q in new_questions.splitlines()
                if q.strip()
            ]

            if not new_category.strip():
                st.error("Please enter a category.")
            elif not questions:
                st.error("Enter at least one question.")
            elif not new_answer.strip():
                st.error("Please enter an answer.")
            else:
                faqs.append({
                    "category": new_category.strip(),
                    "questions": questions,
                    "answer": new_answer.strip(),
                })

                if save_json(FAQ_FILE, faqs):
                    st.success("FAQ added successfully.")
                    st.rerun()

    st.divider()
    st.subheader("Existing FAQs")

    faq_search = st.text_input(
        "Search FAQs",
        placeholder="Search category, question or answer...",
    ).strip().lower()

    matching_faqs = []

    for index, faq in enumerate(faqs):
        questions = faq_questions(faq)

        searchable = " ".join([
            str(faq.get("category", "")),
            " ".join(questions),
            str(faq.get("answer", "")),
        ]).lower()

        if not faq_search or faq_search in searchable:
            matching_faqs.append((index, faq))

    st.caption(f"{len(matching_faqs)} matching FAQ entries")

    for index, faq in matching_faqs:

        original_questions = faq_questions(faq)

        with st.expander(
            f"📚 {faq.get('category', 'Uncategorised')} · FAQ {index + 1}"
        ):

            st.markdown("### Current FAQ")

            for question in original_questions:
                st.write(f"• {question}")

            st.markdown("**Answer**")
            st.write(faq.get("answer", "No answer available."))

            st.divider()
            st.markdown("### Edit FAQ")

            with st.form(f"edit_faq_{index}"):

                edited_category = st.text_input(
                    "Category",
                    value=faq.get("category", ""),
                    key=f"edit_category_{index}",
                )

                edited_questions = st.text_area(
                    "Questions (one per line)",
                    value="\n".join(original_questions),
                    height=110,
                    key=f"edit_questions_{index}",
                )

                edited_answer = st.text_area(
                    "Answer",
                    value=faq.get("answer", ""),
                    height=130,
                    key=f"edit_answer_{index}",
                )

                edit_clicked = st.form_submit_button(
                    "💾 Save FAQ Changes",
                    type="primary",
                    use_container_width=True,
                )

            if edit_clicked:

                questions = [
                    q.strip()
                    for q in edited_questions.splitlines()
                    if q.strip()
                ]

                if not edited_category.strip():
                    st.error("Category cannot be empty.")
                elif not questions:
                    st.error("At least one question is required.")
                elif not edited_answer.strip():
                    st.error("Answer cannot be empty.")
                else:
                    faqs[index]["category"] = edited_category.strip()
                    update_faq_questions(faqs[index], questions)
                    faqs[index]["answer"] = edited_answer.strip()

                    if save_json(FAQ_FILE, faqs):
                        st.success("FAQ updated successfully.")
                        st.rerun()

            st.divider()
            st.markdown("### Delete FAQ")

            with st.form(f"delete_faq_{index}"):

                confirm_delete = st.checkbox(
                    "I understand that this FAQ will be permanently deleted.",
                    key=f"confirm_delete_{index}",
                )

                delete_clicked = st.form_submit_button(
                    "🗑️ Delete This FAQ",
                    use_container_width=True,
                )

            if delete_clicked:

                if not confirm_delete:
                    st.error("Confirm deletion before continuing.")
                else:
                    del faqs[index]

                    if save_json(FAQ_FILE, faqs):
                        st.success("FAQ deleted successfully.")
                        st.rerun()

# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="admin-footer">
    CAMPUSBOT BY TEAM96<br><br>
    J PRATHIV RAJ · SHASHANK SIDDHARTH · NATIONAL COLLEGE, BASAVANAGUDI
</div>
""", unsafe_allow_html=True)
