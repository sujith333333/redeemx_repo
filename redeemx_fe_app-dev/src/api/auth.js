import axios from 'axios';

const API_BASE_URL = 'http://54.167.159.114:8000';


// Login API function to authenticate the user and store the token and user type
export const loginApi = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/v1/auth/login`, data);

    const { token, user_type } = response.data.data; // Assuming the API returns token and user_type

    // Store token and user type in localStorage
    localStorage.setItem('token', token);
    localStorage.setItem('user_type', user_type); // Store user_type directly
    
    return response;
  } catch (error) {
    // Check if the error is an Axios error and if the backend provided a response
    if (error.response) {
      // Backend responded with an error (4xx, 5xx status codes)
      throw error.response.data.error || "Invalid Username or Password"
    } else if (error.request) {
      // No response was received from the backend (e.g., network error)
      throw {
        message: 'No response from server. Please try again later.',
      };
    } else {
      // Something else happened while setting up the request
      throw {
        message: 'An error occurred while processing your request. Please try again.',
      };
    }
  }
};

// Function to get the token from localStorage
export const getToken = () => localStorage.getItem('token');

// Function to get the user's role based on user_type in localStorage
export const getUserRole = () => {
  const user_type = localStorage.getItem('user_type');
  return {
    is_user: user_type === 'user',
    is_admin: user_type === 'admin',
    is_vendor: user_type === 'vendor',
  };
};

// Function to remove token and user data from localStorage during logout
export const removeToken = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user_type');
  window.location.href = '/login';
};


