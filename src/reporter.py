import csv
import json
from pathlib import Path


def save_json_report(results, output_path):
    """
    Save candidate screening results as JSON.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    return output_path


def save_csv_report(results, output_path):
    """
    Save candidate screening results as CSV.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "rank",
        "resume",
        "skill_match",
        "nlp_similarity",
        "education_match",
        "experience_match",
        "final_score",
        "recommendation",
        "matched_skills",
        "missing_skills",
        "reason"
    ]

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for rank, candidate in enumerate(
            results,
            start=1
        ):

            writer.writerow({
                "rank": rank,
                "resume": candidate["resume"],
                "skill_match": candidate["skill_match"],
                "nlp_similarity": candidate["nlp_similarity"],
                "education_match": candidate["education_match"],
                "experience_match": candidate["experience_match"],
                "final_score": candidate["final_score"],
                "recommendation": candidate["recommendation"],
                "matched_skills": ", ".join(
                    candidate["matched_skills"]
                ),
                "missing_skills": ", ".join(
                    candidate["missing_skills"]
                ),
                "reason": candidate["reason"]
            })

    return output_path