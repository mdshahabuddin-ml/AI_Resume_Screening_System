import streamlit as st

st.set_page_config(page_title="Resume History", page_icon="🔄", layout="wide")
st.title("🔄 My Resumes")

st.info(
    "This page is a placeholder for resume version history. To make it persistent, "
    "connect it to a database (e.g. SQLite/Postgres) and save each generated resume "
    "with its ATS score and timestamp — the `resume_payload` built in the Resume "
    "Builder page is already available in `st.session_state` to save."
)

if "resume_payload" in st.session_state:
    st.subheader("Current session resume")
    st.json(st.session_state["resume_payload"])
else:
    st.caption("No resume built yet in this session. Go to Resume Builder to create one.")