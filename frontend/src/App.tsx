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
    console.log('🔐 [AUTH] Checking authentication status...');
    console.log('🔐 [AUTH] Current cookies:', document.cookie);
    
    try {
      const backendUrl = 'http://127.0.0.1:8000';
      const response = await fetch(`${backendUrl}/api/user/top-tracks`, {
        credentials: 'include',
        headers: {
          'Accept': 'application/json',
        }
      });
      
      console.log('🔐 [AUTH] Auth check response status:', response.status);
      
      if (response.ok) {
        console.log('🔐 [AUTH] User is authenticated');
        dispatch({ type: 'SET_USER', payload: { isLoggedIn: true } });
      } else {
        console.log('🔐 [AUTH] User is not authenticated (response not ok)');
        dispatch({ type: 'SET_USER', payload: { isLoggedIn: false } });
      }
    } catch (error) {
      console.log('🔐 [AUTH] User is not authenticated (error):', error);
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