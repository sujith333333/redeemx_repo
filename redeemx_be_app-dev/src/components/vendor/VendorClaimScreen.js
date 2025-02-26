import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, Modal, Table, Dropdown } from "react-bootstrap";
import { vendorClaimRegistration, getVendorData, getVendorClaimsData, getVendorClaimsPoints } from '../../api/vendor';
import { useNavigate } from 'react-router-dom';
import './VendorClaimScreen.css';
import Footer from '../common/Footer';


const VendorClaimScreen = () => {
  const [points, setPoints] = useState("");
  const [error, setError] = useState('');
  const [submissionMessage, setSubmissionMessage] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [claims, setClaims] = useState([]);
  const [showSuccess, setShowSuccess] = useState(false);
  const [filterStatus, setFilterStatus] = useState("All");

  // New State Variables for Vendor Points
  const [totalPoints, setTotalPoints] = useState(0);
  const [pendingPoints, setPendingPoints] = useState(0);
  const [usablePoints, setUsablePoints] = useState(0);

  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(6); // Adjust as needed

  const navigate = useNavigate();

  useEffect(() => {
    const fetchClaims = async () => {
      try {
        const data = await getVendorClaimsData(filterStatus);
        setClaims(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Error fetching claims:", error);
        setClaims([]);
      }
    };
    fetchClaims();
  }, [filterStatus, showSuccess]);

  const handleRequestClick = async () => {
    setShowModal(true);
    setSubmissionMessage("");
    setError("");
    setShowSuccess(false);

    // Fetch vendor points when modal opens
    try {
      const pointsData = await getVendorClaimsPoints();
      if (pointsData) {
        setTotalPoints(pointsData.total_points || 0); 
        setPendingPoints(pointsData.pending_points || 0);
        setUsablePoints(pointsData.usable_points || 0);
      }
    } catch (error) {
      console.log("Error fetching vendor points:", error);
    }
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    const sampleData = await getVendorData();
    const maxPoints = sampleData.points;
    const enteredPoints = parseInt(points, 10);

    if (isNaN(enteredPoints) || enteredPoints <= 0) {
      setError("❌ Please enter a valid positive number.");
      return;
    }

    if (enteredPoints > maxPoints) {
      setError(`❌ Points cannot exceed ${maxPoints}.`);
      return;
    }

    try {
      const body = { points: enteredPoints };
      await vendorClaimRegistration(body);
      setSubmissionMessage("✅ Claim request submitted successfully!");
      setPoints("");
      setError("");
      setShowSuccess(true);

      setTimeout(() => {
        setShowModal(false);
        setShowSuccess(false);
      }, 3000);
    } catch (error) {
      console.error("Error submitting claim:", error);
      setError(error.message);
    }
  };

  // Pagination Logic
  const indexOfLastClaim = currentPage * itemsPerPage;
  const indexOfFirstClaim = indexOfLastClaim - itemsPerPage;
  const currentClaims = claims.slice(indexOfFirstClaim, indexOfLastClaim);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const pageNumbers = [];
  for (let i = 1; i <= Math.ceil(claims.length / itemsPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <>
      <Container fluid className="py-4" style={{ marginTop: 70 }}>
        {/* Filter & Request Button */}
        <Row className="justify-content-center mb-4">
          <Col xs={6} md={4} className="mb-3">
            <Dropdown className="w-100">
              <Dropdown.Toggle className="w-100" style={{ backgroundColor: "#015295" }}>
                {filterStatus}
              </Dropdown.Toggle>
              <Dropdown.Menu>
                <Dropdown.Item onClick={() => setFilterStatus('All')}>All</Dropdown.Item>
                <Dropdown.Item onClick={() => setFilterStatus('Approved')}>Approved</Dropdown.Item>
                <Dropdown.Item onClick={() => setFilterStatus('Pending')}>Pending</Dropdown.Item>
                <Dropdown.Item onClick={() => setFilterStatus('Rejected')}>Rejected</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </Col>

          <Col xs={6} md={3} className="text-md-end text-center">
            <Button style={{ backgroundColor: "#015295" }} size="sm" className="fw-bold w-100" onClick={handleRequestClick}>
              Claims Request
            </Button>
          </Col>
        </Row>

        {/* Claims Table */}
        <Row className="justify-content-center">
          <Col xs={12} md={10} lg={8}>
            <Card.Body>
              <Table striped bordered hover responsive="sm">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Points</th>
                    <th>Status</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {currentClaims.length > 0 ? currentClaims.map((claim, index) => (
                    <tr key={index}>
                      <td>{indexOfFirstClaim + index + 1}</td>
                      <td>{claim.points}</td>
                      <td>{claim.status}</td>
                      <td>{new Date(claim.date).toLocaleString()}</td>
                    </tr>
                  )) : (
                    <tr>
                      <td colSpan="4" className="text-muted">No claims found</td>
                    </tr>
                  )}
                </tbody>
              </Table>
            </Card.Body>
          </Col>

          {/* Pagination */}
          <div className="d-flex justify-content-center mb-3">
            <nav>
              <ul className="pagination">
                {pageNumbers.map((number) => (
                  <li key={number} className={`page-item ${currentPage === number ? 'active' : ''}`}>
                    <button onClick={() => handlePageChange(number)} className="page-link">
                      {number}
                    </button>
                  </li>
                ))}
              </ul>
            </nav>
          </div>
        </Row>

        <Footer />
      </Container>

      {/* Request Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton style={{ backgroundColor: '#015295', color: '#fff' }}>
          <Modal.Title>Request for Claims</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="mb-3">
            <p><strong>Total Points:</strong> {totalPoints}</p>
            <p><strong>Pending Points:</strong> {pendingPoints}</p>
            <p><strong>Usable Points:</strong> {usablePoints}</p>
          </div>

          <Form onSubmit={handleFormSubmit}>
            <Form.Group controlId="points">
              <Form.Label>Enter Points</Form.Label>
              <Form.Control
                type="number"
                value={points}
                onChange={(e) => setPoints(e.target.value)}
                placeholder="Enter points"
                required
              />
            </Form.Group>
            {error && <div className="text-danger mt-2">{error}</div>}
            <Button style={{ backgroundColor: '#015295', color: '#fff' }} type="submit" className="mt-2 w-100">
              Submit
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default VendorClaimScreen;
