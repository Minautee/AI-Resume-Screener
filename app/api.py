from flask import Flask, request, jsonify
import os, logging
from app.resume_parser import extract_resume_text
from app.resume_matcher import compute_similarity
from app.sentiment_analyzer import analyze_open_feedback, analyze_survey
from app.gemini_prompt import extract_resume_details
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload directory exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/resume_match", methods=["POST"])
def resume_match():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    job_desc = request.form.get("job_description")

    if not job_desc:
        return jsonify({"error": "Job description is required"}), 400

    # Save the uploaded file temporarily
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Extract text from the resume
    resume_text = extract_resume_text(file_path)

    # Compute similarity
    similarity = compute_similarity(resume_text, job_desc)

    return jsonify({"similarity_score": similarity})

@app.route("/sentiment_analysis", methods=["POST"])
def sentiment_analysis():
    try:
        # Handle CSV File Upload (Survey Analysis)
        if "csv_file" in request.files:
            logging.info("CSV file received for sentiment analysis.")
            csv_file = request.files["csv_file"]

            if csv_file.filename == "":
                return jsonify({"error": "No selected file"}), 400

            # Read CSV and pass it for analysis
            csv_path = os.path.join("uploads", csv_file.filename)
            csv_file.save(csv_path)  # Save file
            
            # Call function to analyze the CSV
            result = analyze_survey(csv_path)
            return jsonify(result)

        # Handle Open-ended Feedback (JSON input)
        elif request.is_json:
            data = request.get_json()
            feedback = data.get("feedback", "")

            if not feedback:
                return jsonify({"error": "No feedback provided"}), 400

            # Call function to analyze open-ended feedback
            result = analyze_open_feedback(feedback)
            return jsonify(result)

        else:
            return jsonify({"error": "Invalid request format"}), 400

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/extract_resume", methods=["POST"])
def extract_resume():
    data = request.json
    if "resume_text" not in data:
        return jsonify({"error": "Resume text is required"}), 400

    structured_data = extract_resume_details(data["resume_text"])
    return jsonify({"resume_data": structured_data})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Cloud Run sets PORT env variable
    app.run(host="0.0.0.0", port=port, debug=True)