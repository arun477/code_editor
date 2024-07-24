import React from 'react';
import { Link } from 'react-router-dom';
import Styles from  './navbar.module.css';
import {useAuth} from '../contexts/AuthContext'

function Navbar() {
  const {logout, user} = useAuth()
  const handleLogout = () => {
   logout();
  }
  return (
    <nav className={Styles.navbar}>
      <Link className={Styles.link}  to="/">
        <img className={Styles.logo} src="/assets/logo.png" alt="Logo" />
      </Link>
      {user?<button className={Styles.logoutBtn} onClick={handleLogout}>logout</button>:null}
    </nav>
  );
}

export default Navbar;