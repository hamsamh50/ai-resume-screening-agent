import sys
import json
from pathlib import Path

import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.pipeline import screen_resumes
from src.extractor import extract_text

RESULT_FILE = (
    BASE_DIR
    / "output"
    / "screening_results.json"
)

UPLOAD_DIR = (
    BASE_DIR
    / "data"
    / "uploaded_resumes"
)


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from src.pipeline import screen_resumes
from src.extractor import extract_text


# ============================================================
# SESSION STATE
# ============================================================

if "candidates" not in st.session_state:
    st.session_state.candidates = None

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "uploaded_resume_paths" not in st.session_state:
    st.session_state.uploaded_resume_paths = {}


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI Resume Screening Agent")

st.caption(
    "AI-powered resume screening, skill matching, "
    "NLP analysis and candidate ranking"
)


# ============================================================
# SCREEN NEW RESUMES
# ============================================================

with st.container(border=True):

    st.header("🚀 Screen New Resumes")

    # --------------------------------------------------------
    # Job Description
    # --------------------------------------------------------

    st.subheader("1️⃣ Job Description")

    job_description_file = (
        BASE_DIR
        / "data"
        / "job_description.txt"
    )

    default_job_description = ""

    if job_description_file.exists():

        default_job_description = (
            job_description_file.read_text(
                encoding="utf-8"
            )
        )

    job_description = st.text_area(
        "Job Description",
        value=(
            st.session_state.job_description
            if st.session_state.job_description
            else default_job_description
        ),
        height=200,
        placeholder="Enter the job description..."
    )

    # --------------------------------------------------------
    # Resume Upload
    # --------------------------------------------------------

    st.subheader("2️⃣ Upload Resumes")

    uploaded_files = st.file_uploader(
        "Upload candidate PDF resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} resume(s) selected."
        )

    # --------------------------------------------------------
    # Screen Button
    # --------------------------------------------------------

    screen_button = st.button(
        "🚀 Screen Resumes",
        type="primary",
        use_container_width=True
    )


# ============================================================
# RUN SCREENING
# ============================================================

if screen_button:

    if not job_description.strip():

        st.error(
            "Please enter a job description."
        )

        st.stop()

    if not uploaded_files:

        st.error(
            "Please upload at least one PDF resume."
        )

        st.stop()

    # Create upload directory

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    resume_paths = []

    # Save uploaded resumes

    for uploaded_file in uploaded_files:

        file_path = (
            UPLOAD_DIR
            / uploaded_file.name
        )

        file_path.write_bytes(
            uploaded_file.getbuffer()
        )

        resume_paths.append(
            file_path
        )

        st.session_state.uploaded_resume_paths[
            uploaded_file.name
        ] = file_path

    # Save current job description

    st.session_state.job_description = (
        job_description
    )

    # Run AI pipeline

    with st.spinner(
        "🤖 AI is analyzing the resumes..."
    ):

        try:

            results = screen_resumes(
                job_description,
                resume_paths
            )

            st.session_state.candidates = (
                results
            )

            st.success(
                f"Screening completed for "
                f"{len(results)} candidate(s)."
            )

        except Exception as error:

            st.error(
                f"Screening failed: {error}"
            )

            st.stop()


# ============================================================
# LOAD PREVIOUS RESULTS
# ============================================================

if st.session_state.candidates is None:

    if RESULT_FILE.exists():

        try:

            with open(
                RESULT_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                st.session_state.candidates = (
                    json.load(file)
                )

        except Exception as error:

            st.error(
                f"Could not load previous results: "
                f"{error}"
            )

            st.stop()

    else:

        st.info(
            "Upload resumes and click "
            "'Screen Resumes' to begin."
        )

        st.stop()


# ============================================================
# CANDIDATE DATA
# ============================================================

candidates = st.session_state.candidates

if not candidates:

    st.warning(
        "No candidates available."
    )

    st.stop()


dataframe = pd.DataFrame(
    candidates
)


# ============================================================
# SCREENING OVERVIEW
# ============================================================

st.divider()

st.header("📊 Screening Overview")


total_candidates = len(candidates)

review_count = sum(
    candidate["recommendation"] == "REVIEW"
    for candidate in candidates
)

reject_count = sum(
    candidate["recommendation"] == "REJECT"
    for candidate in candidates
)

shortlisted_count = sum(
    candidate["recommendation"] == "SHORTLIST"
    for candidate in candidates
)

average_score = (
    sum(
        candidate["final_score"]
        for candidate in candidates
    )
    / total_candidates
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Total Candidates",
        total_candidates
    )


with col2:

    st.metric(
        "Average Score",
        f"{average_score:.2f}%"
    )


with col3:

    st.metric(
        "Shortlisted",
        shortlisted_count
    )


with col4:

    st.metric(
        "Review",
        review_count
    )


with col5:

    st.metric(
        "Rejected",
        reject_count
    )


# ============================================================
# ANALYTICS
# ============================================================

st.divider()

st.header("📈 Candidate Analytics")


col1, col2 = st.columns(2)


with col1:

    st.subheader(
        "Final Score Comparison"
    )

    chart_data = dataframe[
        ["resume", "final_score"]
    ].copy()

    chart_data = chart_data.set_index(
        "resume"
    )

    st.bar_chart(
        chart_data
    )


with col2:

    st.subheader(
        "Recommendation Distribution"
    )

    recommendation_data = (
        dataframe["recommendation"]
        .value_counts()
    )

    st.bar_chart(
        recommendation_data
    )


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header(
    "🔎 Candidate Filters"
)


recommendations = sorted(
    dataframe[
        "recommendation"
    ]
    .unique()
    .tolist()
)


selected_recommendations = (
    st.sidebar.multiselect(
        "Recommendation",
        recommendations,
        default=recommendations
    )
)


minimum_score = st.sidebar.slider(
    "Minimum Final Score",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=5.0
)


search_text = st.sidebar.text_input(
    "Search Candidate",
    placeholder="Resume name..."
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_dataframe = dataframe[
    dataframe["recommendation"].isin(
        selected_recommendations
    )
]


filtered_dataframe = filtered_dataframe[
    filtered_dataframe["final_score"]
    >= minimum_score
]


if search_text:

    filtered_dataframe = filtered_dataframe[
        filtered_dataframe[
            "resume"
        ].str.contains(
            search_text,
            case=False,
            na=False
        )
    ]


# ============================================================
# CANDIDATE RANKING
# ============================================================

st.divider()

st.header(
    "🏆 Candidate Ranking"
)

st.write(
    f"Showing **{len(filtered_dataframe)}** "
    f"of **{total_candidates}** candidates"
)


# ============================================================
# CSV EXPORT
# ============================================================

st.subheader(
    "📥 Export Results"
)


csv_data = dataframe.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Candidate Report",
    data=csv_data,
    file_name="ranked_candidates.csv",
    mime="text/csv",
    use_container_width=True
)


# ============================================================
# CANDIDATE DETAILS
# ============================================================

filtered_names = (
    filtered_dataframe[
        "resume"
    ]
    .tolist()
)


filtered_candidates = [
    candidate
    for candidate in candidates
    if candidate["resume"]
    in filtered_names
]


for rank, candidate in enumerate(
    filtered_candidates,
    start=1
):

    resume = candidate["resume"]

    final_score = candidate["final_score"]

    skill_match = candidate["skill_match"]

    nlp_similarity = (
        candidate["nlp_similarity"]
    )

    recommendation = (
        candidate["recommendation"]
    )

    education_match = (
        candidate["education_match"]
    )

    experience_match = (
        candidate["experience_match"]
    )

    matched_skills = (
        candidate["matched_skills"]
    )

    missing_skills = (
        candidate["missing_skills"]
    )

    reason = candidate["reason"]


    # --------------------------------------------------------
    # Candidate Badge
    # --------------------------------------------------------

    if final_score >= 70:

        badge = "🟢"

    elif final_score >= 50:

        badge = "🟡"

    else:

        badge = "🔴"


    # --------------------------------------------------------
    # Candidate Expander
    # --------------------------------------------------------

    with st.expander(
        f"{badge}  #{rank}  {resume} "
        f"— {final_score:.2f}% "
        f"— {recommendation}",
        expanded=(rank == 1)
    ):

        # ====================================================
        # SCORE SECTION
        # ====================================================

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Final Score",
                f"{final_score:.2f}%"
            )


        with col2:

            st.metric(
                "Skill Match",
                f"{skill_match:.2f}%"
            )


        with col3:

            st.metric(
                "NLP Similarity",
                f"{nlp_similarity:.2f}%"
            )


        with col4:

            st.metric(
                "Recommendation",
                recommendation
            )


        st.progress(
            min(
                final_score / 100,
                1.0
            )
        )


        # ====================================================
        # RESUME PREVIEW
        # ====================================================

        st.subheader(
            "📄 Resume Preview"
        )


        resume_path = (
            st.session_state
            .uploaded_resume_paths
            .get(resume)
        )


        if (
            resume_path
            and resume_path.exists()
        ):

            try:

                resume_text = extract_text(
                    resume_path
                )

                preview_text = (
                    resume_text[:5000]
                )

                st.text_area(
                    "Extracted Resume Content",
                    value=preview_text,
                    height=300,
                    disabled=True
                )

            except Exception as error:

                st.warning(
                    f"Could not preview resume: "
                    f"{error}"
                )

        else:

            st.info(
                "Resume preview is available "
                "for resumes uploaded during "
                "this session."
            )


        # ====================================================
        # ELIGIBILITY
        # ====================================================

        st.subheader(
            "🎓 Eligibility"
        )


        col1, col2 = st.columns(2)


        with col1:

            if education_match:

                st.success(
                    "Education requirement satisfied"
                )

            else:

                st.error(
                    "Education requirement not satisfied"
                )


        with col2:

            if experience_match:

                st.success(
                    "Experience requirement satisfied"
                )

            else:

                st.error(
                    "Experience requirement not satisfied"
                )


        # ====================================================
        # SKILLS
        # ====================================================

        st.subheader(
            "🛠️ Skill Analysis"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                "#### ✅ Matched Skills"
            )


            if matched_skills:

                for skill in matched_skills:

                    st.success(
                        skill,
                        icon="✅"
                    )

            else:

                st.write(
                    "No matching skills"
                )


        with col2:

            st.markdown(
                "#### ❌ Missing Skills"
            )


            if missing_skills:

                for skill in missing_skills:

                    st.error(
                        skill,
                        icon="❌"
                    )

            else:

                st.success(
                    "No missing skills"
                )


        # ====================================================
        # SCREENING REASON
        # ====================================================

        st.subheader(
            "📝 Screening Reason"
        )


        st.info(
            reason
        )


        # ====================================================
        # AI EXPLANATION
        # ====================================================

        st.subheader(
            "🤖 AI Screening Explanation"
        )


        if recommendation == "REVIEW":

            st.write(
                f"This candidate achieved a final "
                f"relevance score of "
                f"**{final_score:.2f}%**."
            )

            st.write(
                f"The candidate matches "
                f"**{skill_match:.2f}%** of the "
                f"required technical skills."
            )

            if missing_skills:

                st.write(
                    "The main skill gaps identified "
                    "by the screening system are:"
                )

                for skill in missing_skills:

                    st.write(
                        f"• {skill}"
                    )

            st.warning(
                "Recruiter action: Review the "
                "candidate's resume and verify "
                "the missing requirements during "
                "the technical interview."
            )


        elif recommendation == "REJECT":

            st.write(
                f"This candidate achieved a final "
                f"relevance score of "
                f"**{final_score:.2f}%**."
            )

            st.error(
                "The candidate has insufficient "
                "alignment with the required "
                "technical skills."
            )


        else:

            st.success(
                "The candidate strongly matches "
                "the job requirements and should "
                "be considered for the next "
                "recruitment stage."
            )


# ============================================================
# NO FILTER RESULTS
# ============================================================

if not filtered_candidates:

    st.warning(
        "No candidates match the selected filters."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Resume Screening Agent | "
    "PDF Extraction • Skill Matching • "
    "NLP Scoring • Candidate Ranking"
)