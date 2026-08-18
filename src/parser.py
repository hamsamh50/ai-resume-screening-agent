import re


KNOWN_SKILLS = [
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "sql",
    "django",
    "flask",
    "fastapi",
    "react",
    "node.js",
    "rest api",
    "django rest framework",
    "git",
    "github",
    "c",
    "c++",
    "data structures",
    "algorithms",
    "machine learning",
    "deep learning",
    "docker",
]


def extract_skills(text):
    """
    Find known technical skills in resume text.
    """

    text_lower = text.lower()

    found_skills = []

    for skill in KNOWN_SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text_lower):
            found_skills.append(skill)

    return found_skills