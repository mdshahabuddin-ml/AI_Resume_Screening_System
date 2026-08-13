import streamlit as st


def render_keyword_match(matched: list, missing: list):
    total = len(matched) + len(missing)
    pct = round(len(matched) / total * 100, 1) if total else 0

    st.metric("Keyword Match", f"{pct}%")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ Matched**")
        if matched:
            for k in matched:
                st.markdown(f"- {k}")
        else:
            st.caption("No matches found.")
    with col2:
        st.markdown("**❌ Missing**")
        if missing:
            for k in missing:
                st.markdown(f"- {k}")
        else:
            st.caption("Nothing missing — great coverage!")