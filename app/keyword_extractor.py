from keybert import KeyBERT
import re

# Load KeyBERT model (based on SentenceTransformer)
kw_model = KeyBERT()

def extract_keywords_from_jd(jd_text: str, top_n: int = 40) -> list:
    """
    Extract meaningful keywords from a job description using KeyBERT.
    - Removes duplicates
    - Converts to lowercase
    - Strips punctuation and extra spaces
    """

    # Normalize input
    jd_text = re.sub(r"\s+", " ", jd_text.strip())

    # Extract keywords with KeyBERT
    keywords = kw_model.extract_keywords(
        jd_text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=top_n
    )

    # Clean and deduplicate keywords
    cleaned = set()
    for kw, _ in keywords:
        cleaned.add(kw.lower().strip())

    return list(cleaned)
