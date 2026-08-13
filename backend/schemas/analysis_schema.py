from typing import List, Dict, Optional
from pydantic import BaseModel


class SkillGapItem(BaseModel):
    skill: str
    status: str  # "match" | "missing" | "partial"


class SkillGapReport(BaseModel):
    matched: List[str]
    missing: List[str]
    match_percentage: float
    gap_details: List[SkillGapItem]


class JobMatchResult(BaseModel):
    job_title: str
    match_percentage: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    per_skill_score: Dict[str, float] = {}


class SectionScore(BaseModel):
    section: str
    score: float
    status: str  # "good" | "warning" | "poor"
    recommendations: List[str] = []


class ResumeSectionAnalysis(BaseModel):
    sections: List[SectionScore]


class BulletImprovement(BaseModel):
    original: str
    improved: str
    reason: str


class SummaryImprovement(BaseModel):
    original: str
    improved: str
    notes: List[str] = []