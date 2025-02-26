import React, { useEffect, useState } from 'react'
import { Alert, Button, Modal, Spinner } from 'react-bootstrap'
import { DeleteUser, DeleteVendor } from '../../api/admin';

const DeleteModal = ({ show, onHide,user,type }) => {
    const [loading, setLoading] = useState(false);
      const [successMessage, setSuccessMessage] = useState('');
      const [errorMessage, setErrorMessage] = useState(null);
      
      useEffect(() => {
        setSuccessMessage("");
        setErrorMessage("");
      }, []);

  const handleDelete = async () => {
    if (!user || (type !== "user" && type !== "vendor")) return;
console.log(user);

    setLoading(true);
    setSuccessMessage('');
    setErrorMessage('');
    // try {
    //   const res = await DeleteUser(user.id);  
    //   setSuccessMessage(res.message || 'User deleted successfully');
    //   console.log(res);
      
    //   setTimeout(() => onHide(), 1500); 
    // } catch (error) {
    //   console.error(error);
    //   setErrorMessage(error?.data?.error || 'No user found or deletion failed');
    // } finally {
    //   setLoading(false);
    // }
    try {
        let res;
        if (type === "user") {
          res = await DeleteUser(user.id);
        } else if (type === "vendor") {
            console.log(user.id);   
          res = await DeleteVendor(user.id);
        }
        setSuccessMessage(res.message || `${type} deleted successfully`);
        console.log(res);
  
        setTimeout(() => onHide(), 1500);
      } catch (error) {
        console.error(error.response.data,"mes");
        setErrorMessage(error?.data?.error || error?.response?.data?.error ||`No ${type} found or deletion failed`);
      } finally {
        setLoading(false);
      }

  };

  return (
    <Modal show={show} onHide={onHide} size="md" centered>
<Modal.Header closeButton>
<Modal.Title>Delete </Modal.Title>
</Modal.Header>
<Modal.Body style={{display:'flex',flexDirection:'column'}}>
Delete {user?.name} details
</Modal.Body>
{successMessage && <Alert>{successMessage}</Alert>}
{errorMessage && <Alert>{errorMessage}</Alert>}
<Modal.Footer>
<Button variant="primary" onClick={handleDelete} >
  {loading ? <Spinner animation="border" size="sm" /> : 'Confirm Delete'}
  {/* Confirm Delete */}
  </Button>
</Modal.Footer>
</Modal>
  )
}

export default DeleteModal