def get_recommendation(final_score):
    """
    Decide whether a candidate should be shortlisted,
    reviewed, or rejected based on the final score.
    """

    if final_score >= 75:
        return "SHORTLIST"

    elif final_score >= 40:
        return "REVIEW"

    else:
        return "REJECT"


def get_reason(
    recommendation,
    matched_skills,
    missing_skills
):
    """
    Generate a simple explanation for the recommendation.
    """

    if recommendation == "SHORTLIST":
        return (
            "Candidate has a strong match with the "
            "required technical skills."
        )

    elif recommendation == "REVIEW":
        return (
            "Candidate has several relevant skills, "
            "but some required skills are missing."
        )

    else:
        return (
            "Candidate has a low match with the "
            "required technical skills."
        )