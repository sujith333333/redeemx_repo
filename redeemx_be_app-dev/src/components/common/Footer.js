import React from 'react';
import { Button, Row, Col } from 'react-bootstrap';
import { FaHome, FaQrcode, FaHistory, FaClipboardList } from 'react-icons/fa';
import '../../styles/Footer.css';
import { useNavigate } from 'react-router-dom';

const Footer = () => {
  const navigate = useNavigate();
  const userType = localStorage.getItem('user_type'); // Get the user_type from localStorage
  const isAdmin = userType === 'admin';
  const isVendor = userType === 'vendor';
  const isUser = userType === 'user';

  return (
    <footer className="bottom-navigation fixed-bottom">
      <Row className="w-100 text-center">
        {/* Home Button - Common for all roles */}
        <Col xs={isVendor ? 3 : 4} className="d-flex flex-column justify-content-center align-items-center">
          <Button
            className="nav-item text-center"
            onClick={() => {
              if (isAdmin) {
                navigate('/admin/home');
              } else if (isVendor) {
                navigate('/vendor/home');
              } else if (isUser) {
                navigate('/user/home');
              }
            }}
          >
            <FaHome size={24} />
            <p className="mb-0">Home</p>
          </Button>
        </Col>

        {/* Scanner Button - Visible only to Vendor and User */}
        {(isVendor || isUser) && (
          <Col xs={isVendor ? 3 : 4} className="d-flex flex-column justify-content-center align-items-center">
            <Button
              className="nav-item text-center"
              onClick={() => {
                if (isVendor) {
                  navigate('/vendor/scanner');
                } else if (isUser) {
                  navigate('/user/scanner');
                }
              }}
            >
              <FaQrcode size={24} />
              <p className="mb-0">Scanner</p>
            </Button>
          </Col>
        )}

        {/* Claims Button - Visible only to Vendor */}
        {isVendor && (
          <Col xs={3} className="d-flex flex-column justify-content-center align-items-center">
            <Button
              className="nav-item text-center"
              onClick={() => navigate('/vendor/claims')}
            >
              <FaClipboardList size={24} />
              <p className="mb-0">Claims</p>
            </Button>
          </Col>
        )}

        {/* History Button - Visible to Admin, Vendor, and User */}
        {(isAdmin || isVendor || isUser) && (
          <Col xs={isVendor ? 3 : 4} className="d-flex flex-column justify-content-center align-items-center">
            <Button
              className="nav-item text-center"
              onClick={() => {
                if (isAdmin) {
                  navigate('/admin/history');
                } else if (isVendor) {
                  navigate('/vendor/history');
                } else if (isUser) {
                  navigate('/user/history');
                }
              }}
            >
              <FaHistory size={24} />
              <p className="mb-0">History</p>
            </Button>
          </Col>
        )}
      </Row>
    </footer>
  );
};

export default Footer;
