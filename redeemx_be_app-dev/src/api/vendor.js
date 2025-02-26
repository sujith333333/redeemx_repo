import axios from 'axios';
import { getToken } from './auth';
const API_BASE_URL = 'http://54.167.159.114:8000';

export const getVendorData = async () => {
  try {
    const token = getToken();
    if (!token) {
      throw new Error('No token found');
    }
    const response = await axios.get(`${API_BASE_URL}/api/v1/transaction/vendor/points`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data.data;
  } catch (error) {
    console.error('Error fetching employee points:', error);
    if (error.response) {
      throw new Error(
        error.response.data.error || 'Failed to fetch employee points.'
      );
    } else {
      throw new Error('No response from the server. Please try again later.');
    }
  }
};

export const getAllPoints = async (filters) => {
  try {
    const token = getToken();
    if (!token) throw new Error("Vendor is not authenticated.");
 
    const params = new URLSearchParams();
 
    // Check for 'day' filter, send as is
    if (filters.day) {
      params.append("day", filters.day); // Send the day filter if available
    }
    // If 'month' filter is provided, calculate start_date and end_date
    else if (filters.month) {
      const startDate = new Date(filters.month + "-01");
      const endDate = new Date(
        startDate.getFullYear(),
        startDate.getMonth() + 1,
        0
      );
 
      // Convert to Unix timestamp (milliseconds since Jan 1, 1970)
      params.append("start_date", startDate.getTime());
      params.append("end_date", endDate.getTime());
    }
 
    console.log("Sending parameters:", params.toString());
 
    const response = await axios.get(
      `${API_BASE_URL}/api/v1/vendor/all/points/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        params: params, // Sending query parameters
      }
    );
 
    return response.data;
  } catch (error) {
    console.error("Error fetching points:", error);
    return null;
  }
};

export const fetchVendorQRCode = async () => {
  try {
    const token = getToken();
    const response = await axios.get(`${API_BASE_URL}/api/v1/vendor/get/vendors-details`, {
      headers: { Authorization: `Bearer ${token}` },
    });
 
    return response.data;
  } catch (error) {
    console.error('Error fetching QR Code:', error);
    throw new Error('Error fetching QR Code');
  }
};

export const fetchVendors = async () => {
  try {
    const token = getToken();
    const response = await axios.get(`${API_BASE_URL}/api/v1/vendor/get_all/vendors`, {
      headers: { Authorization: `Bearer ${token}` },
    });
 
    return response.data;
  } catch (error) {
    console.error('Error fetching vendors:', error);
    throw error;
  }
};
export const fetchTransactions = async (startDate, endDate, limit = 10, offset = 0) => {
  try {
    const token = getToken();
    if (!token) {
      throw new Error("No token found");
    }

    // Construct query parameters dynamically
    let queryParams = new URLSearchParams();
    if (startDate) queryParams.append("start_date", startDate);
    if (endDate) queryParams.append("end_date", endDate);
    queryParams.append("limit", limit);
    queryParams.append("offset", offset);

    const url = `${API_BASE_URL}/api/v1/vendor/all/transactions?${queryParams.toString()}`;

    const response = await axios.get(url, {
      headers: { Authorization: `Bearer ${token}` },
    });

    return {
      data: response.data.data,
      total: response.data.metadata?.total || 0,
      limit: response.data.metadata?.limit || limit,
      offset: response.data.metadata?.offset || offset,
    };
  } catch (error) {
    console.error("Error fetching debited transactions:", error);
    throw error;
  }
};

export const fetchCreditedTransactions = async (startDate, endDate, limit = 10, offset = 0) => {
  try {
    const token = getToken();
    if (!token) {
      throw new Error("No token found");
    }

    // Construct query parameters dynamically
    let queryParams = new URLSearchParams();
    if (startDate) queryParams.append("start_date", startDate);
    if (endDate) queryParams.append("end_date", endDate);
    queryParams.append("limit", limit);
    queryParams.append("offset", offset);

    const url = `${API_BASE_URL}/api/v1/vendor/user/transactions?${queryParams.toString()}`;

    const response = await axios.get(url, {
      headers: { Authorization: `Bearer ${token}` },
    });

    return {
      data: response.data.data,
      total: response.data.metadata?.total || 0,
      limit: response.data.metadata?.limit || limit,
      offset: response.data.metadata?.offset || offset,
    };
  } catch (error) {
    console.error("Error fetching debited transactions:", error);
    throw error;
  }
};

export const fetchDebitedTransactions = async (startDate, endDate, limit = 10, offset = 0) => {
  try {
    const token = getToken();
    if (!token) {
      throw new Error("No token found");
    }

    // Construct query parameters dynamically
    let queryParams = new URLSearchParams();
    if (startDate) queryParams.append("start_date", startDate);
    if (endDate) queryParams.append("end_date", endDate);
    queryParams.append("limit", limit);
    queryParams.append("offset", offset);

    const url = `${API_BASE_URL}/api/v1/vendor/admin/transactions?${queryParams.toString()}`;

    const response = await axios.get(url, {
      headers: { Authorization: `Bearer ${token}` },
    });

    return {
      data: response.data.data,
      total: response.data.metadata?.total || 0,
      limit: response.data.metadata?.limit || limit,
      offset: response.data.metadata?.offset || offset,
    };
  } catch (error) {
    console.error("Error fetching debited transactions:", error);
    throw error;
  }
};

export const getVendorClaimsData = async (param) => {
  if (param === "All") {
    param = null
  }
  try{
    const token = getToken();
    if (!token) {
      throw new Error('No token found');
    }
  const response = await axios.get(`${API_BASE_URL}/api/v1/vendor/claim/requests`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    params: {
      status: param
    },
  });
  return response.data.data;
} catch (error) {
  console.error('Error fetching employee points:', error);
  if (error.response) {
    throw new Error(
      error.response.data.error || 'Failed to fetch employee points.'
    );
  } else {
    throw new Error('No response from the server. Please try again later.');
  }
}
}

export const vendorClaimRegistration = async (body) => {
  try {
    const token = getToken();
    if (!token) {
      throw new Error('No token found');
    }
    const response = await axios.post(`${API_BASE_URL}/api/v1/vendor/claim/request`, body, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data.data;
  } catch (error) {
    console.error('Error fetching employee points:', error);
    if (error.response) {
      throw new Error(
        error.response.data.error || 'Failed to fetch employee points.'
      );
    } else {
      throw new Error('No response from the server. Please try again later.');
    }
  } 
}
export const getVendorPoints = async () => {
  try {
  const token = getToken();
 if(!token) {
  throw new Error('No Token found') 
 }
 const response = await axios.get(`${API_BASE_URL}/api/v1/vendor/reports`,  {
  headers: {
    Authorization: `Bearer ${token}` 
  }
 })
 return response.data.data; 
  }
  catch(error) {
    console.log('Error fetching vendor points', error); 
if(error.response) {
  throw new Error(error.response.data.error || 'Failed to fetch Vendor Points') 
}
else {
  throw new Error('No response from the server. Please try again later.')
}
  }
}

export const  getVendorClaimsPoints = async () => {
  try {
 const token = getToken()
 if(!token) {
  throw new Error('No Token Found')
 }
 const response = await axios.get(`${API_BASE_URL}/api/v1/vendor/claim/points`, {
  headers: {
    Authorization: `Bearer ${token}` 
  }
 })
 return response.data.data; 
  }
  catch(error) {
    console.log('Error fetching vendor points', error) 
  }
}

