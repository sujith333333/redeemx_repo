import React, { useEffect, useState } from "react"; 
import { Button, Pagination, Spinner, Table } from "react-bootstrap";
import { getVendorPoints } from "../../api/vendor";

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const reportsPerPage = 10;

  useEffect(() => {
    const fetchReports = async () => {
      try { 
        setLoading(true);
        const data = await getVendorPoints(); 
        const formattedReports = data.map((report) => ({
          id: report.id,
          date: new Date(report.date).toLocaleString("en-GB"), 
          userRedeemed: report.points_redeemed_by_employees, 
          vendorBalance: report.vendor_balance_points,
          vendorRedeemed: report.points_redeemed_by_vendor,
        }));
        setReports(formattedReports);
      } catch (error) {
        console.error("Error fetching reports:", error.message);
      } finally {
        setLoading(false);
      }
    };
 
    fetchReports();
  }, []);

  const totalPages = Math.ceil(reports.length / reportsPerPage);
  const startIndex = (currentPage - 1) * reportsPerPage;
  const currentReports = reports.slice(startIndex, startIndex + reportsPerPage);

  const handlePageChange = (pageNumber) => setCurrentPage(pageNumber);

  const downloadCSV = () => {
    const headers = ["S.No", "Date", "User Redeemed", "Vendor Balance", "Vendor Redeemed"];
    const csvRows = [
      headers.join(","), 
      ...reports.map((report, index) =>
        [
          index + 1, 
          `"${report.date}"`, 
          report.userRedeemed,
          `$${report.vendorBalance}`,
          `$${report.vendorRedeemed}`,
        ].join(",")
      ),
    ];

    const csvString = csvRows.join("\n");
    const blob = new Blob([csvString], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "reports.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return ( 
    <main
      className="p-3"
      style={{ marginTop: "46px", height: "calc(100vh - 60px)", overflowY: "auto" }}
    >
      <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "10px" }}>
        <Button style={{ backgroundColor: "#015295", minWidth: "fit-content" }} onClick={downloadCSV}>
          Download
        </Button>
      </div>

      {loading ? (
        <div className="text-center" style={{ height: "80vh", width: "100%", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Spinner variant="secondary" />
        </div>
      ) : reports.length > 0 ? (
        <div className="table-wrapper">
          <Table striped bordered hover responsive="sm" className="table-container">
            <thead>
              <tr>
                <th style={{ backgroundColor: "#015295", color: "#fff" }}>S.No</th>
                <th style={{ backgroundColor: "#015295", color: "#fff" }}>Date</th>
                <th style={{ backgroundColor: "#015295", color: "#fff" }}>User Redeemed</th>
                <th style={{ backgroundColor: "#015295", color: "#fff" }}>Vendor Balance</th>
                <th style={{ backgroundColor: "#015295", color: "#fff" }}>Vendor Redeemed</th>
              </tr>
            </thead>
            <tbody>
              {currentReports.map((report, index) => (
                <tr key={report.id}>
                  <td>{(currentPage - 1) * reportsPerPage + index + 1}</td>
                  <td>{report.date}</td>
                  <td>{report.userRedeemed}</td>
                  <td>{report.vendorBalance}</td>
                  <td>{report.vendorRedeemed}</td>
                </tr>
              ))}
            </tbody>
          </Table>
          <Pagination className="justify-content-center">
            <Pagination.Prev onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1} />
            {[...Array(totalPages)].map((_, index) => (
              <Pagination.Item key={index + 1} active={index + 1 === currentPage} onClick={() => handlePageChange(index + 1)}>
                {index + 1}
              </Pagination.Item>
            ))}
            <Pagination.Next onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages} />
          </Pagination>
        </div>
      ) : (
        <p>No reports found.</p>
      )}
    </main>
  );
};

export default Reports;
 