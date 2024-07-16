import React from 'react';

const ProblemTab = ({ handleChange, activeLang }) => {
    const options = ['en', 'ta', 'hi'];

    const containerStyle = {
        display: 'flex',
        alignItems: 'center',
        borderRadius: '12px',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
        marginBottom: '20px'
    };

    const innerContainerStyle = {
        background: 'white',
        padding: '4px',
        borderRadius: '8px',
        boxShadow: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    };

    const buttonStyle = (isActive) => ({
        position: 'relative',
        padding: '5px 10px',
        margin: '4px',
        borderRadius: '6px',
        fontSize: '13px',
        fontWeight: 'bold',
        color: isActive ? 'white' : '#4b5563',
        transition: 'all 0.3s ease',
        cursor: 'pointer',
        border: 'none',
        outline: 'none',
        background: 'none',
    });

    const activeButtonStyle = {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'linear-gradient(to right, #1a0036, #043e1d)',
        borderRadius: '4px',
        zIndex: 0,
    };

    const getLanguageName = (lang) => {
        switch (lang) {
            case 'en': return 'English';
            case 'ta': return 'தமிழ்';
            case 'hi': return 'हिन्दी';
            default: return lang;
        }
    };

    return (
        <div style={containerStyle}>
            <div style={innerContainerStyle}>
                {options.map((lang) => (
                    <button
                        key={lang}
                        style={buttonStyle(activeLang === lang)}
                        onClick={() => handleChange(lang)}
                    >
                        {activeLang === lang && <div style={activeButtonStyle} />}
                        <span style={{ position: 'relative', zIndex: 1 }}>
                            {getLanguageName(lang)}
                        </span>
                    </button>
                ))}
            </div>
        </div>
    );
};

export default ProblemTab;