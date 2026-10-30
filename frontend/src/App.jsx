import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { MainLayout } from './components/layout/MainLayout';
import { Login } from './pages/Login';
import { TicketList } from './pages/TicketList';
import { TicketDetail } from './pages/TicketDetail';
import { DashboardPage } from './pages/DashboardPage';
import { UserManagement } from './pages/UserManagement';
import { ServiceCategories } from './pages/ServiceCategories';
import { SlaPoliciesPage } from './pages/SlaPoliciesPage';
import { ReportsPage } from './pages/ReportsPage';

export function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public Route: Login */}
            <Route path="/login" element={<Login />} />

            {/* Protected Routes: Main Layout */}
            <Route path="/" element={<MainLayout />}>
              <Route index element={<Navigate to="/tickets" replace />} />
              <Route path="tickets" element={<TicketList />} />
              <Route path="tickets/:id" element={<TicketDetail />} />
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="users" element={<UserManagement />} />
              <Route path="categories" element={<ServiceCategories />} />
              <Route path="sla-policies" element={<SlaPoliciesPage />} />
              <Route path="reports" element={<ReportsPage />} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
