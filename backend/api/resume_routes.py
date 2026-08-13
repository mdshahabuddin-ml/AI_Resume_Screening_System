from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
import io
import os


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_extracted_text(text: str) -> str:
    """
    Clean extracted resume text so it is safe to return as JSON
    and use in ATS processing.
    """

    if not text:
        return ""

    # Remove null characters and other problematic control characters
    cleaned = "".join(
        char
        for char in text
        if char in "\n\r\t" or ord(char) >= 32
    )

    # Normalize line endings
    cleaned = cleaned.replace("\r\n", "\n")
    cleaned = cleaned.replace("\r", "\n")

    # Remove excessive blank lines
    lines = [
        line.strip()
        for line in cleaned.splitlines()
    ]

    cleaned = "\n".join(
        line
        for line in lines
        if line
    )

    return cleaned.strip()


# ============================================================
# FILE TEXT EXTRACTION
# ============================================================

async def extract_resume_text(
    file: UploadFile
) -> Dict[str, Any]:
    """
    Read a PDF, DOCX, or TXT resume and extract text.

    Returns only JSON-safe data.
    """

    filename = file.filename or ""

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    extension = os.path.splitext(filename)[1].lower()

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Only PDF, DOCX and TXT files are supported."
            )
        )

    # Read uploaded file
    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:

        # ----------------------------------------------------
        # TXT
        # ----------------------------------------------------

        if extension == ".txt":

            text = content.decode(
                "utf-8",
                errors="replace"
            )

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        elif extension == ".pdf":

            from pypdf import PdfReader

            reader = PdfReader(
                io.BytesIO(content)
            )

            pages = []

            for page in reader.pages:

                try:
                    page_text = page.extract_text() or ""
                except Exception:
                    page_text = ""

                if page_text:
                    pages.append(page_text)

            text = "\n".join(pages)

        # ----------------------------------------------------
        # DOCX
        # ----------------------------------------------------

        elif extension == ".docx":

            from docx import Document

            document = Document(
                io.BytesIO(content)
            )

            paragraphs = []

            for paragraph in document.paragraphs:

                paragraph_text = paragraph.text.strip()

                if paragraph_text:
                    paragraphs.append(paragraph_text)

            text = "\n".join(paragraphs)

        else:
            text = ""

        # ----------------------------------------------------
        # CLEAN TEXT
        # ----------------------------------------------------

        text = clean_extracted_text(text)

        if not text:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract readable text from "
                    "the uploaded resume."
                )
            )

        return {
            "filename": filename,
            "file_type": extension,
            "character_count": len(text),
            "text": text
        }

    except HTTPException:
        # Keep our intended 400 errors as 400
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Resume processing failed. "
                f"{type(e).__name__}: {str(e)}"
            )
        )


# ============================================================
# UPLOAD RESUME
# ============================================================

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
) -> Dict[str, Any]:
    """
    Upload a resume and extract its text.

    Supported formats:
    - PDF
    - DOCX
    - TXT
    """

    result = await extract_resume_text(file)

    return {
        "success": True,
        **result,
        "message": "Resume uploaded and text extracted successfully."
    }


# ============================================================
# PARSE RESUME
# ============================================================

@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...)
) -> Dict[str, Any]:
    """
    Upload a resume and divide the extracted text
    into common resume sections.
    """

    result = await extract_resume_text(file)

    text = result["text"]

    sections = {
        "summary": "",
        "skills": "",
        "experience": "",
        "education": "",
        "projects": "",
        "certifications": "",
        "achievements": ""
    }

    current_section = None

    section_mapping = {
        "summary": [
            "summary",
            "professional summary",
            "profile",
            "objective"
        ],

        "skills": [
            "skills",
            "technical skills",
            "core skills",
            "technical skill"
        ],

        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history"
        ],

        "education": [
            "education",
            "academic background",
            "academic qualification"
        ],

        "projects": [
            "projects",
            "academic projects",
            "personal projects"
        ],

        "certifications": [
            "certifications",
            "certificates",
            "certification"
        ],

        "achievements": [
            "achievements",
            "accomplishments",
            "awards"
        ]
    }

    for line in text.splitlines():

        cleaned = line.strip()

        if not cleaned:
            continue

        lower_line = cleaned.lower()

        # Remove common Markdown heading symbols
        normalized_line = lower_line.lstrip("#").strip()

        found_section = None

        for section, names in section_mapping.items():

            if normalized_line in names:
                found_section = section
                break

        if found_section:

            current_section = found_section

            continue

        if current_section:

            sections[current_section] += (
                cleaned + "\n"
            )

    # Clean each section
    for section in sections:

        sections[section] = (
            sections[section]
            .strip()
        )

    return {
        "success": True,
        "filename": result["filename"],
        "file_type": result["file_type"],
        "character_count": result["character_count"],
        "sections": sections,
        "text": text
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
def resume_health():

    return {
        "status": "online",
        "service": "Resume API"
    }