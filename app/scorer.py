import difflib
import string
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer, util

# Setup
nltk.download("stopwords")
nltk.download("wordnet")
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
model = SentenceTransformer("all-MiniLM-L6-v2")

# Canonical keyword groups
SYNONYM_GROUPS = {
    "aws": ["amazon web services", "cloud computing"],
    "gcp": ["google cloud", "google cloud platform"],
    "azure": ["microsoft azure"],
    "qa": ["quality assurance", "quality analyst"],
    "github": ["git", "version control"],
    "docker": ["dockerized", "docker container"],
    "container": ["containerized", "containers"],
    "sdet": ["software development engineer in test"],
    "unit test": ["unit testing", "test cases"],
    "problem-solving": ["problem solving", "analytical thinking", "troubleshooting"],
    "communication": ["communicator", "collaboration", "verbal skills"]
}

# Category canonical keywords
CATEGORIES = {
    "Skills": ["java", "python", "qa", "sdet", "microservices"],
    "Tools": ["jmeter", "locust", "swagger", "github"],
    "Cloud": ["aws", "azure", "gcp"],
    "Concepts": ["rest", "unit test", "docker", "container"],
    "Soft Skills": ["communication", "problem-solving"]
}

FUZZY_CUTOFF = 0.8
SEMANTIC_THRESHOLD = 0.65


def normalize_keywords(keywords):
    normalized = []
    for kw in keywords:
        kw = kw.lower().translate(str.maketrans("", "", string.punctuation))
        tokens = kw.split()
        lemmatized = " ".join([
            lemmatizer.lemmatize(tok) for tok in tokens if tok not in stop_words
        ])
        normalized.append(lemmatized.strip())
    return list(set(normalized))


def fuzzy_match(resume_kw, target_kw):
    matches = difflib.get_close_matches(target_kw, resume_kw, n=1, cutoff=FUZZY_CUTOFF)
    return bool(matches)


def semantic_match(keyword, resume_phrases):
    kw_embed = model.encode(keyword, convert_to_tensor=True)
    phrases_embed = model.encode(resume_phrases, convert_to_tensor=True)
    similarities = util.cos_sim(kw_embed, phrases_embed)
    return float(similarities.max()) >= SEMANTIC_THRESHOLD


def match_canonical_keyword(canonical_kw, resume_cleaned):
    all_forms = [canonical_kw] + SYNONYM_GROUPS.get(canonical_kw, [])
    all_forms = normalize_keywords(all_forms)

    for form in all_forms:
        if fuzzy_match(resume_cleaned, form):
            return True
        if any(fuzzy_match([form], [kw]) for kw in resume_cleaned):
            return True
        if semantic_match(form, resume_cleaned):
            return True
    return False


def calculate_ats_score(resume_keywords, required_keywords):
    resume_cleaned = normalize_keywords(resume_keywords)
    required_cleaned = normalize_keywords(required_keywords)

    matched = [kw for kw in required_cleaned if fuzzy_match(resume_cleaned, kw) or semantic_match(kw, resume_cleaned)]
    score = int((len(matched) / len(required_cleaned)) * 100) if required_cleaned else 0
    return score


def find_missing_keywords(resume_keywords, required_keywords):
    resume_cleaned = normalize_keywords(resume_keywords)
    required_cleaned = normalize_keywords(required_keywords)

    missing = [kw for kw in required_cleaned if not fuzzy_match(resume_cleaned, kw) and not semantic_match(kw, resume_cleaned)]
    return sorted(set(missing))


def score_by_category(resume_keywords, required_keywords=None):
    resume_cleaned = normalize_keywords(resume_keywords)
    category_scores = {}
    missing_by_category = {}

    for cat, canonical_list in CATEGORIES.items():
        matched = []
        missing = []
        for canonical_kw in canonical_list:
            if match_canonical_keyword(canonical_kw, resume_cleaned):
                matched.append(canonical_kw)
            else:
                missing.append(canonical_kw)

        score = int((len(matched) / len(canonical_list)) * 100) if canonical_list else 0
        category_scores[cat] = score
        missing_by_category[cat] = sorted(missing)

    return category_scores, missing_by_category
