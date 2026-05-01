from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from recommender import get_recommendations
from resume_parser import parse_resume
import json
import os

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://127.0.0.1:27017/")
db     = client["internshipDB"]

UPLOAD_FOLDER = "C:/Users/HP/OneDrive/Desktop/internship/internship-backend/uploads"

def parse_json(data):
    return json.loads(json.dumps(data, default=str))

def get_sample_internships():
    return [
        {
            "_id": "1",
            "title": "Python Developer Intern",
            "company": "TCS",
            "location": "Chennai",
            "sector": "IT",
            "duration": "3 months",
            "stipend": "10,000/month",
            "skills_required": "Python Django REST API SQL",
            "description": "Build backend APIs using Python and Django"
        },
        {
            "_id": "2",
            "title": "Data Science Intern",
            "company": "Infosys",
            "location": "Bangalore",
            "sector": "Data Science",
            "duration": "6 months",
            "stipend": "15,000/month",
            "skills_required": "Python Machine Learning Data Science pandas numpy",
            "description": "Work on ML models and data analysis projects"
        },
        {
            "_id": "3",
            "title": "React Frontend Intern",
            "company": "Wipro",
            "location": "Remote",
            "sector": "Web Development",
            "duration": "3 months",
            "stipend": "8,000/month",
            "skills_required": "React JavaScript HTML CSS frontend",
            "description": "Build responsive web applications using React"
        },
        {
            "_id": "4",
            "title": "Full Stack Developer Intern",
            "company": "HCL",
            "location": "Chennai",
            "sector": "IT",
            "duration": "6 months",
            "stipend": "12,000/month",
            "skills_required": "React Node.js MongoDB Express full stack JavaScript",
            "description": "Work on full stack web development projects"
        },
        {
            "_id": "5",
            "title": "AI ML Research Intern",
            "company": "DRDO",
            "location": "Delhi",
            "sector": "Research",
            "duration": "6 months",
            "stipend": "20,000/month",
            "skills_required": "Python Machine Learning Deep Learning TensorFlow AI",
            "description": "Research and develop AI models for defence applications"
        },
        {
            "_id": "6",
            "title": "Finance Analyst Intern",
            "company": "SBI",
            "location": "Mumbai",
            "sector": "Finance",
            "duration": "3 months",
            "stipend": "10,000/month",
            "skills_required": "Finance Excel Data Analysis accounting",
            "description": "Analyse financial data and prepare reports"
        },
        {
            "_id": "7",
            "title": "Android Developer Intern",
            "company": "Zoho",
            "location": "Chennai",
            "sector": "Mobile Development",
            "duration": "3 months",
            "stipend": "12,000/month",
            "skills_required": "Android Java Kotlin mobile development",
            "description": "Build Android applications for enterprise clients"
        },
        {
            "_id": "8",
            "title": "Cyber Security Intern",
            "company": "ISRO",
            "location": "Bangalore",
            "sector": "Security",
            "duration": "6 months",
            "stipend": "18,000/month",
            "skills_required": "Cyber Security Network Linux Python ethical hacking",
            "description": "Work on cyber security systems and threat analysis"
        }
    ]

@app.route("/test")
def test():
    return jsonify({"message": "AI Engine is working!"})

@app.route("/test-recommend")
def test_recommend():
    try:
        sample_profile = {
            "skills":    "Python React Data Science Machine Learning SQL pandas",
            "interests": "Web Development AI Data Science Software",
            "degree":    "BTech AI&DS",
            "location":  "Chennai"
        }
        internships = get_sample_internships()
        results = get_recommendations(sample_profile, internships)
        return jsonify({
            "success":         True,
            "recommendations": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/parse-resume", methods=["POST"])
def parse_resume_route():
    try:
        data       = request.json
        resume_url = data.get("resume_url")
        print("Parsing resume from: " + str(resume_url))

        if not resume_url:
            return jsonify({"error": "No resume URL provided"}), 400

        filename  = resume_url.split("/uploads/")[-1]
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print("File path: " + file_path)

        if not os.path.exists(file_path):
            print("File not found at: " + file_path)
            return jsonify({
                "error": "Resume file not found",
                "path":  file_path
            }), 404

        result = parse_resume(file_path)

        return jsonify({
            "success": True,
            "skills":  result["skills"],
            "email":   result["email"],
            "phone":   result["phone"],
            "name":    result["name"]
        })

    except Exception as e:
        print("Parse resume error: " + str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data       = request.json
        student_id = data.get("student_id")
        print("Looking for student_id: " + str(student_id))

        all_students = list(db.students.find())
        print("Total students in DB: " + str(len(all_students)))

        student = None
        student = db.students.find_one({"userId": student_id})

        if not student:
            for s in all_students:
                if str(s.get("userId")) == str(student_id):
                    student = s
                    break

        if not student and all_students:
            student = all_students[0]

        if not student:
            student = {
                "skills":    ["Python", "React", "Data Science"],
                "interests": ["Web Development", "AI"],
                "degree":    "BTech CSE",
                "location":  "Chennai"
            }

        student_profile = {
            "skills":    " ".join(student.get("skills",    [])),
            "interests": " ".join(student.get("interests", [])),
            "degree":    student.get("degree",   "BTech"),
            "location":  student.get("location", "Chennai")
        }

        print("Using profile: " + str(student_profile))

        internships = list(db.internships.find())
        if not internships:
            internships = get_sample_internships()

        recommendations = get_recommendations(student_profile, internships)

        return jsonify({
            "success":         True,
            "student":         student_profile,
            "recommendations": parse_json(recommendations[:10])
        })

    except Exception as e:
        print("Error: " + str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("AI Engine starting on port " + str(port))
    app.run(host="0.0.0.0", port=port, debug=False)
