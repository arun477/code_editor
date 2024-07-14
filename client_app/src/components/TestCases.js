import React, { useState, useEffect } from 'react';
import './problemPage.css';

function TestCases({ testResults }) {
  const [expandedCases, setExpandedCases] = useState([]);

  useEffect(() => {
    setExpandedCases([]);
  }, [testResults]);

  const toggleTestCase = (index) => {
    setExpandedCases(prev => 
      prev.includes(index) 
        ? prev.filter(i => i !== index)
        : [...prev, index]
    );
  };

  const toggleAllTestCases = () => {
    if (!Array.isArray(testResults)) return;
    setExpandedCases(prev => 
      prev.length === testResults.length ? [] : testResults.map((_, i) => i)
    );
  };

  const updateExpandAllButton = () => {
    if (!Array.isArray(testResults)) return 'Expand All';
    return expandedCases.length === testResults.length ? 'Collapse All' : 'Expand All';
  };

  if (!testResults) {
    return null;
  }

  if (testResults.loading) {
    return (
      <div id="test-cases-container">
        <div id="summary-bar">
          <span id="summary-text">Running...</span>
        </div>
        <div id="test-cases">
          <div style={{padding: '10px'}}>Running...</div>
        </div>
      </div>
    );
  }

  if (testResults.error) {
    return (
      <div id="test-cases-container">
        <div id="summary-bar">
          <span id="summary-text">Test Results</span>
        </div>
        <div id="test-cases">
          <div className="error">{testResults.error}</div>
        </div>
      </div>
    );
  }

  // Handle submission results
  if (testResults.passed !== undefined) {
    const allPassed = testResults.passed === testResults.total;
    return (
      <div id="test-cases-container">
        <div id="summary-bar">
          <span id="summary-text" style={{ color: allPassed ? 'var(--success-color)' : 'var(--error-color)' }}>
            {allPassed ? 'All Passed!' : `${testResults.passed}/${testResults.total} Passed`}
          </span>
        </div>
      </div>
    );
  }

  // Handle run results
  if (Array.isArray(testResults)) {
    const passedTests = testResults.filter(result => result.valid).length;

    return (
      <div id="test-cases-container">
        <div id="summary-bar">
          <span id="summary-text">
            {`${passedTests}/${testResults.length} Test Cases Passed`}
          </span>
          <button id="expand-all-btn" onClick={toggleAllTestCases}>
            {updateExpandAllButton()}
          </button>
        </div>
        <div id="test-cases">
          {testResults.map((result, index) => (
            <div key={index} className="test-case">
              <div 
                className={`test-case-summary ${expandedCases.includes(index) ? 'expanded' : ''}`} 
                onClick={() => toggleTestCase(index)}
              >
                <span className="test-case-number">Test {index + 1}</span>
                <span className={`test-case-status ${result.valid ? 'success' : 'status-error'}`}>
                  {result.valid ? 'Passed' : 'Failed'}
                </span>
                <span className="test-case-input">{JSON.stringify(result.input)}</span>
              </div>
              <div className="test-case-details" style={{display: expandedCases.includes(index) ? 'block' : 'none'}}>
                <pre><strong>Input:</strong> {JSON.stringify(result.input, null, 2)}</pre>
                <pre><strong>Expected Output:</strong> {JSON.stringify(result.expected, null, 2)}</pre>
                <pre><strong>Actual Output:</strong> {JSON.stringify(result.output, null, 2)}</pre>
                {result.std_err && <pre className="error"><strong>Error:</strong> {result.std_err}</pre>}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Unexpected test results format
  return (
    <div id="test-cases-container">
      <div id="summary-bar">
        <span id="summary-text" className="error">Unexpected test results format</span>
      </div>
    </div>
  );
}

export default TestCases;