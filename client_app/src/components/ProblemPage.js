import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import CodeEditor from './CodeEditor';
import TestCases from './TestCases';
import './problemPage.css'
import Loader from './Loader';
import ProblemTab from './ProblemTab';

function ProblemPage() {
  const { id } = useParams();
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [testResults, setTestResults] = useState(null);
  const [activeLang, setActiveLang] = useState('en');
  const handleChange = (newLang) => {
    setActiveLang(newLang);
};

  useEffect(() => {
    fetch(`http://localhost:8000/get_problem/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setProblem(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching problem:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div>
    <Loader />
  </div>;
  if (error) return <div>Error: {error}</div>;
  if (!problem) return <div>No problem found</div>;

  let content = ''
  if(activeLang==='en'){
    content = problem?.content
  } else if (activeLang==='ta'){
    content = problem?.content_ta
  }else if (activeLang==='hi'){
    content = problem?.content_hi
  }

  return (
    <div>
      <div id="parent">
        <div id="descriptions">
          <ProblemTab handleChange={handleChange} activeLang={activeLang}/>
          <h2 id="title">{problem.title}</h2>
          <div id="content" dangerouslySetInnerHTML={{ __html: content }} style={{fontSize:'14px'}}></div>
        </div>

        <div id="editor-container">
          <div>
            <CodeEditor 
              initialCode={problem.initial_code} 
              problemId={id} 
              onTestResultsUpdate={setTestResults} 
            />
            <TestCases testResults={testResults} />
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProblemPage;