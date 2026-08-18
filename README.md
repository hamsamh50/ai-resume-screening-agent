#  AI Resume Screening Agent

An AI-powered resume screening system that automatically analyzes candidate resumes against a job description, matches required skills, calculates NLP similarity, evaluates eligibility, ranks candidates, and generates recruitment recommendations.

##  Overview

Recruiters often need to manually review a large number of resumes for a single job opening. This project automates the initial screening process.

The system accepts:

* A job description
* Multiple candidate resumes in PDF format

It then:

1. Extracts text from PDF resumes
2. Identifies candidate skills
3. Extracts required skills from the job description
4. Calculates skill matching
5. Calculates NLP similarity using TF-IDF and cosine similarity
6. Checks education eligibility
7. Checks experience eligibility
8. Calculates a weighted final score
9. Assigns a recommendation
10. Ranks candidates
11. Generates JSON and CSV reports
12. Displays results through a Streamlit dashboard

##  Features

###  Resume Processing

* PDF resume text extraction
* Multiple resume upload
* Resume preview
* Automatic candidate analysis

###  Skill Matching

The system identifies technical skills from resumes and compares them with the required skills in the job description.

Example:

| Required Skill        | Candidate |
| --------------------- | --------- |
| Python                | ?         |
| Django                | ?         |
| JavaScript            | ?         |
| HTML                  | ?         |
| CSS                   | ?         |
| SQL                   | ?         |
| REST API              | ?         |
| Django REST Framework | ?         |
| Git                   | ?         |

###  NLP Analysis

The system uses:

* TF-IDF Vectorization
* Unigrams and bigrams
* Cosine similarity

This provides a text-based similarity score between the job description and candidate resume.

###  Eligibility Analysis

The system evaluates:

* Education requirements
* Experience requirements

###  Candidate Scoring

The final candidate score is calculated using weighted components:

| Component      | Weight |
| -------------- | -----: |
| Skill Match    |    60% |
| NLP Similarity |    25% |
| Education      |    10% |
| Experience     |     5% |

###  Candidate Ranking

Candidates are ranked according to their final screening score.

Recommendations are assigned using:

```text
Score >= 60   ? SHORTLIST
Score >= 30   ? REVIEW
Score < 30    ? REJECT
```

###  Streamlit Dashboard

The interactive dashboard provides:

* Candidate filters
* Minimum score filtering
* Candidate search
* Candidate ranking
* Score comparison
* Recommendation distribution
* Matched skills
* Missing skills
* Resume preview
* Screening explanation
* CSV/JSON export

##  System Architecture

```text
                    +---------------------+
                    ¦   Job Description   ¦
                    +---------------------+
                               ¦
                               ?
                    +---------------------+
                    ¦ Required Skill      ¦
                    ¦ Extraction          ¦
                    +---------------------+
                               ¦
                               ¦
+-----------------+            ¦
¦ Candidate PDFs  ¦            ¦
+-----------------+            ¦
         ¦                     ¦
         ?                     ¦
+-----------------+            ¦
¦ PDF Text        ¦            ¦
¦ Extraction      ¦            ¦
+-----------------+            ¦
         ¦                     ¦
         ?                     ?
+------------------------------------+
¦        Resume Screening Pipeline   ¦
+------------------------------------¦
¦ Skill Matching                     ¦
¦ NLP Similarity                     ¦
¦ Education Eligibility              ¦
¦ Experience Eligibility             ¦
+------------------------------------+
                   ¦
                   ?
          +------------------+
          ¦ Weighted Scoring ¦
          +------------------+
                   ¦
                   ?
          +------------------+
          ¦ Candidate Ranking¦
          +------------------+
                   ¦
          +-----------------+
          ?                 ?
    +------------+    +--------------+
    ¦ Streamlit  ¦    ¦ JSON / CSV   ¦
    ¦ Dashboard  ¦    ¦ Reports      ¦
    +------------+    +--------------+
```

##  Project Structure

```text
ai-resume-screening-agent/
¦
+-- dashboard/
¦   +-- app.py
¦
+-- data/
¦   +-- job_description.txt
¦
+-- src/
¦   +-- __init__.py
¦   +-- agent.py
¦   +-- eligibility.py
¦   +-- extractor.py
¦   +-- main.py
¦   +-- matcher.py
¦   +-- parser.py
¦   +-- pipeline.py
¦   +-- ranker.py
¦   +-- recommender.py
¦   +-- reporter.py
¦   +-- scorer.py
¦
+-- .gitignore
+-- README.md
+-- requirements.txt
```

> Candidate resumes, generated reports, virtual environments, and environment files are excluded from the Git repository for privacy and security.

## Technologies Used

* **Python**
* **Streamlit**
* **Scikit-learn**
* **TF-IDF**
* **Cosine Similarity**
* **PyPDF**
* **Pandas**
* **NumPy**
* **Regular Expressions**
* **Git & GitHub**

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/hamsamh50/ai-resume-screening-agent.git
cd ai-resume-screening-agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

##  Running the Application

### Command-Line Pipeline

Run:

```powershell
python -m src.main
```

The pipeline processes the resumes and generates:

```text
output/screening_results.json
output/ranked_candidates.csv
```

### Streamlit Dashboard

Run:

```powershell
streamlit run dashboard/app.py
```

Then open the local Streamlit URL shown in the terminal.

## Example Screening Result

Example output:

```text
Candidate Ranking

Rank  Resume                   Skill Match    NLP       Final Score
--------------------------------------------------------------------
1     Resume_Hamsa.pdf         66.67          5.35      56.34
2     hresume.pdf              0.00           1.53      15.38
```

Example recommendations:

```text
Resume_Hamsa.pdf ? REVIEW
hresume.pdf      ? REJECT
```

##  Screening Explanation

For every candidate, the system provides an explanation containing:

* Final score
* Skill match percentage
* Matched skills
* Missing skills
* Education eligibility
* Experience eligibility
* Recruitment recommendation

Example:

```text
The candidate matches 66.67% of the required technical skills.

Missing skills:
- REST API
- Django REST Framework
- Git

Recruiter action:
Review the candidate's resume and verify the missing
requirements during the technical interview.
```

##  Reports

The system generates:

### JSON

```text
screening_results.json
```

Contains structured candidate screening information.

### CSV

```text
ranked_candidates.csv
```

Contains ranked candidates and their screening scores.

##  Privacy

Candidate resumes may contain personal information such as:

* Name
* Email
* Phone number
* Education details
* Employment information

Therefore, uploaded resumes and generated output files are excluded from the Git repository using `.gitignore`.

##  Future Improvements

Potential improvements include:

* Transformer-based semantic embeddings
* Sentence-BERT similarity
* Better synonym detection
* Advanced skill normalization
* Experience duration extraction
* Salary/CTC matching
* Job-role classification
* LLM-based resume explanations
* Database integration
* Recruiter authentication
* Cloud deployment
* Candidate comparison dashboard

##  Use Cases

This system can be used for:

* Initial resume screening
* Campus recruitment
* Internship recruitment
* Fresher hiring
* Technical candidate ranking
* Automated recruitment assistance

##  Disclaimer

This project is intended to assist recruiters with initial resume screening. It should not be used as the sole basis for employment decisions. Human review should be performed before making recruitment decisions.

##  Author

**Hamsa M H**

BE  Computer Science and Engineering

GitHub: https://github.com/hamsamh50

---

 If you find this project useful, consider giving the repository a star!
