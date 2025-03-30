import streamlit as st
import requests
import pdfplumber
from docx import Document

st.title("AI-Powered Resume Screening")

# File uploader for resume
resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

# Job description input
job_desc = st.text_area("Enter Job Description")

# Option to upload CSV or enter feedback manually
option = st.radio("Choose Input Type:", ("Enter Feedback Manually", "Upload CSV File"))

if option == "Enter Feedback Manually":
    feedback = st.text_area("Enter Feedback for Sentiment Analysis")
    
elif option == "Upload CSV File":
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if st.button("Analyze"):
    if resume_file is None:
        st.error("Please upload a resume before analyzing.")
    else:
        # Convert file to the correct format
        files = {"file": (resume_file.name, resume_file.getvalue(), resume_file.type)}
        data = {"job_description": job_desc}

        try:
            # Send request to Flask API
            response = requests.post("http://127.0.0.1:8080/resume_match", files=files, data=data, timeout=10)

            if response.status_code == 200:
                st.success("Analysis complete!")
                st.write(response.json())  # Display the response
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the API. Is `api.py` running?")

if st.button("Analyze Sentiment"):
    try:
        if option == "Enter Feedback Manually":
            if not feedback:
                st.error("Please enter feedback before analyzing sentiment.")
            else:
                response = requests.post(
                    "http://127.0.0.1:8080/sentiment_analysis",
                    json={"feedback": feedback},
                    timeout=10
                )

        elif option == "Upload CSV File":
            if uploaded_file is None:
                st.error("Please upload a CSV file before analyzing sentiment.")
            else:
                files = {"csv_file": uploaded_file.getvalue()}  # Read file as bytes
                response = requests.post(
                    "http://127.0.0.1:8080/sentiment_analysis",
                    files={"csv_file": (uploaded_file.name, uploaded_file, "text/csv")},  # Ensure correct file format
                    timeout=10
                )
        # Handle Response
        if response.status_code == 200:
            st.success("Sentiment Analysis Complete!")
            st.json(response.json())  # Display JSON result properly
        else:
            st.error(f"Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the API. Is `api.py` running?")

def extract_text_from_file(uploaded_file):
    """
    Extracts text from uploaded PDF or DOCX resume.
    """
    if uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        text = None  # Unsupported file format
    
    return text

if st.button("Extract Resume Details"):
    if resume_file is None:
        st.error("Please upload a resume before extracting details.")
    else:
        resume_text = extract_text_from_file(resume_file)

        if resume_text:
            try:
                response = requests.post(
                    "http://127.0.0.1:8080/extract_resume",
                    json={"resume_text": resume_text},
                    timeout=10
                )

                if response.status_code == 200:
                    st.success("Resume Data Extracted!")
                    st.write(response.json())
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the API. Is `api.py` running?")
        else:
            st.error("Unsupported file format. Please upload a PDF or DOCX.")
