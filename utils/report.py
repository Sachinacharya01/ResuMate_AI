from fpdf import FPDF
import os
import tempfile
def generate_report(resume_path: str, ats_score: int, missing_keywords: list, role: str) -> str:
   """
   Generate a PDF report of the ATS score and missing keywords.
   Returns the path to the PDF file.
   """
   pdf = FPDF()
   pdf.add_page()
   pdf.set_font("Arial", size=12)
   pdf.cell(200, 10, txt="ResuMate AI - ATS Report", ln=True, align='C')
   pdf.ln(10)
   pdf.cell(200, 10, txt=f"Role Matched: {role}", ln=True)
   pdf.cell(200, 10, txt=f"ATS Match Score: {ats_score}%", ln=True)
   pdf.ln(10)
   pdf.set_font("Arial", size=11)
   if missing_keywords:
       pdf.cell(200, 10, txt="Missing Keywords:", ln=True)
       for kw in missing_keywords:
           pdf.cell(200, 8, txt=f"- {kw}", ln=True)
   else:
       pdf.cell(200, 10, txt="Great! No keywords are missing.", ln=True)
   # Save to temp file
   tmp_dir = tempfile.gettempdir()
   report_path = os.path.join(tmp_dir, "ATS_Report.pdf")
   pdf.output(report_path)
   return report_path