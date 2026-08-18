from src.extractor import extract_text
from src.parser import extract_skills
from src.scorer import calculate_similarity

from src.matcher import (
    extract_required_skills,
    calculate_skill_match,
    get_matched_skills,
    get_missing_skills
)

from src.recommender import (
    get_recommendation,
    get_reason
)

from src.eligibility import (
    check_education,
    check_experience
)


def screen_resumes(job_description, resumes):
    """
    Screen multiple resumes against a job description
    and return ranked candidate results.
    """

    # Extract required skills from job description
    required_skills = extract_required_skills(
        job_description
    )

    results = []

    # Process every resume
    for resume in resumes:

        try:

            # ------------------------------------------------
            # Extract resume text
            # ------------------------------------------------

            text = extract_text(resume)

            # ------------------------------------------------
            # Education
            # ------------------------------------------------

            education_match = check_education(
                job_description,
                text
            )

            # ------------------------------------------------
            # Experience
            # ------------------------------------------------

            experience_match = check_experience(
                job_description,
                text
            )

            # ------------------------------------------------
            # Extract candidate skills
            # ------------------------------------------------

            skills = extract_skills(text)

            # ------------------------------------------------
            # Skill matching
            # ------------------------------------------------

            skill_match_score = calculate_skill_match(
                required_skills,
                skills
            )

            matched_skills = get_matched_skills(
                required_skills,
                skills
            )

            missing_skills = get_missing_skills(
                required_skills,
                skills
            )

            # ------------------------------------------------
            # NLP similarity
            # ------------------------------------------------

            similarity_score = calculate_similarity(
                job_description,
                text
            )

            # ------------------------------------------------
            # Education / Experience scores
            # ------------------------------------------------

            education_score = (
                100 if education_match else 0
            )

            experience_score = (
                100 if experience_match else 0
            )

            # ------------------------------------------------
            # Final score
            # ------------------------------------------------

            final_score = (
                skill_match_score * 0.60
                + similarity_score * 0.25
                + education_score * 0.10
                + experience_score * 0.05
            )

            final_score = round(
                final_score,
                2
            )

            # ------------------------------------------------
            # Recommendation
            # ------------------------------------------------

            recommendation = get_recommendation(
                final_score
            )

            reason = get_reason(
                recommendation,
                matched_skills,
                missing_skills
            )

            # ------------------------------------------------
            # Store result
            # ------------------------------------------------

            results.append({

                "resume": resume.name,

                "skills": skills,

                "matched_skills": matched_skills,

                "missing_skills": missing_skills,

                "skill_match": skill_match_score,

                "nlp_similarity": similarity_score,

                "education_match": education_match,

                "experience_match": experience_match,

                "final_score": final_score,

                "recommendation": recommendation,

                "reason": reason

            })

        except Exception as error:

            print(
                f"ERROR processing "
                f"{resume.name}: {error}"
            )

    # --------------------------------------------------------
    # Rank candidates by final score
    # --------------------------------------------------------

    results.sort(
        key=lambda candidate: candidate["final_score"],
        reverse=True
    )

    return results