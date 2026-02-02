import streamlit as st
import requests

st.title("AI Resume Screening System")

uploaded_file = st.file_uploader("Upload Resume (PDF)")

if uploaded_file:
    response = requests.post(
        "http://127.0.0.1:8000/resume/upload",
        files={"file": uploaded_file}
    )

    data = response.json()

    st.metric("Matching Score", f"{data['score']}%")
    st.progress(data["score"] / 100)

    st.subheader("Application Status")
    if data["status"] == "STRONGLY MATCHED":
        st.success(data["status"])
    elif data["status"] == "GOOD MATCH":
        st.info(data["status"])
    elif data["status"] == "PARTIAL MATCH":
        st.warning(data["status"])
    else:
        st.error(data["status"])

    st.subheader("Matched Skills")
    st.success(", ".join(data["matched_skills"]))

    st.subheader("Missing Skills")
    st.warning(", ".join(data["missing_skills"]))


