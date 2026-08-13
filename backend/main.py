from fastapi import FastAPI

from backend.api import resume_routes
from backend.api import job_routes
from backend.api import ats_routes
from backend.api import builder_routes
from backend.api import recommendation_routes
from backend.api import export_routes


app = FastAPI(
    title="AI-Powered ATS Resume Screening System",
    description="ATS Resume Builder, Analyzer and Job Matching API",
    version="1.0.0"
)


# -----------------------------
# API ROUTERS
# -----------------------------

app.include_router(resume_routes.router)
app.include_router(job_routes.router)
app.include_router(ats_routes.router)
app.include_router(builder_routes.router)
app.include_router(recommendation_routes.router)
app.include_router(export_routes.router)


# -----------------------------
# ROOT ENDPOINT
# -----------------------------

@app.get("/")
def root():
    return {
        "project": "AI-Powered ATS Resume Screening System",
        "status": "running",
        "message": "Resume Screening API is working",
        "docs": "/docs"
    }


# -----------------------------
# HEALTH CHECK
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "ATS Resume Screening API"
    }