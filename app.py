from flask import Flask, render_template, request
import os
import PyPDF2
from docx import Document
from sentence_transformers import SentenceTransformer, util
import re
import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

model = SentenceTransformer('all-MiniLM-L6-v2')

# Skills database
SKILLS_DB = [
"python","java","c++","machine learning","deep learning","nlp",
"flask","django","sql","html","css","javascript","react",
"data analysis","pandas","numpy","tensorflow","pytorch"
]


# -----------------------------
# Database Setup
# -----------------------------

def init_db():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        skills TEXT,
        experience TEXT,
        score REAL
    )
    ''')

    conn.commit()
    conn.close()


def save_candidate(name, skills, experience, score):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO candidates (name,skills,experience,score) VALUES (?,?,?,?)",
        (name, skills, experience, score)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Resume Text Extraction
# -----------------------------

def extract_text(file_path):

    text = ""

    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text

    return text


# -----------------------------
# Skill Extraction
# -----------------------------

def extract_skills(text):

    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def extract_job_skills(job_description):

    job_description = job_description.lower()
    job_skills = []

    for skill in SKILLS_DB:
        if skill in job_description:
            job_skills.append(skill)

    return job_skills


# -----------------------------
# Experience Extraction
# -----------------------------

def extract_experience(text):

    pattern = r'(\d+)\s+years'
    matches = re.findall(pattern, text.lower())

    if matches:
        return max(matches)

    return "0"


# -----------------------------
# Skill Match Score
# -----------------------------

def skill_match_score(candidate_skills, job_skills):

    if len(job_skills) == 0:
        return 0

    matched = set(candidate_skills) & set(job_skills)

    return len(matched) / len(job_skills)


# -----------------------------
# Experience Score
# -----------------------------

def experience_score(candidate_exp):

    exp = int(candidate_exp)

    if exp >= 5:
        return 1
    elif exp >= 3:
        return 0.7
    elif exp >= 1:
        return 0.4
    else:
        return 0.1


# -----------------------------
# AI Similarity Score
# -----------------------------

def calculate_ai_score(resume_text, job_description):

    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    score = util.cos_sim(resume_embedding, job_embedding)

    return float(score)


# -----------------------------
# Main Route
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    results = []
    top_candidate = None

    if request.method == "POST":

        job_description = request.form["job_description"]
        files = request.files.getlist("resumes")

        job_skills = extract_job_skills(job_description)

        for file in files:

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            resume_text = extract_text(filepath)

            skills = extract_skills(resume_text)

            experience = extract_experience(resume_text)

            ai_score = calculate_ai_score(resume_text, job_description)

            skill_score = skill_match_score(skills, job_skills)

            exp_score = experience_score(experience)

            final_score = (0.5 * ai_score) + (0.3 * skill_score) + (0.2 * exp_score)

            save_candidate(file.filename, ", ".join(skills), experience, final_score)

            results.append({
                "name": file.filename,
                "skills": ", ".join(skills),
                "experience": experience,
                "score": round(final_score, 3)
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        if len(results) > 0:
            top_candidate = results[0]

    return render_template("index.html", results=results, top_candidate=top_candidate)


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":

    init_db()

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)