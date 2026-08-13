from typing import Optional, List
from backend.core.resume_parser import parse_resume_file, clean_text
from backend.core.section_detector import detect_sections
from backend.core.ats_scorer import compute_ats_score
from backend.core.ats_formatter import check_formatting
from backend.schemas.analysis_schema import SectionScore, ResumeSectionAnalysis


def analyze_uploaded_resume(filename: str, file_bytes: bytes, job_keywords: Optional[List[str]] = None):
    doc = parse_resume_file(filename, file_bytes)
    doc.text = clean_text(doc.text)

    ats_score = compute_ats_score(doc, job_keywords=job_keywords)
    formatting_report = check_formatting(doc)
    sections = detect_sections(doc.text)

    return {
        "raw_text": doc.text,
        "detected_sections": list(sections.keys()),
        "ats_score": ats_score,
        "formatting_report": formatting_report,
    }


def analyze_sections(text: str) -> ResumeSectionAnalysis:
    sections = detect_sections(text)
    core_sections = ["summary", "skills", "education", "experience", "projects", "certifications"]
    results = []

    for name in core_sections:
        content = sections.get(name, "")
        if not content:
            results.append(SectionScore(
                section=name.title(), score=0, status="poor",
                recommendations=[f"'{name.title()}' section not found — add it to improve ATS parsing."],
            ))
            continue

        score = min(100, 50 + len(content.split()) // 3)
        recs = []
        if name == "summary" and len(content.split()) < 15:
            recs.append("Expand your summary to 2-3 sentences highlighting your top skills and goals.")
            score = min(score, 70)
        if name == "experience" and not any(ch.isdigit() for ch in content):
            recs.append("Add measurable outcomes (%, numbers, timeframes) to your experience bullets.")
            score = min(score, 75)

        status = "good" if score >= 80 else "warning" if score >= 50 else "poor"
        results.append(SectionScore(section=name.title(), score=score, status=status, recommendations=recs))

    return ResumeSectionAnalysis(sections=results)