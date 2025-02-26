import React, { useEffect, useRef, useState } from "react";
import {
  Table,
  Badge,
  Container,
  Row,
  Col,
  Form,
  Button,
  Modal,
  Spinner,
  Pagination,
} from "react-bootstrap";
import { fetchVendors } from "../../api/vendor";
import {
  changeClaimsStatus,
  fetchClaims,
  approveClaim,
  rejectClaim,
} from "../../api/admin";

const AdminVendorTransaction = () => {
  // State for vendors and claims data
  const [vendors, setVendors] = useState([]);
  const [vendorData, setVendorData] = useState([]);

  // Track selected vendor for approval/rejection
  const [selectedVendor, setSelectedVendor] = useState(null);

  // Error/loading states
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  // Modal controls
  const [show, setShow] = useState(false);
  const [deleteShow, setDeleteShow] = useState(false);
  const prevShow = useRef(show);
  const prevDeleteShow = useRef(deleteShow);
  const [transactionId, setTransactionId] = useState("")

  // Points, status, date filters
  const [points, setPoints] = useState(0);
  const [status, setStatus] = useState("");
  const [filterDate, setFilterDate] = useState("");

  // Filtered array after applying status/date
  const [filtered, setFiltered] = useState([]);

  // Modal error & success
  const [modalError, setModalError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");

  // Modal loading
  const [modalLoading, setModalLoading] = useState(false);

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const usersPerPage = 10;

  // -----------------------------
  // Fetch Vendors
  // -----------------------------
  const getVendors = async () => {
    setLoading(true);
    try {
      const response = await fetchVendors();
      if (Array.isArray(response.data)) {
        setVendors(response.data);
      } else {
        setVendors([]);
        console.error("Invalid API response:", response);
      }
    } catch (err) {
      console.error("Error fetching vendors:", err);
      setError("Failed to fetch vendors");
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // Fetch Claims (all or by status)
  // -----------------------------
  const fetchClaimsDetails = async (currentStatus) => {
    setLoading(true);
    try {
      const response = await fetchClaims({ status: currentStatus || "" });
      setVendorData(response.data);
    } catch (err) {
      console.error("Error fetching vendor data:", err);
      setError("Failed to load vendor data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getVendors();
    fetchClaimsDetails(); // fetch all claims by default
  }, []);

  // Re-fetch claims whenever status changes
  useEffect(() => {
    fetchClaimsDetails(status);
  }, [status]);

  // If modals close (approval/rejection), re-fetch claims
  useEffect(() => {
    setTransactionId("")
    if (prevShow.current && !show) {
      fetchClaimsDetails(status);
    }
    if (prevDeleteShow.current && !deleteShow) {
      fetchClaimsDetails(status);
    }
    prevShow.current = show;
    prevDeleteShow.current = deleteShow;
  }, [show, deleteShow, status]);

  // -----------------------------
  // Filter data by date + status
  // -----------------------------
  useEffect(() => {
    if (!vendorData || vendorData.length === 0) {
      setFiltered([]);
      return;
    }
    let filteredData = [...vendorData];

    // Filter by date if selected
    if (filterDate) {
      filteredData = filteredData.filter(
        (v) => v.created_at?.split("T")[0] === filterDate
      );
    }
    // Filter by status
    if (status) {
      filteredData = filteredData.filter(
        (v) => v.status.toLowerCase() === status.toLowerCase()
      );
    }
    setFiltered(filteredData);
  }, [filterDate, vendorData, status]);

  // -----------------------------
  // Approve Claim
  // -----------------------------
  const handleApproveClaim = async () => {
    if (!selectedVendor) return;
    if (points <= 0) {
      setModalError("Points must be greater than 0.");
      return;
    }
    setModalLoading(true);
    setModalError(null);

    try {
      await approveClaim(selectedVendor.id, points,transactionId); // pass vendor ID & points
      setSuccess(true);
      setSuccessMessage(
        `Successfully approved ${points} points for ${selectedVendor.vendor_name}!`
      );
      setModalLoading(false);

      // Hide success & close modal after 5 seconds
      setTimeout(() => {
        setSuccess(false);
        setSuccessMessage("");
        setShow(false);
      }, 5000);
    } catch (error) {
      setModalError(error || "Failed to approve claim. Please try again.");
      setModalLoading(false);

      // Hide error after 5 seconds
      setTimeout(() => {
        setModalError(null);
      }, 5000);
    }
  };

  // -----------------------------
  // Reject Claim
  // -----------------------------
  const handleRejectClaim = async () => {
    if (!selectedVendor) return;
    setModalLoading(true);
    setModalError(null);
    try {
      const response = await rejectClaim(selectedVendor.id);
      setSuccess(response.data.message || "Claim rejected successfully!");
      setModalLoading(false);
      setDeleteShow(false);

      // Clear success after 1.8s
      setTimeout(() => {
        setSuccess(null);
      }, 1800);
    } catch (error) {
      setModalError(error || "Failed to reject claim. Please try again.");
      setModalLoading(false);
    }
  };

  // -----------------------------
  // Open Approve Modal
  // -----------------------------
  const handleSelect = (vendor) => {
    setSelectedVendor(vendor);
    setShow(true);
    setPoints(vendor.points);
  };

  // -----------------------------
  // Open Reject Modal
  // -----------------------------
  const handleDeleteShow = (vendor) => {
    setSelectedVendor(vendor);
    setDeleteShow(true);
  };

  // -----------------------------
  // (Optional) If you want to handle a "delete" logic with "changeClaimsStatus"
  // -----------------------------
  const handleDelete = async () => {
    if (selectedVendor) {
      setModalLoading(true);
      setError(null);
      setSuccess(null);
      try {
        const response = await changeClaimsStatus(selectedVendor.id, {
          status: "REJECTED",
          approved: points,
        });
        setSuccess(response.message);
      } catch (err) {
        console.error("Error updating status:", err);
        setModalError("Failed to Approve");
      } finally {
        setModalLoading(false);
        // Close the modal after 1.5 seconds
        setTimeout(() => {
          setDeleteShow(false);
        }, 1500);
      }
    }
  };

  // -----------------------------
  // Helpers for status badge
  // -----------------------------
  const statusVariants = {
    PENDING: "warning",
    APPROVED: "success",
    REJECTED: "danger",
  };

  const getBadgeVariant = (st) =>
    statusVariants[st?.toUpperCase()] || "secondary";

  // -----------------------------
  // Pagination with "filtered"
  // -----------------------------
  const totalPages = Math.ceil(filtered.length / usersPerPage);
  const startIndex = (currentPage - 1) * usersPerPage;
  const currentUsers = filtered.slice(startIndex, startIndex + usersPerPage);

  const handlePageChange = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <main
      className="bg-white"
      style={{
        marginTop: "50px",
        height: "calc(100vh - 60px)",
        overflowY: "auto",
        backgroundSize: "30px 30px",
      }}
    >
      {error && <p className="text-red-500">{error}</p>}

      <div className="mt-4 p-4 border rounded bg-gray-300">
        <Row className="mb-3">
          <Col
            md={3}
            style={{ display: "flex", justifyContent: "space-between", width: "100%" }}
          >
            {/* Filter by Status */}
            <Form.Select
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setCurrentPage(1); // reset pagination on filter
              }}
              style={{ height: "fit-content" }}
            >
              <option value="">All</option>
              <option value="PENDING">Pending</option>
              <option value="APPROVED">Approved</option>
              <option value="REJECTED">Rejected</option>
            </Form.Select>

            {/* Filter by Date */}
            <Form.Group
              style={{
                marginLeft: "40%",
                display: "flex",
                width: "100%",
                minWidth: "fit-content",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              {filterDate && (
                <Badge
                  onClick={() => {
                    setFilterDate("");
                    setCurrentPage(1);
                  }}
                  style={{ cursor: "pointer", marginRight: "8px", marginTop: "8px" }}
                >
                  clear
                </Badge>
              )}
              {/* <p className="mt-2" style={{ fontSize: "1.1rem", marginRight: "3px" }}>
                Select date:
              </p> */}
              <Form.Control
                type="date"
                value={filterDate || ""}
                onChange={(e) => {
                  setFilterDate(e.target.value);
                  setCurrentPage(1);
                }}
                style={{ height: "fit-content" }}
              />
            </Form.Group>
          </Col>
        </Row>

        <div className="table-responsive">
        <div style={{ marginBottom: '10px' }}>
              <strong>Total Users: </strong>{filtered.length}
            </div>
          <Table striped bordered hover className="text-center">
            <thead className="table-light">
              <tr>
                <th style={{ backgroundColor: "#015295", color: "#fff" }}>S.No</th>
                <th style={{ backgroundColor: "#015295", color: "#fff" }}>
                  VENDOR NAME
                </th>
                <th style={{ backgroundColor: "#015295", color: "#fff" }}>DATE</th>
                <th style={{ backgroundColor: "#015295", color: "#fff" }}>STATUS</th>
                <th style={{ backgroundColor: "#015295", color: "#fff" }}>POINTS</th>
              </tr>
            </thead>
            <tbody>
              {currentUsers.length > 0 ? (
                currentUsers.map((d, index) => (
                  <tr key={d.id}>
                    <td>{(currentPage - 1) * usersPerPage + index + 1}</td>
                    <td>{d.vendor_name.toUpperCase()}</td>
                    <td>{d.created_at.split("T")[0]}</td>
                    <td>{d.status}</td>
                    <td>
                      <Badge bg={getBadgeVariant(d.status)} style={{ fontSize: "16px" }}>
                        {d.points}
                      </Badge>
                      {d.status === "PENDING" && (
                        <>
                          <Button
                            size="sm"
                            style={{ marginLeft: "4px" }}
                            onClick={() => handleSelect(d)}
                          >
                            Approve
                          </Button>
                          <Button
                            size="sm"
                            style={{ marginLeft: "4px" }}
                            onClick={() => handleDeleteShow(d)}
                          >
                            Reject
                          </Button>
                        </>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5}>No claims found.</td>
                </tr>
              )}
            </tbody>
          </Table>

          {/* Pagination */}
          {currentUsers.length > 0 && (
            <Pagination className="justify-content-center">
              <Pagination.Prev
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
              />
              {[...Array(totalPages)].map((_, index) => (
                <Pagination.Item
                  key={index + 1}
                  active={index + 1 === currentPage}
                  onClick={() => handlePageChange(index + 1)}
                >
                  {index + 1}
                </Pagination.Item>
              ))}
              <Pagination.Next
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
              />
            </Pagination>
          )}

          {/* Approve Modal */}
          {selectedVendor && (
            <Modal show={show} onHide={() => setShow(false)} centered>
              <Modal.Header closeButton>
                <Modal.Title>Approve points for {selectedVendor.vendor_name}</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                <Form>
                  <Form.Group>
                    <Form.Label>Points to be Approved: {selectedVendor.points}</Form.Label>
                    <Form.Control
                      type="number"
                      value={points}
                      onChange={(e) => setPoints(e.target.value)}
                    />
                  </Form.Group>
                  <Form.Group>
                    <Form.Label>Transaction Id:</Form.Label> 
                    <Form.Control
                      type=""
                      value={transactionId}
                      onChange={(e) => setTransactionId(e.target.value)}
                    />
                  </Form.Group>
                </Form>

                {successMessage && (
                  <div className="alert alert-success text-center mt-3">
                    {successMessage}
                  </div>
                )}

              
                {modalError && (
                  <div className="alert alert-danger text-center mt-3">
                    {modalError}
                  </div>
                )}
              </Modal.Body>
              <Modal.Footer>
                {modalLoading && (
                  <Spinner
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                  />
                )}
                <Button variant="primary" onClick={handleApproveClaim} disabled={modalLoading}>
                  Approve
                </Button>
              </Modal.Footer>
            </Modal>
          )}

          {/* Reject Modal */}
          {selectedVendor && (
            <Modal show={deleteShow} onHide={() => setDeleteShow(false)} centered>
              <Modal.Header closeButton>
                <Modal.Title>Reject {selectedVendor.vendor_name} Request</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                Points to be Rejected: {selectedVendor.points}
                {success && <div className="text-center mt-3">{success}</div>}
                {modalError && <div className="text-center mt-3">{modalError}</div>}
              </Modal.Body>
              <Modal.Footer>
                {modalLoading && (
                  <Spinner
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                  />
                )}
                <Button
                  variant="danger"
                  onClick={handleRejectClaim}
                  disabled={modalLoading}
                >
                  Reject
                </Button>
              </Modal.Footer>
            </Modal>
          )}
        </div>
      </div>

      {/* Overlay Spinner for overall loading, if desired */}
      {loading && (
        <div
          style={{
            width: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100%",
            zIndex: "2000",
          }}
        >
          <Spinner
            as="span"
            animation="border"
            size="sm"
            role="status"
            aria-hidden="true"
          />
        </div>
      )}
    </main>
  );
};

export default AdminVendorTransaction;
