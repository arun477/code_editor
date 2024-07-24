import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Loader from './Loader';

const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [showLoginPrompt, setshowLoginPrompt] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const registerResponse = await fetch('http://localhost:8000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password,
                }),
            });

            if (registerResponse.ok) {
                // Registration successful, now log in
                const loginResponse = await fetch('http://localhost:8000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email,
                        password,
                    }),
                });

                if (loginResponse.ok) {
                    const data = await loginResponse.json();
                    login(data.access_token);
                    navigate('/');
                } else {
                    setError('Registration successful, but login failed. Please try logging in.');
                }
            } else {
                const errorData = await registerResponse.json();
                setError(errorData.detail || 'Registration failed');
                setshowLoginPrompt(true);
            }
        } catch (error) {
            console.error('Error:', error);
            setError('An unexpected error occurred');
        }
    };

    return (  <div className="loginContainer">
        <form onSubmit={handleSubmit} className="loginForm">
            <h2 className="loginTitle">Register</h2>
            <div className="formGroup">
                <label htmlFor="email" className="formLabel">
                    Email
                </label>
                <input
                    id="email"
                    type="email"
                    placeholder=""
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="formInput"
                />
            </div>
            <div className="formGroup">
                <label htmlFor="password" className="formLabel">
                    Password
                </label>
                <input
                    id="password"
                    type="password"
                    placeholder=""
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="formInput"
                />
            </div>
            <div className="form-actions">
                <button type="submit" className={!loading?"loginButton": "loginButton loginButtonLoading"}>
                   {!loading? "Register":<Loader width={35} height={35} />}
                </button>
            </div>
            {error && <p className="loginError">{error}</p>}
            {true && (
                <p className="registerPrompt">
                    Already have an account?{' '}
                    <Link to="/login" className="register-link">
                        Login here
                    </Link>
                </p>
            )}
        </form>
    </div>)

    return (
        <div className="max-w-md mx-auto mt-8">
            <form
                onSubmit={handleSubmit}
                className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
            >
                <h2 className="text-2xl mb-4">Register</h2>
                {error && <p className="text-red-500 mb-4">{error}</p>}
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                        Email
                    </label>
                    <input
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        id="email"
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-6">
                    <label
                        className="block text-gray-700 text-sm font-bold mb-2"
                        htmlFor="password"
                    >
                        Password
                    </label>
                    <input
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                        id="password"
                        type="password"
                        placeholder="******************"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <div className="flex items-center justify-between">
                    <button
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        type="submit"
                    >
                        Register
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Register;