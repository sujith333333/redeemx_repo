import axios from 'axios';

import { getToken } from './auth'; 
import { BiBody } from 'react-icons/bi';
const API_BASE_URL = 'http://54.167.159.114:8000';


export const uploadFileAPI = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const token = getToken(); 
    if (!token) {
      throw new Error('No token found');
    }

    // Assuming you want to upload the file via POST request
    const response = await axios.post(`${API_BASE_URL}/api/v1/transaction/user-data/upload/transaction`, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data', // Set the content type for file upload
      },
    });

    return response.data;
  } catch (error) {
    console.error("Error uploading file:", error);
    throw error;
  }
};

export const fetchUsers = async () => {
  const token = getToken(); 
    if (!token) {
      throw new Error('No token found');
    }
  try {
    const response = await axios.get(`${API_BASE_URL}/api/v1/user/get_all/users`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    return response.data.data;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

export const createUser = async (userData) => {
  const token = getToken(); 
    if (!token) {
      throw new Error('No token found');
    }
  try {
    const response = await axios.post(`${API_BASE_URL}/api/v1/user/register`, userData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    
    console.error('Error creating user:', error);
    throw error;
  }
};

export const assignPoints = async (user_id, points, description) => {
  const token = getToken();
  if (!token) {
    throw new Error('No token found');
  }

  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/v1/transaction/admin/user/transaction`,
      { user_id, points, description },
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("API Error:", error);

    if (error.response ) {
      throw (error.response.data.error || "Failed to assign points.");
    } else {
      throw ("An unexpected error occurred.");
    }
  }
};

export const AddNewVendor = async (vendor) => {
  const token = getToken(); 
    if (!token) {
      throw new Error('No token found');
    }
  try {
    const response = await axios.post(`${API_BASE_URL}/api/v1/vendor/register`, vendor, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating user:', error);
    throw error;
  }
};

export const DeleteUser = async (user_id) => {
  const token = getToken(); 
    if (!token) {
      throw new Error('No token found');
    }
  try {
    const response = await axios.delete(`${API_BASE_URL}/api/v1/user/delete-user/${user_id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    // console.error('Error deleting user:', error);
    throw error;
  }
};

export const EditUser=async(user_id,user)=>{
  const token = getToken(); 
    if (!token) {
      throw new Error('No token found');
    }
  try {
    const response = await axios.patch(`${API_BASE_URL}/api/v1/user/update-user/${user_id}`,
      user,
       {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    // console.error('Error deleting user:', error);
    throw error;
  }
}

export const EditVendor=async(vendor_id,vendor)=>{
  const token = getToken(); 
    if (!token) {
      throw new Error('No token found');
    }
  try {
    const response = await axios.patch(`${API_BASE_URL}/api/v1/vendor/update-vendor/${vendor_id}`,
      vendor,
       {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}

export const DeleteVendor = async (vendor_id) => {
  const token = getToken(); 
    if (!token) {
      throw new Error('No token found');
    }
  try {
    const response = await axios.delete(`${API_BASE_URL}/api/v1/vendor/delete-vendor/${vendor_id}`,
      {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    // console.error('Error deleting user:', error);
    throw error;
  }
};

export const fetchClaims = async (request = {}) => { 
  const token = getToken();
  if (!token) {
    throw new Error("No token found");
  }

  try {
    const response = await axios.get(`${API_BASE_URL}/api/v1/vendor/claims/by/admin`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      request
    });

    return response.data;
  } catch (error) {
    console.error("Error fetching claims:", error.response?.data || error);
    throw error;
  }
};

export const approveClaim = async (claimId, approvedPoints = null, transaction_reference_id) => {
  const token = getToken();
  if (!token) {
    throw new Error("No token found");
  }

  try {
    const url = `${API_BASE_URL}/api/v1/vendor/admin/approve/${claimId}`;

    // Prepare request payload
    // const body = approvedPoints !== null ? { approved_points: approvedPoints } : {};
    const body = {
      ...(approvedPoints !== null && { approved_points: approvedPoints }),
      ...(transaction_reference_id !== null && { transaction_reference_id }),
    };

    const response = await axios.put(url, body, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    return response.data;
  } catch (error) {
    if (error.response) {
      // Backend responded with an error (4xx, 5xx status codes)
      throw error.response?.data?.error || "Failed to approve points";
    }
    throw error;
  }
};


export const rejectClaim = async (claimId) => {
  const token = getToken();
  if (!token) {
    throw new Error("No token found");
  }

  try {
    const response = await axios.put(`${API_BASE_URL}/api/v1/vendor/admin/reject/${claimId}`, null, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    return response.data;
  } catch (error) {
    console.error("Error rejecting claim:", error.response?.data || error);
    throw error;
  }
};

export const changeClaimsStatus = async (claim_id,request={}) => {  // Default to empty object if no request params are provided
  const token = getToken();
  if (!token) {
    throw new Error("No token found");
  }

  try {
    const response = await axios.put(`${API_BASE_URL}/api/v1/vendor/admin/approve/${claim_id}`, 
      request,
      {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      }
    });

    return response.data;
  } catch (error) {
    console.error("Error in claims:", error.response?.data || error);
    throw error;
  }
};

export const fetchAdminTransactions = async ({ start_date, end_date } = {}) => {
  try {
    const token = getToken();
    if (!token) {
      throw new Error("No token found");
    }

    const params = {};
    if (start_date) params.start_date = new Date(start_date).toISOString();
    if (end_date) params.end_date = new Date(end_date).toISOString();

    const response = await axios.get(`${API_BASE_URL}/api/v1/transaction/overallpoints`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      params,
    });

    return response.data;
  } catch (error) {
    console.error("Error fetching admin transactions:", error.response?.data || error);
    throw error;
  }
};

export const fetchMonthlyTransactions = async (month) => {
  try {
    const token = getToken();
    if (!token) {
      throw new Error("No token found");
    }

    const response = await axios.get(`${API_BASE_URL}/api/v1/transaction/monthlypoints/`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      params: { month }, // Send selected month
    });

    return response.data;
  } catch (error) {
    console.error("Error fetching monthly transactions:", error.response?.data || error);
    throw error;
  }
};


