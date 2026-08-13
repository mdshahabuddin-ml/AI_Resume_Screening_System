import re
from typing import List, Optional
from backend.core.skill_extractor import extract_technical_skills, extract_soft_skills
from backend.core.skills_db import EXPERIENCE_PATTERNS
from backend.schemas.job_schema import JobKeywords


def extract_experience_requirement(text: str) -> Optional[str]:
    lowered = text.lower()
    for pattern in EXPERIENCE_PATTERNS:
        match = re.search(pattern, lowered)
        if match:
            return match.group(0)
    return None


def extract_job_keywords(description: str) -> JobKeywords:
    tech_skills = extract_technical_skills(description)
    soft_skills = extract_soft_skills(description)
    experience = extract_experience_requirement(description)

    all_keywords = sorted(set(tech_skills + soft_skills))

    return JobKeywords(
        required_skills=tech_skills,
        soft_skills=soft_skills,
        tools_and_tech=tech_skills,  # kept separate for future refinement
        experience_years=experience,
        all_keywords=all_keywords,
    )