import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function ProblemList() {
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/all_problems')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setProblems(data.problems);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching problems:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h3>Common Algorithmic Problems</h3>
      <ul>
        {problems.map(problem => (
          <li key={problem.questionId}>
            <Link to={`/problem/${problem.questionId}`}>
              <i className="fas fa-star icon"></i>
              {problem.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProblemList;
