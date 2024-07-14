import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProblemList from './components/ProblemList';
import ProblemPage from './components/ProblemPage';

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<ProblemList />} />
        <Route path="/problem/:id" element={<ProblemPage />} />
      </Routes>
    </div>
  );
}

export default App;