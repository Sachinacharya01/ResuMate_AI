import os
import docx2txt
import textract
import nltk
from nltk.tokenize import word_tokenize

# ✅ Ensure the correct tokenizer is downloaded
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        try:
            text = textract.process(file_path, method='pdftotext')
        except Exception:
            text = textract.process(file_path)
        return text.decode("utf-8")
    elif ext == ".docx":
        return docx2txt.process(file_path)
    else:
        return ""


def clean_and_tokenize(text: str) -> list:
    # ✅ Use default language explicitly to avoid misinterpretation
    tokens = word_tokenize(text.lower(), language='english')
    return list(set(tokens))  # Unique tokens


def extract_sections(text: str) -> dict:
    sections = {
        "education": "",
        "experience": "",
        "skills": "",
        "projects": "",
        "certifications": ""
    }
    current_section = None
    lines = text.splitlines()
    for line in lines:
        line_clean = line.strip().lower()
        if "education" in line_clean:
            current_section = "education"
        elif "experience" in line_clean:
            current_section = "experience"
        elif "skills" in line_clean:
            current_section = "skills"
        elif "project" in line_clean:
            current_section = "projects"
        elif "certification" in line_clean:
            current_section = "certifications"
        if current_section:
            sections[current_section] += line + "\n"
    return sections


def parse_resume(resume_text: str) -> dict:
    """
    Combines section extraction and tokenization.
    Returns a dictionary of sections and extracted tokens.
    """
    sections = extract_sections(resume_text)
    tokens = clean_and_tokenize(resume_text)
    sections["tokens"] = tokens
    return sections
