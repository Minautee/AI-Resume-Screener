import google.generativeai as genai
import pandas as pd
import os
import json
import logging
import re
from config import GOOGLE_API_KEY

# Configure logging
logging.basicConfig(
    filename="logs/sentiment_analysis.log",
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)

def clean_json_response(response_text):
    """Removes markdown code block formatting from Gemini API response."""
    if not response_text:
        return None
    cleaned_text = re.sub(r"```json\s*", "", response_text)
    cleaned_text = re.sub(r"```$", "", cleaned_text)
    return cleaned_text.strip()

def analyze_survey(csv_file):
    """
    Parses CSV survey responses, sends them to LLM, and returns structured insights.
    """
    try:
        # Step 1: Load CSV
        logging.info("Loading CSV file...")
        df = pd.read_csv(csv_file)

        # Step 2: Convert responses into a structured format
        structured_responses = {}

        for column in df.columns:  # Iterate over column headers (questions)
            responses = df[column].dropna().tolist()  # Get non-empty responses
            structured_responses[column] = responses  # Store question-response mapping

        logging.info(f"Structured survey responses: {structured_responses}")

        # Step 3: Prepare prompt for LLM
        prompt = f"""
        You are an HR AI analyzing employee exit survey responses.

        **Survey Responses:**
        {json.dumps(structured_responses, indent=4)}

        **Analyze each response and return structured JSON:**
        {{
            "overall_sentiment": "Positive/Neutral/Negative",
            "attrition_risk": "Low/Medium/High",
            "key_concerns": [
                "Identified issue 1",
                "Identified issue 2"
            ],
            "actionable_recommendations": [
                "Recommendation 1",
                "Recommendation 2"
            ],
            "individual_analysis": {{
                "Question 1": {{
                    "sentiment": "Positive/Neutral/Negative",
                    "concerns": "...",
                    "recommendations": ["..."]
                }},
                "Question 2": {{
                    "sentiment": "Positive/Neutral/Negative",
                    "concerns": "...",
                    "recommendations": ["..."]
                }}
            }}
        }}

        **DO NOT include any explanations, markdown, or extra text. Only return JSON.**
        """

        logging.info("Sending request to Gemini AI for analysis...")
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        if response is None or not response.text.strip():
            logging.error("Gemini API returned an empty response.")
            return {"error": "No response from Gemini API"}

        logging.info(f"Raw response from Gemini API: {response.text}")

        # Clean the response before parsing
        cleaned_response = clean_json_response(response.text)
        if not cleaned_response:
            logging.error("Cleaned response is empty.")
            return {"error": "Failed to parse Gemini response"}

        logging.info(f"Cleaned response: {cleaned_response}")

        # Convert cleaned response to JSON
        analysis = json.loads(cleaned_response)

    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {str(e)}")
        analysis = {"error": "Invalid JSON response from Gemini API"}

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        analysis = {"error": "An error occurred during analysis"}

    logging.info("Survey analysis process completed successfully.")
    return analysis

def analyze_open_feedback(feedback_text):
    """
    Analyzes open-ended feedback and provides insights.
    """
    try:
        logging.info("Analyzing open-ended feedback...")

        # Step 1: Prepare prompt
        prompt = f"""
        You are an HR AI analyzing open-ended employee feedback. 

        **Feedback:** {feedback_text}

        **Analyze and return structured JSON:**
        {{
            "overall_sentiment": "Positive/Neutral/Negative",
            "key_concerns": [
                "Identified issue 1",
                "Identified issue 2"
            ],
            "actionable_recommendations": [
                "Recommendation 1",
                "Recommendation 2"
            ]
        }}

        **DO NOT include any explanations, markdown, or extra text. Only return JSON.**
        """

        logging.info("Sending open-ended feedback to Gemini AI...")
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        if response is None or not response.text.strip():
            logging.error("Gemini API returned an empty response.")
            return {"error": "No response from Gemini API"}

        logging.info(f"Raw response from Gemini API: {response.text}")

        # Clean the response before parsing
        cleaned_response = clean_json_response(response.text)
        if not cleaned_response:
            logging.error("Cleaned response is empty.")
            return {"error": "Failed to parse Gemini response"}

        logging.info(f"Cleaned response: {cleaned_response}")

        # Convert cleaned response to JSON
        analysis = json.loads(cleaned_response)

    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {str(e)}")
        analysis = {"error": "Invalid JSON response from Gemini API"}

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        analysis = {"error": "An error occurred during analysis"}

    logging.info("Open-ended feedback analysis completed successfully.")
    return analysis
