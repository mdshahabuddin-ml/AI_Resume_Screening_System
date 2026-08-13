"""
Detects standard resume sections (CONTACT, SUMMARY, EDUCATION, SKILLS,
EXPERIENCE, PROJECTS, CERTIFICATIONS, ACHIEVEMENTS, LANGUAGES) even when the
user's own heading wording differs (e.g. "Professional Experience" vs
"Work Experience").
"""
import re
from typing import Dict, List
from backend.core.skills_db import STANDARD_SECTION_HEADINGS


def _build_heading_regex():
    all_variants = []
    for canonical, variants in STANDARD_SECTION_HEADINGS.items():
        for v in variants:
            all_variants.append((re.escape(v), canonical))
    # sort longest-first so more specific headings match before generic ones
    all_variants.sort(key=lambda t: -len(t[0]))
    return all_variants


_HEADING_VARIANTS = _build_heading_regex()


def detect_sections(text: str) -> Dict[str, str]:
    """
    Returns a dict mapping canonical section name -> raw text content of
    that section, based on line-by-line heading detection.
    """
    lines = text.split("\n")
    sections: Dict[str, List[str]] = {}
    current = "header"  # anything before the first detected heading
    sections[current] = []

    for line in lines:
        stripped = line.strip()
        matched_canonical = None

        if stripped and len(stripped) < 40:
            lowered = stripped.lower().strip(":-• ")
            for variant_pattern, canonical in _HEADING_VARIANTS:
                if re.fullmatch(variant_pattern, lowered):
                    matched_canonical = canonical
                    break

        if matched_canonical:
            current = matched_canonical
            sections.setdefault(current, [])
            continue

        sections.setdefault(current, []).append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items() if "\n".join(v).strip()}


def detected_section_names(text: str) -> List[str]:
    return [s for s in detect_sections(text).keys() if s != "header"]