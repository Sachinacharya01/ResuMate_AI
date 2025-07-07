# 📄 ResuMate AI

**ResuMate_AI** is an AI-powered resume matcher and ATS scoring tool that compares your resume with job descriptions using keyword extraction, fuzzy matching, and semantic analysis.

## 🚀 Features

- ATS Score with detailed keyword breakdown
- Resume structure validation (Skills, Projects, etc.)
- Semantic similarity using Sentence Transformers
- Missing keyword insights by category (Skills, Tools, Cloud, etc.)
- Streamlit UI with downloadable report

## 🧠 Built With

- Python
- Streamlit
- NLTK, spaCy
- Sentence Transformers
- KeyBERT

## 📦 Setup

```bash
git clone https://github.com/Sachinacharya01/ResuMate_AI.git
cd ResuMate_AI
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
