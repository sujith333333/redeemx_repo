import React, { useEffect, useState } from 'react';
import { Alert, Button, Form, Modal, Spinner } from 'react-bootstrap';
import { EditVendor } from '../../api/admin';

const EditVendorDetails = ({ show, onHide, vendor, type }) => {
  const [formData, setFormData] = useState({
    vendor_name: "",
    name: "",
    email: "",
    emp_id: "",
    mobile_number: "",
    description: ""
  });

  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    if (vendor && show) {
      setFormData({
        vendor_name: vendor.vendor_name || '',
        name: vendor.name || '',
        email: vendor.email || '',
        emp_id: vendor.emp_id || '',
        mobile_number: vendor.mobile_number || '',
        description: vendor.description || ''
      });
      setErrorMessage('');
      setSuccessMessage('');
    }
  }, [vendor, show]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleUpdate = async () => {
    if (!vendor || type !== "vendor") {
      setErrorMessage("Invalid vendor data.");
      return;
    }

    setLoading(true);
    setSuccessMessage('');
    setErrorMessage('');

    const updatedData = Object.keys(formData).reduce((acc, key) => {
      if (formData[key] !== vendor[key]) {
        acc[key] = formData[key];
      }
      return acc;
    }, {});

    if (Object.keys(updatedData).length === 0) {
      setErrorMessage("No changes detected.");
      setLoading(false);
      return;
    }

    try {
      const response = await EditVendor(vendor.id, updatedData);
      console.log(response, "res");

      if (response.success) {
        setSuccessMessage('Vendor details updated successfully!');
        setTimeout(() => onHide(), 1500);
      } else {
        setErrorMessage(response.message || 'Failed to update vendor.');
      }
    } catch (error) {
      setErrorMessage(error?.message || error?.error?.[0] || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="md" centered>
      <Modal.Header closeButton>
        <Modal.Title>Edit {vendor?.name} Details</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          {[
            { label: 'Vendor Name', name: 'vendor_name', type: 'text' },
            { label: 'Name', name: 'name', type: 'text' },
            { label: 'Email', name: 'email', type: 'email' },
            { label: 'Employee ID', name: 'emp_id', type: 'text' },
            { label: 'Mobile Number', name: 'mobile_number', type: 'number' },
            { label: 'Description', name: 'description', type: 'text' }
          ].map((field) => (
            <Form.Group className="mb-3" key={field.name}>
              <Form.Label>{field.label}</Form.Label>
              <Form.Control
                type={field.type}
                name={field.name}
                value={formData[field.name]}
                onChange={handleChange}
              />
            </Form.Group>
          ))}
        </Form>
        {successMessage && <Alert variant="success">{successMessage}</Alert>}
        {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>Cancel</Button>
        <Button variant="primary" onClick={handleUpdate} disabled={loading}>
          {loading ? <Spinner animation="border" size="sm" /> : 'Update Vendor'}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default EditVendorDetails;
