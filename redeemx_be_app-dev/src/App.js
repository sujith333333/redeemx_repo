import React, { useEffect, useState } from 'react';
import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import { getToken, getUserRole } from './api/auth';
import AdminHomeScreen from './components/admin/AdminHomeScreen';
import ChangePassword from './components/ChangePassword';
import Header from './components/common/Header';
import VendorHeader from './components/common/VendorHeader';
import Login from './components/Login';
import UserHistoryScreen from './components/user/UserHistoryScreen';
import UserHomeScreen from './components/user/UserHomeScreen';
import UserScannerScreen from './components/user/UserScannerScreen';
import VendorHistoryScreen from './components/vendor/VendorHistoryScreen';
import VendorHomeScreen from './components/vendor/VendorHomeScreen';
import VendorScannerScreen from './components/vendor/VendorScannerScreen';
import VendorClaimScreen from './components/vendor/VendorClaimScreen';
import './App.css';
const App = () => {
  const [token, setToken] = useState(null);
  const [userType, setUserType] = useState(null);

  useEffect(() => {
    const storedToken = getToken(); 
    const role = getUserRole(); 

    if (storedToken) {
      setToken(storedToken);
        if (role.is_user) {
        setUserType('user');
      } else if (role.is_vendor) {
        setUserType('vendor');
      } else if (role.is_admin) {
        setUserType('admin');
      } else {
        setUserType(null);
      }
    }
  }, [token]);

  

  return (
    <Router>
      <div className="app">
      {userType === 'user' && <Header/>}
      {userType === 'vendor' && <VendorHeader/>}
        <Routes>
          {!token ? (
            <>
              <Route path="/login" element={<Login setToken={setToken} />} />
              <Route path="*" element={<Navigate to="/login" />} /> 
            </>
          ) : (
            <>
              {userType === 'admin' && (
                <Route path="/admin/home" element={<AdminHomeScreen />} />
              )}
              {userType === 'user' && (
                <>
                  <Route path="/user/home" element={<UserHomeScreen />} />
                  <Route path="/user/scanner" element={<UserScannerScreen />} />
                  <Route path="/user/history" element={<UserHistoryScreen />} />
                </>
              )}
              {userType === 'vendor' && (
                <>
                  <Route path="/vendor/home" element={<VendorHomeScreen />} />
                  <Route path="/vendor/scanner" element={<VendorScannerScreen />} />
                  <Route path="/vendor/claims" element={<VendorClaimScreen />} />
                  <Route path="/vendor/history" element={<VendorHistoryScreen />} />
                </>
              )}
              
              <Route path="/change-password" element={<ChangePassword />} /> 
              <Route path="*"
      element={
      <Navigate to={userType === "user" ? "/user/scanner" : `/${userType}/home`} />
  }
/>

            </>
          )}
        </Routes>
        
      </div>
    </Router>
  );
};

export default App;
