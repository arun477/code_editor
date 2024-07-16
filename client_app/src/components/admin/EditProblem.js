import React, { useState, useEffect, useRef } from 'react';
import JSONEditor from 'jsoneditor';
import { Editor } from '@monaco-editor/react';
import MarkdownIt from 'markdown-it';
import MdEditor from 'react-markdown-editor-lite';

import 'jsoneditor/dist/jsoneditor.min.css';
import 'react-markdown-editor-lite/lib/index.css';
import './editProblem.css';

const mdParser = new MarkdownIt({ html: true });

const ProblemEditor = () => {
    const [problemId, setProblemId] = useState('');
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [initialCode, setInitialCode] = useState('');
    const [validationCode, setValidationCode] = useState('');
    const [testCases, setTestCases] = useState('[]');
    const [message, setMessage] = useState({ text: '', type: '' });
    const [loading, setLoading] = useState(false);

    const jsonEditorRef = useRef(null);
    const jsonEditorInstanceRef = useRef(null);
    const _ROOT_URL = 'http://localhost:8000';

    useEffect(() => {
        let id = window.location.pathname.split('/').pop()
        setProblemId(id);
        fetchProblemData(id);

        return () => {
            if (jsonEditorInstanceRef.current) {
                jsonEditorInstanceRef.current.destroy();
            }
        };
    }, []);

    useEffect(() => {
        if (jsonEditorRef.current && !jsonEditorInstanceRef.current) {
            const options = {
                mode: 'code',
                onValidationError: (errors) => {
                    if (errors.length > 0) {
                        showMessage('Invalid JSON in Test Cases. Please correct it.', 'error');
                    }
                },
            };
            jsonEditorInstanceRef.current = new JSONEditor(jsonEditorRef.current, options);
        }
    }, [jsonEditorRef]);

    const fetchProblemData = async (id) => {
        try {
            id = id || problemId
            const response = await fetch(`${_ROOT_URL}/get_problem/${id}`);
            const data = await response.json();
            setTitle(data.title || '');
            setContent(data.content || '');
            setInitialCode(data.initial_code || '');
            setValidationCode(data.validation_func || '');
            jsonEditorInstanceRef.current.set(JSON.parse(data.test_cases) || []);
        } catch (error) {
            console.error('Error fetching problem data:', error);
            showMessage('Failed to load problem data. Please try refreshing the page.', 'error');
        }
    };

    const showMessage = (text, type) => {
        setMessage({ text, type });
        setTimeout(() => setMessage({ text: '', type: '' }), 5000);
    };

    const validateInputs = () => {
        if (!title) {
            showMessage('Please enter a title for the problem.', 'error');
            return false;
        }
        if (!content) {
            showMessage('Please enter a description for the problem.', 'error');
            return false;
        }
        if (!initialCode) {
            showMessage('Please enter initial code for the problem.', 'error');
            return false;
        }
        if (!validationCode) {
            showMessage('Please enter validation code for the problem.', 'error');
            return false;
        }
        const testCasesJson = jsonEditorInstanceRef.current.get();
        if (!testCasesJson || testCasesJson.length === 0) {
            showMessage('Please enter at least one test case for the problem.', 'error');
            return false;
        }
        return true;
    };

    const saveProblem = async () => {
        if (!validateInputs()) return;

        const updatedProblem = {
            title,
            content,
            initial_code: initialCode,
            validation_func: validationCode,
            test_cases: JSON.stringify(jsonEditorInstanceRef.current.get()),
        };

        setLoading(true);

        try {
            const response = await fetch(`${_ROOT_URL}/admin/update-problem/${problemId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedProblem),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw errorData;
            }

            const data = await response.json();
            showMessage(data.message, 'success');
            fetchProblemData();
        } catch (error) {
            console.error('Error:', error);
            if (error.detail && Array.isArray(error.detail)) {
                const errorMessages = error.detail.map((err) => (
                    `<li class="error-item">
            <span class="error-location">${err.loc.join(' > ')}</span>: ${err.msg}
          </li>`
                )).join('');
                showMessage(`<ul class="error-list">${errorMessages}</ul>`, 'error');
            } else {
                showMessage('Failed to update the problem. Please try again.', 'error');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleEditorChange = ({ text }) => {
        setContent(text);
    };

    return (
        <div className="problem-editor">

            <div className="parent">
                <div className="section">
                    <h2 className="section-title">Title</h2>
                    <input
                        id="title"
                        type="text"
                        placeholder="Enter problem title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                    />
                </div>

                <div className="section">
                    <h2 className="section-title">Description</h2>
                    <MdEditor
                        value={content}
                        style={{ height: '400px' }}
                        renderHTML={(text) => mdParser.render(text)}
                        onChange={handleEditorChange}
                        placeholder="Enter problem description here..."
                    />
                </div>

                <div className="section">
                    <h2 className="section-title">Initial Code</h2>
                    <p className="section-note">
                        This is what the user will see before starting their problem. The system will pass
                        the Solution class to the Validation class during execution.
                    </p>
                    <div className="editor-code-container">
                        <Editor
                            height="300px"
                            defaultLanguage="python"
                            theme="vs-dark"
                            value={initialCode}
                            onChange={setInitialCode}
                            options={{
                                minimap: { enabled: false },
                                fontSize: 14,
                                tabSize: 4,
                                insertSpaces: true,
                                wordWrap: 'on',
                            }}
                        />
                    </div>
                </div>

                <div className="section">
                    <h2 className="section-title">Validation Code</h2>
                    <p className="section-note">
                        This code validates the user's solution. Solution and Validation classes are
                        required. The system will pass the Solution class to the Validation class during execution. The
                        Validation class should return a tuple: (boolean indicating pass/fail, return value if any).
                    </p>
                    <div className="editor-code-container">
                        <Editor
                            height="300px"
                            defaultLanguage="python"
                            theme="vs-dark"
                            value={validationCode}
                            onChange={setValidationCode}
                            options={{
                                minimap: { enabled: false },
                                fontSize: 14,
                                tabSize: 4,
                                insertSpaces: true,
                                wordWrap: 'on',
                            }}
                        />
                    </div>
                </div>

                <div className="section">
                    <h2 className="section-title">Test Cases</h2>
                    <div ref={jsonEditorRef} className="jsoneditor" />
                </div>

                <div className="controls">
                    <button className="save-btn" onClick={saveProblem} disabled={loading}>
                        Save Changes
                    </button>
                    {loading && <div className="loading-indicator">Saving...</div>}
                </div>
                {message.text && (
                    <div className={`message ${message.type}`} dangerouslySetInnerHTML={{ __html: message.text }} />
                )}
            </div>
        </div>
    );
};

export default ProblemEditor;