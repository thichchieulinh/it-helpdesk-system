import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import axiosClient from '../api/axiosClient';
import {
  Ticket,
  Plus,
  Clock,
  AlertTriangle,
  CheckCircle2,
  Search,
  Filter,
  User as UserIcon,
  RefreshCw,
  Tag
} from 'lucide-react';

export const TicketsPage = () => {
  const { currentUser } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchTickets = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await axiosClient.get('/tickets');
      setTickets(data);
    } catch (err) {
      console.error('Lỗi khi tải danh sách ticket:', err);
      setError('Không thể tải dữ liệu từ máy chủ backend (Port 8080).');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'OPEN':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
            Mới tiếp nhận
          </span>
        );
      case 'IN_PROGRESS':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-600"></span>
            Đang xử lý
          </span>
        );
      case 'RESOLVED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
            Đã giải quyết
          </span>
        );
      case 'CLOSED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-600 border border-slate-200">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-400"></span>
            Đã đóng
          </span>
        );
      default:
        return <span>{status}</span>;
    }
  };

  const getPriorityBadge = (priority) => {
    switch (priority) {
      case 'CRITICAL':
        return <span className="text-xs font-semibold text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">Khẩn cấp</span>;
      case 'HIGH':
        return <span className="text-xs font-semibold text-orange-600 bg-orange-50 px-2 py-0.5 rounded border border-orange-200">Cao</span>;
      case 'MEDIUM':
        return <span className="text-xs font-medium text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">Trung bình</span>;
      case 'LOW':
      default:
        return <span className="text-xs font-medium text-slate-600 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">Thấp</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Danh sách Yêu cầu Hỗ trợ
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Xin chào <span className="font-semibold text-slate-700">{currentUser?.fullName}</span>, bạn đang đăng nhập với quyền{' '}
            <span className="font-semibold text-indigo-600">{currentUser?.role}</span>.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchTickets}
            title="Làm mới dữ liệu"
            className="p-2 text-slate-500 hover:text-slate-800 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-colors shadow-sm cursor-pointer"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          <button
            className="inline-flex items-center gap-2 px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-sm font-semibold rounded-xl shadow-sm transition-colors cursor-pointer"
          >
            <Plus className="w-4 h-4" />
            <span>Tạo yêu cầu mới</span>
          </button>
        </div>
      </div>

      {/* Thông báo lỗi nếu có */}
      {error && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-sm text-red-700 flex items-center justify-between">
          <span>{error}</span>
          <button onClick={fetchTickets} className="font-semibold underline cursor-pointer">Thử lại</button>
        </div>
      )}

      {/* Bảng dữ liệu Ticket từ Backend */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex items-center justify-between gap-4">
          <div className="text-sm font-semibold text-slate-800 flex items-center gap-2">
            <Ticket className="w-4 h-4 text-indigo-600" />
            <span>Danh sách sự cố kỹ thuật ({tickets.length})</span>
          </div>
          <span className="text-xs text-slate-400">Dữ liệu thời gian thực từ Spring Boot REST API</span>
        </div>

        {loading ? (
          <div className="py-16 text-center text-slate-400 text-sm">
            <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-indigo-600" />
            <span>Đang tải danh sách từ Backend...</span>
          </div>
        ) : tickets.length === 0 ? (
          <div className="py-16 text-center text-slate-400 text-sm">
            Chưa có yêu cầu hỗ trợ nào trong hệ thống.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-600">
              <thead className="bg-slate-50/70 border-b border-slate-100 text-xs uppercase font-semibold text-slate-400 tracking-wider">
                <tr>
                  <th className="py-3 px-4">Mã phiếu</th>
                  <th className="py-3 px-4">Tiêu đề sự cố</th>
                  <th className="py-3 px-4">Danh mục</th>
                  <th className="py-3 px-4">Độ ưu tiên</th>
                  <th className="py-3 px-4">Trạng thái</th>
                  <th className="py-3 px-4">Người yêu cầu</th>
                  <th className="py-3 px-4">Kỹ thuật viên phụ trách</th>
                  <th className="py-3 px-4">Hạn xử lý (SLA)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {tickets.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-3.5 px-4 font-mono font-semibold text-xs text-indigo-600">
                      {t.ticketCode}
                    </td>
                    <td className="py-3.5 px-4 font-medium text-slate-900 max-w-xs truncate">
                      {t.title}
                    </td>
                    <td className="py-3.5 px-4 text-xs text-slate-600">
                      <span className="inline-flex items-center gap-1">
                        <Tag className="w-3 h-3 text-slate-400" />
                        {t.category?.name || 'N/A'}
                      </span>
                    </td>
                    <td className="py-3.5 px-4">
                      {getPriorityBadge(t.priority)}
                    </td>
                    <td className="py-3.5 px-4">
                      {getStatusBadge(t.status)}
                    </td>
                    <td className="py-3.5 px-4 text-xs text-slate-700">
                      <div className="font-medium">{t.requester?.fullName}</div>
                      <div className="text-[11px] text-slate-400">{t.requester?.department}</div>
                    </td>
                    <td className="py-3.5 px-4 text-xs text-slate-700">
                      {t.assignee ? (
                        <div>
                          <div className="font-medium text-slate-900">{t.assignee.fullName}</div>
                          <div className="text-[11px] text-slate-400">IT Support</div>
                        </div>
                      ) : (
                        <span className="text-slate-400 italic">Chưa tiếp nhận</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-xs">
                      {t.dueDate ? (
                        <div className="flex items-center gap-1">
                          <Clock className="w-3 h-3 text-slate-400" />
                          <span className={t.isOverdue ? 'text-rose-600 font-semibold' : 'text-slate-600'}>
                            {new Date(t.dueDate).toLocaleString('vi-VN', {
                              hour: '2-digit',
                              minute: '2-digit',
                              day: '2-digit',
                              month: '2-digit'
                            })}
                          </span>
                          {t.isOverdue && (
                            <span className="text-[10px] font-bold text-rose-700 bg-rose-50 px-1.5 py-0.5 rounded border border-rose-200">
                              Quá hạn
                            </span>
                          )}
                        </div>
                      ) : (
                        <span className="text-slate-400">N/A</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
