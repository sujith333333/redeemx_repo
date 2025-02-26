import React, { useState, useEffect } from "react";
import { Container, Row, Col, Form, Alert, Spinner, Modal, Button } from "react-bootstrap";
import { sendPointsToVendor, getVendors } from "../../api/user";

const successSound = new Audio("https://www.myinstants.com/media/sounds/cash.mp3"); // Replace with actual sound

const UserSendPointsToVendor = () => {
  const [vendors, setVendors] = useState([]);
  const [selectedVendor, setSelectedVendor] = useState("");
  const [points, setPoints] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [transactionDetails, setTransactionDetails] = useState(null);

  useEffect(() => {
    const fetchVendors = async () => {
      setLoading(true);
      try {
        const data = await getVendors();
        if (Array.isArray(data.data)) {
          setVendors(data.data);
        } else {
          setVendors([]);
          console.error("Invalid API response:", data);
        }
      } catch (error) {
        console.error("Error fetching vendors:", error);
        setError("Failed to fetch vendors");
      } finally {
        setLoading(false);
      }
    };
    fetchVendors();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!selectedVendor || !points) {
      setError("Please select a vendor and enter points.");
      return;
    }

    try {
      await sendPointsToVendor(selectedVendor, points);

      // Capture transaction details
      setTransactionDetails({
        vendor: selectedVendor,
        points: points,
        date: new Date().toLocaleString(),
      });

      // Play success sound
      successSound.play();

      // Show modal
      setShowModal(true);

      // Reset form fields
      setSelectedVendor("");
      setPoints("");
    } catch (error) {
      console.error("Error sending points:", error);
      setError(error.message || "Error sending points to vendor.");
    }
  };

  return (
    <Container className="mt-4">
      <Row className="justify-content-center">
        <Col xs={12} md={8} className="p-4 shadow-sm rounded bg-white">
          <h4 className="text-center mb-3" style={{color:"#015295"}}>Send Points to Vendor</h4>
          {error && <p className="text-center" style={{color:"red"}}>{error}</p>}
        
          {loading ? (
            <div className="text-center">
              <Spinner animation="border" variant="primary" />
            </div>
          ) : (
            <Form onSubmit={handleSubmit}>
              <Form.Group controlId="vendorSelect" className="mb-3">
                <Form.Label className="fw-bold" style={{color:"#015295"}}>Select Vendor</Form.Label>
                <Form.Select
                  value={selectedVendor}
                  onChange={(e) => setSelectedVendor(e.target.value)}
                  required
                >
                  <option value="">Vendor Name</option>
                  {vendors.length > 0 ? (
                    vendors.map((vendor, index) => (
                      <option key={index} value={vendor}>
                        {vendor}
                      </option>
                    ))
                  ) : (
                    <option disabled>No vendors available</option>
                  )}
                </Form.Select>
              </Form.Group>

              <Form.Group controlId="pointsInput" className="mb-3">
                <Form.Label className="fw-bold" style={{color:"#015295"}}>Enter Points</Form.Label>
                <Form.Control
                  type="number"
                  placeholder="Enter points"
                  value={points}
                  onChange={(e) => setPoints(e.target.value)}
                  required
                  min="1"
                />
              </Form.Group>

              <div className="text-center mt-3">
                <img
                  src="https://cdn-icons-png.flaticon.com/128/9347/9347219.png"
                  alt="Send Points"
                  className="icon-send cursor-pointer"
                  onClick={handleSubmit}
                  style={{ width: "50px", height: "50px" }}
                />
              </div>
            </Form>
          )}
        </Col>
      </Row>

      {/* Success Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Body className="text-center">
        
          {transactionDetails && (
            <>
            <div
                className="d-inline-block bg-success text-white fw-bold rounded-circle p-3 mb-2"
                style={{ fontSize: "24px", minWidth: "60px", minHeight: "60px" }}
              >
                {transactionDetails.points}
              </div>
              <p className="text-success">✅ Points Sent Successfully!</p>
              <p className="fw-bold mt-2">Vendor: {transactionDetails.vendor}</p>
              
              <p className="fw-bold mt-2">Date: {transactionDetails.date}</p>
            </>
          )}
          
          <Button variant="success" onClick={() => setShowModal(false)}>
            OK
          </Button>
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default UserSendPointsToVendor;
