from docx import Document
from PyPDF2 import PdfReader


def extract_text_from_pdf(file):
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_docx(file):
    document = Document(file.file)
    text = ""
    for para in document.paragraphs:
        text += para.text + "\n"
    return text


def extract_resume_text(file):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file format")


