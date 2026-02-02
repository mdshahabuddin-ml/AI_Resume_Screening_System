from fastapi import APIRouter, UploadFile, File

from backend.core.resume_parser import extract_resume_text
from backend.core.skill_extractor import extract_skills
from backend.core.matcher import calculate_score

router = APIRouter()


def get_status(score: int) -> str:
    if score >= 75:
        return "STRONGLY MATCHED"
    elif score >= 60:
        return "GOOD MATCH"
    elif score >= 45:
        return "PARTIAL MATCH"
    else:
        return "NOT A MATCH"


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # ✅ Safety check
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        return {"error": "Only PDF and DOCX files are supported"}

    # 1️⃣ Extract resume text (THIS WAS MISSING ❌)
    resume_text = extract_resume_text(file)

    # 2️⃣ Extract resume skills
    resume_skills = extract_skills(resume_text)

    # 3️⃣ Calculate score and matched skills
    score, matched_skills, job_skills = calculate_score(resume_skills)

    # 4️⃣ Find missing skills
    missing_skills = list(set(job_skills) - set(resume_skills))

    # 5️⃣ Get ATS status
    status = get_status(score)

    # 6️⃣ Return response
    return {
        "filename": file.filename,
        "skills_found": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score": score,
        "status": status
    }

