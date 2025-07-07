import pytest
from app import scorer

@pytest.fixture
def resume_keywords():
    return [
        "Python", "QA", "SDET", "unit testing", "Git",
        "AWS", "Docker", "team collaboration", "REST", "problem-solving"
    ]

@pytest.fixture
def jd_keywords():
    return [
        "Java", "Python", "microservices", "QA", "Docker", "JMeter",
        "AWS", "Azure", "unit test", "communication", "GitHub"
    ]

def test_normalize_keywords():
    raw = ["Dockerized", "Git.", "QA", "Unit-Testing"]
    norm = scorer.normalize_keywords(raw)
    assert any("docker" in w for w in norm)
    assert "git" in norm or "github" in norm
    assert "qa" in norm
    assert any("unit" in w or "test" in w for w in norm)

def test_calculate_ats_score(resume_keywords, jd_keywords):
    score = scorer.calculate_ats_score(resume_keywords, jd_keywords)
    assert 0 <= score <= 100

def test_find_missing_keywords(resume_keywords, jd_keywords):
    missing = scorer.find_missing_keywords(resume_keywords, jd_keywords)
    assert isinstance(missing, list)
    for kw in missing:
        assert kw not in scorer.normalize_keywords(resume_keywords)

def test_score_by_category(resume_keywords):
    category_scores, missing = scorer.score_by_category(resume_keywords)
    assert "Skills" in category_scores
    assert isinstance(category_scores["Skills"], int)
    assert isinstance(missing["Tools"], list)
    for cat in ["Skills", "Tools", "Cloud", "Concepts", "Soft Skills"]:
        assert cat in category_scores
        assert cat in missing
