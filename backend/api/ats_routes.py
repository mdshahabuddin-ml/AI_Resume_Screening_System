from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
import re


router = APIRouter(
    prefix="/api/ats",
    tags=["ATS Analysis"]
)


# =========================================================
# REQUEST SCHEMAS
# =========================================================

class ATSRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: Optional[str] = None


class ATSJobRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: str = Field(..., min_length=20)


# =========================================================
# STOP WORDS
# =========================================================

STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "are",
    "you", "your", "our", "from", "will", "have", "has",
    "was", "were", "been", "being", "into", "using",
    "used", "use", "work", "working", "role", "job",
    "candidate", "candidates", "ability", "strong",
    "good", "excellent", "knowledge", "experience",
    "skills", "skill", "responsible", "responsibilities",
    "required", "requirements", "preferred", "including",
    "such", "other", "their", "they", "them", "who",
    "what", "when", "where", "which", "while", "about",
    "over", "under", "through", "within", "also",
    "more", "than", "then", "very", "can", "should",
    "must", "may", "our", "its", "it's"
}


# =========================================================
# SKILL/SYNONYM NORMALIZATION
# =========================================================

SKILL_GROUPS = {
    "python": {"python", "python3"},
    "machine learning": {
        "machine learning",
        "machine-learning",
        "ml"
    },
    "deep learning": {
        "deep learning",
        "deep-learning",
        "dl"
    },
    "artificial intelligence": {
        "artificial intelligence",
        "artificial-intelligence",
        "ai"
    },
    "natural language processing": {
        "natural language processing",
        "nlp"
    },
    "large language models": {
        "large language model",
        "large language models",
        "llm",
        "llms"
    },
    "pandas": {"pandas"},
    "numpy": {"numpy"},
    "scikit-learn": {
        "scikit-learn",
        "scikit learn",
        "sklearn"
    },
    "tensorflow": {"tensorflow"},
    "pytorch": {"pytorch"},
    "fastapi": {"fastapi"},
    "flask": {"flask"},
    "streamlit": {"streamlit"},
    "sql": {"sql"},
    "postgresql": {"postgresql", "postgres"},
    "mysql": {"mysql"},
    "mongodb": {"mongodb", "mongo"},
    "git": {"git"},
    "github": {"github"},
    "docker": {"docker"},
    "kubernetes": {"kubernetes", "k8s"},
    "rest api": {
        "rest api",
        "rest apis",
        "restful api",
        "restful apis"
    },
    "data structures": {
        "data structures",
        "data structure"
    },
    "algorithms": {
        "algorithms",
        "algorithm"
    },
    "data science": {"data science"},
    "exploratory data analysis": {
        "exploratory data analysis",
        "eda"
    },
    "feature engineering": {
        "feature engineering"
    },
    "generative ai": {
        "generative ai",
        "genai"
    },
    "computer vision": {
        "computer vision",
        "cv"
    },
    "opencv": {"opencv"},
    "docker": {"docker"},
    "cloud": {"cloud"},
    "aws": {"aws"},
    "azure": {"azure"},
    "gcp": {"gcp", "google cloud"},
}


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text: str) -> str:

    text = text.lower()

    text = text.replace(
        "scikit learn",
        "scikit-learn"
    )

    text = text.replace(
        "machine-learning",
        "machine learning"
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# SECTION DETECTION
# =========================================================

def check_sections(text: str):

    text_lower = normalize_text(text)

    sections = {
        "summary": [
            "summary",
            "professional summary",
            "objective",
            "profile"
        ],

        "skills": [
            "skills",
            "technical skills",
            "core skills"
        ],

        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "internship"
        ],

        "education": [
            "education",
            "academic background",
            "qualifications"
        ],

        "projects": [
            "projects",
            "academic projects",
            "personal projects"
        ],

        "certifications": [
            "certifications",
            "certificates",
            "certification"
        ],

        "achievements": [
            "achievements",
            "accomplishments"
        ]
    }

    result = {}

    for section, keywords in sections.items():

        result[section] = any(
            keyword in text_lower
            for keyword in keywords
        )

    return result


# =========================================================
# CONTACT INFORMATION
# =========================================================

def check_contact_information(text: str):

    email_exists = bool(
        re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text
        )
    )

    phone_exists = bool(
        re.search(
            r"(?:\+91[\s-]?)?[6-9]\d{9}\b",
            text
        )
        or
        re.search(
            r"\+?\d[\d\s\-()]{9,}",
            text
        )
    )

    linkedin_exists = "linkedin.com" in text.lower()

    github_exists = "github.com" in text.lower()

    return {
        "email": email_exists,
        "phone": phone_exists,
        "linkedin": linkedin_exists,
        "github": github_exists
    }


# =========================================================
# EXTRACT KEYWORDS FROM JOB DESCRIPTION
# =========================================================

def extract_keywords(job_description: str):

    if not job_description:
        return []

    text = normalize_text(job_description)

    # First identify known technical skills
    detected_skills = []

    for canonical, variations in SKILL_GROUPS.items():

        for variation in variations:

            if variation in text:

                detected_skills.append(canonical)
                break

    # Generic words
    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
        text
    )

    generic_keywords = []

    for word in words:

        word = word.lower()

        if word not in STOP_WORDS:

            generic_keywords.append(word)

    result = set(
        detected_skills + generic_keywords
    )

    return sorted(result)


# =========================================================
# KEYWORD MATCHING
# =========================================================

def calculate_keyword_match(
    resume_text: str,
    job_description: str
):

    if not job_description.strip():

        return {
            "score": 0,
            "matched": [],
            "missing": [],
            "total": 0
        }

    resume = normalize_text(resume_text)

    keywords = extract_keywords(
        job_description
    )

    matched = []
    missing = []

    for keyword in keywords:

        if keyword in resume:

            matched.append(keyword)

        else:

            # Check skill variations
            matched_by_variation = False

            if keyword in SKILL_GROUPS:

                for variation in SKILL_GROUPS[keyword]:

                    if variation in resume:

                        matched_by_variation = True
                        break

            if matched_by_variation:

                matched.append(keyword)

            else:

                missing.append(keyword)

    total = len(keywords)

    if total == 0:

        score = 0

    else:

        score = round(
            len(matched) / total * 100,
            2
        )

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "total": total
    }


# =========================================================
# SECTION SCORE
# =========================================================

def calculate_section_score(sections):

    weights = {
        "summary": 10,
        "skills": 15,
        "experience": 15,
        "education": 10,
        "projects": 10,
        "certifications": 5,
        "achievements": 5
    }

    earned = 0
    total = sum(weights.values())

    for section, weight in weights.items():

        if sections.get(section, False):

            earned += weight

    return round(
        earned / total * 100,
        2
    )


# =========================================================
# READABILITY / LENGTH
# =========================================================

def calculate_readability_score(text: str):

    words = text.split()

    word_count = len(words)

    if 350 <= word_count <= 900:

        return 100

    elif 250 <= word_count < 350:

        return 85

    elif 900 < word_count <= 1100:

        return 85

    elif 150 <= word_count < 250:

        return 65

    else:

        return 50


# =========================================================
# ACTION VERB CHECK
# =========================================================

ACTION_VERBS = {
    "developed",
    "implemented",
    "built",
    "designed",
    "created",
    "optimized",
    "analyzed",
    "trained",
    "deployed",
    "integrated",
    "automated",
    "engineered",
    "improved",
    "developed",
    "led",
    "managed",
    "configured",
    "tested",
    "evaluated"
}


def calculate_action_verb_score(text: str):

    text_lower = normalize_text(text)

    found = []

    for verb in ACTION_VERBS:

        if re.search(
            rf"\b{re.escape(verb)}\b",
            text_lower
        ):

            found.append(verb)

    if len(found) >= 8:

        return 100

    elif len(found) >= 5:

        return 85

    elif len(found) >= 3:

        return 70

    elif len(found) >= 1:

        return 55

    return 40


# =========================================================
# ATS SCORE
# =========================================================

def calculate_ats_score(
    text: str,
    job_description: str = ""
):

    text = text.strip()

    sections = check_sections(text)

    contact = check_contact_information(text)

    keyword_result = calculate_keyword_match(
        text,
        job_description
    )

    # -----------------------------------------------------
    # Contact score
    # -----------------------------------------------------

    contact_score = 0

    if contact["email"]:
        contact_score += 40

    if contact["phone"]:
        contact_score += 30

    if contact["linkedin"]:
        contact_score += 15

    if contact["github"]:
        contact_score += 15


    # -----------------------------------------------------
    # Section score
    # -----------------------------------------------------

    section_score = calculate_section_score(
        sections
    )


    # -----------------------------------------------------
    # Readability score
    # -----------------------------------------------------

    readability_score = calculate_readability_score(
        text
    )


    # -----------------------------------------------------
    # Action verb score
    # -----------------------------------------------------

    action_score = calculate_action_verb_score(
        text
    )


    # -----------------------------------------------------
    # Keyword score
    # -----------------------------------------------------

    keyword_score = keyword_result["score"]


    # -----------------------------------------------------
    # Skills score
    # -----------------------------------------------------

    skills_score = 100 if sections["skills"] else 0


    # -----------------------------------------------------
    # Experience / project score
    # -----------------------------------------------------

    experience_project_score = 0

    if sections["experience"]:
        experience_project_score += 50

    if sections["projects"]:
        experience_project_score += 50


    # =====================================================
    # FINAL WEIGHTED ATS SCORE
    # =====================================================

    breakdown = {

        "keyword_match": round(
            keyword_score,
            2
        ),

        "section_completeness": round(
            section_score,
            2
        ),

        "contact_information": round(
            contact_score,
            2
        ),

        "skills_section": round(
            skills_score,
            2
        ),

        "experience_projects": round(
            experience_project_score,
            2
        ),

        "readability": round(
            readability_score,
            2
        ),

        "action_verbs": round(
            action_score,
            2
        )
    }


    # If JD exists, give keyword matching higher importance
    # If JD doesn't exist, redistribute the weight.

    if job_description.strip():

        overall_score = (

            keyword_score * 0.30 +

            section_score * 0.15 +

            contact_score * 0.10 +

            skills_score * 0.10 +

            experience_project_score * 0.15 +

            readability_score * 0.05 +

            action_score * 0.15
        )

    else:

        overall_score = (

            section_score * 0.20 +

            contact_score * 0.15 +

            skills_score * 0.15 +

            experience_project_score * 0.20 +

            readability_score * 0.15 +

            action_score * 0.15
        )


    overall_score = round(
        min(max(overall_score, 0), 100),
        2
    )


    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    recommendations = []


    if not contact["email"]:

        recommendations.append(
            "Add a professional email address."
        )


    if not contact["phone"]:

        recommendations.append(
            "Add a professional phone number."
        )


    if not contact["linkedin"]:

        recommendations.append(
            "Add a LinkedIn profile URL."
        )


    if not contact["github"]:

        recommendations.append(
            "Add a GitHub profile if applying for technical roles."
        )


    for section, exists in sections.items():

        if not exists:

            recommendations.append(
                f"Consider adding a {section.title()} section."
            )


    if job_description.strip():

        if keyword_score < 50:

            recommendations.append(
                "Low job-description keyword match. "
                "Add relevant skills and technologies that you genuinely possess."
            )

        elif keyword_score < 75:

            recommendations.append(
                "Improve keyword alignment with the target job description."
            )

        else:

            recommendations.append(
                "Good keyword alignment with the target job description."
            )


    word_count = len(text.split())


    if word_count < 250:

        recommendations.append(
            "Resume appears too short. Add relevant project and experience details."
        )

    elif word_count > 1100:

        recommendations.append(
            "Resume may be too long. Remove unnecessary content."
        )


    if action_score < 70:

        recommendations.append(
            "Use stronger action verbs such as Developed, Implemented, "
            "Designed, Optimized, Built, and Deployed."
        )


    return {

        "success": True,

        "ats_score": overall_score,

        "overall_score": overall_score,

        "breakdown": breakdown,

        "contact": contact,

        "sections": sections,

        "keyword_match_score": keyword_score,

        "matched_keywords": keyword_result["matched"][:100],

        "missing_keywords": keyword_result["missing"][:100],

        "keyword_total": keyword_result["total"],

        "recommendations": recommendations

    }


# =========================================================
# POST /score
# =========================================================

@router.post("/score")
def ats_score(request: ATSRequest):

    return calculate_ats_score(
        request.resume_text,
        request.job_description or ""
    )


# =========================================================
# POST /analyze
# =========================================================

@router.post("/analyze")
def ats_analyze(request: ATSJobRequest):

    return calculate_ats_score(
        request.resume_text,
        request.job_description
    )