import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useApi } from '../utils/api';
import './login.css';
import Loader from './Loader';

const Login = () => {
    const [email, setEmail] = useState('');
    const [loading, setLoading] = useState(false);
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [showRegisterPrompt, setShowRegisterPrompt] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();
    const { login, user } = useAuth();
    const { callApi } = useApi();

    useEffect(() => {
        if (user) {
            navigate('/');
        }
    }, [user, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setShowRegisterPrompt(false);
        if(loading){
            return
        }

        try {
            setLoading(true)
            const data = await callApi('/login', {
                method: 'POST',
                body: JSON.stringify({ email, password }),
            });

            login(data.access_token);
            const origin = location.state?.from?.pathname || '/';
            navigate(origin);
        } catch (error) {
            console.error('Error:', error);
            if (error.message === 'Invalid credentials') {
                setError('Invalid email or password.');
                setShowRegisterPrompt(true);
            } else {
                setError(error.message || 'Login failed');
            }
        }
        setLoading(false)
    };

    return (
        <div className="loginContainer">
            <form onSubmit={handleSubmit} className="loginForm">
                <h2 className="loginTitle">Welcome Back!</h2>
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
                       {!loading? "Sign In":<Loader width={35} height={35} />}
                    </button>
                </div>
                {true && (
                    <p className="registerPrompt">
                        Don't have an account?{' '}
                        <Link to="/register" className="register-link">
                            Register here
                        </Link>
                    </p>
                )}
                {error && <p className="loginError">{error}</p>}
               
            </form>
        </div>
    );
};

export default Login;
