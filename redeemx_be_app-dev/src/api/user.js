import axios from "axios";
import { getToken } from "./auth";

const API_BASE_URL = "http://54.167.159.114:8000";

export const getAllPoints = async (filters) => {
  try {
    const token = getToken();
    if (!token) throw new Error("User is not authenticated.");

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
      `${API_BASE_URL}/api/v1/user/all/points/`,
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

export const getEmployeeData = async () => {
  try {
    const token = getToken();
    if (!token) {
      throw new Error("No token found");
    }

    const response = await axios.get(
      `${API_BASE_URL}/api/v1/transaction/user/points`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    return response.data.data;
  } catch (error) {
    console.error("Error fetching employee points:", error);

    // Handle backend errors with proper message
    if (error.response) {
      throw new Error(
        error.response.data.error || "Failed to fetch employee points."
      );
    } else {
      throw new Error("No response from the server. Please try again later.");
    }
  }
};

export const changePassword = async (oldPassword, newPassword) => {
  try {
    const token = getToken();
    if (!token) {
      throw new Error("No token found");
    }

    const response = await axios.patch(
      `${API_BASE_URL}/api/v1/user/change-password`,
      {
        old_password: oldPassword,
        new_password: newPassword,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error("Error changing password:", error);
    throw error;
  }
};

export const sendPointsToVendor = async (vendor_name, points) => {
  try {
    const token = getToken(); // Fetch the token from auth.js
    if (!token) throw new Error("User is not authenticated.");
    const response = await axios.post(
      `${API_BASE_URL}/api/v1/transaction/user/vendor/transaction`,
      { vendor_name, points },
      {
        headers: {
          Authorization: `Bearer ${token}`, // Send token in Authorization header
        },
      }
    );
    return response.data; // Return the response from the backend
  } catch (error) {
    console.error("Error sending points to vendor:", error);
    throw new Error(
      (error.response && error.response.data && error.response.data.error) ||
        "Error sending points to vendor."
    );
  }
};

export const getVendors = async () => {
  try {
    const token = getToken();
    if (!token) throw new Error("User is not authenticated.");

    const response = await axios.get(
      `${API_BASE_URL}/api/v1/user/vendor/details`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    return response.data || [];
  } catch (error) {
    console.error("Error fetching vendors:", error);
    throw new Error("Failed to fetch vendors.");
  }
};


export const fetchUserTransactions = async (startDate, endDate) => {
  return fetchTransactions('recent-transactions', startDate, endDate);
};

export const fetchUserCreditTransactions = async (startDate, endDate) => {
  return fetchTransactions('credit-transactions', startDate, endDate);
};

export const fetchUserDebitTransactions = async (startDate, endDate) => {
  return fetchTransactions('debit-transactions', startDate, endDate);
};

const fetchTransactions = async (endpoint, startDate, endDate) => {
  try {
    const token = getToken();
    if (!token) {
      throw new Error("No token found");
    }

    const params = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;

    const response = await axios.get(`${API_BASE_URL}/api/v1/user/${endpoint}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params,
    });

    console.log("API Response:", response.data);
    return response.data.data;
  } catch (error) {
    console.error(`Error fetching ${endpoint}:`, error);
    throw error;
  }
};

