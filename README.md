AI Resume Screening & Candidate Ranking System

Project Overview:
The "AI Resume Screening & Candidate Ranking System" is an intelligent recruitment automation tool that helps HR teams quickly analyze resumes and identify the most relevant candidates for a job position.
The system uses "Natural Language Processing (NLP)and semantic similarity models" to extract skills, analyze experience, and rank candidates according to their relevance to a given job description.
This project reduces manual resume screening effort and improves hiring efficiency.

 Features:
⦁	 Upload resumes in "PDF and DOCX formats"
⦁	 Automatic "resume text extraction"
⦁	"Skill extraction" from resumes
⦁	 "Experience detection"
⦁	 "Job description analysis"
⦁	 "AI-based semantic similarity scoring"
⦁	 "Candidate ranking system"
⦁	"Top candidate automatic selection"
⦁	 "Admin dashboard interface"
⦁	 "SQLite database storage for candidate records"


Technologies Used:

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Python                | Backend programming          |
| Flask                 | Web framework                |
| Sentence Transformers | AI-based semantic similarity |
| NLP Techniques        | Skill and keyword extraction |
| PyPDF2                | PDF text extraction          |
| python-docx           | DOCX resume reading          |
| SQLite                | Database storage             |
| Bootstrap             | Dashboard UI                 |

 How the System Works:
1. The user uploads resumes and provides a job description.
2. The system extracts text from resumes.
3. NLP techniques identify "skills and experience".
4. The job description is analyzed to extract required skills.
5. The system calculates:
   AI semantic similarity
   Skill match score
   Experience score
6. A "weighted scoring algorithm"ranks candidates.
7. The system displays results on the "admin dashboard" and highlights the "top candidate".

 Installation Guide:
 Step 1: Clone the repository
git clone https://github.com/yourusername/AI_Resume_Screener.git
 Step 2: Open project folder
cd AI_Resume_Screener
Step 3: Create virtual environment
python -m venv venv
 Step 4: Activate virtual environment
Windows:
venv\Scripts\activate
 Step 5: Install dependencies
pip install flask sentence-transformers PyPDF2 python-docx
Step 6: Run the application
python app.py
Step 7: Open browser
http://127.0.0.1:5000

Use Case:
This system is useful for:
⦁	HR departments
⦁	Recruitment agencies
⦁	AI-based hiring platforms
⦁	 Automated talent screening

It significantly reduces manual effort and improves candidate selection accuracy.

Future Enhancements:
⦁	Possible improvements include:
⦁	 Bias-aware AI scoring
⦁	 Resume comparison tools
⦁	 HR analytics dashboard
⦁	 Integration with recruitment platforms
⦁	Advanced NLP skill extraction using spaCy

Author
Saiqa Ishaq

 License:
This project is created for "educational and research purposes".
