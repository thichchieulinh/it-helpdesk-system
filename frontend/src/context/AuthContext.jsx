import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const savedUser = localStorage.getItem('helpdesk_user');
      return savedUser ? JSON.parse(savedUser) : null;
    } catch (e) {
      console.error('Lỗi khi đọc user từ localStorage:', e);
      return null;
    }
  });

  const [loading, setLoading] = useState(false);

  const login = (userData) => {
    setCurrentUser(userData);
    localStorage.setItem('helpdesk_user', JSON.stringify(userData));
  };

  const logout = () => {
    setCurrentUser(null);
    localStorage.removeItem('helpdesk_user');
  };

  return (
    <AuthContext.Provider value={{ currentUser, login, logout, loading, setLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth phải được sử dụng bên trong AuthProvider');
  }
  return context;
};
