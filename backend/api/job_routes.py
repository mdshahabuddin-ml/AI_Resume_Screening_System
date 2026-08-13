from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import re

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


class JobDescriptionRequest(BaseModel):
    title: str = Field(..., min_length=2)
    description: str = Field(..., min_length=20)


class JobMatchRequest(BaseModel):
    resume_text: str = Field(..., min_length=20)
    job_description: str = Field(..., min_length=20)


COMMON_SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "node.js",
    "fastapi",
    "flask",
    "django",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "github",
    "rest api",
    "api",
    "nlp",
    "computer vision",
    "langchain",
    "llm",
    "data analysis",
    "power bi",
    "tableau"
]


def extract_skills(text: str) -> List[str]:

    text_lower = text.lower()

    found = []

    for skill in COMMON_SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found.append(skill)

    return sorted(set(found))


@router.post("/analyze")
def analyze_job(request: JobDescriptionRequest):

    skills = extract_skills(request.description)

    return {
        "success": True,
        "job_title": request.title,
        "skills": skills,
        "skill_count": len(skills),
        "description_length": len(request.description)
    }


@router.post("/match")
def match_resume_to_job(request: JobMatchRequest):

    resume_skills = set(extract_skills(request.resume_text))
    job_skills = set(extract_skills(request.job_description))

    if not job_skills:
        raise HTTPException(
            status_code=400,
            detail="No recognizable technical skills found in job description."
        )

    matched = sorted(resume_skills.intersection(job_skills))
    missing = sorted(job_skills - resume_skills)

    score = round(
        (len(matched) / len(job_skills)) * 100,
        2
    )

    return {
        "success": True,
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "matched_count": len(matched),
        "required_skill_count": len(job_skills)
    }


@router.get("/skills")
def available_skills():

    return {
        "count": len(COMMON_SKILLS),
        "skills": sorted(COMMON_SKILLS)
    }