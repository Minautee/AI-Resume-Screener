# 📝 AI-Powered Resume Screening  

This project provides an **AI-powered resume screening** system that:  
- **Matches resumes** with job descriptions  
- **Analyzes sentiment** in open-ended feedback and CSV files  
- **Extracts structured details** from resumes  

The backend is built with **Flask** and the frontend with **Streamlit**.  
It can be deployed on **Google Cloud Run** for serverless execution.  

---

## **🚀 Features**
✔️ Resume Matching (NLP-based similarity score)  
✔️ Sentiment Analysis (CSV feedback & open-ended surveys/feedback)  
✔️ Resume Parsing (Extracts structured details)  

---

## **🛠️ Installation & Setup**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### **2️⃣ Create a Virtual Environment and Install Dependencies**

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

## **🛠️ Running the Application**
### **3️⃣ Start the Flask API**
```sh
cd backend
python api.py
```

### **4️⃣ Start the Streamlit Frontend**
```sh
cd frontend
streamlit run app.py
```
