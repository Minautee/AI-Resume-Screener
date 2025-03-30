from sentence_transformers import SentenceTransformer, util
from config import GOOGLE_API_KEY 
import logging, re
import google.generativeai as genai

# Configure logging
logging.basicConfig(
    filename="logs/resume_match.log",  # Save logs in a file
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_json_response(response_text):
    """Cleans AI response to remove any JSON or structured formatting."""
    if not response_text:
        return "Error: No response from AI."

    # Remove JSON-like structures manually
    response_text = re.sub(r"```json\s*|\s*```", "", response_text, flags=re.MULTILINE)
    response_text = re.sub(r"[\{\}\[\]\"]", "", response_text)  # Strip JSON brackets/quotes
    response_text = re.sub(r":\s+", ": ", response_text)  # Fix spacing after colons
    return response_text.strip()

def compute_similarity(resume_text, job_description):
    # Compute embeddings
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    # Compute similarity score
    similarity_score = util.pytorch_cos_sim(resume_embedding, job_embedding).item()

    # Prompt for evaluation
    evaluation_prompt = f"""
    Analyze the following resume against the job description.

    **Resume:** {resume_text}
    **Job Description:** {job_description}

    Provide a structured evaluation in simple readable **plain text** with no JSON, no Markdown, and no special formatting.
    
    Format the response **like this**:
    
    Strengths:
    - Mention key strengths of the candidate.

    Weaknesses:
    - Mention gaps in experience or skills.

    Fit Analysis:
    - Why they would be a good fit.
    - Why they might not be a good fit.
    - Final Overall Assessment: Strong Fit / Moderate Fit / Weak Fit.

    **Do NOT return JSON, lists, or code blocks. Just return plain text.**
    """

    # Generate response using Gemini
    response = genai.GenerativeModel("gemini-2.0-flash").generate_content(evaluation_prompt)

    evaluation_text = response.text
    evaluation_text = clean_json_response(response.text)

    # Final output
    output = f"""
    **Resume vs Job Description Similarity Score**: {similarity_score:.2f}

    {evaluation_text}
    """

    return output

    similarity_score = util.pytorch_cos_sim(resume_embedding, job_embedding)
    return similarity_score.item()