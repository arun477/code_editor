import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProblemList from './components/ProblemList';
import ProblemPage from './components/ProblemPage';
import Collections from './components/Collections';
import EditProblem from './components/admin/EditProblem';

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Collections />} />
        <Route path="/admin/edit-problem/:id" element={<EditProblem />} />
        <Route path="/module/:id" element={<ProblemList />} />
        <Route path="/problem/:id" element={<ProblemPage />} />
      </Routes>
    </div>
  );
}

export default App;