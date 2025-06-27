import React from 'react'
import './Header.css'
import logo from '../img/logo.svg'
const Header = () => {
    return (
        <div className="header">
            <nav className="navbar">
                <img src={logo} alt="logo" />
                <a href="#"><h2>Pastebin</h2></a>
                <a href="#"><h2>О нас</h2></a>
            </nav>
            <div className="authorization">
                <a class="btn btn-login">
                    Вход
                </a>
                <a class="btn btn-login">
                    Регистрация
                </a>
            </div>
        </div>
    );
}

export default Header