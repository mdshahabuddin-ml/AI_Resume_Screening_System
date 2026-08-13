"""
Central reference lists used for skill/keyword extraction, matching, and
gap analysis. In a production system this would live in a database and be
user-editable / crowd-sourced. Keeping it as a well-organized Python module
makes it trivial to extend and keeps the rest of the code dependency-free.
"""

TECHNICAL_SKILLS = {
    # Languages
    "python", "java", "c++", "c#", "javascript", "typescript", "go", "rust",
    "sql", "r", "scala", "kotlin", "swift", "php", "ruby", "matlab",
    # ML / AI
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
    "sklearn", "opencv", "huggingface", "transformers", "llm", "genai",
    "generative ai", "reinforcement learning", "xgboost", "pandas", "numpy",
    "data preprocessing", "feature engineering", "model deployment",
    # Web / Backend
    "fastapi", "flask", "django", "rest api", "restful api", "graphql",
    "node.js", "express", "react", "next.js", "vue", "angular", "streamlit",
    "html", "css", "tailwind", "bootstrap",
    # Data / Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "jenkins",
    "git", "github", "gitlab", "linux", "bash", "terraform", "ansible",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "kafka",
    "spark", "hadoop", "airflow", "snowflake", "power bi", "tableau",
    "excel", "data visualization", "etl",
    # General SWE
    "microservices", "system design", "unit testing", "agile", "scrum",
    "object oriented programming", "oop", "data structures", "algorithms",
}

SOFT_SKILLS = {
    "communication", "problem solving", "teamwork", "leadership",
    "time management", "adaptability", "critical thinking", "creativity",
    "collaboration", "attention to detail", "analytical skills",
    "project management", "presentation skills", "mentoring",
    "decision making", "conflict resolution", "work ethic",
}

# Words/phrases that usually flag an "experience requirement" in a JD
EXPERIENCE_PATTERNS = [
    r"(\d+)\+?\s*(?:to\s*\d+\s*)?years?\s+(?:of\s+)?experience",
    r"(\d+)\+?\s*years?\s+in\s+\w+",
]

STANDARD_SECTION_HEADINGS = {
    "contact": ["contact", "contact information", "personal information"],
    "summary": ["summary", "professional summary", "objective", "profile",
                "career objective", "about me"],
    "education": ["education", "academic background", "qualifications"],
    "skills": ["skills", "technical skills", "core competencies",
               "key skills", "areas of expertise"],
    "experience": ["experience", "work experience", "professional experience",
                   "employment history", "career history"],
    "projects": ["projects", "academic projects", "personal projects",
                 "key projects"],
    "certifications": ["certifications", "certificates", "licenses"],
    "achievements": ["achievements", "awards", "honors", "accomplishments"],
    "languages": ["languages", "language proficiency"],
}

ATS_UNSAFE_ELEMENTS_HINTS = [
    "table", "text box", "image", "icon", "column", "header/footer graphic",
]