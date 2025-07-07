from sentence_transformers import SentenceTransformer, util

# Load pre-trained model (MiniLM is fast and effective for semantic search)
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_semantic_score(resume_text: str, jd_text: str) -> float:
    """
    Calculate semantic similarity between resume and job description.
    Returns a percentage score (0 to 100).
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    embeddings = model.encode([resume_text, jd_text], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

    return round(similarity * 100, 2)
