from utils import scorer

def test_calculate_ats_score_full_match():
    resume = ["python", "selenium", "api", "automation"]
    required = ["Python", "Selenium"]
    score = scorer.calculate_ats_score(resume, required)
    assert score == 100

def test_calculate_ats_score_partial_match():
    resume = ["python"]
    required = ["Python", "Selenium"]
    score = scorer.calculate_ats_score(resume, required)
    assert score == 50

def test_calculate_ats_score_no_match():
    resume = ["java", "c++"]
    required = ["Python", "Selenium"]
    score = scorer.calculate_ats_score(resume, required)
    assert score == 0

def test_calculate_ats_score_empty_required():
    resume = ["python", "selenium"]
    required = []
    score = scorer.calculate_ats_score(resume, required)
    assert score == 0

def test_find_missing_keywords_some():
    resume = ["python", "api"]
    required = ["Python", "Selenium", "Automation"]
    missing = scorer.find_missing_keywords(resume, required)
    assert missing == ["Selenium", "Automation"]

def test_find_missing_keywords_none():
    resume = ["python", "selenium", "automation"]
    required = ["Python", "Selenium"]
    missing = scorer.find_missing_keywords(resume, required)
    assert missing == []

def test_find_missing_keywords_all():
    resume = []
    required = ["Python", "Selenium"]
    missing = scorer.find_missing_keywords(resume, required)
    assert missing == ["Python", "Selenium"]
