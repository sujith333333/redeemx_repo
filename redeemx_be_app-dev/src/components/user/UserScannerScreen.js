import React, { useState } from "react";
import { Container, Row, Col, Card, Alert } from "react-bootstrap";
import UserSendPoints from "./UserSendPoints";
import UserSendPointsToVendor from "./UserSendPointsToVendor";
import "../../styles/UserScannerScreen.css";
import Footer from "../common/Footer";

const UserScannerScreen = () => {
  const [showContent, setShowContent] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  return (
    <Container fluid className="d-flex flex-column justify-content-center align-items-center vh-100 text-center">
      {/* Icon Selection Section */}
      <Row className="justify-content-center w-100 mb-4">
        <Col xs={6} md={3} className="d-flex justify-content-center">
          <Card
            className={`icon-card ${showContent === "vendors" ? "active" : ""}`}
            onClick={() => setShowContent("vendors")}
          >
            <div className="icon-overlay">
              <img
                src="https://cdn-icons-png.flaticon.com/128/10233/10233443.png"
                alt="SendToVendor"
                className="custom-icon"
              />
              <p className="icon-text" style={{color:"#015295"}}>Send To Vendor</p>
            </div>
          </Card>
        </Col>

        <Col xs={6} md={3} className="d-flex justify-content-center">
          <Card
            className={`icon-card ${showContent === "qr" ? "active" : ""}`}
            onClick={() => setShowContent("qr")}
          >
            <div className="icon-overlay">
              <img
                src="https://cdn-icons-png.flaticon.com/128/18222/18222059.png"
                alt="SendByQR"
                className="custom-icon"
              />
              <p className="icon-text" style={{color:"#015295"}}>Send By QR</p>
            </div>
          </Card>
        </Col>
      </Row>

      {/* Content Section */}
      <Row className="justify-content-center w-100">
        <Col xs={12} md={8} className="d-flex flex-column align-items-center">
          {showContent === "vendors" && <UserSendPointsToVendor />}
          {showContent === "qr" && <UserSendPoints />}
          {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
        </Col>
      </Row>

      {/* Footer Section */}
      <Footer />
    </Container>
  );
};

export default UserScannerScreen;

