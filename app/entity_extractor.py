import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    skills, experience, education = [], [], []

    for ent in doc.ents:
        if ent.label_ in ["ORG"]:  # Organizations (companies where someone worked)
            experience.append(ent.text)
        elif ent.label_ in ["DATE"]:  # Work experience years, graduation dates
            experience.append(ent.text)
        elif ent.label_ in ["GPE"]:  # Places might be linked to education or work
            experience.append(ent.text)
        elif ent.label_ in ["PERSON"]:  # Not relevant for extraction
            continue
        elif ent.label_ in ["FAC", "LOC"]:  # Not useful for experience
            continue

    # Extract skills manually using keyword matching
    skill_keywords = [
            "Python", "Java", "C++", "JavaScript", "React", "Node.js", "Angular",
            "Vue.js", "Django", "Flask", "Spring Boot", "Microservices", "SQL", 
            "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "Git", "Docker", "Kubernetes", 
            "AWS", "Azure", "Google Cloud", "CI/CD", "Jenkins", "REST API", 
            "GraphQL", "Linux", "Bash Scripting", "Data Structures", "Algorithms",
            "OOP", "Software Development Life Cycle", "Machine Learning", "AI",
            "TensorFlow", "PyTorch", "Agile", "Scrum", "TDD", "Cloud Computing"
        ]
    for token in doc:
        if token.text in skill_keywords:
            skills.append(token.text)

    return {
        "skills": list(set(skills)),
        "experience": list(set(experience)),
        "education": list(set(education))
    }
