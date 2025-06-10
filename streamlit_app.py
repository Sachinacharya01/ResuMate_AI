import streamlit as st
from utils.parser import extract_text_from_file, clean_and_tokenize
from utils.scorer import calculate_ats_score, find_missing_keywords
from utils.structure_check import check_resume_structure
from utils.report import generate_report
import json
import os
# Load job description data
with open('job_roles.json', 'r') as file:
   job_data = json.load(file)
st.set_page_config(page_title="ResuMate AI - Resume Checker Bot", layout="wide")
st.title("🤖 ResuMate AI – Smart Resume Checker")
st.markdown("Upload your resume and select a job role to get an ATS-friendly score and improvement tips!")
# Sidebar config
with st.sidebar:
   st.header("📄 Upload Resume")
   uploaded_file = st.file_uploader("Choose your resume (PDF or DOCX)", type=['pdf', 'docx'])
   st.header("💼 Select Job Role")
   selected_role = st.selectbox("Choose a role", list(job_data.keys()))
   st.markdown("---")
   st.caption("Developed by Sachin R | Powered by OpenAI")
# Main logic
if uploaded_file and selected_role:
   resume_text = extract_text_from_file(uploaded_file)
   resume_keywords = clean_and_tokenize(resume_text)
   job_keywords = clean_and_tokenize(job_data[selected_role])
   # Score calculation
   score = calculate_ats_score(resume_keywords, job_keywords)
   missing_keywords = find_missing_keywords(resume_keywords, job_keywords)
   # Structure check
   structure = check_resume_structure(resume_text)
   # Display score
   st.subheader("📊 ATS Score")
   st.progress(score / 100)
   st.success(f"Your resume ATS match score: **{score}%**")
   # Structure feedback
   st.subheader("🧱 Resume Structure Check")
   for section, present in structure.items():
       st.write(f"**{section.capitalize()}**: {'✅ Present' if present else '❌ Missing'}")
   # Keywords
   st.subheader("🔑 Missing Keywords")
   if missing_keywords:
       st.warning(", ".join(missing_keywords))
   else:
       st.success("Your resume covers all relevant keywords!")
   # Report download
   if st.button("📥 Download Full Report"):
       report_path = generate_report(score, structure, missing_keywords, uploaded_file.name)
       with open(report_path, "rb") as f:
           st.download_button(
               label="Download Report",
               data=f,
               file_name=os.path.basename(report_path),
               mime="application/pdf"
           )
