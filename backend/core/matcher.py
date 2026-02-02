from backend.core.skill_config import SKILL_CONFIG

def calculate_score(resume_skills):
    JOB_SKILLS = [
        "python",
        "java",
        "machine learning",
        "sql",
        "communication",
        "chatgpt"
    ]

    matched_skills = list(set(resume_skills) & set(JOB_SKILLS))

    score = int((len(matched_skills) / len(JOB_SKILLS)) * 100)

    return score, matched_skills, JOB_SKILLS

