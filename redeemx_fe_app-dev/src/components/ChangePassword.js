import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { changePassword } from "../api/user";
import { Container, Row, Col, Form, Button, InputGroup } from "react-bootstrap";
import { removeToken } from "../api/auth";
import { FaEye, FaEyeSlash } from "react-icons/fa";

const ChangePassword = () => {
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [passwordTyped, setPasswordTyped] = useState(false);
  const [passwordMatch, setPasswordMatch] = useState(null);
  
  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const navigate = useNavigate();

  const passwordCriteria = [
    { id: 1, rule: "At least 8 characters", test: (pw) => pw.length >= 8 },
    { id: 2, rule: "One uppercase letter", test: (pw) => /[A-Z]/.test(pw) },
    { id: 3, rule: "One lowercase letter", test: (pw) => /[a-z]/.test(pw) },
    { id: 4, rule: "One number", test: (pw) => /\d/.test(pw) },
    { id: 5, rule: "One special character (@$!%*?&)", test: (pw) => /[@$!%*?&]/.test(pw) },
  ];

  const handleNewPasswordChange = (e) => {
    setNewPassword(e.target.value);
    setPasswordTyped(true);
    setPasswordMatch(null);
  };

  const handleConfirmPasswordChange = (e) => {
    const value = e.target.value;
    setConfirmNewPassword(value);
    setPasswordMatch(value === newPassword && value.length > 0);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsLoading(true);

    const isPasswordValid = passwordCriteria.every(({ test }) => test(newPassword));
    if (!isPasswordValid) {
      setError("New password does not meet all the conditions.");
      setIsLoading(false);
      return;
    }

    if (newPassword !== confirmNewPassword) {
      setError("New Password and Confirm New Password do not match.");
      setIsLoading(false);
      return;
    }

    try {
      await changePassword(oldPassword, newPassword, confirmNewPassword);
      setSuccess("✅ Password changed successfully!");

      setOldPassword("");
      setNewPassword("");
      setConfirmNewPassword("");
      setPasswordTyped(false);
      setPasswordMatch(null);

      setTimeout(() => {
        removeToken();
      }, 1000);
    } catch (error) {
      setError(error.response?.data?.error || "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center vh-100">
      <Row className="w-100">
        <Col xs={12} sm={8} md={6} lg={4} className="mx-auto">
          <div className="p-4 border rounded shadow-lg bg-white">
            <Form onSubmit={handleSubmit}>
              {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
              {success && <p style={{ color: "green", textAlign: "center" }}>{success}</p>}

              {/* Old Password */}
              <Form.Group className="mb-3">
                <Form.Label style={{ fontWeight: "bold" }}>Old Password</Form.Label>
                <InputGroup className="position-relative">
                  <Form.Control
                    type={showOldPassword ? "text" : "password"}
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                    required
                    placeholder="Enter your old password"
                  />
                  <span
                    onClick={() => setShowOldPassword(!showOldPassword)}
                    style={{
                      position: "absolute",
                      right: "10px",
                      top: "50%",
                      transform: "translateY(-50%)",
                      cursor: "pointer",
                      color: "#6c757d"
                    }}
                  >
                    {showOldPassword ? <FaEyeSlash /> : <FaEye />}
                  </span>
                </InputGroup>
              </Form.Group>

              {/* New Password */}
              <Form.Group className="mb-3">
                <Form.Label style={{ fontWeight: "bold" }}>New Password</Form.Label>
                <InputGroup className="position-relative">
                  <Form.Control
                    type={showNewPassword ? "text" : "password"}
                    value={newPassword}
                    onChange={handleNewPasswordChange}
                    required
                    placeholder="Enter new password"
                  />
                  <span
                    onClick={() => setShowNewPassword(!showNewPassword)}
                    style={{
                      position: "absolute",
                      right: "10px",
                      top: "50%",
                      transform: "translateY(-50%)",
                      cursor: "pointer",
                      color: "#6c757d"
                    }}
                  >
                    {showNewPassword ? <FaEyeSlash /> : <FaEye />}
                  </span>
                </InputGroup>

                {/* Password Criteria */}
                <ul className="small mt-2" style={{ paddingLeft: "15px", listStyle: "none" }}>
                  {passwordCriteria.map(({ id, rule, test }) => (
                    <li key={id} style={{ color: passwordTyped ? (test(newPassword) ? "green" : "red") : "black" }}>
                      {passwordTyped ? (test(newPassword) ? "✅" : "❌") : "•"} {rule}
                    </li>
                  ))}
                </ul>
              </Form.Group>

              {/* Confirm New Password */}
              <Form.Group className="mb-3">
                <Form.Label style={{ fontWeight: "bold" }}>Confirm New Password</Form.Label>
                <InputGroup className="position-relative">
                  <Form.Control
                    type={showConfirmPassword ? "text" : "password"}
                    value={confirmNewPassword}
                    onChange={handleConfirmPasswordChange}
                    required
                    placeholder="Confirm your new password"
                  />
                  <span
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    style={{
                      position: "absolute",
                      right: "10px",
                      top: "50%",
                      transform: "translateY(-50%)",
                      cursor: "pointer",
                      color: "#6c757d"
                    }}
                  >
                    {showConfirmPassword ? <FaEyeSlash /> : <FaEye />}
                  </span>
                </InputGroup>

                {/* Password Match Indicator */}
                {confirmNewPassword.length > 0 && (
                  <p
                    className="small mt-1"
                    style={{
                      color: passwordMatch ? "green" : "red",
                      fontWeight: "bold",
                      display: "flex",
                      alignItems: "center",
                    }}
                  >
                    {passwordMatch ? "✅" : "❌"}{" "}
                    {passwordMatch ? "Passwords match" : "New Password and Confirm New Password do not match"}
                  </p>
                )}
              </Form.Group>

              {/* Submit Button */}
              <div className="d-flex justify-content-center">
              
                                <Button
                  type="submit"
                  disabled={isLoading}
                  style={{
                    backgroundColor: "#015295",
                    borderColor: "#015295",
                    color: "white",
                    padding: "6px 12px",
                    fontSize: "16px",
                    borderRadius: "5px",
                    width: "50%",
                    minWidth: "220px",
                    whiteSpace: "nowrap",
                    textAlign: "center",
                    overflow: "hidden",
                  }}
                >
                  {isLoading ? "Changing Password..." : "Change Password"}
                </Button>
              </div>
            </Form>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default ChangePassword;



