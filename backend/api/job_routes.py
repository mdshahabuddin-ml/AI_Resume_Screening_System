from fastapi import APIRouter
from backend.schemas.job_schema import JobRequest

router = APIRouter()

jobs_db = []

@router.post("/add")
def add_job(job: JobRequest):
    jobs_db.append(job.dict())
    return {"message": "Job added successfully"}

@router.get("/list")
def list_jobs():
    return jobs_db
