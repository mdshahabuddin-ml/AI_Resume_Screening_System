from typing import List, Dict, Optional
from pydantic import BaseModel


class FormattingIssue(BaseModel):
    severity: str  # "error" | "warning" | "pass"
    message: str


class ATSFormattingReport(BaseModel):
    checks: List[FormattingIssue]
    formatting_score: float  # 0-100


class ATSScoreBreakdown(BaseModel):
    keyword_match: float
    formatting: float
    skills: float
    experience: float
    education: float
    contact_information: float


class ATSScoreResponse(BaseModel):
    overall_score: float
    breakdown: ATSScoreBreakdown
    strengths: List[str]
    warnings: List[str]
    matched_keywords: List[str] = []
    missing_keywords: List[str] = []