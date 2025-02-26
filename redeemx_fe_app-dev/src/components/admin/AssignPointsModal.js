import React, { useState, useEffect } from 'react';
import { assignPoints } from '../../api/admin';
import { Button, Modal, Alert, Spinner } from 'react-bootstrap';
import Form from 'react-bootstrap/Form';
import { FaEye, FaEyeSlash } from 'react-icons/fa';

const AssignPointsModal = ({ show, onHide, user }) => {
  const pointsTypes = ['General', 'Reward', 'Incentive'];
  const [points, setPoints] = useState(20);
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [pointsType, setPointsType] = useState('General');

  const handleAssign = async () => {
    if (!user) return;
    
    setLoading(true);
    setSuccessMessage('');
    setErrorMessage('');

    try {
      const response = await assignPoints(user.id, points, pointsType);
      setSuccessMessage(response.message || "Points assigned successfully!");

      // Close modal after success
      setTimeout(() => {
        onHide();
      }, 1500);
    } catch (error) {
      
      setErrorMessage(error || "Failed to assign points.");
      
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!show) {
      setSuccessMessage('');
      setErrorMessage('');
      setPoints(20);
    }
  }, [show]);

  return (
    <Modal show={show} onHide={onHide} size="md" centered>
      <Modal.Header closeButton>
        <Modal.Title>Assign Points to {user?.name}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {successMessage && <Alert variant="success">{successMessage}</Alert>}
        {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

        <Form>
          <Form.Group>
            <Form.Label>Points To be Assigned</Form.Label>
            <Form.Control
              type="number"
              value={points}
              onChange={(e) => setPoints((e.target.value))} // Ensure it's a number
              
            />
          </Form.Group>
          <Form.Group>
            <Form.Label>Points Type</Form.Label>
            <Form.Select value={pointsType} onChange={(e) => setPointsType(e.target.value)}>
              {pointsTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button style={{ backgroundColor: "#015295" }} onClick={handleAssign} disabled={loading}>
          {loading ? <Spinner animation="border" size="sm" /> : 'Assign'}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default AssignPointsModal;
