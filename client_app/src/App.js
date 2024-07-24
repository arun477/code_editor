import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProblemList from './components/ProblemList';
import ProblemPage from './components/ProblemPage';
import Collections from './components/Collections';
import EditProblem from './components/admin/EditProblem';
import Login from './components/Login';
import Register from './components/Register';
import { AuthProvider, ProtectedRoute } from './contexts/AuthContext';

function App() {
    return (
        <AuthProvider>
            <Navbar />
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route
                    path="/"
                    element={
                        <ProtectedRoute>
                            <Collections />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/admin/edit-problem/:id"
                    element={
                        <ProtectedRoute>
                            <EditProblem />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/module/:id"
                    element={
                        <ProtectedRoute>
                            <ProblemList />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/problem/:id"
                    element={
                        <ProtectedRoute>
                            <ProblemPage />
                        </ProtectedRoute>
                    }
                />
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </AuthProvider>
    );
}

export default App;
