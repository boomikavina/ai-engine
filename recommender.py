from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_recommendations(student_profile, internships):
    """
    student_profile = {
        skills: "Python React SQL",
        interests: "Data Science Web Dev"
    }
    internships = [
        { title, company, skills_required, description }
    ]
    """

    # Step 1 — combine student skills and interests into one text
    student_text = (
        student_profile.get("skills", "") + " " +
        student_profile.get("interests", "") + " " +
        student_profile.get("degree", "") + " " +
        student_profile.get("location", "")
    ).lower()

    print(f"Student text: {student_text}")

    # Step 2 — combine each internship into one text
    internship_texts = []
    for internship in internships:
        text = (
            internship.get("title", "") + " " +
            internship.get("skills_required", "") + " " +
            internship.get("description", "") + " " +
            internship.get("location", "") + " " +
            internship.get("sector", "")
        ).lower()
        internship_texts.append(text)

    # Step 3 — if no internships found return empty
    if not internship_texts:
        return []

    # Step 4 — combine student text with all internship texts
    all_texts = [student_text] + internship_texts

    # Step 5 — TF-IDF converts text to numbers
    # TF-IDF = Term Frequency Inverse Document Frequency
    # It finds which words are most important
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Step 6 — Cosine Similarity compares student vector
    # with each internship vector
    # Result is a number between 0 and 1
    # 1 = perfect match, 0 = no match
    student_vector    = tfidf_matrix[0]
    internship_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(student_vector, internship_vectors)[0]

    # Step 7 — add match score to each internship
    results = []
    for i, internship in enumerate(internships):
        score = round(float(similarities[i]) * 100, 1) # convert to percentage
        results.append({
            **internship,
            "match_score": score
        })

    # Step 8 — sort by highest match score first
    results.sort(key=lambda x: x["match_score"], reverse=True)

    print(f"Top match: {results[0]['title']} - {results[0]['match_score']}%")

    return results