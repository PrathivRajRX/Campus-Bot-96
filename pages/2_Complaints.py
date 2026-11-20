
import re
import uuid
from datetime import datetime

import streamlit as st

from styles.theme import apply_theme, brand_header, hero, footer
from shared_db import create_complaint, get_complaint


st.set_page_config(
    page_title="CampusBot | Complaints",
    page_icon="🎓",
    layout="wide"
)

apply_theme()

brand_header()

hero(
    "Student Grievance Portal",
    "Raise a concern and track its progress. "
    "Choose anonymous or identified submission."
)

if "new_complaint_id" not in st.session_state:
    st.session_state.new_complaint_id = None

if "tracked_complaint" not in st.session_state:
    st.session_state.tracked_complaint = None

if "tracking_attempted" not in st.session_state:
    st.session_state.tracking_attempted = False

submit_tab, track_tab = st.tabs([
    "📝 Submit Complaint",
    "🔍 Track Complaint"
])

with submit_tab:

    st.markdown("## Register a Complaint")

    complaint_type = st.radio(
        "How would you like to submit?",
        [
            "Anonymous Complaint",
            "Identified Complaint"
        ],
        horizontal=True,
        help=(
            "Anonymous complaints do not ask for your "
            "name, email or phone number."
        )
    )

    is_identified = complaint_type == "Identified Complaint"

    with st.form("complaint_form", clear_on_submit=True):

        if is_identified:

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

        else:

            name = ""
            email = ""
            phone = ""

            st.info(
                "🔒 Anonymous mode: this form does not ask "
                "for your name, email address or phone number. "
                "Avoid including identifying details in your "
                "description."
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

            if not subject or not description:

                st.error(
                    "Please complete the complaint subject "
                    "and description."
                )

            elif is_identified and not all([name, email, phone]):

                st.error(
                    "Please complete all student information fields."
                )

            elif is_identified and not re.fullmatch(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                email
            ):

                st.error("Please enter a valid email address.")

            elif is_identified and not re.fullmatch(
                r"[6-9][0-9]{9}",
                phone
            ):

                st.error(
                    "Please enter a valid 10-digit Indian mobile number."
                )

            elif not agree:

                st.warning("Please confirm your information.")

            else:

                complaint_id = "NCB-" + uuid.uuid4().hex[:8].upper()

                complaint = {
                    "id": complaint_id,
                    "complaint_type": (
                        "Identified" if is_identified else "Anonymous"
                    ),
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "category": category,
                    "subject": subject,
                    "description": description,
                    "status": "Submitted",
                    "assigned_department": "Not Assigned",
                    "admin_remarks": "",
                    "submitted_at": datetime.now().astimezone().isoformat(
                        timespec="seconds"
                    ),
                    "activity_history": [
                        {
                            "timestamp": datetime.now().astimezone().isoformat(
                                timespec="seconds"
                            ),
                            "actor": "Student",
                            "action": "Complaint Submitted",
                            "details": "Complaint registered successfully."
                        }
                    ]
                }

                try:
                    create_complaint(complaint)

                    st.session_state.new_complaint_id = complaint_id

                    st.success(
                        "Your complaint has been registered successfully!"
                    )

                except Exception:
                    st.error(
                        "Unable to save your complaint. "
                        "Please try again later."
                    )

    if st.session_state.new_complaint_id:

        st.divider()

        st.success("Your complaint has been registered successfully!")

        st.markdown("### 🎉 Complaint Registered")

        st.write("Your unique complaint tracking ID:")

        st.code(
            st.session_state.new_complaint_id,
            language=None
        )

        st.info(
            "Please save this ID. You will need it to "
            "track your complaint."
        )

        if st.button("Dismiss tracking ID"):
            st.session_state.new_complaint_id = None
            st.rerun()


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

            try:
                result = get_complaint(
                    tracking_id.strip().upper()
                )

                st.session_state.tracked_complaint = result
                st.session_state.tracking_attempted = True

            except Exception:
                st.error(
                    "The tracking service is temporarily unavailable. "
                    "Please try again later."
                )

    result = st.session_state.tracked_complaint

    if result:

        st.divider()

        st.success("Complaint record found.")

        st.markdown("### Complaint Overview")

        st.code(result.get("id", "N/A"), language=None)

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("**Complaint Type**")
            st.write(result.get("complaint_type", "N/A"))

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

        st.markdown("### 📍 Complaint Progress")

        if status == "Rejected":

            st.error(
                "This complaint has been rejected "
                "by the administration."
            )

        else:

            stages = [
                "Submitted",
                "Under Review",
                "Resolved"
            ]

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

        st.markdown("### 🏢 Department Information")

        department = result.get(
            "assigned_department",
            "Not yet assigned"
        )

        st.info(f"Assigned Department: {department}")

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

    elif st.session_state.tracking_attempted:
        st.error(
            "Complaint not found. Please verify your reference ID."
        )


st.info(
    "Privacy note: Anonymous submissions do not request "
    "contact details. Do not include your identity in the "
    "complaint text if you wish to remain anonymous. "
    "The hosting platform may still retain technical logs."
)

footer()
