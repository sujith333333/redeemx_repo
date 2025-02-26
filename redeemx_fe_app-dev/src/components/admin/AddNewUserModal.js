import React, { useState, useEffect } from 'react';
import { Button, Modal, Spinner, Alert, InputGroup } from 'react-bootstrap';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { createUser } from '../../api/admin';

const AddNewUserModal = ({ show, onHide }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    username: '',
    emp_id: '',
    mobile_number: '',
    password: '',
  });

  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    if (!show) {
      // Reset form and messages when the modal closes
      setFormData({
        name: '',
        email: '',
        username: '',
        emp_id: '',
        mobile_number: '',
        password: '',
      });
      setErrors({});
      setSuccessMessage('');
      setErrorMessage('');
    }
  }, [show]);

  const validateForm = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = 'Name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.username) newErrors.username = 'Username is required';
    if (!formData.emp_id) newErrors.emp_id = 'Employee ID is required';
    if (!formData.mobile_number) newErrors.mobile_number = 'Mobile number is required';
    if (!formData.password) newErrors.password = 'Password is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (validateForm()) {
      setSuccessMessage('');
      setErrorMessage('');
      setLoading(true);

      try {
        const res = await createUser(formData);

        if (res && res.success) {
          setSuccessMessage('User added successfully!');

          // Clear form values
          setFormData({
            name: '',
            email: '',
            username: '',
            emp_id: '',
            mobile_number: '',
            password: '',
          });

          setErrors({});

          // Close the modal after a short delay (1.5s)
          setTimeout(() => {
            setSuccessMessage('');
            onHide(); // Close modal
          }, 1000);
        } else {
          setErrorMessage(res.message || 'Failed to add user.');
        }
      } catch (error) {
        setErrorMessage(error.response?.data?.error[0]?.error || error.response?.data?.error || 'Something went wrong.');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <Modal show={show} onHide={onHide} size="lg" centered>
      <Modal.Header closeButton>
        <Modal.Title className="justify-content-center">Add New User</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {successMessage && <Alert variant="success" className="text-center">{successMessage}</Alert>}
        {errorMessage && <Alert variant="danger" className="text-center">{errorMessage}</Alert>}

        <Form>
          {[
            { label: 'Name', name: 'name', type: 'text' },
            { label: 'Email', name: 'email', type: 'email' },
            { label: 'Username', name: 'username', type: 'text' },
            { label: 'Employee ID', name: 'emp_id', type: 'text' },
            { label: 'Mobile Number', name: 'mobile_number', type: 'number' },
          ].map((field) => (
            <Form.Group as={Row} className="mb-3" key={field.name}>
              <Form.Label column sm="3">{field.label}</Form.Label>
              <Col sm="9">
                <Form.Control
                  type={field.type}
                  placeholder={field.label}
                  name={field.name}
                  value={formData[field.name]}
                  onChange={handleChange}
                  isInvalid={!!errors[field.name]}
                />
                <Form.Control.Feedback type="invalid">{errors[field.name]}</Form.Control.Feedback>
              </Col>
            </Form.Group>
          ))}

          {/* Password Field with Embedded Eye Icon */}
          <Form.Group as={Row} className="mb-3">
            <Form.Label column sm="3">Password</Form.Label>
            <Col sm="9">
              <InputGroup className="position-relative">
                <Form.Control
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  isInvalid={!!errors.password}
                />
                <InputGroup.Text
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    cursor: 'pointer',
                    backgroundColor: 'transparent',
                    borderLeft: 'none'
                  }}
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </InputGroup.Text>
                <Form.Control.Feedback type="invalid">{errors.password}</Form.Control.Feedback>
              </InputGroup>
            </Col>
          </Form.Group>
        </Form>
      </Modal.Body>

      <Modal.Footer className="justify-content-right">
        <Button style={{ backgroundColor: "#015295" }} onClick={handleSubmit} disabled={loading}>
          {loading ? (
            <>
              <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
              {' '}Adding...
            </>
          ) : (
            'Add'
          )}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default AddNewUserModal;
