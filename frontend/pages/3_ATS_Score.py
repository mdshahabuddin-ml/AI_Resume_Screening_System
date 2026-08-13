import streamlit as st
import requests
import os
import sys


# =========================================================
# PATH
# =========================================================

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

from components.config import API_BASE_URL


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="ATS Score",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 ATS Score")

st.write(
    "Upload a resume and paste a target job description "
    "to get an explainable ATS compatibility score."
)


# =========================================================
# RESUME UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"],
    key="ats_upload"
)


# =========================================================
# JOB DESCRIPTION
# =========================================================

job_description = st.text_area(
    "Job Description",
    height=250,
    placeholder="Paste the complete job description here..."
)


# =========================================================
# CALCULATE
# =========================================================

if st.button(
    "Calculate ATS Score",
    type="primary"
):

    if not uploaded_file:

        st.warning(
            "⚠️ Please upload a resume first."
        )

        st.stop()


    if not job_description.strip():

        st.warning(
            "⚠️ Please enter the target job description."
        )

        st.stop()


    try:

        # -------------------------------------------------
        # Step 1: Upload resume to FastAPI
        # -------------------------------------------------

        files = {

            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )

        }


        upload_response = requests.post(
            f"{API_BASE_URL}/resume/upload",
            files=files,
            timeout=30
        )


        upload_response.raise_for_status()


        upload_result = upload_response.json()


        resume_text = upload_result.get(
            "text",
            ""
        )


        if not resume_text.strip():

            st.error(
                "❌ Could not extract text from the resume."
            )

            st.stop()


        # -------------------------------------------------
        # Step 2: Send extracted text to ATS engine
        # -------------------------------------------------

        payload = {

            "resume_text": resume_text,

            "job_description": job_description

        }


        response = requests.post(

            f"{API_BASE_URL}/api/ats/score",

            json=payload,

            timeout=30

        )


        # -------------------------------------------------
        # Validation error
        # -------------------------------------------------

        if response.status_code == 422:

            st.error(
                "❌ FastAPI validation error."
            )

            st.json(
                response.json()
            )

            st.stop()


        response.raise_for_status()


        result = response.json()


        # =================================================
        # SCORE
        # =================================================

        score = result.get(
            "overall_score",
            result.get(
                "ats_score",
                0
            )
        )


        st.success(
            "✅ ATS analysis completed successfully."
        )


        st.divider()


        # =================================================
        # MAIN SCORE
        # =================================================

        st.subheader("🎯 Overall ATS Score")


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "ATS Score",
                f"{score:.1f}/100"
            )


        with col2:

            keyword_score = result.get(
                "keyword_match_score",
                0
            )

            st.metric(
                "Keyword Match",
                f"{keyword_score:.1f}%"
            )


        with col3:

            matched = result.get(
                "matched_keywords",
                []
            )

            st.metric(
                "Matched Keywords",
                len(matched)
            )


        # =================================================
        # SCORE INTERPRETATION
        # =================================================

        if score >= 85:

            st.success(
                "🟢 Excellent ATS compatibility"
            )

        elif score >= 70:

            st.success(
                "🟢 Good ATS compatibility"
            )

        elif score >= 55:

            st.warning(
                "🟡 Moderate ATS compatibility"
            )

        else:

            st.error(
                "🔴 Low ATS compatibility"
            )


        # =================================================
        # BREAKDOWN
        # =================================================

        st.subheader(
            "📊 ATS Score Breakdown"
        )


        breakdown = result.get(
            "breakdown",
            {}
        )


        if breakdown:

            for name, value in breakdown.items():

                label = name.replace(
                    "_",
                    " "
                ).title()


                st.write(
                    f"**{label}: {value:.1f}%**"
                )


                st.progress(
                    min(
                        max(
                            int(value),
                            0
                        ),
                        100
                    )
                )

        else:

            st.info(
                "No score breakdown was returned by the backend."
            )


        # =================================================
        # SECTIONS
        # =================================================

        st.subheader(
            "📑 Resume Sections"
        )


        sections = result.get(
            "sections",
            {}
        )


        section_cols = st.columns(4)


        for index, (section, exists) in enumerate(
            sections.items()
        ):

            with section_cols[index % 4]:

                if exists:

                    st.success(
                        f"✅ {section.title()}"
                    )

                else:

                    st.error(
                        f"❌ {section.title()}"
                    )


        # =================================================
        # CONTACT INFORMATION
        # =================================================

        st.subheader(
            "📞 Contact Information"
        )


        contact = result.get(
            "contact",
            {}
        )


        contact_cols = st.columns(4)


        for index, (name, exists) in enumerate(
            contact.items()
        ):

            with contact_cols[index]:

                if exists:

                    st.success(
                        f"✅ {name.title()}"
                    )

                else:

                    st.warning(
                        f"⚠️ {name.title()} missing"
                    )


        # =================================================
        # MATCHED KEYWORDS
        # =================================================

        st.subheader(
            "✅ Matched Keywords"
        )


        matched_keywords = result.get(
            "matched_keywords",
            []
        )


        if matched_keywords:

            st.write(
                ", ".join(
                    matched_keywords
                )
            )

        else:

            st.info(
                "No matching keywords found."
            )


        # =================================================
        # MISSING KEYWORDS
        # =================================================

        st.subheader(
            "❌ Missing Keywords"
        )


        missing_keywords = result.get(
            "missing_keywords",
            []
        )


        if missing_keywords:

            st.write(
                ", ".join(
                    missing_keywords
                )
            )

        else:

            st.success(
                "Excellent! No major missing keywords detected."
            )


        # =================================================
        # RECOMMENDATIONS
        # =================================================

        st.subheader(
            "💡 ATS Recommendations"
        )


        recommendations = result.get(
            "recommendations",
            []
        )


        if recommendations:

            for recommendation in recommendations:

                st.markdown(
                    f"- {recommendation}"
                )

        else:

            st.success(
                "No major recommendations."
            )


    # =====================================================
    # CONNECTION ERROR
    # =====================================================

    except requests.exceptions.ConnectionError:

        st.error(
            f"❌ Cannot connect to FastAPI at "
            f"{API_BASE_URL}:8000."
        )


    # =====================================================
    # TIMEOUT
    # =====================================================

    except requests.exceptions.Timeout:

        st.error(
            "⏱️ FastAPI request timed out."
        )


    # =====================================================
    # HTTP ERROR
    # =====================================================

    except requests.exceptions.HTTPError as e:

        st.error(
            f"❌ Backend returned an HTTP error: {e}"
        )

        try:

            st.json(
                response.json()
            )

        except Exception:

            st.text(
                response.text
            )


    # =====================================================
    # OTHER ERROR
    # =====================================================

    except Exception as e:

        st.error(
            f"❌ Unexpected error: {type(e).__name__}: {e}"
        )