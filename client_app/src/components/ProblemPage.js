import React, { useRef, useEffect, useState } from 'react';
import * as monaco from 'monaco-editor';

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
    <div className="code-editor">
      <div ref={editorRef} style={{ height: '400px' }}></div>
      <div className="controls">
        <button onClick={runCode}>Run <i className="fas fa-play icon"></i></button>
        <button onClick={submitCode}>Submit</button>
      </div>
    </div>
  );
}

export default CodeEditor;