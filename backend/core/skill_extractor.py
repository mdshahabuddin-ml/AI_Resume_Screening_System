from backend.core.skill_config import SKILL_CONFIG

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for category in SKILL_CONFIG:
        for skill in SKILL_CONFIG[category]:
            if skill in text:
                found_skills.append(skill)

    return list(set(found_skills))

