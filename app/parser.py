import os
import re
import docx2txt
import fitz  # PyMuPDF
from nltk.corpus import stopwords
import nltk

# Ensure stopwords are downloaded
nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))

def extract_text_from_file(file_path: str) -> str:
    """
    Extract raw text from a PDF or DOCX resume file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return docx2txt.process(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF (fitz).
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def clean_and_tokenize(text: str) -> list:
    """
    Normalize text:
    - Lowercase
    - Remove punctuation
    - Split into words
    - Remove stopwords
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)  # remove punctuation
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words and word.strip()]
    return tokens
