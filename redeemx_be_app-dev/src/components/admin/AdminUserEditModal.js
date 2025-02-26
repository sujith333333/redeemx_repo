import React, { useState } from 'react';
import { Button, Modal } from 'react-bootstrap';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';

const AdminUserEditModal = ({ show, onHide,user}) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    username: '',
    emp_id: '',
    mobile_number: '',
    password: '',
    confirmPassword: '',
  });

  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = 'Name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.username) newErrors.username = 'Username is required';
    if (!formData.emp_id) newErrors.emp_id = 'Employee ID is required';
    if (!formData.mobile_number) newErrors.mobile_number = 'Mobile number is required';
    if (!formData.password) newErrors.password = 'Password is required';
    if (formData.password !== formData.confirmPassword) newErrors.confirmPassword = 'Passwords do not match';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validateForm()) {
      const { confirmPassword, ...userData } = formData;
      setFormData({
        name: '',
        email: '',
        username: '',
        emp_id: '',
        mobile_number: '',
        password: '',
        confirmPassword: '',}
      );
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <Modal show={show} onHide={onHide} size="lg" centered>
      <Modal.Header closeButton>
        <Modal.Title>Add New User</Modal.Title>
      </Modal.Header>
      <Modal.Body>
<p>{user}</p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="primary" onClick={handleSubmit}>Add</Button>
      </Modal.Footer>
    </Modal>
  );
};

export default AdminUserEditModal;
