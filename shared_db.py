
import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase():
    config = st.secrets["supabase"]

    url = config["url"]
    key = config["service_role_key"]

    return create_client(url, key)


def create_complaint(complaint):
    payload = dict(complaint)

    payload.setdefault("activity_history", [])
    payload.setdefault("assigned_department", "Not Assigned")
    payload.setdefault("admin_remarks", "")

    get_supabase().table("complaints").insert(payload).execute()


def get_complaint(complaint_id):
    response = (
        get_supabase()
        .table("complaints")
        .select(
            "id, complaint_type, category, subject, status, "
            "submitted_at, assigned_department, admin_remarks"
        )
        .eq("id", complaint_id)
        .limit(1)
        .execute()
    )

    return response.data[0] if response.data else None


def list_complaints():
    response = (
        get_supabase()
        .table("complaints")
        .select("*")
        .order("submitted_at", desc=True)
        .execute()
    )

    return response.data or []


def update_complaint(complaint_id, changes):
    (
        get_supabase()
        .table("complaints")
        .update(changes)
        .eq("id", complaint_id)
        .execute()
    )


def migrate_complaints(complaints):
    if not complaints:
        return 0

    records = []

    for complaint in complaints:
        record = dict(complaint)

        has_details = any(
            str(record.get(field, "")).strip()
            for field in ("name", "email", "phone")
        )

        record.setdefault(
            "complaint_type",
            "Identified" if has_details else "Anonymous"
        )

        record.setdefault("name", "")
        record.setdefault("email", "")
        record.setdefault("phone", "")
        record.setdefault("assigned_department", "Not Assigned")
        record.setdefault("admin_remarks", "")
        record.setdefault("activity_history", [])

        records.append(record)

    get_supabase().table("complaints").upsert(
        records,
        on_conflict="id"
    ).execute()

    return len(records)
