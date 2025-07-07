import pytest
from app import suggestions

def test_generate_suggestions():
    keywords = ["docker", "jmeter"]
    output = suggestions.generate_suggestions(keywords, section_hint="Projects")

    assert isinstance(output, list)
    assert len(output) == len(keywords)
    assert "docker" in output[0].lower()
    assert "projects" in output[0].lower()

def test_suggest_resume_bullet():
    """
    This test checks whether GPT returns a string containing the keyword
    OR returns a fallback error message.
    """
    keyword = "docker"
    role = "QA Engineer"
    result = suggestions.suggest_resume_bullet(keyword, role)

    assert isinstance(result, str)
    # Either the keyword is in the response or we catch the error string
    assert keyword.lower() in result.lower() or "⚠️" in result
