import os
import sys
import requests
import streamlit as st


# ============================================================
# FRONTEND PATH
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(
    os.path.join(CURRENT_DIR, "..")
)

if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

from components.config import API_BASE_URL


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Resume Builder",
    page_icon="📝",
    layout="wide",
)


# ============================================================
# API URL
# ============================================================

API_BASE_URL = API_BASE_URL.rstrip("/")


# ============================================================
# TITLE
# ============================================================

st.title("📝 ATS Resume Builder")

st.write(
    "Create a professional, ATS-friendly resume and "
    "generate a preview, PDF, or DOCX."
)


# ============================================================
# PERSONAL / CONTACT INFORMATION
# ============================================================

st.header("👤 Personal Information")

col1, col2 = st.columns(2)

with col1:

    full_name = st.text_input(
        "Full Name *",
        placeholder="Md Shahabuddin",
    )

    title = st.text_input(
        "Professional Title",
        placeholder="AI/ML Engineer",
    )

    email = st.text_input(
        "Email",
        placeholder="your.email@example.com",
    )

    phone = st.text_input(
        "Phone",
        placeholder="+91 9876543210",
    )


with col2:

    location = st.text_input(
        "Location",
        placeholder="Jaipur, India",
    )

    linkedin = st.text_input(
        "LinkedIn",
        placeholder="https://linkedin.com/in/username",
    )

    github = st.text_input(
        "GitHub",
        placeholder="https://github.com/username",
    )

    portfolio = st.text_input(
        "Portfolio",
        placeholder="https://yourportfolio.com",
    )


# ============================================================
# PROFESSIONAL SUMMARY
# ============================================================

st.header("📄 Professional Summary")

summary = st.text_area(
    "Professional Summary",
    height=150,
    placeholder=(
        "Motivated Computer Science student specializing in "
        "Artificial Intelligence and Machine Learning..."
    ),
)


# ============================================================
# SKILLS
# ============================================================

st.header("🛠️ Skills")

skills_text = st.text_area(
    "Skills",
    height=100,
    placeholder=(
        "Python, Machine Learning, Deep Learning, "
        "Pandas, NumPy, Scikit-learn, TensorFlow, SQL"
    ),
)

skills = [
    skill.strip()
    for skill in skills_text.split(",")
    if skill.strip()
]


# ============================================================
# EDUCATION
# ============================================================

st.header("🎓 Education")

education_count = st.number_input(
    "Number of Education Entries",
    min_value=1,
    max_value=5,
    value=1,
    step=1,
)

education = []

for i in range(int(education_count)):

    st.subheader(f"Education {i + 1}")

    col1, col2 = st.columns(2)

    with col1:

        degree = st.text_input(
            "Degree",
            key=f"education_degree_{i}",
            placeholder="B.Tech Computer Science",
        )

        institution = st.text_input(
            "Institution",
            key=f"education_institution_{i}",
            placeholder="Apex University",
        )

        education_location = st.text_input(
            "Location",
            key=f"education_location_{i}",
            placeholder="Jaipur, India",
        )

    with col2:

        start_date = st.text_input(
            "Start Date",
            key=f"education_start_{i}",
            placeholder="2023",
        )

        end_date = st.text_input(
            "End Date",
            key=f"education_end_{i}",
            placeholder="2027",
        )

        gpa = st.text_input(
            "GPA / Percentage",
            key=f"education_gpa_{i}",
            placeholder="8.5 CGPA",
        )

    education.append(
        {
            "degree": degree,
            "institution": institution,
            "location": education_location or None,
            "start_date": start_date or None,
            "end_date": end_date or None,
            "gpa": gpa or None,
        }
    )


# ============================================================
# WORK EXPERIENCE
# ============================================================

st.header("💼 Work Experience")

experience_count = st.number_input(
    "Number of Experience Entries",
    min_value=0,
    max_value=5,
    value=0,
    step=1,
)

experience = []

for i in range(int(experience_count)):

    st.subheader(f"Experience {i + 1}")

    col1, col2 = st.columns(2)

    with col1:

        exp_title = st.text_input(
            "Job Title",
            key=f"experience_title_{i}",
            placeholder="Machine Learning Intern",
        )

        company = st.text_input(
            "Company",
            key=f"experience_company_{i}",
            placeholder="ABC Technologies",
        )

        exp_location = st.text_input(
            "Location",
            key=f"experience_location_{i}",
            placeholder="Remote",
        )

    with col2:

        exp_start = st.text_input(
            "Start Date",
            key=f"experience_start_{i}",
            placeholder="June 2025",
        )

        exp_end = st.text_input(
            "End Date",
            key=f"experience_end_{i}",
            placeholder="August 2025",
        )

    bullets_text = st.text_area(
        "Responsibilities / Achievements",
        key=f"experience_bullets_{i}",
        height=120,
        placeholder=(
            "Developed machine learning models\n"
            "Improved model performance\n"
            "Built REST APIs for model deployment"
        ),
    )

    bullets = [
        bullet.strip()
        for bullet in bullets_text.split("\n")
        if bullet.strip()
    ]

    experience.append(
        {
            "title": exp_title,
            "company": company,
            "location": exp_location or None,
            "start_date": exp_start or None,
            "end_date": exp_end or None,
            "bullets": bullets,
        }
    )


# ============================================================
# PROJECTS
# ============================================================

st.header("🚀 Projects")

project_count = st.number_input(
    "Number of Projects",
    min_value=0,
    max_value=8,
    value=1,
    step=1,
)

projects = []

for i in range(int(project_count)):

    st.subheader(f"Project {i + 1}")

    project_name = st.text_input(
        "Project Name",
        key=f"project_name_{i}",
        placeholder="AI Resume Screening System",
    )

    project_description = st.text_area(
        "Project Description",
        key=f"project_description_{i}",
        height=100,
        placeholder="Describe the project...",
    )

    project_bullets_text = st.text_area(
        "Project Highlights",
        key=f"project_bullets_{i}",
        height=100,
        placeholder=(
            "Developed ATS scoring model\n"
            "Built FastAPI backend\n"
            "Created Streamlit interface"
        ),
    )

    project_bullets = [
        bullet.strip()
        for bullet in project_bullets_text.split("\n")
        if bullet.strip()
    ]

    tech_stack_text = st.text_input(
        "Technology Stack",
        key=f"project_tech_{i}",
        placeholder=(
            "Python, FastAPI, Streamlit, Scikit-learn"
        ),
    )

    tech_stack = [
        tech.strip()
        for tech in tech_stack_text.split(",")
        if tech.strip()
    ]

    project_link = st.text_input(
        "Project Link",
        key=f"project_link_{i}",
        placeholder=(
            "https://github.com/username/project"
        ),
    )

    projects.append(
        {
            "name": project_name,
            "description": project_description or None,
            "bullets": project_bullets,
            "tech_stack": tech_stack,
            "link": project_link or None,
        }
    )


# ============================================================
# CERTIFICATIONS
# ============================================================

st.header("🏆 Certifications")

certification_count = st.number_input(
    "Number of Certifications",
    min_value=0,
    max_value=8,
    value=0,
    step=1,
)

certifications = []

for i in range(int(certification_count)):

    st.subheader(f"Certification {i + 1}")

    col1, col2 = st.columns(2)

    with col1:

        certification_name = st.text_input(
            "Certification Name",
            key=f"certification_name_{i}",
            placeholder="Machine Learning Certification",
        )

        issuer = st.text_input(
            "Issuer",
            key=f"certification_issuer_{i}",
            placeholder="Coursera",
        )

    with col2:

        certification_date = st.text_input(
            "Date",
            key=f"certification_date_{i}",
            placeholder="2026",
        )

    certifications.append(
        {
            "name": certification_name,
            "issuer": issuer or None,
            "date": certification_date or None,
        }
    )


# ============================================================
# ACHIEVEMENTS
# ============================================================

st.header("🏅 Achievements")

achievements_text = st.text_area(
    "Achievements",
    height=100,
    placeholder=(
        "Completed 160 Days of Problem Solving\n"
        "Participated in AI/ML hackathons"
    ),
)

achievements = [
    achievement.strip()
    for achievement in achievements_text.split("\n")
    if achievement.strip()
]


# ============================================================
# LANGUAGES
# ============================================================

st.header("🌐 Languages")

languages_text = st.text_input(
    "Languages",
    placeholder="English, Hindi",
)

languages = [
    language.strip()
    for language in languages_text.split(",")
    if language.strip()
]


# ============================================================
# TEMPLATE
# ============================================================

st.header("🎨 Resume Template")

template = st.selectbox(
    "Choose Template",
    options=[
        "classic",
        "modern",
        "technical",
        "graduate",
    ],
    index=0,
)


# ============================================================
# BUILD RESUME PAYLOAD
# ============================================================

resume_payload = {
    "resume": {
        "contact": {
            "full_name": full_name,
            "title": title or None,
            "email": email or None,
            "phone": phone or None,
            "location": location or None,
            "linkedin": linkedin or None,
            "github": github or None,
            "portfolio": portfolio or None,
        },
        "summary": summary or None,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "achievements": achievements,
        "languages": languages,
    },
    "template": template,
}


# ============================================================
# SAVE PAYLOAD
# ============================================================

st.session_state["resume_payload"] = resume_payload


# ============================================================
# GENERATE RESUME PREVIEW
# ============================================================

st.divider()

if st.button(
    "🚀 Generate Resume Preview",
    type="primary",
    use_container_width=True,
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not full_name.strip():

        st.error("❌ Please enter your full name.")
        st.stop()

    if not email.strip():

        st.warning(
            "Email is optional, but adding it is recommended "
            "for a professional resume."
        )

    # --------------------------------------------------------
    # PREVIEW ENDPOINT
    # --------------------------------------------------------

    preview_url = (
        f"{API_BASE_URL}/api/builder/preview"
    )

    try:

        with st.spinner("Generating resume preview..."):

            response = requests.post(
                preview_url,
                json=resume_payload,
                timeout=30,
            )

        # ----------------------------------------------------
        # VALIDATION ERROR
        # ----------------------------------------------------

        if response.status_code == 422:

            st.error(
                "❌ Resume data validation failed."
            )

            try:
                st.json(response.json())
            except ValueError:
                st.code(response.text)

            st.stop()

        # ----------------------------------------------------
        # NOT FOUND
        # ----------------------------------------------------

        if response.status_code == 404:

            st.error(
                "❌ Resume Builder endpoint not found."
            )

            st.code(
                f"POST {preview_url}"
            )

            st.stop()

        # ----------------------------------------------------
        # SERVER ERROR
        # ----------------------------------------------------

        if response.status_code >= 500:

            st.error(
                f"❌ Backend error: "
                f"{response.status_code}"
            )

            st.code(response.text)

            st.stop()

        response.raise_for_status()

        result = response.json()

        # ----------------------------------------------------
        # GET GENERATED RESUME TEXT
        # ----------------------------------------------------

        generated_resume_text = result.get(
            "resume_text",
            "",
        )

        if not generated_resume_text.strip():

            st.error(
                "❌ Backend returned an empty resume."
            )

            st.stop()

        # ----------------------------------------------------
        # SAVE GENERATED TEXT
        # ----------------------------------------------------

        st.session_state[
            "generated_resume_text"
        ] = generated_resume_text

        # ----------------------------------------------------
        # SHOW PREVIEW
        # ----------------------------------------------------

        st.success(
            "✅ Resume generated successfully!"
        )

        st.subheader("📄 Resume Preview")

        st.code(
            generated_resume_text,
            language=None,
        )

        st.info(
            "Your resume is ready. Scroll down to "
            "download it as PDF or DOCX."
        )

    except requests.exceptions.ConnectionError as e:

        st.error(
            f"❌ Cannot connect to FastAPI at "
            f"{API_BASE_URL}"
        )

        st.code(str(e))

    except requests.exceptions.Timeout:

        st.error(
            "❌ Backend request timed out."
        )

    except requests.exceptions.RequestException as e:

        st.error(
            f"❌ API request failed: {e}"
        )

    except Exception as e:

        st.error(
            f"❌ Unexpected error: {e}"
        )


# ============================================================
# DOWNLOAD SECTION
# ============================================================

if "generated_resume_text" in st.session_state:

    st.divider()

    st.header("📥 Download Resume")

    resume_text = st.session_state[
        "generated_resume_text"
    ]

    col1, col2 = st.columns(2)


    # ========================================================
    # PDF DOWNLOAD
    # ========================================================

    with col1:

        st.subheader("📄 PDF")

        if st.button(
            "🔄 Prepare PDF",
            use_container_width=True,
            key="prepare_pdf",
        ):

            pdf_url = (
                f"{API_BASE_URL}/export/pdf"
            )

            try:

                with st.spinner(
                    "Generating PDF..."
                ):

                    pdf_response = requests.post(
                        pdf_url,

                        # IMPORTANT:
                        # Export API expects resume_text
                        # NOT resume_payload
                        json={
                            "resume_text": resume_text
                        },

                        timeout=60,
                    )

                if pdf_response.status_code == 200:

                    st.session_state[
                        "pdf_data"
                    ] = pdf_response.content

                    st.success(
                        "✅ PDF is ready!"
                    )

                elif pdf_response.status_code == 422:

                    st.error(
                        "❌ PDF request validation failed."
                    )

                    try:
                        st.json(
                            pdf_response.json()
                        )
                    except ValueError:
                        st.code(
                            pdf_response.text
                        )

                elif pdf_response.status_code == 404:

                    st.error(
                        "❌ PDF endpoint not found."
                    )

                    st.code(
                        f"Expected:\n"
                        f"POST {pdf_url}"
                    )

                else:

                    st.error(
                        f"❌ PDF export failed: "
                        f"{pdf_response.status_code}"
                    )

                    st.code(
                        pdf_response.text
                    )

            except requests.exceptions.ConnectionError as e:

                st.error(
                    "❌ Cannot connect to FastAPI "
                    "for PDF generation."
                )

                st.code(str(e))

            except requests.exceptions.Timeout:

                st.error(
                    "❌ PDF generation timed out."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"❌ PDF request failed: {e}"
                )


        if "pdf_data" in st.session_state:

            st.download_button(
                label="⬇️ Download Resume as PDF",
                data=st.session_state["pdf_data"],
                file_name=(
                    f"{full_name.strip().replace(' ', '_')}"
                    "_Resume.pdf"
                ),
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf",
            )


    # ========================================================
    # DOCX DOWNLOAD
    # ========================================================

    with col2:

        st.subheader("📝 DOCX")

        if st.button(
            "🔄 Prepare DOCX",
            use_container_width=True,
            key="prepare_docx",
        ):

            docx_url = (
                f"{API_BASE_URL}/export/docx"
            )

            try:

                with st.spinner(
                    "Generating DOCX..."
                ):

                    docx_response = requests.post(
                        docx_url,

                        # IMPORTANT:
                        # Export API expects resume_text
                        json={
                            "resume_text": resume_text
                        },

                        timeout=60,
                    )

                if docx_response.status_code == 200:

                    st.session_state[
                        "docx_data"
                    ] = docx_response.content

                    st.success(
                        "✅ DOCX is ready!"
                    )

                elif docx_response.status_code == 422:

                    st.error(
                        "❌ DOCX request validation failed."
                    )

                    try:
                        st.json(
                            docx_response.json()
                        )
                    except ValueError:
                        st.code(
                            docx_response.text
                        )

                elif docx_response.status_code == 404:

                    st.error(
                        "❌ DOCX endpoint not found."
                    )

                    st.code(
                        f"Expected:\n"
                        f"POST {docx_url}"
                    )

                else:

                    st.error(
                        f"❌ DOCX export failed: "
                        f"{docx_response.status_code}"
                    )

                    st.code(
                        docx_response.text
                    )

            except requests.exceptions.ConnectionError as e:

                st.error(
                    "❌ Cannot connect to FastAPI "
                    "for DOCX generation."
                )

                st.code(str(e))

            except requests.exceptions.Timeout:

                st.error(
                    "❌ DOCX generation timed out."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"❌ DOCX request failed: {e}"
                )


        if "docx_data" in st.session_state:

            st.download_button(
                label="⬇️ Download Resume as DOCX",
                data=st.session_state["docx_data"],
                file_name=(
                    f"{full_name.strip().replace(' ', '_')}"
                    "_Resume.docx"
                ),
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                ),
                use_container_width=True,
                key="download_docx",
            )

else:

    st.info(
        "Generate the resume preview first. "
        "The PDF and DOCX download buttons will "
        "appear here."
    )