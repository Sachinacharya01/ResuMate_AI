def check_resume_sections(resume_text):
   sections = ["skills", "experience", "education", "projects", "summary", "certifications"]
   return {section.capitalize(): (section in resume_text.lower()) for section in sections}


def check_resume_structure():
    return None
