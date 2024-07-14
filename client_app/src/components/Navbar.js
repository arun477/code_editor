import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav>
      <Link to="/">
        <img src="/assets/logo.png" alt="Logo" style={{ width: '40px', height: '40px' }} />
      </Link>
    </nav>
  );
}

export default Navbar;