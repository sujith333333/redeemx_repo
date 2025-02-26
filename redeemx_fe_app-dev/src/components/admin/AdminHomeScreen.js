import React, { useEffect, useState } from "react";
import { Button, Row, Col } from "react-bootstrap";
import {
  AiOutlineUser,
  AiOutlineFileDone,
  AiFillEdit,
  AiOutlineLogout,
  AiOutlineMenu,
  AiOutlineDown,
  AiOutlineUp,
  AiOutlineFileText
} from "react-icons/ai";
import { MdDashboard } from 'react-icons/md';
import { Route, Router, Routes, useNavigate } from "react-router-dom";
import AdminDashboard from "./AdminDashboard";
import AdminUsersScreen from "./AdminUsersScreen";
import AdminVendorScreen from "./AdminVendorScreen";
import AdminVendorTransaction from "./AdminVendorTransaction";
import ChangePassword from "../ChangePassword";
import Reports from "./Reports";

const AdminHomeScreen = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isExpanded, setIsExpanded] = useState(false);
  const [visibleSection, setVisibleSection] = useState("dashboard");

  const handleButtonClick = (section) => {
    setVisibleSection(section);
  };

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_type");
    window.location.href = "/login";
  };

  return (
    <div className="d-flex">
      <aside
        className={`bg-light text-dark p-4 d-flex flex-column gap-3 ${
          isSidebarOpen ? "d-block" : "d-none"
        }`}
        style={{
          position: "fixed",
          maxWidth: "fit-content",
          width: "250px",
          height: "100%",
          overflowY: "auto",
          overflowX: "hidden",
          zIndex: 1000,
          transform: isSidebarOpen ? "translateX(0)" : "translateX(-100%)",
          transition: "transform 0.3s ease-in-out",
          background: "linear-gradient(to bottom, #f1f1f1, #e3e3e3)"
        }}
      >
        <div className="d-flex justify-content-between align-items-center">
          <img height={60} src="/images/ajalogo.png" alt="logo" style={{marginLeft: "-25px"}} /> 
          <h3 className="text-2xl font-bold" style={{ color: "#015295", marginLeft: "-25px" }}> 
            RedeemX
          </h3>
        </div>
        <nav className="d-flex flex-column align-items-start gap-2" style={{ width: "100%", padding: "14px" }}>
          <Button
            variant="light"
            className={`d-flex align-items-center justify-content-center py-2 ${visibleSection === "dashboard" ? "active" : ""}`}
            style={{ width: "100%", minWidth: "fit-content" }}
            onClick={() => handleButtonClick("dashboard")}
          >
            <MdDashboard />
            Dashboard
          </Button>
          <Button
            variant="light"
            className={`d-flex align-items-center w-100 gap-2 ${visibleSection === "users" ? "active" : ""}`}
            onClick={() => handleButtonClick("users")}
          >
            <AiOutlineUser /> Users
          </Button>
          <Button
            variant="light"
            className={`d-flex align-items-center gap-2 ${visibleSection === "vendors" ? "active" : ""}`}
            style={{ width: "100%", minWidth: "fit-content" }}
            onClick={() => setIsExpanded(!isExpanded)}
          >
            <AiOutlineFileDone /> Vendors
            {isExpanded ? <AiOutlineUp className="mt-1 ms-5" size={12} /> : <AiOutlineDown className="mt-1 ms-5" size={12} />}
          </Button>
          {isExpanded && (
            <Row className="mt-1 d-flex flex-column align-items-center" style={{ marginLeft: "24px"}}> 
              <Col className="mb-2">
                <Button
                  variant="light"
                  className={`text-dark p-1 ${visibleSection === "Vendor List" ? "active" : ""}`}
                  onClick={() => handleButtonClick("Vendor List")}
                >
                  Vendor List
                </Button>
              </Col>
              <Col>
                <Button
                  variant="light"
                  className={`text-dark p-1 ${visibleSection === "Vendor Transactions" ? "active" : ""}`}
                  onClick={() => handleButtonClick("Vendor Transactions")}
                >
                  Vendor Transactions
                </Button>
              </Col>
            </Row>
          )}
          <Button
            variant="light"
            className={`d-flex align-items-center justify-content-center py-2 gap-1 ${visibleSection === "Change Password" ? "active" : ""}`}
            style={{ width: "100%", minWidth: "fit-content" }}
            onClick={() => handleButtonClick("Change Password")}
          >
            <AiFillEdit />
            Change Password
          </Button>
          <Button
            variant="light"
            className={`d-flex align-items-center justify-content-center py-2 gap-1 ${visibleSection === "Reports" ? "active" : ""}`}
            style={{ width: "100%", minWidth: "fit-content" }}
            onClick={() => handleButtonClick("Reports")} 
          >
          <AiOutlineFileText />
            Reports 
          </Button>
          <Button className="d-flex align-items-center gap-2" variant="light" onClick={toggleSidebar}>
            <AiOutlineLogout /> Close
          </Button>
        </nav>

        <Button variant="danger" className="d-flex align-items-center gap-2 mt-auto" onClick={handleLogout}>
          <AiOutlineLogout /> Logout
        </Button>
      </aside>

      <div
        className="flex-grow-1 bg-light"
        style={{
          marginLeft: isSidebarOpen ? "250px" : "0",
          position: "relative",
          transition: "margin-left 0.3s"
        }}
      >
        <header
          className="bg-white d-flex align-items-center p-3"
          style={{
            position: "fixed",
            width: isSidebarOpen ? "calc(100% - 250px)" : "100%",
            background: "linear-gradient(to right, #f0f0f0, #d0d0d0)"
          }}
        >
          <div className={`bg-light text-dark ${isSidebarOpen ? "d-none" : "d-block"}`}>
            <Button variant="primary" className="d-flex align-items-center" onClick={toggleSidebar} style={{ left: "20px", backgroundColor: "#015295",}}>
              <AiOutlineMenu />
            </Button>
          </div>
          <div style={{ width: "100%" }}>
            <h3 className="text-2xl font-bold text-center" style={{ color: '#015295' }}>{visibleSection.toUpperCase()}</h3>
          </div>
        </header>

        <main className="p-4" style={{ minHeight: "fit-content", overflow: "hidden" }}>
          {visibleSection === "dashboard" && <AdminDashboard />}
          {visibleSection === "users" && <AdminUsersScreen />}
          {visibleSection === "Vendor List" && <AdminVendorScreen />}
          {visibleSection === "Vendor Transactions" && <AdminVendorTransaction />}
          {visibleSection === "Change Password" && <ChangePassword />}
          {visibleSection === "Reports" && <Reports />}
        </main>
      </div>
    </div>
  );
};

export default AdminHomeScreen; 