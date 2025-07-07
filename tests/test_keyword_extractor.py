import pytest
from app import keyword_extractor

sample_jd = """
We are looking for a highly skilled Software Test Engineer with experience in Java, Selenium, and API testing.
Familiarity with JMeter, Locust, and automation frameworks is preferred. The candidate should have hands-on
experience with RESTful APIs, Docker, AWS, and CI/CD tools like GitHub Actions. Strong problem-solving and
communication skills are a must.
"""


def test_extract_keywords_from_jd_default():
    keywords = keyword_extractor.extract_keywords_from_jd(sample_jd)

    assert isinstance(keywords, list)
    assert len(keywords) > 0

    # Check some expected keywords are present
    expected_keywords = {"java", "selenium", "jmeter", "locust", "api", "docker", "aws"}
    matched_keywords = set([kw.lower() for kw in keywords])

    assert expected_keywords.intersection(matched_keywords)


def test_extract_keywords_custom_top_n():
    keywords = keyword_extractor.extract_keywords_from_jd(sample_jd, top_n=5)
    assert len(keywords) <= 5
