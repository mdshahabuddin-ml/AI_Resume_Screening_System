"""
Pydantic schemas for resume data — used by the Resume Builder,
the Resume Parser, and every service that reads/writes resume data.
"""
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class Education(BaseModel):
    degree: str
    institution: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None


class Experience(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    bullets: List[str] = Field(default_factory=list)


class Project(BaseModel):
    name: str
    description: Optional[str] = None
    bullets: List[str] = Field(default_factory=list)
    tech_stack: List[str] = Field(default_factory=list)
    link: Optional[str] = None


class Certification(BaseModel):
    name: str
    issuer: Optional[str] = None
    date: Optional[str] = None


class ContactInfo(BaseModel):
    full_name: str
    title: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None


class ResumeData(BaseModel):
    """The full, structured representation of a resume — whether it was
    typed in through the Resume Builder or extracted from an uploaded file."""
    contact: ContactInfo
    summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)

    # Populated automatically when parsed from an uploaded file
    raw_text: Optional[str] = None


class ResumeBuildRequest(BaseModel):
    resume: ResumeData
    template: str = "classic"  # classic | modern | technical | graduate