import React, { useEffect, useState } from "react";
import { Card, Button, Alert, Modal, Table, Spinner } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { AiOutlineCalendar } from "react-icons/ai";
import {
  fetchAdminTransactions,
  fetchMonthlyTransactions,
  uploadFileAPI,
} from "../../api/admin";
import "../../styles/AdminDashBoard.css";
import { 
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
import { Bar, Pie } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const ResponseTable = ({ data }) => {
  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>Employee ID</th>
          <th>Details</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => (
          <tr key={index} className={!item.emp_id ? "table-danger" : ""}>
            <td>{item.emp_id || "N/A"}</td>
            <td>{item.details}</td>
            {/* <td>
              <Button>Add</Button>
            </td> */}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

const AdminDashboard = () => {
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const today = new Date();
  const currentMonthIndex = today.getMonth();
  const currentYear = today.getFullYear();

  const [file, setFile] = useState(null);
  const [fileUploaded, setFileUploaded] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [responseData, setResponseData] = useState(null);
  const [showTime, setShowTime] = useState(false);
  const [cardData, setCardsData] = useState({});
  const [monthData, setMonthData] = useState({});
  const [yearData, setYearData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [monthLoading, setMonthLoading] = useState(false);
  const [yearLoading, setYearLoading] = useState(false);

  const [startDate, setStartDate] = useState(
    `${currentYear}-${(currentMonthIndex + 1).toString().padStart(2, "0")}-01`
  );
  const [endDate, setEndDate] = useState(
    new Date(currentYear, currentMonthIndex + 1, 0).toISOString().split("T")[0]
  );

  const [monthStart, setMonthStart] = useState(
    `${currentYear}-${(currentMonthIndex + 1).toString().padStart(2, "0")}-01`
  );
  const [monthEnd, setMonthEnd] = useState(
    new Date(currentYear, currentMonthIndex + 1, 0).toISOString().split("T")[0]
  );

  const startOfYear = `${currentYear}-01-01`;
  const endOfYear = `${currentYear}-12-31`;
  const [selectedMonth, setSelectedMonth] = useState(currentMonthIndex);
  const [uploadedDates, setUploadedDates] = useState(() => {
    return JSON.parse(localStorage.getItem("uploadedDates")) || {};
  });

  const getTransactionsMonth = async (month) => {
    setMonthLoading(true);
    setError(null);
    try {
      const res = await fetchMonthlyTransactions(month + 1);
      setMonthData(res.data);
    } catch (error) {
      setError(error?.data?.error || "No Data Available");
    } finally {
      setMonthLoading(false);
    }
  };
  const handleMonthChange = (event) => {
    const selected = event.target.value;
    setSelectedMonth(parseInt(selected) - 1);
  };

  const getTransactionsCards = async (start, end) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchAdminTransactions({
        start_date: start,
        end_date: end,
      });
      setCardsData(res.data);
    } catch (error) {
      setError(error?.data?.error || "No Data Available");
    } finally {
      setLoading(false);
    }
  };

  const getTransactionsYear = async () => {
    setYearLoading(true);
    setError(null);
    try {
      const res = await fetchAdminTransactions({
        start_date: startOfYear,
        end_date: endOfYear,
      });
      setYearData(res.data);
    } catch (error) {
      setError(error?.data?.error || error?.message || "No Data Available");
    } finally {
      setYearLoading(false);
    }
  };

  useEffect(() => {
    getTransactionsCards(startDate, endDate);
    getTransactionsMonth(selectedMonth);
    getTransactionsYear();
  }, [selectedMonth]);

  const handleGetTimeFrame = () => {
    setShowTime(false);
  };

  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_type");
    window.location.href = "/login";
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
  };

  const handleFileUpload = async () => {
    if (!file) {
      setErrorMessage("Please select a file first.");
      setShowModal(true);
      setTimeout(() => {
        setErrorMessage(null);
        setShowModal(false);
        setFileUploaded(false) 
      }, 5000);

      return;
    }

    const selectedDate = new Date().toLocaleDateString("en-GB"); 

    if (uploadedDates[selectedDate]) {
      setErrorMessage(`File already uploaded for ${selectedDate}.`);
      setShowModal(true);
      setTimeout(() => {
        setErrorMessage(null);
        setShowModal(false);
        setUploading(false) 
      }, 3000);

      return;
    }

    setUploading(true);
    try {
      const response = await uploadFileAPI(file);
      const updatedDates = { ...uploadedDates, [selectedDate]: true };
      setUploadedDates(updatedDates);
      localStorage.setItem("uploadedDates", JSON.stringify(updatedDates));

      setFileUploaded(true);
      setErrorMessage(null);
      setResponseData(response);
      setShowModal(true);
    } catch (error) {
      console.error("File upload failed:", error);
      setErrorMessage("File upload failed. Please try again.");
      setResponseData(null);
      setShowModal(true);
      setTimeout(() => {
        setErrorMessage(null);
        setShowModal(false);
      }, 3000);
    }
    setUploading(false);
  };

  const handleCloseModal = () => setShowModal(false);

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Monthly Data",
      },
    },
  };

  const labels = [
    "Employees assigned points",
    "Points redeemed by vendor",
    "Vendor balance points",
    "Points redeemed by employees",
    "Employees balance points",
  ];

  const yearChartData = {
    labels,
    datasets: [
      {
        label: `${selectedMonth}`,
        data: [
          yearData?.points_assigned_to_employee,
          yearData?.points_claimed_by_vendor,
          yearData?.points_yet_to_approve_to_vendor,
          yearData?.total_points_user_sends_to_vendor,
          yearData?.points_assigned_to_employee_balance,
        ],
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgb(122, 156, 230, 0.2)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgb(122, 156, 230)",
        ],
      },
    ],
  };

  const monthChartData = {
    labels,
    datasets: [
      {
        label: `${selectedMonth}`,
        data: monthData
          ? [
              monthData.points_assigned_to_employee,
              monthData?.points_claimed_by_vendor,
              monthData?.points_yet_to_approve_to_vendor,
              monthData?.total_points_user_sends_to_vendor,
              monthData?.points_assigned_to_employee_balance,
            ]
          : [0, 0, 0, 0, 0],
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgb(122, 156, 230, 0.2)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgb(122, 156, 230)",
        ],
        borderWidth: 1,
      },
    ],
  };

  const renderMonthChart = () => {
    if (monthLoading) {
      return (
        <div className="text-center">
          <Spinner animation="border" variant="primary" />
          <p>Loading data...</p>
        </div>
      );
    }

    // Check if the data has no useful values (all values are zero)
    if (!monthData || Object.values(monthData).every((value) => value === 0)) {
      return <p>No data available </p>;
    }

    return <Pie data={monthChartData} />;
  };

  useEffect(() => {
    if (startDate && endDate) {
      getTransactionsCards(startDate, endDate);
    }
  }, [startDate, endDate]);

  useEffect(() => {
    getTransactionsMonth(selectedMonth);
  }, [selectedMonth]);

  return (
    <>
      <main
        style={{
          marginTop: "55px",
          height: "calc(100vh - 60px)",
          overflowY: "auto",
        }}
      >
        <section className="mb-1">
          <div className="d-flex flex-column gap-2">
            <h3 style={{ color: "#015295" }}>Assign Points</h3>
            <div
              style={{ display: "flex", flexDirection: "column", gap: "4px" }}
            >
              <input
                type="file"
                className="form-control"
                onChange={handleFileChange}
                disabled={uploading}
              />
              <button
                disabled={uploading}
                onClick={handleFileUpload}
                style={{
                  backgroundColor: "#015295",
                  color: "white",
                  border: "none",
                  borderRadius: "10px",
                  padding: "7px",
                }}
              >
                {uploading ? (
                  <>
                    <Spinner
                      as="span"
                      animation="border"
                      size="sm"
                      role="status"
                      aria-hidden="true"
                    />{" "}
                    Uploading...
                  </>
                ) : (
                  "Upload File"
                )}
              </button>
            </div>
          </div>
          {errorMessage && (
            <Alert variant="danger" className="mt-3">
              {errorMessage}
            </Alert>
          )}
        </section>
        {/* Overview Section */}
        <h2 className="mt-3" style={{ color: "#015295" }}>
          Overview
        </h2>
        <section>
          <div
            style={{
              display: "flex",
              width: "100%",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <span>
              <p style={{ color: "#015295" }}>
                {new Date(startDate).toLocaleDateString("en-GB", {
                  day: "numeric",
                  month: "numeric",
                  year: "numeric",
                })}{" "}
                -{" "}
                {new Date(endDate).toLocaleDateString("en-GB", {
                  day: "numeric",
                  month: "numeric",
                  year: "numeric",
                })}
              </p>
            </span>
            <div
              onClick={() => setShowTime(true)}
              style={{
                display: "flex",
                gap: "2px",
                alignItems: "center",
                justifyContent: "center",
                marginRight: "20px",
                cursor: "pointer",
              }}
            >
              <p style={{ fontSize: "1rem" }}>Select Time Frame</p>
              <AiOutlineCalendar size={20} className="mb-2" />
            </div>
          </div>
          <div className="row row-cols-1 row-cols-md-2 row-cols-lg-5 g-3 mb-4">
            <div className="col">
              <Card>
                <Card.Body>
                  <Card.Text>Points assigned to employees</Card.Text>
                  <h3 className="points-color">
                    {cardData?.points_assigned_to_employee || 0}
                  </h3>
                </Card.Body>
              </Card>
            </div>
            <div className="col">
              <Card>
                <Card.Body>
                  <Card.Text>Points redeemed by employees</Card.Text>
                  <h3 className="points-color">
                    {cardData?.total_points_user_sends_to_vendor || 0}
                  </h3>
                </Card.Body>
              </Card>
            </div>
            <div className="col">
              <Card>
                <Card.Body>
                  <Card.Text>Employees leftover points</Card.Text>
                  <h3 className="points-color">
                    {cardData?.points_assigned_to_employee_balance || 0}
                  </h3>
                </Card.Body>
              </Card>
            </div>
            <div className="col">
              <Card>
                <Card.Body>
                  <Card.Text>Points redeemed by vendor</Card.Text>
                  <h3 className="points-color">
                    {cardData?.points_claimed_by_vendor || 0}
                  </h3>
                </Card.Body>
              </Card>
            </div>
            <div className="col">
              <Card>
                <Card.Body>
                  <Card.Text>Vendor balance points</Card.Text>
                  <h3 className="points-color">
                    {cardData?.points_yet_to_approve_to_vendor || 0}
                  </h3>
                </Card.Body>
              </Card>
            </div>
          </div>

          <div className="row g-3 mb-2">
            <div className="col-12 col-lg-6">
              <Card>
                <Card.Body>
                  <div
                    style={{ display: "flex", justifyContent: "space-between" }}
                  >
                    <h5>Status Breakdown For {monthNames[selectedMonth]}</h5>
                    <select
                      value={selectedMonth + 1}
                      onChange={handleMonthChange}
                    >
                      {monthNames.map((month, index) => (
                        <option key={index} value={index + 1}>
                          {month}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div
                    style={{
                      width: "100%",
                      height: "300px",
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    {renderMonthChart()}
                  </div>
                </Card.Body>
              </Card>
            </div>

            <div className="col-12 col-lg-6">
              <Card>
                <Card.Body>
                  <h5>Yearly Overview for {currentYear}</h5>
                  <div style={{ width: "100%", height: "300px" }}>
                    {yearLoading ? (
                      <div className="text-center">
                        <Spinner animation="border" variant="primary" />
                        <p>Loading data...</p>
                      </div>
                    ) : (
                      <Bar options={options} data={yearChartData} />
                    )}
                  </div>
                </Card.Body>
              </Card>
            </div>
          </div>
        </section>
      </main>

      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Upload Status</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {fileUploaded ? (
            <div>
              <h5>File uploaded successfully!</h5>
              <ResponseTable data={responseData?.data || []} />
            </div>
          ) : (
            <p>{errorMessage}</p>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showTime} onHide={() => setShowTime(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Select Time Frame</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form className="time-frame-form">
            <div className="form-group">
              <label>Start Date</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label>End Date</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
          </form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            style={{ backgroundColor: "#015295" }}
            type="submit"
            onClick={handleGetTimeFrame}
          >
            Get
          </Button>
          <Button variant="secondary" onClick={() => setShowTime(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default AdminDashboard;

