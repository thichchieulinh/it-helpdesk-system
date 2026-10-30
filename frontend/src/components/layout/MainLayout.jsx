import React, { useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CreateTicketModal } from '../tickets/CreateTicketModal';

export const MainLayout = () => {
  const { currentUser } = useAuth();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="flex min-h-screen" style={{ backgroundColor: 'var(--bg)', color: 'var(--text)' }}>
      {/* Sidebar trái cố định 232px */}
      <Sidebar />

      {/* Vùng nội dung chính */}
      <div className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
        {/* Topbar cao 56px */}
        <Header onOpenCreateModal={() => setIsCreateModalOpen(true)} />

        {/* Nội dung cuộn, padding 24px theo quy chuẩn Design System */}
        <main className="flex-1 p-6 overflow-y-auto">
          <div className="max-w-[1400px] mx-auto">
            <Outlet context={{ openCreateModal: () => setIsCreateModalOpen(true) }} />
          </div>
        </main>
      </div>

      {/* Modal Tạo Yêu Cầu Toàn Cục */}
      <CreateTicketModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSuccess={(newTicket) => {
          setIsCreateModalOpen(false);
          // Gửi event để các trang nghe thấy nếu cần refresh
          window.dispatchEvent(new CustomEvent('ticket-created', { detail: newTicket }));
        }}
      />
    </div>
  );
};
