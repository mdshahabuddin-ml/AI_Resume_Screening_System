from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List
import re

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


class RecommendationRequest(BaseModel):

    resume_text: str = Field(..., min_length=30)

    target_role: str = ""


SKILL_ROLES = {

    "AI/ML Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "pandas",
        "numpy",
        "sql",
        "git"
    ],

    "Python Developer": [
        "python",
        "fastapi",
        "django",
        "flask",
        "rest api",
        "sql",
        "git",
        "docker"
    ],

    "Data Scientist": [
        "python",
        "pandas",
        "numpy",
        "scikit-learn",
        "machine learning",
        "sql",
        "statistics",
        "data analysis"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "data analysis",
        "statistics"
    ],

    "Backend Developer": [
        "python",
        "fastapi",
        "django",
        "rest api",
        "sql",
        "docker",
        "git"
    ]
}


def extract_skills(text: str):

    text = text.lower()

    all_skills = set()

    for skills in SKILL_ROLES.values():
        all_skills.update(skills)

    found = []

    for skill in all_skills:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill)

    return set(found)


@router.post("/roles")
def recommend_roles(request: RecommendationRequest):

    resume_skills = extract_skills(request.resume_text)

    recommendations = []

    for role, required_skills in SKILL_ROLES.items():

        matched = [
            skill
            for skill in required_skills
            if skill in resume_skills
        ]

        missing = [
            skill
            for skill in required_skills
            if skill not in resume_skills
        ]

        score = round(
            len(matched) /
            len(required_skills) *
            100,
            2
        )

        recommendations.append({
            "role": role,
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing
        })

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return {
        "success": True,
        "recommendations": recommendations
    }


@router.post("/skill-gap")
def skill_gap(request: RecommendationRequest):

    resume_skills = extract_skills(request.resume_text)

    role = request.target_role

    if role not in SKILL_ROLES:

        return {
            "success": False,
            "message": "Role not found.",
            "available_roles": list(SKILL_ROLES.keys())
        }

    required = set(SKILL_ROLES[role])

    matched = sorted(
        required.intersection(resume_skills)
    )

    missing = sorted(
        required - resume_skills
    )

    return {
        "success": True,
        "role": role,
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": round(
            len(matched) / len(required) * 100,
            2
        )
    }