import streamlit as st
from app import parser, scorer, report, semantic, keyword_extractor
from app.structure_check import check_resume_sections
import tempfile
import os

st.set_page_config(page_title="ResuMate AI", layout="wide")
st.title("📄 ResuMate AI: ATS Resume Matcher")

# Tabs layout
tabs = st.tabs(["📄 Resume Matcher", "📘 About"])

with tabs[0]:
    st.header("📎 Upload Resume & Job Description")

    resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    jd_text = st.text_area("Paste Job Description here")
    role = st.text_input("Target Role", value="Software Test Engineer")

    if st.button("🚀 Generate ATS Report"):
        if resume_file and jd_text:
            # Save uploaded resume to a temp file
            suffix = "." + resume_file.name.split(".")[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(resume_file.read())
                tmp_path = tmp.name

            resume_text = parser.extract_text_from_file(tmp_path)
            jd_keywords = parser.clean_and_tokenize(jd_text)
            resume_tokens = parser.clean_and_tokenize(resume_text)

            ats_score = scorer.calculate_ats_score(resume_tokens, jd_keywords)
            semantic_score = semantic.calculate_semantic_score(resume_text, jd_text)
            total_score = round((ats_score * 0.4 + semantic_score * 0.6), 2)
            structure_feedback = check_resume_sections(resume_text)

            st.success(f"✅ ATS Keyword Score: {ats_score}%")
            st.info(f"🧠 Semantic Similarity Score: {semantic_score:.2f}%")
            st.markdown(f"🎯 Weighted Total Score: **{total_score}%**")

            category_scores, missing_by_category = scorer.score_by_category(resume_tokens, jd_keywords)

            st.subheader("📊 Score Breakdown by Category:")
            for cat, score in category_scores.items():
                missing = missing_by_category.get(cat, [])
                st.write(f"**{cat}**: {score}%")
                if missing:
                    st.write(f"Missing: {', '.join(missing)}")

            st.subheader("📋 Resume Structure Feedback:")
            st.json(structure_feedback)

            # Generate report
            pdf_path = report.generate_report(tmp_path, ats_score, list(missing_by_category.values()), role)
            with open(pdf_path, "rb") as f:
                st.download_button("📄 Download ATS Report (PDF)", f, file_name="ATS_Report.pdf")

            os.remove(tmp_path)
        else:
            st.warning("Please upload a resume and provide job description text.")

with tabs[1]:
    st.header("About This App")
    st.markdown("""
    **ResuMate AI** helps you evaluate your resume against job descriptions using:
    - ✅ Keyword matching
    - 🧠 Semantic similarity
    - 📊 Section-based scoring
    - 📄 Downloadable ATS report

    > Built with 💙 by [Sachin Acharya](https://github.com/Sachinacharya01/ResuMate_AI)
    """)
