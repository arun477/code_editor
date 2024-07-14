import React from 'react';
import { Link } from 'react-router-dom';
import Styles from  './navbar.module.css';

function Navbar() {
  return (
    <nav className={Styles.navbar}>
      <Link className={Styles.link}  to="/">
        <img className={Styles.logo} src="/assets/logo.png" alt="Logo" />
      </Link>
    </nav>
  );
}

export default Navbar;