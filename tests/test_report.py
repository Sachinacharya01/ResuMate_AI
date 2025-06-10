from utils import report
import os

def test_generate_report_creates_pdf():
    # Input mock data
    resume_path = "sample_resume.docx"  # not used inside the function currently
    score = 85
    missing_keywords = ["Selenium", "REST API"]
    role = "Automation Engineer"

    # Run function
    output_path = report.generate_report(resume_path, score, missing_keywords, role)

    # Check file created
    assert os.path.exists(output_path)
    assert output_path.endswith(".pdf")

    # Check file has content
    assert os.path.getsize(output_path) > 100

    # Cleanup
    os.remove(output_path)
