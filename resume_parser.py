import pdfplumber
import re

SKILL_KEYWORDS = [
    "python", "java", "javascript", "c++", "c#", "ruby", "php",
    "swift", "kotlin", "typescript", "golang", "rust", "scala",
    "react", "angular", "vue", "node.js", "express", "django", "flask",
    "html", "css", "bootstrap", "tailwind", "jquery",
    "machine learning", "deep learning", "data science",
    "artificial intelligence", "tensorflow", "pytorch", "keras",
    "scikit-learn", "pandas", "numpy", "matplotlib", "nlp",
    "sql", "mysql", "postgresql", "mongodb", "firebase", "redis",
    "aws", "azure", "google cloud", "docker", "kubernetes",
    "git", "linux", "excel", "power bi", "tableau",
    "android", "ios", "flutter", "cyber security", "networking",
    "data analysis", "statistics", "r programming", "hadoop", "spark"
]

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
        print("Extracted text length: " + str(len(text)))
        return text.lower()
    except Exception as e:
        print("PDF read error: " + str(e))
        return ""

def extract_skills_from_text(text):
    found_skills = []
    text_lower = text.lower()
    for skill in SKILL_KEYWORDS:
        if skill.lower() in text_lower:
            found_skills.append(skill.title())
    print("Skills found: " + str(found_skills))
    return found_skills

def extract_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else ""

def extract_phone(text):
    phone_pattern = r'\b[6-9]\d{9}\b'
    phones = re.findall(phone_pattern, text)
    return phones[0] if phones else ""

def extract_name(text):
    lines = text.strip().split("\n")
    for line in lines[:5]:
        line = line.strip()
        if len(line) > 2 and len(line) < 40:
            if not any(char.isdigit() for char in line):
                if "@" not in line and "http" not in line:
                    return line.title()
    return ""

def parse_resume(pdf_path):
    print("Parsing resume: " + pdf_path)
    text = extract_text_from_pdf(pdf_path)

    if not text:
        return {
            "skills":   [],
            "email":    "",
            "phone":    "",
            "name":     "",
            "raw_text": ""
        }

    skills = extract_skills_from_text(text)
    email  = extract_email(text)
    phone  = extract_phone(text)
    name   = extract_name(text)

    return {
        "skills":   skills,
        "email":    email,
        "phone":    phone,
        "name":     name,
        "raw_text": text[:500]
    }
