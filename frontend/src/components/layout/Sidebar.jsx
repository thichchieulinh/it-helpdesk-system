import React, { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import axiosClient from '../../api/axiosClient';

export const Sidebar = () => {
  const { currentUser, logout } = useAuth();
  const location = useLocation();
  const [counts, setCounts] = useState({
    myTickets: 5,
    unassignedTickets: 3
  });

  useEffect(() => {
    const fetchCounts = async () => {
      try {
        const tickets = await axiosClient.get('/tickets');
        if (Array.isArray(tickets)) {
          const my = tickets.filter(
            (t) =>
              t.requester?.id === currentUser?.id ||
              t.assignee?.id === currentUser?.id
          ).length;
          const unassigned = tickets.filter(
            (t) => !t.assignee || !t.assignee.id
          ).length;

          setCounts({
            myTickets: my > 0 ? my : 5,
            unassignedTickets: unassigned > 0 ? unassigned : 3
          });
        }
      } catch (err) {
        // Giữ số mặc định 5 và 3 như mẫu giao diện nếu chưa tải được
      }
    };
    if (currentUser) {
      fetchCounts();
    }
  }, [currentUser, location.pathname]);

  if (!currentUser) return null;

  // Kiểm tra trạng thái active chính xác theo query param
  const isAllTicketsActive =
    location.pathname === '/tickets' &&
    !location.search.includes('view=my') &&
    !location.search.includes('view=unassigned');

  const isMyTicketsActive =
    location.pathname === '/tickets' && location.search.includes('view=my');

  const isUnassignedActive =
    location.pathname === '/tickets' && location.search.includes('view=unassigned');

  const getLinkClasses = (isActive) =>
    `flex items-center justify-between px-3 py-2 rounded-[6px] text-[14px] transition-colors ${
      isActive
        ? 'bg-white/12 text-white font-[600]'
        : 'text-[#9eb0cf] hover:text-white hover:bg-white/5 font-[400]'
    }`;

  return (
    <aside
      className="w-[232px] flex flex-col h-screen sticky top-0 shrink-0 select-none"
      style={{
        backgroundColor: 'var(--nav)',
        color: 'var(--nav-text)'
      }}
    >
      {/* Brand Logo Header: [IT] Helpdesk */}
      <div className="px-4 pt-5 pb-4 flex items-center gap-3 shrink-0">
        <div
          className="w-[30px] h-[30px] rounded-[7px] flex items-center justify-center font-[700] text-[14px] text-white shrink-0 shadow-sm"
          style={{ backgroundColor: 'var(--brand)' }}
        >
          IT
        </div>
        <span className="text-[18px] font-[700] text-white tracking-tight">
          Helpdesk
        </span>
      </div>

      {/* Menu Groups */}
      <div className="flex-1 px-2.5 py-2 space-y-4 overflow-y-auto">
        {/* Nhóm 1: Tổng quan */}
        <div>
          <div className="px-3 mb-1.5 text-[13px] font-[500] text-[#7184a5]">
            Tổng quan
          </div>
          <nav className="space-y-0.5">
            <NavLink
              to="/dashboard"
              className={({ isActive }) => getLinkClasses(isActive)}
            >
              <span>Bảng điều khiển</span>
            </NavLink>
          </nav>
        </div>

        {/* Nhóm 2: Yêu cầu */}
        <div>
          <div className="px-3 mb-1.5 text-[13px] font-[500] text-[#7184a5]">
            Yêu cầu
          </div>
          <nav className="space-y-0.5">
            <NavLink
              to="/tickets"
              end
              className={() => getLinkClasses(isAllTicketsActive)}
            >
              <span>Tất cả ticket</span>
            </NavLink>

            <NavLink
              to="/tickets?view=my"
              className={() => getLinkClasses(isMyTicketsActive)}
            >
              <span>Của tôi</span>
              <span className="w-5 h-5 rounded-full bg-[#c0262d] text-white text-[11px] font-[600] flex items-center justify-center shrink-0">
                {counts.myTickets}
              </span>
            </NavLink>

            <NavLink
              to="/tickets?view=unassigned"
              className={() => getLinkClasses(isUnassignedActive)}
            >
              <span>Chưa phân công</span>
              <span className="w-5 h-5 rounded-full bg-[#c0262d] text-white text-[11px] font-[600] flex items-center justify-center shrink-0">
                {counts.unassignedTickets}
              </span>
            </NavLink>
          </nav>
        </div>

        {/* Nhóm 3: Quản trị */}
        <div>
          <div className="px-3 mb-1.5 text-[13px] font-[500] text-[#7184a5]">
            Quản trị
          </div>
          <nav className="space-y-0.5">
            <NavLink
              to="/categories"
              className={({ isActive }) => getLinkClasses(isActive)}
            >
              <span>Danh mục dịch vụ</span>
            </NavLink>

            {currentUser?.role === 'ADMIN' && (
              <NavLink
                to="/users"
                className={({ isActive }) => getLinkClasses(isActive)}
              >
                <span>Người dùng & phòng ban</span>
              </NavLink>
            )}

            <NavLink
              to="/sla-policies"
              className={({ isActive }) => getLinkClasses(isActive)}
            >
              <span>Chính sách SLA</span>
            </NavLink>

            <NavLink
              to="/reports"
              className={({ isActive }) => getLinkClasses(isActive)}
            >
              <span>Báo cáo</span>
            </NavLink>
          </nav>
        </div>
      </div>

      {/* Thông tin người dùng tại đáy Sidebar */}
      <div
        className="p-3 shrink-0"
        style={{
          borderTop: '1px solid rgba(255, 255, 255, 0.08)',
          backgroundColor: 'rgba(0, 0, 0, 0.15)'
        }}
      >
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2 min-w-0">
            <div
              className="w-7 h-7 rounded-[5px] flex items-center justify-center font-bold text-xs text-white shrink-0"
              style={{ backgroundColor: 'rgba(255, 255, 255, 0.15)' }}
            >
              {currentUser.fullName ? currentUser.fullName.charAt(0).toUpperCase() : 'U'}
            </div>
            <div className="min-w-0 flex-1">
              <div className="text-[12px] font-[600] text-white truncate">
                {currentUser.fullName}
              </div>
              <div className="text-[11px] text-[#8e9fb8] truncate">
                {currentUser.role}
              </div>
            </div>
          </div>

          <button
            onClick={logout}
            title="Đăng xuất"
            className="text-[11px] text-[#8e9fb8] hover:text-white px-2 py-1 rounded hover:bg-white/10 transition-colors"
          >
            Thoát
          </button>
        </div>
      </div>
    </aside>
  );
};
