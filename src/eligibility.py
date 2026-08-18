import re


def check_education(job_description, resume_text):
    """
    Check whether the resume contains an education
    qualification relevant to the job description.
    """

    job_lower = job_description.lower()
    resume_lower = resume_text.lower()

    education_keywords = [
        "be",
        "b.e",
        "btech",
        "b.tech",
        "bachelor of engineering",
        "bachelor of technology",
        "computer science",
        "cse",
    ]

    job_requires_education = any(
        keyword in job_lower
        for keyword in education_keywords
    )

    if not job_requires_education:
        return True

    return any(
        keyword in resume_lower
        for keyword in education_keywords
    )


def check_experience(job_description, resume_text):
    """
    Check whether the candidate appears suitable for
    the experience requirement.
    """

    job_lower = job_description.lower()
    resume_lower = resume_text.lower()

    # Freshers are explicitly accepted
    if "freshers are welcome" in job_lower:
        if "fresher" in resume_lower or "fresher" in resume_lower:
            return True

    # Look for experience numbers such as 1 year / 2 years
    experience_match = re.search(
        r"(\d+)\s*[-to]+\s*(\d+)\s*years?",
        job_lower
    )

    if experience_match:
        max_years = int(experience_match.group(2))

        # Fresher = 0 years
        if "fresher" in resume_lower:
            return max_years >= 0

    return True