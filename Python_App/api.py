from flask import Flask, request, jsonify
from app import extract_text_from_pdf, extract_technical_keywords, generate_interview_questions
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_resume', methods=['POST'])  # Ensure POST method is allowed
def upload_resume():
    print("Upload endpoint hit")  # Confirm the endpoint is reached

    if 'resume' not in request.files:
        print("No file part in request")
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['resume']

    if file.filename == '':
        print("No selected file")
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        print("File type not allowed")
        return jsonify({"error": "File type not allowed"}), 400

    # File received
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    print(f"Saving file to {file_path}")
    file.save(file_path)

    # Extract text and keywords
    resume_text = extract_text_from_pdf(file_path)
    print(f"Extracted text from PDF: {resume_text[:200]}")  # Print the first 200 characters for debugging

    keywords = extract_technical_keywords(resume_text)
    print(f"Extracted keywords: {keywords}")

    questions = generate_interview_questions(keywords)
    print(f"Generated questions: {questions}")

    return jsonify({
        "keywords": keywords,
        "questions": questions.get('result', [])
    })

if __name__ == '__main__':
    app.run(debug=True)
