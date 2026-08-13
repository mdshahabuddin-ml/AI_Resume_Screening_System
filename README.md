# 📄 AI-Powered ATS Resume Screening System

An AI-powered Applicant Tracking System (ATS) designed to help users create, analyze, score, and optimize resumes according to specific job descriptions.

The system uses a **Streamlit frontend** and **FastAPI backend** to provide resume building, resume parsing, ATS scoring, job matching, skills-gap analysis, keyword matching, and resume export functionality.

---

## 🚀 Project Overview

The AI-Powered ATS Resume Screening System simulates important functionality of modern Applicant Tracking Systems.

The application helps candidates understand how well their resume matches a target job description and provides recommendations for improving their resume.

### Main Features

- 📝 Resume Builder
- 🔍 Resume Analyzer
- 🎯 ATS Resume Scoring
- 💼 Job Matcher
- 🏆 Multiple Job Ranking
- 🧠 Skills Gap Analysis
- 🔑 Keyword Matching
- 📄 PDF Resume Export
- 📝 DOCX Resume Export
- 📃 TXT Resume Export
- ⚡ FastAPI REST APIs
- 📊 Keyword Match Visualization
- 🐳 Docker Support
- 🔗 GitHub-ready project

---

# 🏗️ System Architecture

```text
                         USER
                           │
                           ▼
              ┌─────────────────────────┐
              │     Streamlit Frontend  │
              │                         │
              │  Resume Builder         │
              │  Resume Analyzer        │
              │  ATS Score              │
              │  Job Matcher            │
              │  Skills Gap             │
              └────────────┬────────────┘
                           │
                        HTTP/REST
                           │
                           ▼
              ┌─────────────────────────┐
              │      FastAPI Backend    │
              │                         │
              │  Resume APIs            │
              │  ATS APIs               │
              │  Builder APIs            │
              │  Job APIs               │
              │  Recommendation APIs    │
              │  Export APIs             │
              └────────────┬────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   Resume Processing    ATS Engine     Job Matching
          │                │                │
          ▼                ▼                ▼
    Text Extraction    Score Engine    Keyword Analysis
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ Results & Recommendations│
              └─────────────────────────┘