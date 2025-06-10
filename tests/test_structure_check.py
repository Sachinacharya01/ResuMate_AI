from utils import structure_check

def test_check_resume_sections_all_present():
    resume_text = """
        Summary: Experienced QA
        Skills: Python, Selenium
        Experience: 5 years
        Education: B.Tech
        Projects: Resume Parser
        Certifications: ISTQB
    """
    result = structure_check.check_resume_sections(resume_text)
    assert all(result.values())  # All should be True

def test_check_resume_sections_partial_present():
    resume_text = """
        Skills: Python, SQL
        Experience: 4 years
        Education: B.E.
    """
    result = structure_check.check_resume_sections(resume_text)
    assert result["Skills"] is True
    assert result["Experience"] is True
    assert result["Education"] is True
    assert result["Projects"] is False
    assert result["Summary"] is False
    assert result["Certifications"] is False

def test_check_resume_sections_none_present():
    resume_text = "This is a random text without any section headers."
    result = structure_check.check_resume_sections(resume_text)
    assert all(not v for v in result.values())  # All should be False
