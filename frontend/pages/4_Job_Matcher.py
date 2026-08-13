# ============================================================
# JOB MATCHER
# AI-Powered ATS Resume Screening System
# Streamlit Frontend + FastAPI Backend
# ============================================================

import os
import sys

import requests
import streamlit as st


# ============================================================
# PROJECT IMPORTS
# ============================================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from components.config import API_BASE_URL
from components.keyword_chart import render_keyword_match


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Job Matcher | AI ATS System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL PURPLE THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN APPLICATION
       ====================================================== */

    .stApp {
        background-color: #F5F3FF !important;
    }

    .main {
        background-color: #F5F3FF !important;
    }

    .block-container {
        max-width: 1400px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1 {
        color: #4C1D95 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }

    h2 {
        color: #5B21B6 !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #6D28D9 !important;
        font-weight: 700 !important;
    }


    /* ======================================================
       NORMAL TEXT
       ====================================================== */

    p {
        color: #475569 !important;
    }

    label {
        color: #334155 !important;
        font-weight: 600 !important;
    }


    /* ======================================================
       TEXT INPUTS
       ====================================================== */

    .stTextInput input,
    .stTextArea textarea {

        background-color: #FFFFFF !important;

        color: #1E293B !important;

        border: 1px solid #C4B5FD !important;

        border-radius: 10px !important;

        font-size: 16px !important;

    }


    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {

        color: #94A3B8 !important;

    }


    .stTextInput input:focus,
    .stTextArea textarea:focus {

        border-color: #7C3AED !important;

        box-shadow:
            0 0 0 1px #7C3AED !important;

    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {

        background-color: #7C3AED !important;

        color: #FFFFFF !important;

        border: none !important;

        border-radius: 9px !important;

        font-weight: 700 !important;

        padding: 0.6rem 1.4rem !important;

        transition: all 0.2s ease-in-out !important;

    }


    .stButton > button:hover {

        background-color: #6D28D9 !important;

        color: #FFFFFF !important;

        border: none !important;

        transform: translateY(-1px);

    }


    /* ======================================================
       CARDS
       ====================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {

        background-color: #FFFFFF !important;

        border: 1px solid #DDD6FE !important;

        border-radius: 14px !important;

        box-shadow:
            0 4px 14px rgba(109, 40, 217, 0.08) !important;

    }


    /* ======================================================
       METRICS
       ====================================================== */

    [data-testid="stMetric"] {

        background-color: #FFFFFF !important;

        border: 1px solid #DDD6FE !important;

        border-radius: 12px !important;

        padding: 18px !important;

        box-shadow:
            0 4px 12px rgba(109, 40, 217, 0.08) !important;

    }


    [data-testid="stMetricValue"] {

        color: #7C3AED !important;

        font-weight: 800 !important;

    }


    [data-testid="stMetricLabel"] {

        color: #64748B !important;

        font-weight: 600 !important;

    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {

        border-color: #DDD6FE !important;

    }


    /* ======================================================
       ALERTS
       ====================================================== */

    [data-testid="stAlert"] {

        border-radius: 10px !important;

    }


    /* ======================================================
       PROGRESS BAR
       ====================================================== */

    [data-testid="stProgressBar"] > div > div {

        background-color: #7C3AED !important;

    }


    /* ======================================================
       CODE / JSON BLOCK
       ====================================================== */

    code {

        color: #6D28D9 !important;

    }


    /* ======================================================
       EXPANDER
       ====================================================== */

    [data-testid="stExpander"] {

        border: 1px solid #DDD6FE !important;

        border-radius: 10px !important;

        background-color: #FFFFFF !important;

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FASTAPI ENDPOINT CONFIGURATION
# ============================================================

# Remove trailing slash if present
API_BASE_URL = API_BASE_URL.rstrip("/")


# Primary endpoint
MATCH_ENDPOINT = f"{API_BASE_URL}/jobs/match"

# Alternative endpoint
# This protects your application if your FastAPI router
# uses /api/jobs/match instead.
MATCH_ENDPOINT_API = f"{API_BASE_URL}/api/jobs/match"


# ============================================================
# HELPER FUNCTION
# ============================================================

def call_job_match_api(payload):
    """
    Send resume + job description to FastAPI.

    First tries:
        POST /jobs/match

    If that returns 404, tries:
        POST /api/jobs/match

    Returns:
        requests.Response
    """

    # --------------------------------------------------------
    # Try primary endpoint
    # --------------------------------------------------------

    response = requests.post(
        MATCH_ENDPOINT,
        json=payload,
        timeout=30,
    )

    # --------------------------------------------------------
    # If primary endpoint doesn't exist,
    # try /api/jobs/match
    # --------------------------------------------------------

    if response.status_code == 404:

        response = requests.post(
            MATCH_ENDPOINT_API,
            json=payload,
            timeout=30,
        )

    return response


# ============================================================
# PAGE HEADER
# ============================================================

st.title("💼 Job Matcher")

st.write(
    "Compare your resume with a job description "
    "and identify matching and missing skills."
)


# ============================================================
# BACKEND STATUS
# ============================================================

with st.expander("⚙️ Backend Configuration"):

    st.write(
        f"**FastAPI Base URL:** `{API_BASE_URL}`"
    )

    st.write(
        f"**Primary Match Endpoint:** "
        f"`{MATCH_ENDPOINT}`"
    )

    st.write(
        f"**Alternative Match Endpoint:** "
        f"`{MATCH_ENDPOINT_API}`"
    )


# ============================================================
# RESUME TEXT
# ============================================================

st.subheader("📄 Resume")

resume_text = st.text_area(
    "Paste your resume text",
    value=st.session_state.get(
        "resume_text",
        ""
    ),
    height=250,
    placeholder=(
        "Paste your complete resume text here..."
    ),
)


# ============================================================
# SAVE RESUME TO SESSION
# ============================================================

if resume_text.strip():

    st.session_state["resume_text"] = resume_text


# ============================================================
# SINGLE JOB MATCHING
# ============================================================

st.divider()

st.subheader("🔎 Compare Against One Job")

job_title = st.text_input(
    "Job Title",
    value="AI/ML Engineer",
)


job_description = st.text_area(
    "Job Description",
    height=220,
    placeholder=(
        "Paste the complete job description here..."
    ),
)


# ============================================================
# MATCH BUTTON
# ============================================================

if st.button(
    "🎯 Calculate Job Match",
    type="primary",
    use_container_width=False,
):

    # --------------------------------------------------------
    # Validate resume
    # --------------------------------------------------------

    if not resume_text.strip():

        st.warning(
            "⚠️ Please provide your resume text."
        )

    # --------------------------------------------------------
    # Validate job description
    # --------------------------------------------------------

    elif not job_description.strip():

        st.warning(
            "⚠️ Please provide a job description."
        )

    else:

        payload = {
            "resume_text": resume_text.strip(),

            "job_description":
                job_description.strip(),

            "job_title":
                job_title.strip()
                if job_title.strip()
                else "Target Role",
        }


        # ----------------------------------------------------
        # FastAPI request
        # ----------------------------------------------------

        try:

            with st.spinner(
                "🔄 Analyzing resume against job..."
            ):

                response = call_job_match_api(
                    payload
                )


            # =================================================
            # VALIDATION ERROR
            # =================================================

            if response.status_code == 422:

                st.error(
                    "❌ FastAPI validation error."
                )

                try:

                    st.json(
                        response.json()
                    )

                except Exception:

                    st.text(
                        response.text
                    )


            # =================================================
            # NOT FOUND
            # =================================================

            elif response.status_code == 404:

                st.error(
                    "❌ Job matching endpoint was not found."
                )

                st.info(
                    "Open FastAPI Swagger documentation at "
                    "http://127.0.0.1:8000/docs "
                    "and verify that the job matching "
                    "POST endpoint exists."
                )

                st.code(
                    """
Expected one of these endpoints:

POST /jobs/match

or

POST /api/jobs/match
"""
                )


            # =================================================
            # OTHER HTTP ERRORS
            # =================================================

            elif response.status_code != 200:

                st.error(
                    f"❌ FastAPI returned HTTP "
                    f"{response.status_code}"
                )

                try:

                    st.json(
                        response.json()
                    )

                except Exception:

                    st.text(
                        response.text
                    )


            # =================================================
            # SUCCESS
            # =================================================

            else:

                result = response.json()


                # ------------------------------------------------
                # Extract API values safely
                # ------------------------------------------------

                returned_job_title = result.get(
                    "job_title",
                    payload["job_title"]
                )


                match_percentage = result.get(
                    "match_percentage",
                    result.get(
                        "match_score",
                        result.get(
                            "score",
                            0
                        )
                    )
                )


                matched_keywords = result.get(
                    "matched_keywords",
                    []
                )


                missing_keywords = result.get(
                    "missing_keywords",
                    []
                )


                # ------------------------------------------------
                # Convert score safely
                # ------------------------------------------------

                try:

                    match_percentage = float(
                        match_percentage
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    match_percentage = 0.0


                # =================================================
                # SUCCESS MESSAGE
                # =================================================

                st.success(
                    "✅ Job matching completed successfully."
                )


                # =================================================
                # MATCH SCORE
                # =================================================

                st.subheader(
                    "📊 Job Match Score"
                )


                score_col1, score_col2 = st.columns(
                    [1, 2]
                )


                with score_col1:

                    st.metric(
                        "Match Percentage",
                        f"{match_percentage:.2f}%"
                    )


                with score_col2:

                    if match_percentage >= 80:

                        st.success(
                            "🟢 Excellent Match"
                        )

                    elif match_percentage >= 65:

                        st.info(
                            "🔵 Good Match"
                        )

                    elif match_percentage >= 50:

                        st.warning(
                            "🟡 Moderate Match"
                        )

                    else:

                        st.error(
                            "🔴 Low Match"
                        )


                # =================================================
                # KEYWORD ANALYSIS
                # =================================================

                st.divider()

                st.subheader(
                    "🔑 Keyword Analysis"
                )


                keyword_col1, keyword_col2 = st.columns(
                    2
                )


                # ------------------------------------------------
                # MATCHED
                # ------------------------------------------------

                with keyword_col1:

                    st.markdown(
                        "### ✅ Matched Keywords"
                    )


                    if matched_keywords:

                        for keyword in matched_keywords:

                            st.markdown(
                                f"- **{keyword}**"
                            )

                    else:

                        st.info(
                            "No matching keywords found."
                        )


                # ------------------------------------------------
                # MISSING
                # ------------------------------------------------

                with keyword_col2:

                    st.markdown(
                        "### ❌ Missing Keywords"
                    )


                    if missing_keywords:

                        for keyword in missing_keywords:

                            st.markdown(
                                f"- **{keyword}**"
                            )

                    else:

                        st.success(
                            "🎉 No major missing keywords found."
                        )


                # =================================================
                # KEYWORD CHART
                # =================================================

                if (
                    matched_keywords
                    or missing_keywords
                ):

                    st.divider()

                    st.subheader(
                        "📈 Keyword Match Visualization"
                    )


                    try:

                        render_keyword_match(
                            matched_keywords,
                            missing_keywords
                        )

                    except Exception as chart_error:

                        st.warning(
                            "Keyword chart could not "
                            f"be rendered: {chart_error}"
                        )


                # =================================================
                # API RESPONSE
                # =================================================

                with st.expander(
                    "🔍 View FastAPI Response"
                ):

                    st.json(
                        result
                    )


        # ========================================================
        # CONNECTION ERROR
        # ========================================================

        except requests.exceptions.ConnectionError as error:

            st.error(
                "❌ Cannot connect to FastAPI backend."
            )

            st.code(
                f"""
Backend URL:
{API_BASE_URL}

Error:
{error}
"""
            )

            st.info(
                """
Start your FastAPI backend in another terminal:

python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
"""
            )


        # ========================================================
        # TIMEOUT ERROR
        # ========================================================

        except requests.exceptions.Timeout:

            st.error(
                "❌ FastAPI request timed out."
            )

            st.info(
                "Please check whether the backend "
                "is processing the request correctly."
            )


        # ========================================================
        # REQUEST ERROR
        # ========================================================

        except requests.exceptions.RequestException as error:

            st.error(
                f"❌ Job matching request failed: {error}"
            )


        # ========================================================
        # UNEXPECTED ERROR
        # ========================================================

        except Exception as error:

            st.error(
                f"❌ Unexpected error: {error}"
            )


# ============================================================
# MULTIPLE JOB RANKING
# ============================================================

st.divider()

st.subheader(
    "🏆 Rank Against Multiple Jobs"
)

st.caption(
    "Paste one job per block and separate jobs "
    "using a line containing only ---"
)


multi_jobs_raw = st.text_area(
    "Jobs",
    height=280,
    placeholder=(
        "AI/ML Engineer\n"
        "We are looking for an AI/ML Engineer "
        "with Python, Machine Learning and FastAPI.\n"
        "---\n"
        "Python Developer\n"
        "We need a Python developer with "
        "FastAPI, SQL and Docker.\n"
        "---\n"
        "Data Scientist\n"
        "Looking for a Data Scientist with "
        "Pandas, NumPy and Machine Learning."
    ),
)


# ============================================================
# RANK JOBS BUTTON
# ============================================================

if st.button(
    "🏆 Rank Jobs",
    type="primary",
):

    # --------------------------------------------------------
    # Validate resume
    # --------------------------------------------------------

    if not resume_text.strip():

        st.warning(
            "⚠️ Please provide your resume text."
        )

        st.stop()


    # --------------------------------------------------------
    # Validate jobs
    # --------------------------------------------------------

    if not multi_jobs_raw.strip():

        st.warning(
            "⚠️ Please provide at least one job."
        )

        st.stop()


    # ========================================================
    # PARSE JOB BLOCKS
    # ========================================================

    blocks = [
        block.strip()
        for block in multi_jobs_raw.split("---")
        if block.strip()
    ]


    jobs = []


    for block in blocks:

        lines = block.split(
            "\n",
            1
        )


        title = lines[0].strip()


        description = (
            lines[1].strip()
            if len(lines) > 1
            else ""
        )


        if title and description:

            jobs.append(
                {
                    "title": title,
                    "description": description,
                }
            )


    # ========================================================
    # INVALID FORMAT
    # ========================================================

    if not jobs:

        st.warning(
            "⚠️ Invalid job format."
        )


        st.info(
            """
Use this format:

AI/ML Engineer
We are looking for an AI/ML Engineer with Python...
---
Python Developer
We need a Python developer with FastAPI...
---
Data Scientist
Looking for a Data Scientist with Pandas...
"""
        )

        st.stop()


    # ========================================================
    # START RANKING
    # ========================================================

    ranked_jobs = []


    progress = st.progress(
        0
    )


    total_jobs = len(
        jobs
    )


    # ========================================================
    # PROCESS EACH JOB
    # ========================================================

    for index, job in enumerate(jobs):


        payload = {

            "resume_text":
                resume_text.strip(),

            "job_description":
                job["description"].strip(),

            "job_title":
                job["title"].strip(),
        }


        try:

            response = call_job_match_api(
                payload
            )


            # ------------------------------------------------
            # Validation error
            # ------------------------------------------------

            if response.status_code == 422:

                st.error(
                    f"❌ Validation error for "
                    f"{job['title']}"
                )

                try:

                    st.json(
                        response.json()
                    )

                except Exception:

                    st.text(
                        response.text
                    )

                continue


            # ------------------------------------------------
            # Endpoint not found
            # ------------------------------------------------

            if response.status_code == 404:

                st.error(
                    "❌ FastAPI job matching endpoint "
                    "was not found."
                )

                st.info(
                    "Check http://127.0.0.1:8000/docs"
                )

                break


            # ------------------------------------------------
            # Other errors
            # ------------------------------------------------

            response.raise_for_status()


            # ------------------------------------------------
            # JSON response
            # ------------------------------------------------

            result = response.json()


            # ------------------------------------------------
            # Get score
            # ------------------------------------------------

            match_percentage = result.get(
                "match_percentage",
                result.get(
                    "match_score",
                    result.get(
                        "score",
                        0
                    )
                )
            )


            try:

                match_percentage = float(
                    match_percentage
                )

            except (
                ValueError,
                TypeError
            ):

                match_percentage = 0.0


            # ------------------------------------------------
            # Store result
            # ------------------------------------------------

            ranked_jobs.append(
                {
                    "job_title":
                        result.get(
                            "job_title",
                            job["title"]
                        ),

                    "match_percentage":
                        match_percentage,

                    "matched_keywords":
                        result.get(
                            "matched_keywords",
                            []
                        ),

                    "missing_keywords":
                        result.get(
                            "missing_keywords",
                            []
                        ),
                }
            )


        except requests.exceptions.RequestException as error:

            st.error(
                f"❌ Failed to analyze "
                f"{job['title']}: {error}"
            )


        # ----------------------------------------------------
        # Update progress
        # ----------------------------------------------------

        progress.progress(
            (index + 1) / total_jobs
        )


    progress.empty()


    # ========================================================
    # SORT JOBS BY SCORE
    # ========================================================

    ranked_jobs.sort(
        key=lambda item:
            item["match_percentage"],
        reverse=True
    )


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    if ranked_jobs:

        st.success(
            f"✅ Successfully ranked "
            f"{len(ranked_jobs)} job(s)."
        )


        st.subheader(
            "🏆 Recommended Jobs"
        )


        medals = [
            "🥇",
            "🥈",
            "🥉",
        ]


        for index, job in enumerate(
            ranked_jobs
        ):

            medal = (
                medals[index]
                if index < 3
                else "▪️"
            )


            st.markdown(
                f"## {medal} "
                f"{job['job_title']}"
            )


            score = job[
                "match_percentage"
            ]


            # ------------------------------------------------
            # Score display
            # ------------------------------------------------

            score_col1, score_col2 = st.columns(
                2
            )


            with score_col1:

                st.metric(
                    "Match Percentage",
                    f"{score:.2f}%"
                )


            with score_col2:

                if score >= 80:

                    st.success(
                        "🟢 Excellent Match"
                    )

                elif score >= 65:

                    st.info(
                        "🔵 Good Match"
                    )

                elif score >= 50:

                    st.warning(
                        "🟡 Moderate Match"
                    )

                else:

                    st.error(
                        "🔴 Low Match"
                    )


            # ------------------------------------------------
            # Keywords
            # ------------------------------------------------

            col1, col2 = st.columns(
                2
            )


            with col1:

                st.markdown(
                    "### ✅ Matched Keywords"
                )


                if job[
                    "matched_keywords"
                ]:

                    for keyword in job[
                        "matched_keywords"
                    ]:

                        st.markdown(
                            f"- **{keyword}**"
                        )

                else:

                    st.write(
                        "No matched keywords."
                    )


            with col2:

                st.markdown(
                    "### ❌ Missing Keywords"
                )


                if job[
                    "missing_keywords"
                ]:

                    for keyword in job[
                        "missing_keywords"
                    ]:

                        st.markdown(
                            f"- **{keyword}**"
                        )

                else:

                    st.success(
                        "No major missing keywords."
                    )


            st.divider()


    else:

        st.error(
            "❌ Could not calculate matches "
            "for any of the provided jobs."
        )