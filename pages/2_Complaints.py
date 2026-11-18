
import streamlit as st
import json
import uuid
import re

from pathlib import Path
from datetime import datetime

from styles.theme import apply_theme, brand_header, hero, footer


# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CampusBot | Complaints",
    page_icon="🎓",
    layout="wide"
)

apply_theme()

BASE_DIR = Path(__file__).resolve().parent.parent
FILE = BASE_DIR / "complaints.json"


# ==========================================
# DATABASE
# ==========================================

def load_complaints():

    if not FILE.exists():
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        st.error("Unable to load complaint records.")
        return []


def save_complaints(data):

    temp_file = FILE.with_suffix(".json.tmp")

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    temp_file.replace(FILE)


# ==========================================
# BRANDING
# ==========================================

brand_header()

hero(
    "Student Grievance Portal",
    "A dedicated platform to raise concerns and track their resolution."
)

st.markdown("")


# ==========================================
# SESSION STATE
# ==========================================

if "last_complaint_id" not in st.session_state:
    st.session_state.last_complaint_id = None

if "tracked_complaint" not in st.session_state:
    st.session_state.tracked_complaint = None


# ==========================================
# PORTAL NAVIGATION
# ==========================================

submit_tab, track_tab = st.tabs([
    "📝  Submit Complaint",
    "🔍  Track Complaint"
])


# ==========================================
# SUBMIT COMPLAINT
# ==========================================

with submit_tab:

    st.markdown("## Register a Complaint")

    st.caption(
        "Provide your details and describe the issue "
        "so the college administration can assist you."
    )

    with st.form("complaint_form", clear_on_submit=False):

        st.markdown("### 👤 Student Information")

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Full Name *",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email Address *",
                placeholder="example@gmail.com"
            )

        with col2:

            phone = st.text_input(
                "Phone Number *",
                placeholder="10-digit mobile number",
                max_chars=10
            )

        st.divider()

        st.markdown("### 📋 Complaint Information")

        category = st.selectbox(
            "Complaint Category *",
            [
                "Academic Issues",
                "Faculty-related Complaint",
                "Infrastructure and Facilities",
                "Fees and Accounts",
                "Library and Laboratories",
                "Harassment and Ragging",
                "Transport and Parking",
                "Hostel and Canteen",
                "Student Services",
                "Examination Issues",
                "Other"
            ]
        )

        subject = st.text_input(
            "Complaint Subject *",
            placeholder="Briefly describe your issue",
            max_chars=120
        )

        description = st.text_area(
            "Complaint Description *",
            placeholder="Explain your complaint in detail...",
            height=180,
            max_chars=3000
        )

        st.markdown("")

        agree = st.checkbox(
            "I confirm that the information provided is accurate."
        )

        submitted = st.form_submit_button(
            "📩 Submit Complaint",
            use_container_width=True
        )

        if submitted:

            name = name.strip()
            email = email.strip()
            phone = phone.strip()
            subject = subject.strip()
            description = description.strip()

            if not all([
                name, email, phone, subject, description
            ]):

                st.error("Please complete all required fields.")

            elif not re.fullmatch(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                email
            ):

                st.error("Please enter a valid email address.")

            elif not re.fullmatch(r"[6-9][0-9]{9}", phone):

                st.error(
                    "Please enter a valid 10-digit Indian mobile number."
                )

            elif not agree:

                st.warning("Please confirm your information.")

            else:

                complaints = load_complaints()

                complaint_id = (
                    "NCB-" + uuid.uuid4().hex[:8].upper()
                )

                complaint = {

                    "id": complaint_id,

                    "name": name,
                    "email": email,
                    "phone": phone,

                    "category": category,
                    "subject": subject,
                    "description": description,

                    "status": "Submitted",

                    "admin_remarks": "",

                    "submitted_at": datetime.now().astimezone().isoformat(
                        timespec="seconds"
                    )
                }

                complaints.append(complaint)

                try:

                    save_complaints(complaints)

                    st.session_state.last_complaint_id = complaint_id

                    st.success(
                        "Your complaint has been registered successfully!"
                    )

                except OSError:

                    st.error(
                        "Unable to save your complaint. Please try again."
                    )


    # ======================================
    # SUCCESS CARD
    # ======================================

    if st.session_state.last_complaint_id:

        st.divider()

        st.markdown("### 🎉 Complaint Registered")

        st.success("Your complaint has been successfully submitted.")

        st.write("Your unique complaint tracking ID:")

        st.code(
            st.session_state.last_complaint_id,
            language=None
        )

        st.info(
            "Please save this ID. You will need it to track your complaint."
        )

        if st.button("Copy Complaint ID"):

            st.code(st.session_state.last_complaint_id)


# ==========================================
# TRACK COMPLAINT
# ==========================================

with track_tab:

    st.markdown("## Track Your Complaint")

    st.caption(
        "Enter your complaint reference number "
        "to view its latest status."
    )

    with st.form("track_form"):

        tracking_id = st.text_input(
            "Complaint Reference ID",
            placeholder="NCB-XXXXXXXX"
        )

        track_button = st.form_submit_button(
            "🔍 Track Complaint",
            use_container_width=True
        )

        if track_button:

            if not tracking_id.strip():

                st.warning("Please enter your complaint ID.")

            else:

                complaints = load_complaints()

                result = next(
                    (
                        c for c in complaints
                        if c.get("id", "").lower()
                        == tracking_id.strip().lower()
                    ),
                    None
                )

                st.session_state.tracked_complaint = result

    # ======================================
    # DISPLAY TRACKING RESULT
    # ======================================

    result = st.session_state.tracked_complaint

    if result:

        st.divider()

        st.success("Complaint record found.")

        st.markdown("### Complaint Overview")

        st.code(result.get("id", "N/A"))

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("**Complaint Category**")
            st.write(result.get("category", "N/A"))

            st.markdown("**Complaint Subject**")
            st.write(result.get("subject", "N/A"))

        with col2:

            st.markdown("**Submission Date**")
            st.write(result.get("submitted_at", "N/A"))

            st.markdown("**Current Status**")

            status = result.get("status", "Submitted")

            if status == "Resolved":

                st.success("✓ Resolved")

            elif status == "Rejected":

                st.error("Rejected")

            elif status == "Under Review":

                st.warning("Under Review")

            else:

                st.info("Submitted")

        # ==================================
        # STATUS TIMELINE
        # ==================================

        st.markdown("### 📍 Complaint Progress")

        stages = [
            "Submitted",
            "Under Review",
            "Resolved"
        ]

        if status == "Rejected":

            st.error(
                "This complaint has been rejected by the administration."
            )

        else:

            current_stage = (
                stages.index(status)
                if status in stages
                else 0
            )

            for index, stage in enumerate(stages):

                if index < current_stage:

                    st.success(f"✓ {stage}")

                elif index == current_stage:

                    st.info(f"● {stage} — Current Status")

                else:

                    st.caption(f"○ {stage} — Pending")

        st.divider()

        # ==================================
        # DEPARTMENT
        # ==================================

        st.markdown("### 🏢 Department Information")

        department = result.get(
            "assigned_department",
            "Not yet assigned"
        )

        st.info(f"Assigned Department: {department}")

        # ==================================
        # ADMIN REMARKS
        # ==================================

        st.markdown("### 💬 Administration Remarks")

        remarks = result.get("admin_remarks", "")

        if remarks:

            st.write(remarks)

        else:

            st.caption(
                "No administrative remarks have been added yet."
            )

        st.divider()

        st.caption(
            "For urgent matters, contact the college administration directly."
        )

    elif result is None and st.session_state.tracked_complaint is not None:

        st.error("Complaint not found. Please verify your reference ID.")


# ==========================================
# FOOTER
# ==========================================

footer()
