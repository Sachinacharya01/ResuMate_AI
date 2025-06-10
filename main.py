import streamlit as st
from utils.parser import extract_text_from_file, clean_and_tokenize, extract_sections
from utils.scorer import calculate_ats_score, find_missing_keywords
from utils.report import generate_report
import json
import os
import tempfile
import nltk
# Download punkt for tokenization
nltk.download('punkt')
# Load job role keywords
with open('job_roles.json', 'r') as f:
   job_roles = json.load(f)
st.set_page_config(page_title="ResuMate AI - Resume Checker", layout="wide")
st.title("🤖 ResuMate AI - Smart Resume Checker")
st.markdown("Upload your resume and let AI match it against job roles.")
# Job role selection
selected_role = st.selectbox("Choose a job role to match:", list(job_roles.keys()))
# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=['pdf', 'docx'])
if uploaded_file and selected_role:
   # Save uploaded file to a temp location
   with tempfile.NamedTemporaryFile(delete=False) as tmp:
       tmp.write(uploaded_file.read())
       tmp_path = tmp.name
   # Extract and process text
   resume_text = extract_text_from_file(tmp_path)
   resume_keywords = clean_and_tokenize(resume_text)
   resume_sections = extract_sections(resume_text)
   required_keywords = job_roles[selected_role]
   # Score calculation
   ats_score = calculate_ats_score(resume_keywords, required_keywords)
   missing_keywords = find_missing_keywords(resume_keywords, required_keywords)
   # Display results
   st.subheader("📊 ATS Score")
   st.progress(int(ats_score))
   st.success(f"Your resume scored {ats_score}% match for {selected_role}.")
   st.subheader("🔍 Missing Keywords")
   if missing_keywords:
       st.warning("Consider adding these keywords to your resume:")
       st.write(", ".join(missing_keywords))
   else:
       st.info("Great! Your resume includes all key terms.")
   # Resume Sections
   st.subheader("📑 Resume Sections Detected")
   for section, content in resume_sections.items():
       if content.strip():
           st.markdown(f"**{section.title()}**")
           st.text_area("", content.strip(), height=100)
   # Report download
   report_path = generate_report(tmp_path, ats_score, missing_keywords, selected_role)
   with open(report_path, "rb") as f:
       st.download_button("📥 Download Report", f, file_name="ATS_Report.pdf")
   # Clean temp files
   os.remove(tmp_path)
   os.remove(report_path)