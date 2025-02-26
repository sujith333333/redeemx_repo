import React, { useEffect, useRef, useState } from 'react';
import { Button, Table, Container, Row, Col, Spinner, Pagination } from 'react-bootstrap';
import SearchBar from './SearchBar';
import '../../styles/AdminUser.css';
import AddNewVendorModal from './AddNewVendorModal';
import { fetchVendors } from '../../api/vendor';
import { AiFillEdit, AiOutlineDelete } from 'react-icons/ai';
import DeleteModal from './DeleteModal';
import EditVendorDetails from './EditVendorDetails';

const AdminVendorScreen = () => {
  const [modalShow, setModalShow] = useState(false);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // For filtering/search
  const [filteredUser, setFilteredUser] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  // For modals
  const [deleteShow, setDeleteShow] = useState(false);
  const [selectedVendor, setSelectedVendor] = useState(null);
  const [editShow, setEditShow] = useState(false);

  // For detecting modal closure to refresh data
  const prevModalShow = useRef(modalShow);
  const prevDeleteShow = useRef(deleteShow);
  const prevEditShow = useRef(editShow);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const vendorsPerPage = 10;

  // --------------------------------------------------------------------------
  // Fetch vendors
  // --------------------------------------------------------------------------
  const loadUsers = async () => {
    setLoading(true);
    try {
      const data = await fetchVendors();
      setUsers(data.data);
    } catch (error) {
      console.log('Failed to fetch vendors:', error);
      setErrorMessage('Failed to fetch vendors');
    }
    setLoading(false);
  };

  useEffect(() => {
    loadUsers();
  }, []);

  // Reload data after modals close
  useEffect(() => {
    if (
      (prevModalShow.current && !modalShow) ||
      (prevDeleteShow.current && !deleteShow) ||
      (prevEditShow.current && !editShow)
    ) {
      loadUsers();
    }
    prevModalShow.current = modalShow;
    prevDeleteShow.current = deleteShow;
    prevEditShow.current = editShow;
  }, [modalShow, deleteShow, editShow]);

  // --------------------------------------------------------------------------
  // Handle Search
  // --------------------------------------------------------------------------
  useEffect(() => {
    if (searchTerm) {
      const filtered = users.filter((user) => {
        return (
          user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          user.email.toLowerCase().includes(searchTerm.toLowerCase())
        );
      });
      setFilteredUser(filtered);
    } else {
      setFilteredUser(users);
    }

    // Reset to page 1 whenever the search changes
    setCurrentPage(1);
  }, [searchTerm, users]);

  const handleSearch = (searchValue) => {
    setSearchTerm(searchValue);
  };

  // --------------------------------------------------------------------------
  // Pagination Logic
  // --------------------------------------------------------------------------
  const totalPages = Math.ceil(filteredUser.length / vendorsPerPage);
  const startIndex = (currentPage - 1) * vendorsPerPage;
  const currentVendors = filteredUser.slice(startIndex, startIndex + vendorsPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  // --------------------------------------------------------------------------
  // Modals
  // --------------------------------------------------------------------------
  const handleDelete = (vendor) => {
    setSelectedVendor(vendor);
    setDeleteShow(true);
  };

  const handleEdit = (vendor) => {
    setSelectedVendor(vendor);
    setEditShow(true);
  };

  return (
    <Container
      fluid
      className="p-4"
      style={{ marginTop: '60px', height: 'calc(100vh - 60px)', overflowY: 'auto' }}
    >
      {/* Search Bar & Add Vendor Button */}
      <Row className="mb-3 align-items-center">
        <Col xs={12} md={6} className="mb-2 mb-md-0">
          <SearchBar onSearch={handleSearch} />
        </Col>
        <Col xs={12} md={6} className="text-md-end">
          <Button
            variant="primary"
            onClick={() => setModalShow(true)}
            style={{ minWidth: 'fit-content', backgroundColor: '#015295' }}
          >
            Add New Vendor
          </Button>
        </Col>
      </Row>

      {/* Vendor Modal */}
      <AddNewVendorModal show={modalShow} onHide={() => setModalShow(false)} />

      {/* Delete Modal */}
      <DeleteModal
        show={deleteShow}
        onHide={() => setDeleteShow(false)}
        user={selectedVendor}
        type="vendor"
      />

      {/* Edit Vendor Modal */}
      <EditVendorDetails
        show={editShow}
        onHide={() => setEditShow(false)}
        user={selectedVendor}
        type="user"
      />

      {/* Table Section */}
      {loading ? (
        <div
          className="text-center"
          style={{
            width: '100%',
            height: '79vh',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <Spinner animation="border" />
          <p>Loading Vendors...</p>
        </div>
      ) : users.length > 0 ? (
        <div className="table-wrapper">
          <div style={{ marginBottom: '10px' }}>
            <strong>Total Vendors: </strong>
            {filteredUser.length}
          </div>
          <Table striped bordered hover responsive="sm" className="table-container">
            <thead>
              <tr>
                <th style={{ backgroundColor: '#015295', color: '#fff' }}>S.No</th>
                <th style={{ backgroundColor: '#015295', color: '#fff' }}>NAME</th>
                <th style={{ backgroundColor: '#015295', color: '#fff' }}>EMAIL</th>
                <th style={{ backgroundColor: '#015295', color: '#fff' }}>MOBILE NUMBER</th>

              </tr>
            </thead>
            <tbody>
              {currentVendors.map((vendor, index) => (
                <tr key={vendor.id}>
                  {/* Continuous numbering across pages */}
                  <td>{(currentPage - 1) * vendorsPerPage + index + 1}</td>
                  <td>{vendor.name}</td>
                  <td>{vendor.email}</td>
                  <td>{vendor.mobile_number}</td>
                </tr>
              ))}
            </tbody>
          </Table>

          {/* Pagination */}
          {filteredUser.length > 0 && (
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
        </div>
      ) : (
        <p className="text-center">No vendors found.</p>
      )}
    </Container>
  );
};

export default AdminVendorScreen;
