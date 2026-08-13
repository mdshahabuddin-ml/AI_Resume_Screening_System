from backend.core.matcher import match_keywords, skill_gap_report
from backend.core.keyword_extractor import extract_job_keywords
from backend.ml.similarity import compute_similarity
from backend.schemas.analysis_schema import JobMatchResult, SkillGapReport


def match_resume_to_job(resume_text: str, job_description: str, job_title: str = "Target Role") -> JobMatchResult:
    job_keywords = extract_job_keywords(job_description)
    result = match_keywords(resume_text, job_keywords.all_keywords)

    # blend exact keyword match (70%) with semantic similarity (30%)
    semantic = compute_similarity(resume_text, job_description)
    blended = round(result["match_percentage"] * 0.7 + semantic * 0.3, 2)

    return JobMatchResult(
        job_title=job_title,
        match_percentage=blended,
        matched_keywords=result["matched"],
        missing_keywords=result["missing"],
        per_skill_score={k: 100.0 for k in result["matched"]},
    )


def get_skill_gap(resume_text: str, job_description: str) -> SkillGapReport:
    job_keywords = extract_job_keywords(job_description)
    report = skill_gap_report(resume_text, job_keywords.all_keywords)
    return SkillGapReport(**report)