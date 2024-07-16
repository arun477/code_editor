import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import Styles from './problemList.module.css'
import Loader from './Loader';
import { useParams } from 'react-router-dom'

function ProblemList() {
  const { id } = useParams();
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [meta, setMeta] = useState({})


  async function getProblems() {
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
  }


  async function getModuleMeta() {
    try {
      const response = await fetch(`http://localhost:8000/get-module`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ module_id: id }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setMeta(data || {})

    } catch (err) {
      console.log(err);
    }
  }

  useEffect(() => {
    getModuleMeta();
    getProblems();
  }, []);

  if (loading) return <div><Loader /></div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className={Styles.parent}>
      <div className={Styles.heading}>
        <div>
          <img
            style={{
              width: "98px",
              height: "57px",
              borderRadius: "7px",
            }}
            src={'http://localhost:8000/' + meta?.banner_img} alt={meta?.banner_title} className="banner-img" />
        </div>
        <div style={{display:'flex', flexDirection:'column', marginLeft: '10px'}}>
          <h3 style={{margin:0}}>{meta?.banner_title}</h3>
          <p style={{
            fontSize: "12px",
            margin: "0px",
            color: "666",
            fontWeight: "normal"
          }}>{meta?.banner_description}</p>
        </div>

      </div>

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
