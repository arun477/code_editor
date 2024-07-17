import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import CodeEditor from './CodeEditor';
import TestCases from './TestCases';
import './problemPage.css';
import Loader from './Loader';
import ProblemTab from './ProblemTab';

function ProblemPage() {
    const { id } = useParams();
    const [problem, setProblem] = useState(null);
    const [content, setContent] = useState('');
    const [loading, setLoading] = useState(true);
    const [contentLoading, setContentLoading] = useState(false);
    const [error, setError] = useState(null);
    const [testResults, setTestResults] = useState(null);
    const [activeLang, setActiveLang] = useState('en');

    async function getLangSpecificDescription(lang) {
        setContentLoading(true);
        try {
            const response = await fetch(`http://localhost:8000/available_langs/${lang}/${id}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            let data = await response.json();
            setContent(data?.content || '');
        } catch (err) {
            console.log(err);
        }
        setContentLoading(false);
    }

    const handleChange = (newLang) => {
        if (newLang === activeLang) {
            return;
        }
        setActiveLang(newLang);
        getLangSpecificDescription(newLang);
    };

    useEffect(() => {
        fetch(`http://localhost:8000/get_problem/${id}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                setProblem(data);
                setContent(data?.content);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching problem:', error);
                setError(error.message);
                setLoading(false);
            });
    }, [id]);

    if (loading)
        return (
            <div>
                <Loader />
            </div>
        );
    if (error) return <div>Error: {error}</div>;
    if (!problem) return <div>No problem found</div>;

    return (
        <div>
            <div id="parent">
                <div id="descriptions">
                    <ProblemTab
                        handleChange={handleChange}
                        activeLang={activeLang}
                        problemId={id}
                    />
                    {!contentLoading ? (
                        <div>
                            <h2 id="title">{problem.title}</h2>
                            <div
                                id="content"
                                dangerouslySetInnerHTML={{ __html: content }}
                                style={{ fontSize: '14px' }}
                            ></div>
                        </div>
                    ) : (
                        <Loader />
                    )}
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
    );
}

export default ProblemPage;
