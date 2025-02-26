import React, { useEffect, useState } from 'react'
import { Alert, Button, Form, Modal, Spinner } from 'react-bootstrap'
import { EditUser } from '../../api/admin'

const EditModal = ({ show, onHide, user ,type}) => {
    const [formData,setFormData]=useState({
        "username": "",
  "name": "",
  "email": "",
  "emp_id": "",
  "mobile_number": ""
    })

    const [loading, setLoading] = useState(false);
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        if (user) {
            setErrorMessage("");
            setSuccessMessage("");
            setFormData({
                username: user.username || '',
                name: user.name || '',
                email: user.email || '',
                emp_id: user.emp_id || '',
                mobile_number: user.mobile_number || ''
            });
        }
    }, [user]);
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleDelete= async()=>{
        console.log(user.id,"user");
        
        if (!user || type !== "user") return;
        
        if(type == 'user'){
            setLoading(true);
            setSuccessMessage('');
            setErrorMessage('');
            const updatedData = Object.keys(formData).reduce((acc, key) => {
                if (formData[key] !== user[key]) {
                    acc[key] = formData[key];
                }
                return acc;
            }, {});
        console.log(updatedData);
        
            if (Object.keys(updatedData).length === 0) {
                setErrorMessage("No changes detected.");
                setLoading(false);
                return;
            }
    
            try {
                const response = await EditUser(user?.id,updatedData);
                console.log(response,"res");
                if (response.success) {
                    setTimeout(() => {
                        onHide();
                    }, 1500);
                    setSuccessMessage('User details updated successfully!');
                    
                } else {
                    setErrorMessage(response.message || 'Failed to update user.');
                    console.log(errorMessage,"err");
                    
                }
            } catch (error) {
                setErrorMessage(error?.message|| error?.error[0] || 'Something went wrong.');
            } finally {
                setLoading(false);
            }
        }
    }

  return (
    <Modal show={show} onHide={onHide} size="md" centered>
<Modal.Header closeButton>
<Modal.Title>Edit {user?.name} Details</Modal.Title>
</Modal.Header>
<Modal.Body>
                <Form>
                    {[
                        { label: 'Username', name: 'username', type: 'text' },
                        { label: 'Name', name: 'name', type: 'text' },
                        { label: 'Email', name: 'email', type: 'email' },
                        { label: 'Employee ID', name: 'emp_id', type: 'text' },
                        { label: 'Mobile Number', name: 'mobile_number', type: 'number' }
                    ].map((field) => (
                        <Form.Group className="mb-3" key={field.name}>
                            <Form.Label>{field.label}</Form.Label>
                            <Form.Control
                                type={field.type}
                                name={field.name}
                                value={formData[field.name]}
                                onChange={handleChange}
                            />
                        </Form.Group>
                    ))}
                </Form>
                {successMessage && <Alert>{successMessage}</Alert>}
                {errorMessage && <Alert>{errorMessage}</Alert>}

            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={onHide}>Cancel</Button>
                <Button variant="primary" onClick={handleDelete} disabled={loading}>
                    {loading ? <Spinner animation="border" size="sm" /> : 'Update User'}
                </Button>
            </Modal.Footer>
</Modal>
    
  )
}

export default EditModal