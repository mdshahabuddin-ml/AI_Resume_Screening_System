from backend.core.keyword_extractor import extract_job_keywords
from backend.schemas.job_schema import JobKeywords


def analyze_job_description(description: str) -> JobKeywords:
    return extract_job_keywords(description)