import React from 'react';
import { Link } from 'react-router-dom';

function Header({ handleNavigation }) {
    return (
        <header>
            <div className="lhs">
                <div className="logo">
                    <img src={require("./assets/GEHCLOGO.png")} alt="LOGO" className="logo" />
                </div>
                {/* <span>Product</span>
                <span>About Us</span> */}
                <Link to="/" onClick={() => handleNavigation('/')}>Home Page</Link>
                <Link to="/home" onClick={() => handleNavigation('/home')}>Database Select</Link>
                <Link to="/admin" onClick={() => handleNavigation('/admin')}>Admin Page</Link>
                {/* Add more Links as needed */}
            </div>
            <div className="rhs">
                <button className="try-now-btn">
                    <span>Try Now</span>
                </button>
            </div>
        </header>
    );
}

export default Header;
