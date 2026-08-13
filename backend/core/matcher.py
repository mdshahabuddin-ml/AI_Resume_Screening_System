from typing import List, Dict
from backend.core.skill_extractor import extract_all_skills


def match_keywords(resume_text: str, job_keywords: List[str]) -> Dict:
    """Compares job keywords against skills actually found in the resume."""
    resume_skills = set(extract_all_skills(resume_text))
    job_kw = set(k.lower() for k in job_keywords)

    matched = sorted(resume_skills & job_kw)
    missing = sorted(job_kw - resume_skills)

    match_percentage = round((len(matched) / len(job_kw) * 100), 2) if job_kw else 0.0

    return {
        "matched": matched,
        "missing": missing,
        "match_percentage": match_percentage,
        "total_job_keywords": len(job_kw),
    }


def skill_gap_report(resume_text: str, required_skills: List[str]) -> Dict:
    result = match_keywords(resume_text, required_skills)
    gap_details = []
    for skill in sorted(set(k.lower() for k in required_skills)):
        status = "match" if skill in result["matched"] else "missing"
        gap_details.append({"skill": skill, "status": status})

    return {
        "matched": result["matched"],
        "missing": result["missing"],
        "match_percentage": result["match_percentage"],
        "gap_details": gap_details,
    }

