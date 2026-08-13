from typing import List, Optional
from pydantic import BaseModel


class JobDescriptionRequest(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: str


class JobKeywords(BaseModel):
    required_skills: List[str]
    soft_skills: List[str]
    tools_and_tech: List[str]
    experience_years: Optional[str] = None
    all_keywords: List[str]