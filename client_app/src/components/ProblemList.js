import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import Styles from './problemList.module.css'
import Loader from './Loader';

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

  if (loading) return <div><Loader /></div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className={Styles.parent}>
      <h3 className={Styles.heading}>Common Algorithmic Problems</h3>
      <ul className={Styles.list}>
        {problems.map(problem => (
          <li className={Styles.listItem} key={problem.questionId}>
            <Link className={Styles.link} to={`/problem/${problem.questionId}`}>
              <i className="fas fa-star icon"></i>
              <FontAwesomeIcon icon={faStar} className={Styles.icon} />
              {problem.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProblemList;
