
import React, { useState, useEffect } from "react";
import { Button, Modal, Container, Row, Col, Form, Alert, InputGroup } from "react-bootstrap";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import { Spinner } from "react-bootstrap";
import { AddNewVendor } from "../../api/admin";

const AddNewVendorModal = ({ show, onHide }) => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    username: "",
    emp_id: "",
    mobile_number: "",
    password: "",
    vendor_name: "",
    description: "",
    bank_name: "",
    account_holder_name: "",
    account_number: "",
    ifsc_code: "",
    branch_name: "",
    aadhar_card: "",
    pan_card: "",
  });

  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    if (!show) {
      setFormData({
        name: "",
        email: "",
        username: "",
        emp_id: "",
        mobile_number: "",
        password: "",
        vendor_name: "",
        description: "",
        bank_name: "",
        account_holder_name: "",
        account_number: "",
        ifsc_code: "",
        branch_name: "",
        aadhar_card: "",
        pan_card: "",
      });
      setErrors({});
      setSuccessMessage("");
      setErrorMessage("");
    }
  }, [show]);

  const validateForm = () => {
    const newErrors = {};
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
    const accountNumberPattern = /^\d+$/;
    const ifscCodePattern = /^[A-Za-z]{4}\d{7}$/;
    const aadharCardPattern = /^\d{12}$/;
    const panCardPattern = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;

    if (!formData.name) newErrors.name = "Name is required";
    if (!formData.email) newErrors.email = "Email is required";
    if (!formData.username) newErrors.username = "Username is required";
    if (!formData.mobile_number) newErrors.mobile_number = "Mobile number is required";
    if (!formData.password) newErrors.password = "Password is required";
    else if (!passwordPattern.test(formData.password))
      newErrors.password =
        "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.";
    if (!formData.vendor_name) newErrors.vendor_name = "Vendor name is required";
    if (!formData.bank_name) newErrors.bank_name = "Bank name is required";
    if (!formData.account_holder_name) newErrors.account_holder_name = "Account holder name is required";
    if (!formData.account_number) newErrors.account_number = "Account number is required";
    else if (!accountNumberPattern.test(formData.account_number))
      newErrors.account_number = "Account number must contain only digits.";
    if (!formData.ifsc_code) newErrors.ifsc_code = "IFSC code is required";
    else if (!ifscCodePattern.test(formData.ifsc_code))
      newErrors.ifsc_code = "IFSC code must have the first 4 characters as letters and the remaining 7 as digits.";
    if (!formData.branch_name) newErrors.branch_name = "Branch name is required";
    if (!formData.aadhar_card) newErrors.aadhar_card = "Aadhar card number is required";
    else if (!aadharCardPattern.test(formData.aadhar_card))
      newErrors.aadhar_card = "Aadhar card number must contain only digits.";
    if (!formData.pan_card) newErrors.pan_card = "PAN card number is required";
    else if (!panCardPattern.test(formData.pan_card)) newErrors.pan_card = "PAN card format is invalid. It should be in the format ABCDE1234F.";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setSuccessMessage("");
    setErrorMessage("");
    setLoading(true);

    try {
      const requestData = {
        ...formData,
        vendor_name: formData.vendor_name,
        description: formData.description,
        mobile_number: formData.mobile_number,
      };

      console.log("Sending Data:", requestData);
      const res = await AddNewVendor(requestData);
      console.log("Response:", res);

      if (res && res.success) {
        setSuccessMessage("Vendor added successfully!");
        setFormData({
          name: "",
          email: "",
          username: "",
          emp_id: "",
          mobile_number: "",
          password: "",
          vendor_name: "",
          description: "",
          bank_name: "",
          account_holder_name: "",
          account_number: "",
          ifsc_code: "",
          branch_name: "",
          aadhar_card: "",
          pan_card: "",
        });
        setTimeout(() => {
          onHide();
          setSuccessMessage(""); // Clear success message
        }, 1500);
      } else {
        setErrorMessage(res.message || "Failed to add vendor.");
      }
    } catch (error) {
      console.error("Error:", error);

      if (error.response && error.response.data) {
        const apiErrors = error.response.data.error;
        if (Array.isArray(apiErrors)) {
          setErrorMessage(apiErrors.join("\n"));
        } else {
          setErrorMessage(apiErrors || "Something went wrong.");
        }
      } else {
        setErrorMessage("An unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
    <Modal show={show} onHide={onHide} size="lg" centered>
      <Modal.Header closeButton>
        <Modal.Title>Add New Vendor</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {successMessage && <Alert variant="success" className="text-center mt-3">{successMessage}</Alert>}
        {errorMessage && <Alert variant="danger" className="text-center mt-3">{errorMessage}</Alert>}

        <Form>
          {[
            { label: "Name", name: "name", type: "text" },
            { label: "Email", name: "email", type: "email" },
            { label: "Username", name: "username", type: "text" },
            { label: "Employee ID", name: "emp_id", type: "text" },
            { label: "Mobile Number", name: "mobile_number", type: "number" },
            { label: "Vendor Name", name: "vendor_name", type: "text" },
            { label: "Description", name: "description", type: "text" },
            { label: "Bank Name", name: "bank_name", type: "text" },
            { label: "Account Holder Name", name: "account_holder_name", type: "text" },
            { label: "Account Number", name: "account_number", type: "text" },
            { label: "IFSC Code", name: "ifsc_code", type: "text" },
            { label: "Branch Name", name: "branch_name", type: "text" },
            { label: "Aadhar Card", name: "aadhar_card", type: "text" },
            { label: "PAN Card", name: "pan_card", type: "text" },
          ].map((field) => (
            <Form.Group as={Row} className="mb-3" key={field.name}>
              <Form.Label column xs={12} md={3} className="text-md-end">
                {field.label}
              </Form.Label>
              <Col xs={12} md={9}>
                <Form.Control
                  type={field.type}
                  placeholder={field.label}
                  name={field.name}
                  value={formData[field.name]}
                  onChange={handleChange}
                  isInvalid={!!errors[field.name]}
                />
                <Form.Control.Feedback type="invalid">
                  {errors[field.name]}
                </Form.Control.Feedback>
              </Col>
            </Form.Group>
          ))}

          {/* Password Field with Eye Icon */}
          <Form.Group as={Row} className="mb-3">
            <Form.Label column xs={12} md={3} className="text-md-end">
              Password
            </Form.Label>
            <Col xs={12} md={9}>
              <InputGroup>
                <Form.Control
                  type={showPassword ? "text" : "password"}
                  placeholder="Password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  isInvalid={!!errors.password}
                />
                <InputGroup.Text
                  onClick={() => setShowPassword(!showPassword)}
                  style={{ cursor: "pointer", backgroundColor: "transparent", borderLeft: "none" }}
                >
                  {showPassword ? <FaEyeSlash /> : <FaEye />}
                </InputGroup.Text>
                <Form.Control.Feedback type="invalid">
                  {errors.password}
                </Form.Control.Feedback>
              </InputGroup>
            </Col>
          </Form.Group>
        </Form>
      </Modal.Body>

      <Modal.Footer>
        <Button style={{ backgroundColor: "#015295" }} onClick={handleSubmit} disabled={loading}>
          {loading ? <Spinner animation="border" size="sm" /> : "Add"}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default AddNewVendorModal;

