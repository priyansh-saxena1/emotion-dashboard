import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider, useAppContext } from './contexts/AppContext';
import { LoginView } from './views/LoginView';
import { DashboardView } from './views/DashboardView';

function AppContent() {
  const { state, dispatch } = useAppContext();

  useEffect(() => {
    // Check if user is logged in by trying to fetch user data
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch('/api/user/top-tracks');
      if (response.ok) {
        dispatch({ type: 'SET_USER', payload: { isLoggedIn: true } });
      }
    } catch (error) {
      // User is not logged in, which is fine
      dispatch({ type: 'SET_USER', payload: { isLoggedIn: false } });
    }
  };

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={state.user.isLoggedIn ? <Navigate to="/" /> : <LoginView />} 
        />
        <Route 
          path="/" 
          element={state.user.isLoggedIn ? <DashboardView /> : <Navigate to="/login" />} 
        />
      </Routes>
    </Router>
  );
}

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;