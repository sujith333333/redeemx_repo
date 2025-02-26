import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginApi } from "../api/auth";
import { Container, Row, Col, Form, Button, Spinner, InputGroup } from "react-bootstrap";
import { FaEye, FaEyeSlash } from "react-icons/fa";

const Login = ({ setToken }) => {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  
  const navigate = useNavigate();

  const isValidEmail = (input) => /\S+@\S+\.\S+/.test(input);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    
    const data = { password };
    if (isValidEmail(identifier)) {
      data.email = identifier;
    } else {
      data.emp_id = identifier;
    }

    try {
      const response = await loginApi(data);
      const { token, user_type } = response.data.data;

      localStorage.setItem("token", token);
      localStorage.setItem("user_type", user_type);
      setToken(token);

      if (user_type === "admin") navigate("/admin/home");
      else if (user_type === "user") navigate("/user/home");
      else if (user_type === "vendor") navigate("/vendor/home");
      else setError("Unrecognized user role.");
    } catch (error) {
      setError(error || "Invalid credentials or server error.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center vh-100">
      <Row className="w-100">
        <Col xs={12} sm={8} md={6} lg={4} className="mx-auto">
          <div className="text-center mb-4">
            <img src="images/ajalogo.png" alt="Logo" style={{ width: "30%" }} />
            <h2 style={{ color: "#015295", fontWeight:"800" }}>RedeemX</h2>
          </div>
          <div className="p-4 border rounded shadow-lg bg-white">
            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3">
                <Form.Label style={{ fontWeight: "bold" }}>Email or Employee ID</Form.Label>
                <Form.Control
                  type="text"
                  value={identifier}
                  onChange={(e) => setIdentifier(e.target.value)}
                  required
                  placeholder="Enter your Email or Employee ID"
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label style={{ fontWeight: "bold" }}>Password</Form.Label>
                <InputGroup className="position-relative">
                  <Form.Control
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    placeholder="Enter your Password"
                    style={{borderRadius:"5px"}}
                  />
                  <span
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      position: "absolute",
                      right: "10px",
                      top: "50%",
                      transform: "translateY(-50%)",
                      cursor: "pointer",
                      color: "#6c757d"
                    }}
                  >
                    {showPassword ? <FaEyeSlash /> : <FaEye />}
                  </span>
                </InputGroup>
              </Form.Group>
              {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

              <Button
                type="submit"
                className="w-50 d-flex justify-content-center align-items-center"
                disabled={isLoading}
                style={{
                  backgroundColor: "#015295",
                  borderColor: "#015295",
                  color: "white",
                  padding: "10px",
                  fontSize: "16px",
                  borderRadius: "5px",
                  display: "block",
                  margin: "0 auto",
                  height: "40px"
                }}
              >
                {isLoading ? (
                  <>
                    <Spinner 
                      as="span"
                      animation="border"
                      size="sm"
                      role="status"
                      aria-hidden="true"
                      className="me-2"
                    />
                    Login...
                  </>
                ) : (
                  "Login"
                )}
              </Button>
            </Form>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default Login;
