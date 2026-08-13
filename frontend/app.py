import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI ATS Resume System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL LIGHT-BLUE + GOLD THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       REMOVE STREAMLIT TOP HEADER / BLACK BAR
       ======================================================== */

    [data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }


    /* ========================================================
       MAIN APPLICATION BACKGROUND
       ======================================================== */

    .stApp {
        background-color: #EEF6FF !important;
    }

    .main {
        background-color: #EEF6FF !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }


    /* ========================================================
       DEEP GOLD / YELLOW SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background-color: #B8860B !important;
        border-right: 1px solid #8B6508 !important;
    }

    /* Sidebar all text */
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Sidebar headings */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Sidebar navigation */
    [data-testid="stSidebarNav"] {
        background-color: #B8860B !important;
    }

    /* Sidebar navigation links */
    [data-testid="stSidebarNav"] a {
        color: #FFFFFF !important;
        border-radius: 8px !important;
        margin: 3px 8px !important;
    }

    /* Sidebar hover */
    [data-testid="stSidebarNav"] a:hover {
        background-color: #9C7209 !important;
        color: #FFFFFF !important;
    }

    /* Selected sidebar page */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #8B6508 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: #D4AF37 !important;
    }


    /* ========================================================
       MAIN HEADINGS
       ======================================================== */

    h1 {
        color: #173B6C !important;
        font-weight: 750 !important;
    }

    h2 {
        color: #1E40AF !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #334155 !important;
        font-weight: 650 !important;
    }


    /* ========================================================
       NORMAL TEXT
       ======================================================== */

    p {
        color: #475569 !important;
    }

    li {
        color: #475569 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 650 !important;
        padding: 0.55rem 1.2rem !important;
    }

    .stButton > button:hover {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }


    /* ========================================================
       TEXT INPUTS
       ======================================================== */

    .stTextInput input,
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #BFDBFE !important;
        border-radius: 8px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 1px #2563EB !important;
    }


    /* ========================================================
       SELECT BOX
       ======================================================== */

    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #BFDBFE !important;
        border-radius: 8px !important;
    }


    /* ========================================================
       CONTAINERS / CARDS
       ======================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D7E7F7 !important;
        border-radius: 12px !important;
        box-shadow: 0 3px 12px rgba(37, 99, 235, 0.07) !important;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D7E7F7 !important;
        border-radius: 10px !important;
        padding: 18px !important;
        box-shadow: 0 3px 10px rgba(37, 99, 235, 0.06) !important;
    }

    [data-testid="stMetricValue"] {
        color: #2563EB !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 8px !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #BFDBFE !important;
    }


    /* ========================================================
       CODE BOXES
       ======================================================== */

    /* Only used when we intentionally call st.code().
       Prevents the homepage from looking like a code editor. */

    [data-testid="stCode"] {
        border-radius: 8px !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MAIN TITLE
# ============================================================

st.title("📄 AI-Powered ATS Resume Builder & Screening System")

st.write(
    "Build, analyze, score, match, and optimize resumes "
    "using Artificial Intelligence, Machine Learning, "
    "Natural Language Processing, and FastAPI."
)

st.divider()


# ============================================================
# PLATFORM INTRODUCTION
# ============================================================

st.header("🚀 Resume Intelligence Platform")

st.write(
    "Use the modules below to create ATS-friendly resumes, "
    "evaluate resumes against job descriptions, identify "
    "missing skills, and discover suitable job opportunities."
)


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# LEFT COLUMN
# ------------------------------------------------------------

with col1:

    with st.container(border=True):
        st.subheader("📝 Resume Builder")
        st.write(
            "Create a professional ATS-friendly resume from "
            "structured information including education, skills, "
            "projects, experience, certifications, and achievements."
        )

    with st.container(border=True):
        st.subheader("🔍 Resume Analyzer")
        st.write(
            "Upload an existing PDF, DOCX, or TXT resume and "
            "analyze its structure, sections, skills, and content."
        )

    with st.container(border=True):
        st.subheader("🎯 ATS Score")
        st.write(
            "Calculate resume compatibility using keyword matching, "
            "section completeness, contact information, readability, "
            "skills, and action-verb analysis."
        )


# ------------------------------------------------------------
# RIGHT COLUMN
# ------------------------------------------------------------

with col2:

    with st.container(border=True):
        st.subheader("💼 Job Matcher")
        st.write(
            "Compare your resume with one or more job descriptions "
            "and calculate the job-match percentage."
        )

    with st.container(border=True):
        st.subheader("🧠 Skills Gap Analysis")
        st.write(
            "Identify missing technical skills and determine which "
            "skills should be improved for a target role."
        )

    with st.container(border=True):
        st.subheader("📚 Resume History")
        st.write(
            "Review previous resume screening and analysis results "
            "and track improvements."
        )


# ============================================================
# SYSTEM ARCHITECTURE
# ============================================================

st.divider()

st.header("⚙️ System Architecture")

st.write(
    "The application follows a frontend-backend architecture "
    "where Streamlit communicates with the FastAPI REST API."
)


# ============================================================
# ARCHITECTURE CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    with st.container(border=True):
        st.caption("FRONTEND")
        st.subheader("Streamlit")
        st.write(
            "Interactive user interface for resume creation, "
            "analysis, ATS scoring, job matching, and skills analysis."
        )


with col2:

    with st.container(border=True):
        st.caption("BACKEND")
        st.subheader("FastAPI")
        st.write(
            "REST API responsible for resume processing, ATS scoring, "
            "job matching, skill-gap analysis, and document generation."
        )


with col3:

    with st.container(border=True):
        st.caption("AI / ML")
        st.subheader("Python")
        st.write(
            "Machine learning, NLP, keyword extraction, resume analysis, "
            "and intelligent scoring."
        )


# ============================================================
# FASTAPI CONNECTION
# ============================================================

st.divider()

st.header("🔌 Backend Connection")

st.write(
    "The Streamlit frontend communicates with the FastAPI backend "
    "running at:"
)

st.info("FastAPI Backend: http://127.0.0.1:8000")


# ============================================================
# API MODULES
# ============================================================

st.subheader("Available Backend Services")


api_col1, api_col2 = st.columns(2)


with api_col1:

    st.write("### 📄 Resume Services")

    st.markdown(
        """
        - `/resume/upload`
        - `/resume/parse`
        - `/resume/health`
        """
    )

    st.write("### 🎯 ATS Services")

    st.markdown(
        """
        - `/api/ats/score`
        - `/api/ats/analyze`
        """
    )


with api_col2:

    st.write("### 💼 Job Services")

    st.markdown(
        """
        - `/jobs/match`
        - `/jobs/analyze`
        - `/recommendations/roles`
        """
    )

    st.write("### 📥 Export Services")

    st.markdown(
        """
        - `/export/pdf`
        - `/export/docx`
        - `/export/txt`
        """
    )


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.divider()

st.header("🛠️ Technology Stack")


tech1, tech2, tech3, tech4 = st.columns(4)


with tech1:
    st.metric("Frontend", "Streamlit")


with tech2:
    st.metric("Backend", "FastAPI")


with tech3:
    st.metric("Language", "Python")


with tech4:
    st.metric("AI / ML", "NLP + ML")


# ============================================================
# PROJECT STATUS
# ============================================================

st.divider()

st.header("✅ Project Status")


status_col1, status_col2, status_col3 = st.columns(3)


with status_col1:
    st.success("Frontend Running")


with status_col2:
    st.success("FastAPI Backend")


with status_col3:
    st.success("AI/ML Services")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI-Powered ATS Resume Builder & Screening System • "
    "Python • Streamlit • FastAPI • Machine Learning • NLP"
)