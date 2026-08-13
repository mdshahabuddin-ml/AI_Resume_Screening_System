import streamlit as st


def render_ats_score(ats_score: dict):
    overall = ats_score["overall_score"]
    breakdown = ats_score["breakdown"]

    color = "🟢" if overall >= 80 else "🟡" if overall >= 60 else "🔴"
    st.metric("ATS Score", f"{overall}/100 {color}")

    cols = st.columns(3)
    labels = [
        ("Keyword Match", "keyword_match"),
        ("Formatting", "formatting"),
        ("Skills", "skills"),
        ("Experience", "experience"),
        ("Education", "education"),
        ("Contact Info", "contact_information"),
    ]
    for i, (label, key) in enumerate(labels):
        with cols[i % 3]:
            st.progress(min(int(breakdown[key]), 100), text=f"{label}: {breakdown[key]}%")

    if ats_score.get("strengths"):
        st.markdown("**✅ Strengths**")
        for s in ats_score["strengths"]:
            st.markdown(f"- {s}")

    if ats_score.get("warnings"):
        st.markdown("**⚠️ Areas to improve**")
        for w in ats_score["warnings"]:
            st.markdown(f"- {w}")