import React, { useState } from 'react';
import Header from './components/Header';
import ResumeUpload from './components/ResumeUpload';
import QuestionList from './components/QuestionList';
import QuestionEditor from './components/QuestionEditor';
import Footer from './components/Footer';
import './App.css';

function App() {
  const [questions, setQuestions] = useState([]);

  return (
    <div className="app-container">
      <Header />
      <main>
        <ResumeUpload setQuestions={setQuestions} />
        <QuestionList questions={questions} />
        <QuestionEditor />
      </main>
      <Footer />
    </div>
  );
}

export default App;
