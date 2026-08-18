import re
from src.parser import KNOWN_SKILLS

def skill_exists(text, skill):
    """
    Check whether a skill exists as a complete word/phrase.
    Prevents false matches such as:
    java -> javascript
    c -> css
    git -> github
    """

    pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

    return re.search(pattern, text.lower()) is not None


def extract_required_skills(job_description):
    """
    Extract technical skills only from the Required Skills section.
    """

    text = job_description.lower()

    start_marker = "required skills:"

    if start_marker not in text:
        return []

    skills_section = text.split(start_marker, 1)[1]

    section_markers = [
        "education:",
        "experience:",
        "responsibilities:",
        "qualifications:"
    ]

    end_position = len(skills_section)

    for marker in section_markers:
        position = skills_section.find(marker)

        if position != -1:
            end_position = min(end_position, position)

    skills_section = skills_section[:end_position]

    required_skills = []

    for skill in KNOWN_SKILLS:
        if skill_exists(skills_section, skill):
            required_skills.append(skill)

    return required_skills


def calculate_skill_match(required_skills, candidate_skills):
    """
    Calculate percentage of required skills
    found in the candidate resume.
    """

    if not required_skills:
        return 0.0

    matched_skills = set(required_skills) & set(candidate_skills)

    score = (
        len(matched_skills) /
        len(required_skills)
    ) * 100

    return round(score, 2)


def get_matched_skills(required_skills, candidate_skills):
    """
    Return required skills that are present
    in the candidate resume.
    """

    return [
        skill
        for skill in required_skills
        if skill in candidate_skills
    ]


def get_missing_skills(required_skills, candidate_skills):
    """
    Return required skills that are missing
    from the candidate resume.
    """

    return [
        skill
        for skill in required_skills
        if skill not in candidate_skills
    ]