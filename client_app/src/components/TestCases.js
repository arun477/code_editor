import React, { useState } from 'react';
import './problemPage.css';

function TestCases({ testCases }) {
  testCases = testCases || [];
  const [expandedCases, setExpandedCases] = useState([]);

  const toggleTestCase = (index) => {
    setExpandedCases(prev => 
      prev.includes(index) 
        ? prev.filter(i => i !== index)
        : [...prev, index]
    );
  };

  const toggleAllTestCases = () => {
    setExpandedCases(prev => 
      prev.length === testCases.length ? [] : testCases.map((_, i) => i)
    );
  };

  return (
    <div id="test-cases-container">
    <div id="summary-bar">
      <span id="summary-text">Test Results</span>
      <button id="expand-all-btn">Expand All</button>
    </div>
    <div id="test-cases"></div>
  </div>
  )

  return (
    <div className="test-cases">
      <div className="summary-bar">
        <span>Test Results</span>
        <button onClick={toggleAllTestCases}>
          {expandedCases.length === testCases.length ? 'Collapse All' : 'Expand All'}
        </button>
      </div>
      {testCases.map((testCase, index) => (
        <div key={index} className="test-case">
          <div className="test-case-summary" onClick={() => toggleTestCase(index)}>
            <span className="test-case-number">Test {index + 1}</span>
            <span className={`test-case-status ${testCase.valid ? 'success' : 'error'}`}>
              {testCase.valid ? 'Passed' : 'Failed'}
            </span>
            <span className="test-case-input">{JSON.stringify(testCase.input)}</span>
          </div>
          {expandedCases.includes(index) && (
            <div className="test-case-details">
              <pre><strong>Input:</strong> {JSON.stringify(testCase.input, null, 2)}</pre>
              <pre><strong>Expected Output:</strong> {JSON.stringify(testCase.expected, null, 2)}</pre>
              <pre><strong>Actual Output:</strong> {JSON.stringify(testCase.output, null, 2)}</pre>
              {testCase.std_err && <pre className="error"><strong>Error:</strong> {testCase.std_err}</pre>}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default TestCases;