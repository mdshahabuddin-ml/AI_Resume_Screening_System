"""
Checks a parsed resume document against common ATS formatting pitfalls:
multi-column layouts, tables, embedded images/icons, unusual section
headings, missing contact info, and non-standard fonts.
"""
import re
from typing import List
from backend.core.resume_parser import ParsedDocument
from backend.core.section_detector import detected_section_names
from backend.schemas.ats_schema import FormattingIssue, ATSFormattingReport

STANDARD_CANONICAL_SECTIONS = {
    "summary", "education", "skills", "experience", "projects",
    "certifications", "achievements", "languages",
}

SAFE_FONTS_HINTS = ["arial", "calibri", "times", "helvetica", "georgia", "verdana"]


def check_formatting(doc: ParsedDocument) -> ATSFormattingReport:
    checks: List[FormattingIssue] = []
    penalty = 0

    # Columns
    if doc.num_columns_detected > 1:
        checks.append(FormattingIssue(
            severity="warning",
            message="Multiple columns detected — ATS parsers often read multi-column resumes out of order. Use a single-column layout.",
        ))
        penalty += 20
    else:
        checks.append(FormattingIssue(severity="pass", message="Single-column layout detected."))

    # Tables
    if doc.has_tables:
        checks.append(FormattingIssue(
            severity="warning",
            message="Tables detected — ATS systems frequently fail to parse content inside tables. Use plain text with standard headings instead.",
        ))
        penalty += 15
    else:
        checks.append(FormattingIssue(severity="pass", message="No tables detected."))

    # Images / icons
    if doc.has_images:
        checks.append(FormattingIssue(
            severity="warning",
            message="Images or icons detected — avoid putting text inside images and skip decorative icons; ATS systems cannot read them.",
        ))
        penalty += 10
    else:
        checks.append(FormattingIssue(severity="pass", message="No images/icons detected."))

    # Section headings
    sections_found = set(detected_section_names(doc.text))
    missing_core = {"experience", "education", "skills"} - sections_found
    if missing_core:
        checks.append(FormattingIssue(
            severity="warning",
            message=f"Could not clearly detect standard section heading(s): {', '.join(sorted(missing_core))}. Use conventional headings like 'Experience', 'Education', 'Skills'.",
        ))
        penalty += 10 * len(missing_core)
    else:
        checks.append(FormattingIssue(severity="pass", message="Standard section headings detected."))

    # Contact info presence (email / phone pattern)
    has_email = bool(re.search(r"[\w.\-]+@[\w\-]+\.[a-zA-Z]{2,}", doc.text))
    has_phone = bool(re.search(r"(\+?\d[\d\-\s()]{8,}\d)", doc.text))
    if not has_email or not has_phone:
        missing_contact = []
        if not has_email:
            missing_contact.append("email")
        if not has_phone:
            missing_contact.append("phone number")
        checks.append(FormattingIssue(
            severity="error",
            message=f"Missing contact information: {', '.join(missing_contact)}.",
        ))
        penalty += 15
    else:
        checks.append(FormattingIssue(severity="pass", message="Contact information (email & phone) found."))

    # Excessive length (rough heuristic on page count when available)
    if doc.page_count and doc.page_count > 2:
        checks.append(FormattingIssue(
            severity="warning",
            message=f"Resume is {doc.page_count} pages — consider trimming to 1-2 pages for better ATS and recruiter readability.",
        ))
        penalty += 5
    else:
        checks.append(FormattingIssue(severity="pass", message="Resume length is within a reasonable page count."))

    formatting_score = max(0, 100 - penalty)
    return ATSFormattingReport(checks=checks, formatting_score=formatting_score)