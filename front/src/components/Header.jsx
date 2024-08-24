import React from 'react'
import './Header.css'
import logo from '../img/logo.svg'
const Header = () => {
    return (
        <nav className="navbar">
            <img src={logo} alt="logo" />
            <h2>Pastebin</h2>
            <a href="#"><h2>О нас</h2></a>
        </nav>
    );
}

export default Header