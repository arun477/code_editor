import React, { useRef, useEffect, useState } from 'react';
import * as monaco from 'monaco-editor';
import './problemPage.css';

function CodeEditor({ initialCode, problemId }) {
  const editorRef = useRef(null);
  const [code, setCode] = useState(initialCode);

  useEffect(() => {
    if (editorRef.current) {
      const editor = monaco.editor.create(editorRef.current, {
        value: code,
        language: 'python',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 14,
        tabSize: 4,
        insertSpaces: true,
        wordWrap: 'on'
      });

      editor.onDidChangeModelContent(() => {
        setCode(editor.getValue());
      });

      return () => editor.dispose();
    }
  }, [initialCode]);

  const runCode = () => {
    fetch('http://localhost:8000/run_code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, problem_id: problemId }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Run results:', data);
        // Handle the results, update TestCases component
      })
      .catch(error => console.error('Error running code:', error));
  };

  const submitCode = () => {
    fetch('http://localhost:8000/submit_code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, problem_id: problemId }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Submit results:', data);
        // Handle the results, update TestCases component
      })
      .catch(error => console.error('Error submitting code:', error));
  };

  return (
    <div>
      <div id="parent">
        <div id="descriptions">
          <h2 id="title"></h2>
          <div id="content"></div>
        </div>

        <div id="editor-container">
          <div id="editor-sub">
            {/* <div id="editor"></div> */}
            <div id='editor' ref={editorRef} ></div>
          </div>

          <div id="output-container">
            <div id="controls">
              <button id="run-btn">Run <i class="fas fa-play icon"></i></button>
              <button id="submit-btn">Submit</button>
            </div>

            <div id="test-cases-container">
              <div id="summary-bar">
                <span id="summary-text">Test Results</span>
                <button id="expand-all-btn">Expand All</button>
              </div>
              <div id="test-cases"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CodeEditor;