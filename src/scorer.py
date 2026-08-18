from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(
    job_description,
    resume_text,
    required_skills=None
):
    """
    Calculate improved resume-job similarity.

    Combines:
    - TF-IDF text similarity: 70%
    - Required skill coverage: 30%
    """

    job_description = job_description.lower()
    resume_text = resume_text.lower()

    # ----------------------------------------
    # 1. TF-IDF similarity
    # ----------------------------------------

    documents = [
        job_description,
        resume_text
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True
    )

    vectors = vectorizer.fit_transform(documents)

    tfidf_score = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0] * 100

    # ----------------------------------------
    # 2. Required skill coverage
    # ----------------------------------------

    skill_score = 0.0

    if required_skills:
        matched = 0

        for skill in required_skills:
            if skill.lower() in resume_text:
                matched += 1

        skill_score = (
            matched / len(required_skills)
        ) * 100

    # ----------------------------------------
    # 3. Combined NLP score
    # ----------------------------------------

    similarity_score = (
        tfidf_score * 0.70
        + skill_score * 0.30
    )

    return round(similarity_score, 2)