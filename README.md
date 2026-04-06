# ◈ CareerLens AI
### AI Resume Screening · Job Recommendation · Resume Builder

---

## Setup

```bash
# 1. Clone / extract the project folder
cd careerlens

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

> Make sure `jobs.csv` is in the same folder as `app.py`

---

## Modules

| Module | What it does |
|--------|-------------|
| **Resume Screening** | Upload a PDF resume → extracts skills using NLP keyword matching → shows skill coverage and quick role preview |
| **Job Recommendations** | TF-IDF + cosine similarity matching against 88 job roles → shows matched skills (green) and skill gaps (red) per role |
| **Resume Builder** | Form-based builder → generates a clean downloadable PDF resume + shows skill gap for your target role |

---

## Dataset
`jobs.csv` — 88 job roles, pipe-separated skills per role.

---

## Tech Stack
- Python 3.10+
- Streamlit (UI)
- PyMuPDF / fitz (PDF parsing)
- scikit-learn TF-IDF + cosine similarity (matching)
- fpdf2 (PDF generation)
- pandas (data handling)
