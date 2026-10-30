import React, { useState, useEffect, useCallback } from 'react';
import { useSearchParams, useOutletContext } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axiosClient from '../api/axiosClient';
import { StatusBadge, PriorityBadge, OverdueBadge } from '../components/common/Badge';
import { TicketDetailDrawer } from '../components/tickets/TicketDetailDrawer';
import {
  Search,
  RefreshCw,
  Clock,
  X,
  Inbox
} from 'lucide-react';

export const TicketList = () => {
  const { currentUser } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();
  const outletCtx = useOutletContext();

  const isEmployee = currentUser?.role === 'EMPLOYEE';

  const urlView = searchParams.get('view') || '';
  const urlStatus = searchParams.get('status') || '';
  const urlPriority = searchParams.get('priority') || '';
  const urlSearch = searchParams.get('search') || '';
  const urlOverdue = searchParams.get('overdue') === 'true';

  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState(urlSearch);
  const [activeTab, setActiveTab] = useState(urlStatus || 'ALL');
  const [filterPriority, setFilterPriority] = useState(urlPriority);
  const [onlyOverdue, setOnlyOverdue] = useState(urlOverdue);

  // Drawer chi tiết ticket
  const [selectedTicketId, setSelectedTicketId] = useState(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  // Lắng nghe khi có ticket mới tạo từ Header
  useEffect(() => {
    const handleTicketCreated = () => fetchTickets();
    window.addEventListener('ticket-created', handleTicketCreated);
    return () => window.removeEventListener('ticket-created', handleTicketCreated);
  }, []);

  useEffect(() => {
    setActiveTab(urlStatus || 'ALL');
    setFilterPriority(urlPriority);
    setSearchTerm(urlSearch);
    setOnlyOverdue(urlOverdue);
  }, [urlStatus, urlPriority, urlSearch, urlOverdue]);

  const fetchTickets = useCallback(async () => {
    setLoading(true);
    try {
      const params = {};
      if (activeTab !== 'ALL') {
        params.status = activeTab;
      }
      if (filterPriority) {
        params.priority = filterPriority;
      }
      if (searchTerm.trim()) {
        params.search = searchTerm.trim();
      }
      if (isEmployee && currentUser?.id) {
        params.requesterId = currentUser.id;
      }

      const data = await axiosClient.get('/tickets', { params });
      let result = data;
      if (onlyOverdue) {
        result = data.filter((t) => t.isOverdue);
      }
      if (urlView === 'my') {
        result = result.filter(
          (t) =>
            t.requester?.id === currentUser?.id ||
            t.assignee?.id === currentUser?.id
        );
      } else if (urlView === 'unassigned') {
        result = result.filter((t) => !t.assignee || !t.assignee.id);
      }
      setTickets(result);
    } catch (err) {
      console.error('Lỗi khi tải ticket:', err);
    } finally {
      setLoading(false);
    }
  }, [activeTab, filterPriority, searchTerm, onlyOverdue, isEmployee, currentUser?.id, urlView]);

  useEffect(() => {
    fetchTickets();
  }, [fetchTickets]);

  const handleRowClick = (ticketId) => {
    setSelectedTicketId(ticketId);
    setIsDrawerOpen(true);
  };

  const handleRowKeyDown = (e, ticketId) => {
    if (e.key === 'Enter') {
      handleRowClick(ticketId);
    }
  };

  // Tính số lượng cho các tab
  const countAll = tickets.length;
  const countOpen = tickets.filter((t) => t.status === 'OPEN').length;
  const countInProgress = tickets.filter((t) => t.status === 'IN_PROGRESS').length;
  const countResolved = tickets.filter((t) => t.status === 'RESOLVED').length;
  const countClosed = tickets.filter((t) => t.status === 'CLOSED').length;

  return (
    <div className="space-y-4">
      {/* Tiêu đề trang & Thanh công cụ */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-[20px] font-[600] tracking-tight" style={{ color: 'var(--text)' }}>
            {urlView === 'my'
              ? 'Yêu cầu của tôi'
              : urlView === 'unassigned'
              ? 'Yêu cầu chưa phân công'
              : isEmployee
              ? 'Yêu cầu của tôi'
              : 'Tất cả ticket'}
          </h1>
          <p className="text-[13px] mt-0.5" style={{ color: 'var(--muted)' }}>
            {urlView === 'my'
              ? 'Các phiếu hỗ trợ do bạn tạo hoặc được phân công phụ trách xử lý'
              : urlView === 'unassigned'
              ? 'Danh sách các yêu cầu đang chờ tiếp nhận và phân công kỹ thuật viên IT'
              : isEmployee
              ? 'Quản lý và theo dõi tiến trình xử lý các yêu cầu hỗ trợ của bạn'
              : 'Theo dõi hàng đợi tiếp nhận, xử lý sự cố và giám sát cam kết SLA'}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchTickets}
            title="Làm mới danh sách"
            className="h-[34px] px-3 rounded-[6px] text-[13px] font-[500] flex items-center gap-1.5 transition-colors"
            style={{
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--line)',
              color: 'var(--text)'
            }}
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Làm mới</span>
          </button>
        </div>
      </div>

      {/* Tabs lọc theo trạng thái kèm số đếm & Bộ lọc nhanh */}
      <div
        className="rounded-[8px] p-3 space-y-3"
        style={{
          backgroundColor: 'var(--surface)',
          border: '1px solid var(--line)'
        }}
      >
        <div className="flex flex-wrap items-center justify-between gap-2 border-b pb-2.5" style={{ borderColor: 'var(--line)' }}>
          {/* Tab lọc có số đếm */}
          <div className="flex items-center gap-1 overflow-x-auto text-[13px]">
            {[
              { key: 'ALL', label: 'Tất cả' },
              { key: 'OPEN', label: 'Mới' },
              { key: 'IN_PROGRESS', label: 'Đang xử lý' },
              { key: 'RESOLVED', label: 'Đã giải quyết' },
              { key: 'CLOSED', label: 'Đã đóng' }
            ].map((tab) => {
              const isActive = activeTab === tab.key;
              return (
                <button
                  key={tab.key}
                  onClick={() => {
                    setActiveTab(tab.key);
                    setOnlyOverdue(false);
                  }}
                  className="px-3 py-1.5 rounded-[6px] text-[13px] font-[500] flex items-center gap-1.5 transition-colors whitespace-nowrap"
                  style={{
                    backgroundColor: isActive ? 'var(--brand-soft)' : 'transparent',
                    color: isActive ? 'var(--brand)' : 'var(--muted)'
                  }}
                >
                  <span>{tab.label}</span>
                </button>
              );
            })}

            {!isEmployee && (
              <button
                onClick={() => setOnlyOverdue(!onlyOverdue)}
                className="px-3 py-1.5 rounded-[6px] text-[13px] font-[500] flex items-center gap-1.5 transition-colors whitespace-nowrap"
                style={{
                  backgroundColor: onlyOverdue ? 'var(--err-soft)' : 'transparent',
                  color: onlyOverdue ? 'var(--err)' : 'var(--muted)'
                }}
              >
                <span>Trễ SLA</span>
              </button>
            )}
          </div>

          {/* Lọc theo mức ưu tiên */}
          <div className="flex items-center gap-2">
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="h-[32px] px-2.5 text-[12px] rounded-[6px] focus:outline-none"
              style={{
                backgroundColor: 'var(--bg)',
                border: '1px solid var(--line)',
                color: 'var(--text)'
              }}
            >
              <option value="">Tất cả mức ưu tiên</option>
              <option value="CRITICAL">Khẩn cấp</option>
              <option value="HIGH">Cao</option>
              <option value="MEDIUM">Trung bình</option>
              <option value="LOW">Thấp</option>
            </select>
          </div>
        </div>

        {/* Ô tìm kiếm từ khóa */}
        <div className="relative">
          <Search
            className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
            style={{ color: 'var(--muted)' }}
          />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Tìm theo tiêu đề, mã ticket, mô tả hoặc phòng ban..."
            className="w-full h-[34px] pl-9 pr-8 text-[13px] rounded-[6px] focus:outline-none"
            style={{
              backgroundColor: 'var(--bg)',
              border: '1px solid var(--line)',
              color: 'var(--text)'
            }}
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>

      {/* Bảng Ticket theo chuẩn Design System */}
      <div
        className="rounded-[8px] overflow-hidden"
        style={{
          backgroundColor: 'var(--surface)',
          border: '1px solid var(--line)'
        }}
      >
        {loading ? (
          <div className="py-20 text-center text-[13px]" style={{ color: 'var(--muted)' }}>
            Đang tải dữ liệu ticket...
          </div>
        ) : tickets.length === 0 ? (
          <div className="py-16 text-center text-[13px] flex flex-col items-center justify-center space-y-1.5" style={{ color: 'var(--muted)' }}>
            <Inbox className="w-8 h-8 opacity-40 mb-1" />
            <div className="font-[600]" style={{ color: 'var(--text)' }}>
              Không có ticket phù hợp
            </div>
            <p className="text-[12px]">
              Thử đổi bộ lọc hoặc từ khóa tìm kiếm.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-[13px]">
              <thead
                style={{
                  backgroundColor: 'var(--bg)',
                  borderBottom: '1px solid var(--line)',
                  color: 'var(--muted)'
                }}
              >
                <tr className="text-[12px] uppercase font-[600]">
                  <th className="py-2.5 px-3.5 w-24">Mã</th>
                  <th className="py-2.5 px-3.5">Tiêu đề yêu cầu</th>
                  <th className="py-2.5 px-3.5 whitespace-nowrap">Danh mục</th>
                  <th className="py-2.5 px-3.5 whitespace-nowrap">Mức ưu tiên</th>
                  <th className="py-2.5 px-3.5 whitespace-nowrap">Trạng thái</th>
                  <th className="py-2.5 px-3.5 whitespace-nowrap">Người yêu cầu</th>
                  <th className="py-2.5 px-3.5 whitespace-nowrap">Phụ trách</th>
                  <th className="py-2.5 px-3.5 whitespace-nowrap">Hạn SLA</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map((t) => (
                  <tr
                    key={t.id}
                    tabIndex={0}
                    onClick={() => handleRowClick(t.id)}
                    onKeyDown={(e) => handleRowKeyDown(e, t.id)}
                    className="cursor-pointer transition-colors focus:outline-none"
                    style={{
                      borderBottom: '1px solid var(--line)',
                      height: '44px'
                    }}
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--bg)')}
                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
                  >
                    <td className="py-2.5 px-3.5 font-mono font-[500] whitespace-nowrap" style={{ color: 'var(--brand)' }}>
                      {t.ticketCode}
                    </td>

                    <td className="py-2.5 px-3.5 font-[500] max-w-sm" style={{ color: 'var(--text)' }}>
                      <div className="line-clamp-2 leading-snug">{t.title}</div>
                    </td>

                    <td className="py-2.5 px-3.5 whitespace-nowrap" style={{ color: 'var(--muted)' }}>
                      {t.category?.name || 'N/A'}
                    </td>

                    <td className="py-2.5 px-3.5 whitespace-nowrap">
                      <PriorityBadge priority={t.priority} />
                    </td>

                    <td className="py-2.5 px-3.5 whitespace-nowrap">
                      <StatusBadge status={t.status} />
                    </td>

                    <td className="py-2.5 px-3.5 whitespace-nowrap" style={{ color: 'var(--text)' }}>
                      <div>{t.requester?.fullName}</div>
                      <div className="text-[11px]" style={{ color: 'var(--muted)' }}>{t.requester?.department}</div>
                    </td>

                    <td className="py-2.5 px-3.5 whitespace-nowrap" style={{ color: 'var(--text)' }}>
                      {t.assignee ? (
                        <span>{t.assignee.fullName}</span>
                      ) : (
                        <span className="italic text-[12px]" style={{ color: 'var(--muted)' }}>
                          Chưa có
                        </span>
                      )}
                    </td>

                    <td className="py-2.5 px-3.5 whitespace-nowrap">
                      {t.dueDate ? (
                        <div className="flex items-center gap-1.5">
                          <span className={`text-[12px] ${t.isOverdue ? 'text-[var(--err)] font-[600]' : ''}`}>
                            {new Date(t.dueDate).toLocaleString('vi-VN', {
                              hour: '2-digit',
                              minute: '2-digit',
                              day: '2-digit',
                              month: '2-digit'
                            })}
                          </span>
                          {t.isOverdue && <OverdueBadge isOverdue={true} />}
                        </div>
                      ) : (
                        <span style={{ color: 'var(--muted)' }}>N/A</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div
          className="p-3 text-[12px] flex items-center justify-between"
          style={{
            backgroundColor: 'var(--bg)',
            color: 'var(--muted)',
            borderTop: '1px solid var(--line)'
          }}
        >
          <span>Hiển thị <strong>{tickets.length}</strong> yêu cầu</span>
          <span className="font-mono text-[11px]">Bấm vào hàng để mở chi tiết (Drawer)</span>
        </div>
      </div>

      {/* Drawer trượt từ phải sang */}
      <TicketDetailDrawer
        ticketId={selectedTicketId}
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        onTicketUpdated={() => fetchTickets()}
      />
    </div>
  );
};
