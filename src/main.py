from pathlib import Path

from src.pipeline import screen_resumes

from src.reporter import (
    save_json_report,
    save_csv_report
)

def main():

    print("=" * 60)
    print("           AI RESUME SCREENING AGENT")
    print("=" * 60)

    project_dir = Path(__file__).resolve().parent.parent

    # ========================================================
    # Job Description
    # ========================================================

    job_description_path = (
        project_dir /
        "data" /
        "job_description.txt"
    )

    if not job_description_path.exists():

        print(
            "\nERROR: job_description.txt not found."
        )

        return

    job_description = job_description_path.read_text(
        encoding="utf-8"
    )

    print("\nJob Description loaded successfully.")

    print(
        f"Job description length: "
        f"{len(job_description)} characters"
    )

    # ========================================================
    # Resume Folder
    # ========================================================

    resumes_folder = (
        project_dir /
        "data" /
        "resumes"
    )

    if not resumes_folder.exists():

        print(
            "\nERROR: resumes folder not found."
        )

        return

    resumes = [
        file
        for file in resumes_folder.iterdir()
        if file.is_file()
    ]

    print(
        f"\nResumes found: {len(resumes)}"
    )

    if not resumes:

        print(
            "\nPlease add resumes to:"
        )

        print("data/resumes/")

        return

    print("\nFiles detected:")

    for file in resumes:

        print(
            f" - {file.name}"
        )

    print("\nReading resumes...\n")

    # ========================================================
    # Screen Resumes
    # ========================================================

    results = screen_resumes(
        job_description,
        resumes
    )

    # ========================================================
    # Candidate Ranking
    # ========================================================

    print("\n" + "=" * 60)

    print(
        "                 CANDIDATE RANKING"
    )

    print("=" * 60)

    print(
        f"{'Rank':<6}"
        f"{'Resume':<25}"
        f"{'Skill Match':<15}"
        f"{'NLP':<12}"
        f"{'Final Score':<12}"
    )

    print("-" * 70)

    for rank, candidate in enumerate(
        results,
        start=1
    ):

        print(
            f"{rank:<6}"
            f"{candidate['resume']:<25}"
            f"{candidate['skill_match']:<15.2f}"
            f"{candidate['nlp_similarity']:<12.2f}"
            f"{candidate['final_score']:<12.2f}"
        )

    # ========================================================
    # Save Reports
    # ========================================================

    json_path = (
        project_dir /
        "output" /
        "screening_results.json"
    )

    csv_path = (
        project_dir /
        "output" /
        "ranked_candidates.csv"
    )

    save_json_report(
        results,
        json_path
    )

    save_csv_report(
        results,
        csv_path
    )

    # ========================================================
    # Completion
    # ========================================================

    print("\n" + "=" * 60)

    print(
        "Resume processing completed."
    )

    print("=" * 60)

    print(
        f"\nJSON report saved to: "
        f"{json_path}"
    )

    print(
        f"CSV report saved to: "
        f"{csv_path}"
    )


if __name__ == "__main__":
    main()