from app.semantic import calculate_semantic_score


def test_semantic_score_output():
    resume_text = """
    Experienced QA Engineer skilled in writing automation scripts using Selenium and Python.
    Worked on REST API testing and integrated tests into CI/CD pipelines.
    """
    jd_text = """
    We are looking for a QA Engineer experienced in Selenium, REST APIs, and CI/CD integration.
    Must have experience writing automated scripts in Python.
    """

    score = calculate_semantic_score(resume_text, jd_text)

    assert isinstance(score, (int, float)), "Score must be a number"
    assert 0 <= score <= 100, "Score must be between 0 and 100"
