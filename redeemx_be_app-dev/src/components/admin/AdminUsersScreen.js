import React, { useEffect, useRef, useState } from 'react';
import { Button, Pagination, Spinner, Table } from 'react-bootstrap';
import AddNewUserModal from './AddNewUserModal';
import AssignPointsModal from './AssignPointsModal';
import { fetchUsers, createUser } from '../../api/admin';
import SearchBar from './SearchBar';
import '../../styles/AdminUser.css';
import { AiFillEdit } from "react-icons/ai";
import { AiOutlineDelete } from "react-icons/ai";
import AdminUserEditModal from './AdminUserEditModal';
import DeleteModal from './DeleteModal';
import EditModal from './EditModal';

const AdminUsersScreen = () => {
  const [modalShow, setModalShow] = useState(false);
  const [assignModalShow, setAssignModalShow] = useState(false);
  const [addUserModalShow, setAddUserModalShow] = useState(false);
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);
  const [sucessMessage, setSucessMessage] = useState(null);
  const [filteredUser, setFilteredUser] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [deleteShow, setDeleteShow] = useState(false);
  const [editShow, setEditShow] = useState(false);
  const prevModalShow = useRef(modalShow);
  const prevDeleteShow = useRef(deleteShow);
  const prevEditShow = useRef(editShow);


  const [currentPage, setCurrentPage] = useState(1);
  const usersPerPage = 10;

  const loadUsers = async () => {
    setLoading(true);
    try {
      const data = await fetchUsers();
      setUsers(data);
    } catch (error) {
      console.log('Failed to fetch users:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadUsers();
  }, []);
  useEffect(() => {
    if ((prevModalShow.current && !modalShow) || (prevDeleteShow.current && !deleteShow) || (prevEditShow.current && !editShow)) {
      loadUsers(); // Refresh users only when the modal closes
    }
    // Update previous state values for next render
    prevModalShow.current = modalShow;
    prevDeleteShow.current = deleteShow;
    prevEditShow.current = editShow
  }, [modalShow, deleteShow, editShow]);

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
  }, [searchTerm, users]);
  const handleSearch = (searchTerm) => {
    setSearchTerm(searchTerm)
  }
  const handleAssignPoints = (user) => {
    setSelectedUser(user);
    setAssignModalShow(true);
  }
  const handleDelete = (user) => {
    setSelectedUser(user);
    setDeleteShow(true);
  }
  const handleEdit = (user) => {
    setSelectedUser(user);
    setEditShow(true);
  }

  const totalPages = Math.ceil(filteredUser.length / usersPerPage);
  const startIndex = (currentPage - 1) * usersPerPage;
  const currentUsers = filteredUser.slice(startIndex, startIndex + usersPerPage);

  const handlePageChange = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <main className="p-3" style={{
      marginTop: "46px",
      height: "calc(100vh - 60px)",
      overflowY: "auto",
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
        <SearchBar onSearch={handleSearch} />
        <Button onClick={() => setModalShow(true)} style={{ minWidth: 'fit-content', backgroundColor: "#015295" }}>Add New User</Button>
      </div>
      <AddNewUserModal
        show={modalShow}
        onHide={() => setModalShow(false)}
      />

      {loading ? (
        <div className="text-center" style={{ height: '80vh', width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Spinner variant='secondary' />
        </div>
      ) :
        users.length > 0 ? (
          <div className='table-wrapper'>
            <div style={{ marginBottom: '10px' }}>
              <strong>Total Users: </strong>{filteredUser.length}
            </div>
            <Table striped bordered hover responsive="sm" className="table-container">
              <thead >
                <tr >
                  <th style={{ backgroundColor: "#015295", color: "#fff" }}>S.No</th>
                  <th style={{ backgroundColor: "#015295", color: "#fff" }}>EMP ID</th>
                  <th style={{ backgroundColor: "#015295", color: "#fff" }}>NAME</th>
                  <th style={{ backgroundColor: "#015295", color: "#fff" }}>EMAIL</th>
                  <th style={{ backgroundColor: "#015295", color: "#fff" }}>MOBILE NUMBER</th>
                  <th style={{ backgroundColor: "#015295", color: "#fff" }}>USERNAME</th>
                  <th style={{ backgroundColor: "#015295", color: "#fff" }}>ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                {currentUsers.map((user, index) => (
                  <tr key={user.id}>
                    <td>{(currentPage - 1) * usersPerPage + index + 1}</td> {/* S.No */}
                    <td>{user.emp_id}</td>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>{user.mobile_number}</td>
                    <td>{user.username}</td>
                    <td><Button
                      style={{ backgroundColor: "#015295" }} size="sm"
                      onClick={() => handleAssignPoints(user)}>Assign</Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
            <Pagination className="justify-content-center" >
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

            <AssignPointsModal
              show={assignModalShow}
              onHide={() => setAssignModalShow(false)}
              user={selectedUser} />
            <DeleteModal
              show={deleteShow}
              onHide={() => setDeleteShow(false)}
              user={selectedUser}
              type={"user"}
            />
            <EditModal
              show={editShow}
              onHide={() => setEditShow(false)}
              user={selectedUser}
              type={"user"}
            />
          </div>
        ) : (
          <p>No users found.</p>
        )}
    </main>
  );
};

export default AdminUsersScreen;
