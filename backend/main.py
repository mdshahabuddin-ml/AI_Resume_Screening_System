from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.resume_routes import router as resume_router

app = FastAPI(title="AI Resume Screening System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router, prefix="/resume", tags=["Resume"])

@app.get("/")
def home():
    return {"status": "AI Resume Screening System API running"}

