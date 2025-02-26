import React from 'react';
import { NavLink } from 'react-router-dom';
import { Row, Col } from 'react-bootstrap';
import '../../styles/Menu.css';

const Menu = ({ isOpen, closeMenu, isAdmin, isVendor, isUser }) => {
  return (
    <nav className={`menu ${isOpen ? 'open' : ''}`}>
      <Row className="menu-items">
        {isUser && (
          <>
            <Col xs={12} md={4}>
              <NavLink to="/user/home" onClick={closeMenu} className="menu-link">Home</NavLink>
            </Col>
            <Col xs={12} md={4}>
              <NavLink to="/user/scanner" onClick={closeMenu} className="menu-link">Scanner</NavLink>
            </Col>
            <Col xs={12} md={4}>
              <NavLink to="/user/history" onClick={closeMenu} className="menu-link">History</NavLink>
            </Col>
          </>
        )}
        {isVendor && (
          <>
            <Col xs={12} md={4}>
              <NavLink to="/vendor/home" onClick={closeMenu} className="menu-link">Home</NavLink>
            </Col>
            <Col xs={12} md={4}>
              <NavLink to="/vendor/scanner" onClick={closeMenu} className="menu-link">Scanner</NavLink>
            </Col>
            <Col xs={12} md={4}>
              <NavLink to="/vendor/claims" onClick={closeMenu} className="menu-link">Claims Data</NavLink>
            </Col>
            <Col xs={12} md={4}>
              <NavLink to="/vendor/history" onClick={closeMenu} className="menu-link">History</NavLink>
            </Col>
            
          </>
        )}
        {isAdmin && (
          <>
            <Col xs={12} md={4}>
              <NavLink to="/admin/home" onClick={closeMenu} className="menu-link">Home</NavLink>
            </Col>
            <Col xs={12} md={4}>
              <NavLink to="/admin/users" onClick={closeMenu} className="menu-link">Manage Users</NavLink>
            </Col>
            <Col xs={12} md={4}>
              <NavLink to="/admin/vendors" onClick={closeMenu} className="menu-link">Manage Vendors</NavLink>
            </Col>
          </>
        )}
        <Col xs={12} md={4}>
          <NavLink to="/change-password" onClick={closeMenu} className="menu-link">Change Password</NavLink>
        </Col>
        <Col xs={12} md={4}>
          <NavLink to="/logout" onClick={closeMenu} className="menu-link">Logout</NavLink>
        </Col>
      </Row>
    </nav>
  );
};

export default Menu;
