import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()  # load all environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page_obj = reader.pages[page]
        text += str(page_obj.extract_text())
    return text

# Prompt Template
input_prompt = """
In the output, Dont add unnessary starting lines like Sure, Here is the output and all. Give the out as I specified below.
Analyze the provided resume and generate detailed, section-by-section feedback. Your response should cover the following aspects:

Overall Structure & Formatting:

Evaluate the organization, clarity, and visual layout.
Check for consistent formatting (font, spacing, bullet points, etc.).
Determine if the resume is easily scannable and ATS-friendly.
Content Quality & Clarity:

Assess the clarity and conciseness of the language used.
Look for grammatical errors, awkward phrasing, or redundancy.
Determine if the content effectively communicates the candidate’s value.
Professional Summary / Objective:

Evaluate whether the summary provides a clear, unique value proposition.
Identify if it highlights specific achievements or strengths relevant to the target role.
Work Experience:

Review each job description for clarity, relevance, and impact.
Look for the use of action verbs and quantifiable metrics (e.g., percentages, numbers).
Identify any vague or overly generic statements that could be improved.
Education & Certifications:

Check if the education section includes relevant details (e.g., institutions, degrees, dates).
Determine if additional details such as honors, coursework, or certifications are provided where relevant.
Skills & Competencies:

Evaluate the relevance of the listed skills to the intended job market.
Consider if skills are prioritized or categorized (e.g., technical, soft skills) and if proficiency levels are indicated.
ATS Optimization & Keywords:

Assess whether the resume uses industry-specific keywords and standardized section headings.
Ensure that the language aligns with common job descriptions in the candidate’s field.
Strengths & Areas for Improvement:

Summarize the main strengths of the resume.
Clearly identify any weaknesses or sections that require improvement.
Provide concrete, actionable suggestions for enhancement.
Overall Rating:

Conclude with an overall rating on a scale (for example, 1 to 10) that reflects the resume’s effectiveness in communicating the candidate’s qualifications.
Expected Output:
Return a structured response that includes:

Summary of Findings: A brief overview of the general quality of the resume.
Give Rating out of 10.
Section-by-Section Feedback: Detailed comments on each resume section with specific suggestions.
Actionable Recommendations: Clear steps the candidate can take to improve the resume specific to the resume(e.g., “Add quantifiable achievements in the Work Experience section”)
Give Exact changes need to make
"""

# Streamlit app
st.title("Resume Rating and Feedback")
st.text("Update Your Resume and get shortlist")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF file")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        pdf_text = input_pdf_text(uploaded_file)
        # Concatenate the prompt with the resume content from the PDF
        full_prompt = input_prompt + "\n\nResume Content:\n" + pdf_text
        response = get_gemini_response(full_prompt)
        st.subheader(response)
