import React, { useEffect, useState } from 'react';
import { Col, Row } from 'react-bootstrap';
import { FaBars, FaChartBar, FaHistory, FaHome, FaLock, FaQrcode, FaSignOutAlt, FaTimes } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { getToken, getUserRole, removeToken } from '../../api/auth';
import '../../styles/Header.css';
const VendorHeader = ({ username }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isPasswordModalOpen, setIsPasswordModalOpen] = useState(false); // State for modal
  const [token, setToken] = useState(null);
  const [userType, setUserType] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedToken = getToken();
    const role = getUserRole();

    if (storedToken) {
      setToken(storedToken);
      if (role.is_user) {
        setUserType('user');
      } else if (role.is_vendor) {
        setUserType('vendor');
      } else if (role.is_admin) {
        setUserType('admin');
      } else {
        setUserType(null);
      }
    }
  }, [token]);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  const handleNavigation = (path) => {
    if (userType === 'admin') {
      navigate(`/admin${path}`);
    } else if (userType === 'vendor') {
      navigate(`/vendor${path}`);
    } else if (userType === 'user') {
      navigate(`/user${path}`);
    } else {
      navigate(path);
    }
    if(path==='/change-password'){
      navigate('/change-password')
    }
    closeMenu();
  };

  const handleLogout = () => {
    setToken(null);
    setUserType(null);
    removeToken(); // Remove token and user details from local storage
    window.location.href = '/login'; // Redirect to login page
  };

  const openPasswordModal = () => {
    setIsPasswordModalOpen(true); // Set modal open to true
  };

  const closePasswordModal = () => {
    setIsPasswordModalOpen(false); // Set modal open to false
  };

  return (
    <header className="header fixed-top">
      <Row className="align-items-center justify-content-between px-3">
        <Col xs={4} md={4} className="d-flex align-items-center">
        <div className="menu-icon" onClick={toggleMenu}>
            <FaBars size={24} />
        </div>
        </Col>
        <Col xs={4} md={4} className="text-center">
          <h1 className="header-title">RedeemX</h1>
        </Col>
        <Col xs={4} md={4} className="d-flex justify-content-end">
        <img src="/images/ajalogo.png" alt="Logo" className="header-logo" />
        </Col>
      </Row>

      <div className={`dropdown-menu ${isMenuOpen ? 'show' : ''}`}>
        <ul>
          <li onClick={() => handleNavigation('/home')}>
            <FaHome /> Home
          </li>
          <li onClick={() => handleNavigation('/scanner')}>
            <FaQrcode /> Scanner
          </li>
          <li onClick={() => handleNavigation('/claims')}>
            <FaChartBar /> Claims Data
          </li>
          <li onClick={() => handleNavigation('/history')}>
            <FaHistory /> History
          </li>
          <li onClick={() => handleNavigation('/change-password')}>
            <FaLock /> Change Password
          </li>
          <li onClick={handleLogout}>
            <FaSignOutAlt /> Logout
          </li>
          <li onClick={closeMenu}>
            <FaTimes /> Cancel
          </li>
        </ul>
      </div>

      
    </header>
  );
};

export default VendorHeader;
