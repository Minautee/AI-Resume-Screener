import google.generativeai as genai
import os, re
import json
import logging
from config import GOOGLE_API_KEY 

# Configure logging
logging.basicConfig(
    filename="logs/extract_resume.log",  # Save logs in a file
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def clean_json_response(response_text):
    """Removes markdown code block formatting (```json ... ```) from Gemini's response."""
    if not response_text:
        return None  # Prevent empty response errors

    cleaned_text = re.sub(r"```json\s*", "", response_text)  # Remove opening markdown
    cleaned_text = re.sub(r"```$", "", cleaned_text)  # Remove closing markdown
    return cleaned_text.strip()  # Ensure no extra spaces or newlines

def extract_resume_details(resume_text):
    """
    Uses Gemini AI to extract structured details from resume text.
    """
    logging.info("Starting resume extraction process.")

    # Strictly enforce JSON format in the prompt
    """
    Uses Gemini AI to extract structured details from resume text.
    """
    logging.info("Starting resume extraction process.")

    prompt = f"""
    You are an AI that extracts structured information from resumes.
    
    Extract the following details in **strict JSON format only**:

    {{
        "name": "John Doe",
        "skills": ["Python", "SQL", "Machine Learning"],
        "education": ["B.Tech in Computer Science"],
        "experience": [
            {{
                "company": "XYZ Corp",
                "role": "Software Engineer",
                "duration": "Jan 2020 - Present",
                "responsibilities": [
                    "Built an ETL pipeline that reduced data processing time by 40%",
                    "Collaborated with clients to automate workflows, reducing workload by 15%",
                    "Developed RESTful APIs to integrate multiple internal systems"
                ]
            }}
        ],
        "projects": [
            {{
                "title": "Automated Resume Screening",
                "description": "Developed an AI-powered resume parser using NLP and LLMs to match candidates with job descriptions."
            }},
            {{
                "title": "E-Commerce Dashboard",
                "description": "Built an interactive dashboard in Power BI to visualize sales and customer trends."
            }}
        ],
        "certifications": [
            "AWS Certified Solutions Architect",
            "Google Professional Data Engineer"
        ],
        "extra_curricular": [
            "Member of AI Research Club",
            "Volunteered for community coding workshops"
        ],
        "awards": [
            "Best AI Project - 2023"
        ],
        "references": [
            {{
                "name": "Jane Smith",
                "contact": "jane.smith@example.com",
                "relationship": "Former Manager at XYZ Corp"
            }}
        ],
        "hobbies": ["Chess", "Hiking", "Blogging about AI"]
    }}

    Resume Text:
    \"\"\"{resume_text}\"\"\"

    **DO NOT** include any explanation, markdown, or extra text. Only return JSON.
    """

    try:
        logging.info("Sending request to Gemini API...")
        model = genai.GenerativeModel("gemini-2.0-flash")  # Use reliable model
        response = model.generate_content(prompt)

        # Check if response is None
        if response is None or not response.text.strip():
            logging.error("Gemini API returned an empty response.")
            return {"error": "No response from Gemini API"}

        # Log raw response for debugging
        logging.info(f"Raw response from Gemini API: {response.text}")

        # Clean the response before parsing
        cleaned_response = clean_json_response(response.text)
        if not cleaned_response:
            logging.error("Cleaned response is empty.")
            return {"error": "Failed to parse Gemini response"}

        logging.info(f"Cleaned response: {cleaned_response}")

        # Convert cleaned response to JSON
        extracted_data = json.loads(cleaned_response)

    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {str(e)}")
        extracted_data = {"error": "Invalid JSON response from Gemini API"}

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        extracted_data = {"error": "An error occurred during extraction"}

    logging.info("Extraction process completed successfully.")
    return extracted_data
