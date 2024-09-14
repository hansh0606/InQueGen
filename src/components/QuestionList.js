import React from 'react';

function QuestionList({ questions }) {
  return (
    <section>
      <h2>Generated Questions</h2>
      <ul>
        {questions.map((question, index) => (
          <li key={index}>{question}</li>
        ))}
      </ul>
    </section>
  );
}

export default QuestionList;
