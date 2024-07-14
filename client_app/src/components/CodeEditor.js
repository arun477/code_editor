import React, { useRef, useEffect, useState } from 'react';
import * as monaco from 'monaco-editor';
import './problemPage.css';

function CodeEditor({ initialCode, problemId, onTestResultsUpdate }) {
  const editorRef = useRef(null);
  const [code, setCode] = useState(initialCode);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (editorRef.current) {
      const editor = monaco.editor.create(editorRef.current, {
        value: code,
        language: 'python',
        theme: 'vs-dark',
        automaticLayout: false,
        minimap: { enabled: false },
        fontSize: 14,
        tabSize: 4,
        insertSpaces: true,
        wordWrap: 'on',
        layout: {
          width: '100%',
          height: '100%'
        },
      });

      editor.onDidChangeModelContent(() => {
        setCode(editor.getValue());
      });

      return () => editor.dispose();
    }
  }, [initialCode]);

  const runOrSubmitCode = async (endpoint) => {
    if (isRunning) return;
    setIsRunning(true);
    onTestResultsUpdate({ loading: true });

    try {
      const response = await fetch(`http://localhost:8000/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, problem_id: problemId }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      if (data.job_id) {
        await checkJobStatus(data.job_id, endpoint);
      } else {
        throw new Error('No job ID received from server');
      }
    } catch (error) {
      console.error(`Error ${endpoint}:`, error);
      onTestResultsUpdate({ error: `${error.message}` });
    } finally {
      setIsRunning(false);
    }
  };

  const checkJobStatus = async (jobId, endpoint) => {
    const maxAttempts = 25;
    const delay = 1000; // 1 second

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        const response = await fetch('http://localhost:8000/check/status', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ job_id: jobId }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
          throw new Error(data.error);
        }

        if (data.status === 'done') {
          if (endpoint === 'run_code') {
            if (data.result && data.result.outputs && data.result.outputs.results) {
              onTestResultsUpdate(data.result.outputs.results);
            } else {
              throw new Error(data.result.error);
            }
          } else {
            if (data.result && data.result.output) {
              onTestResultsUpdate(data.result.output);
            } else {
              throw new Error(data.result.error);
            }
          }
          return;
        }

        if (attempt < maxAttempts) {
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      } catch (error) {
        console.error("Error fetching job status:", error);
        throw error;
      }
    }

    throw new Error('Job timed out');
  };

  return (
    <div>
      <div id="editor-sub">
        <div ref={editorRef} style={{ height: '400px' }}></div>
      </div>
      <div>
        <div id="controls">
          <button id="run-btn" onClick={() => runOrSubmitCode('run_code')} disabled={isRunning}>
            Run <i className="fas fa-play icon"></i>
          </button>
          <button id="submit-btn" onClick={() => runOrSubmitCode('submit_code')} disabled={isRunning}>
            Submit
          </button>
        </div>
      </div>
    </div>
  );
}

export default CodeEditor;