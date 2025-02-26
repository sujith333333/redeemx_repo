import React, { useState, useEffect } from "react";
import { Button, Container, Row, Col, Form, Alert, Card } from "react-bootstrap";
import { getAllPoints } from "../../api/vendor";
import { format } from "date-fns";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from "chart.js";
import ChartDataLabels from 'chartjs-plugin-datalabels';
import '../../styles/UserHomeScreen.css';
import Footer from "../common/Footer";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend, ChartDataLabels);

const VendorHomeScreen = () => {
  const today = new Date();
  const currentDate = format(today, "yyyy-MM-dd");

  const [selected, setSelected] = useState("balance");
  const [points, setPoints] = useState({ balance: 0, credited: 0, debited: 0 });
  const [filters, setFilters] = useState({ date: currentDate, month: "----, ----" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => { fetchPoints(); }, [filters]);

  const fetchPoints = async () => {
    setLoading(true);
    setError(null);
    try {
      let updatedFilters = {};

      if (filters.date) {
        updatedFilters = { day: filters.date };
      } else if (filters.month !== "----, ----") {
        updatedFilters = { month: filters.month };
      }

      const response = await getAllPoints(updatedFilters);
      console.log("API Response:", response);

      if (response?.data?.length > 0) {
        setPoints(response.data[0]);
      } else {
        setPoints({ balance: 0, credited: 0, debited: 0 });
      }
    } catch (error) {
      console.error("Error fetching points:", error);
      setError("Error fetching data. Please try again later.");
      setPoints({ balance: 0, credited: 0, debited: 0 });
    }
    setLoading(false);
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;

    if (name === "date") {
      setFilters({ date: value ? format(new Date(value), "yyyy-MM-dd") : "", month: "----, ----" });
    } else if (name === "month") {
      setFilters({ date: "", month: value || "----, ----" });
    }
  };

  const barData = {
    labels: ["Available Points", "Credited Points", "Claimed Points"],
    datasets: [
      {
        label: "Available Points",
        data: [points.balance, null, null],  
        backgroundColor: "#015295",
        borderColor: "#004d40",
        borderWidth: 1,
      },
      {
        label: "Credited",
        data: [null, points.credited, null],  
        backgroundColor: "#047857",
        borderColor: "#01579b",
        borderWidth: 1,
      },
      {
        label: "Claims",
        data: [null, null, points.debited],  
        backgroundColor: "#B91C1C",
        borderColor: "#c62828",
        borderWidth: 1,
      },
    ],
  };

  return (
    <Container fluid className="text-center py-4 user-container">
      <h5 className="header-title">Your Points Summary</h5>
      {error && <Alert variant="danger">{error}</Alert>}

      <Row className="justify-content-end mb-3">
        <Col xs={6} sm={3} md={2} className="text-end">
          <Form.Control 
            type="date" 
            name="date" 
            value={filters.date} 
            onChange={handleFilterChange} 
            disabled={loading} 
          />
        </Col>
        <Col xs={6} sm={3} md={2} className="text-end">
          <Form.Control 
            type="month" 
            name="month" 
            value={filters.month === "----, ----" ? "" : filters.month} 
            onChange={handleFilterChange} 
            disabled={loading} 
            placeholder="----, ----"
          />
        </Col>
      </Row>

      {filters.month !== "----, ----" && (
        <Row className="justify-content-end mt-3">
          <Col xs="auto">
            <p style={{color:"#015295"}}><strong>Selected Month:</strong> {filters.month}</p>
          </Col>
        </Row>
      )}

      <Row className="justify-content-center mb-3">
        <Col xs={12} md={8} lg={6}>
          <Card.Body className="d-flex justify-content-between align-items-center">
            {[{ type: "balance", label: "Available Points", color: "#1E3A8A" }, { type: "credited", label: "Credited Points", color: "#047857" }, { type: "debited", label: "Claimed Points", color: "#B91C1C" }].map((btn, index) => (
              <Button
                key={index}
                className="custom-button"
                style={{ backgroundColor: btn.color, border: "none" }}
                onClick={() => setSelected(btn.type)}
                disabled={loading}
              >
                {selected === btn.type ? `${btn.label} ${points[btn.type]}` : btn.label}
              </Button>
            ))}
          </Card.Body>
        </Col>
      </Row>

      <Row className="justify-content-center">
        <Col xs={12} md={6} className="d-flex justify-content-center">
          <div style={{ width: "90%", maxWidth: "450px"}}>
            <h6 className="mb-3" style={{color:"#015295"}}>Points Bar Chart</h6>
            <Bar data={barData}  plugins={[ChartDataLabels]} />
          </div>
        </Col>
      </Row>

      <Footer />
    </Container>
  );
};

export default VendorHomeScreen;
