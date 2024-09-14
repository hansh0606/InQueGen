import React, { useState } from 'react';
import axios from 'axios';
import './ResumeUpload.css';

function ResumeUpload({ setQuestions }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState(""); // For displaying success or error messages

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setMessage(""); // Clear any previous message
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('resume', selectedFile);
    
    try {
      const response = await axios.post('http://127.0.0.1:5000/upload_resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          
        },
      });

      if (response.data.error) {
        setMessage(response.data.error);
      } else {
        // Split the response result into individual questions
        const questions = response.data.result.split('\n').filter(question => question.trim() !== '');
        setQuestions(questions);
        setMessage("File submitted successfully.");
      }
    } catch (error) {
      console.error('Error uploading the file:', error);
      setMessage("There was an error submitting the file. Please try again.");
    }
  };

  return (
    <section className="resume-upload-section">
      <div className="description-container">
        <h2>Build Questions from Your Resume</h2>
        <p>
          Upload your resume to automatically generate interview questions tailored to your experience.
          Our tool analyzes your resume to create questions that reflect your skills and strengths.
        </p>
        <p>
          Focus on key areas with customizable questions.
          Save time and prepare confidently with questions made just for you.
        </p>
      </div>
      <div className="image-container">
        <img src="/qa1.png" alt="Resume Upload" className="upload-image" />
      </div>
      <div className="upload-container">
      <input 
          type="file" 
          accept=".pdf, .doc, .docx, .txt" 
          id="resume-upload" 
          className="upload-input" 
          onChange={handleFileChange} 
          style={{ display: 'none' }} // Hide the input
        />
        <label htmlFor="resume-upload" className="upload-button">
          {selectedFile ? selectedFile.name : "Upload Resume"}
        </label>
        <button onClick={handleUpload} className="upload-button">
          Submit Resume
        </button>

        {message && <div className="message">{message}</div>}
      </div>
    </section>
  );
}

export default ResumeUpload;
