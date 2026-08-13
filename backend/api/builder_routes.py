from fastapi import APIRouter, Form
from typing import List, Optional
from backend.schemas.resume_schema import ResumeBuildRequest
from backend.services.resume_builder import build_resume_text
from backend.core.resume_optimizer import improve_bullet, improve_summary, improve_with_llm

router = APIRouter(prefix="/api/builder", tags=["Builder"])


@router.post("/preview")
async def preview_resume(payload: ResumeBuildRequest):
    return {"resume_text": build_resume_text(payload.resume)}


@router.post("/improve-bullet")
async def improve_bullet_endpoint(bullet: str = Form(...), target_keywords: Optional[str] = Form(None)):
    keywords = [k.strip() for k in target_keywords.split(",")] if target_keywords else None

    llm_result = improve_with_llm(
        bullet,
        "Rewrite this resume bullet point to be ATS-friendly: start with a strong action verb, "
        "be concise, and highlight impact. Do not invent facts or numbers that aren't implied."
    )
    if llm_result:
        return {"original": bullet, "improved": llm_result, "reason": "AI-generated rewrite."}

    return improve_bullet(bullet, target_keywords=keywords)


@router.post("/improve-summary")
async def improve_summary_endpoint(summary: str = Form(...), target_role: Optional[str] = Form(None),
                                    top_skills: Optional[str] = Form(None)):
    skills = [s.strip() for s in top_skills.split(",")] if top_skills else None

    llm_result = improve_with_llm(
        summary,
        f"Rewrite this resume professional summary for the role of {target_role or 'the target job'} "
        "to be specific, ATS-friendly, and 2-3 sentences long. Do not invent facts not present in the original."
    )
    if llm_result:
        return {"original": summary, "improved": llm_result, "notes": ["AI-generated rewrite."]}

    return improve_summary(summary, target_role=target_role, top_skills=skills)