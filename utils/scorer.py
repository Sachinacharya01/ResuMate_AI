def calculate_ats_score(resume_keywords: list, required_keywords: list) -> int:
    """

   Calculate ATS match score between resume and job role.

   """

    if not required_keywords:
        return 0

    matched = [kw for kw in required_keywords if kw.lower() in resume_keywords]

    score = int((len(matched) / len(required_keywords)) * 100)

    return score


def find_missing_keywords(resume_keywords: list, required_keywords: list) -> list:
    """

   Identify missing keywords from the resume.

   """

    return [kw for kw in required_keywords if kw.lower() not in resume_keywords]
