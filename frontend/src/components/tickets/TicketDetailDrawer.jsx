import React, { useState, useEffect, useRef } from 'react';
import axiosClient from '../../api/axiosClient';
import { useAuth } from '../../context/AuthContext';
import { StatusBadge, PriorityBadge, OverdueBadge } from '../common/Badge';
import {
  X,
  Clock,
  User,
  Tag,
  Send,
  Loader2,
  CheckCircle2,
  Archive,
  RotateCcw,
  UserCheck,
  AlertCircle
} from 'lucide-react';

export const TicketDetailDrawer = ({ ticketId, isOpen, onClose, onTicketUpdated }) => {
  const { currentUser } = useAuth();
  const [ticket, setTicket] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [replyText, setReplyText] = useState('');
  const [submittingReply, setSubmittingReply] = useState(false);
  const [updatingStatus, setUpdatingStatus] = useState(false);
  const [error, setError] = useState('');

  const commentsEndRef = useRef(null);

  // Lắng nghe phím ESC để đóng Drawer
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Tải chi tiết ticket và bình luận khi mở Drawer
  useEffect(() => {
    if (isOpen && ticketId) {
      const fetchData = async () => {
        setLoading(true);
        setError('');
        try {
          const [tData, cData] = await Promise.all([
            axiosClient.get(`/tickets/${ticketId}`),
            axiosClient.get(`/tickets/${ticketId}/comments`)
          ]);
          setTicket(tData);
          setComments(cData || []);
        } catch (err) {
          console.error('Lỗi khi tải chi tiết ticket:', err);
          setError('Không thể tải dữ liệu yêu cầu.');
        } finally {
          setLoading(false);
        }
      };
      fetchData();
      setReplyText('');
    }
  }, [isOpen, ticketId]);

  if (!isOpen) return null;

  const role = currentUser?.role;
  const isAgentOrAdmin = role === 'AGENT' || role === 'ADMIN';
  const isCreator = ticket?.requester?.id === currentUser?.id;

  const handleUpdateStatus = async (newStatus, assigneeId = null) => {
    setUpdatingStatus(true);
    setError('');
    try {
      const payload = {
        status: newStatus,
        assigneeId: assigneeId !== null ? assigneeId : (ticket.assignee?.id || null)
      };
      const updated = await axiosClient.patch(`/tickets/${ticket.id}/status`, payload);
      setTicket(updated);
      onTicketUpdated?.(updated);
    } catch (err) {
      console.error('Lỗi cập nhật trạng thái:', err);
      setError(typeof err === 'string' ? err : 'Không thể cập nhật tiến trình.');
    } finally {
      setUpdatingStatus(false);
    }
  };

  const handleSendReply = async (e) => {
    e.preventDefault();
    if (!replyText.trim()) return;

    setSubmittingReply(true);
    try {
      const newComment = await axiosClient.post(`/tickets/${ticket.id}/comments`, {
        userId: currentUser?.id,
        content: replyText.trim()
      });
      setComments((prev) => [...prev, newComment]);
      setReplyText('');
      setTimeout(() => {
        commentsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      console.error('Lỗi gửi phản hồi:', err);
      setError('Lỗi gửi phản hồi.');
    } finally {
      setSubmittingReply(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Mask mờ */}
      <div
        onClick={onClose}
        className="absolute inset-0 bg-black/30 transition-opacity"
      />

      {/* Drawer trượt từ phải sang (rộng tối đa 460px) */}
      <div
        className="absolute inset-y-0 right-0 max-w-[460px] w-full flex flex-col shadow-xl animate-in slide-in-from-right duration-200"
        style={{
          backgroundColor: 'var(--surface)',
          borderLeft: '1px solid var(--line)',
          color: 'var(--text)'
        }}
      >
        {/* Drawer Header */}
        <div
          className="p-4 flex items-center justify-between shrink-0"
          style={{ borderBottom: '1px solid var(--line)', backgroundColor: 'var(--surface)' }}
        >
          <div className="flex items-center gap-2">
            <span
              className="text-[13px] font-[600] font-mono px-2 py-0.5 rounded-[4px]"
              style={{ backgroundColor: 'var(--brand-soft)', color: 'var(--brand)' }}
            >
              {ticket?.ticketCode || '...'}
            </span>
            {ticket && <StatusBadge status={ticket.status} />}
            {ticket && <PriorityBadge priority={ticket.priority} />}
            {ticket?.isOverdue && <OverdueBadge isOverdue={true} />}
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-[6px] hover:bg-slate-100 text-slate-500 hover:text-slate-800 transition-colors"
            title="Đóng (Esc)"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Drawer Body - Cuộn */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {loading ? (
            <div className="py-20 text-center text-[13px]" style={{ color: 'var(--muted)' }}>
              Đang tải chi tiết...
            </div>
          ) : ticket ? (
            <>
              {error && (
                <div
                  className="p-2.5 rounded-[6px] text-[12px] flex items-center gap-1.5"
                  style={{ backgroundColor: 'var(--err-soft)', color: 'var(--err)' }}
                >
                  <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                  <span>{error}</span>
                </div>
              )}

              {/* Tiêu đề & Mô tả */}
              <div>
                <h2 className="text-[16px] font-[600] leading-snug" style={{ color: 'var(--text)' }}>
                  {ticket.title}
                </h2>
                <div
                  className="mt-2 text-[13px] p-3 rounded-[6px] whitespace-pre-line leading-relaxed"
                  style={{ backgroundColor: 'var(--bg)', border: '1px solid var(--line)' }}
                >
                  {ticket.description || 'Không có mô tả chi tiết.'}
                </div>
              </div>

              {/* Danh sách thông tin dạng 2 cột */}
              <div
                className="p-3 rounded-[6px] text-[13px] space-y-2"
                style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--line)' }}
              >
                <div className="flex items-center justify-between">
                  <span style={{ color: 'var(--muted)' }}>Người yêu cầu:</span>
                  <span className="font-[500]">{ticket.requester?.fullName} ({ticket.requester?.department})</span>
                </div>

                <div className="flex items-center justify-between">
                  <span style={{ color: 'var(--muted)' }}>Danh mục:</span>
                  <span className="font-[500]">{ticket.category?.name}</span>
                </div>

                <div className="flex items-center justify-between">
                  <span style={{ color: 'var(--muted)' }}>Phụ trách:</span>
                  <span className="font-[500]">
                    {ticket.assignee ? ticket.assignee.fullName : 'Chưa tiếp nhận'}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span style={{ color: 'var(--muted)' }}>Hạn SLA:</span>
                  <span className={`font-[500] ${ticket.isOverdue ? 'text-[var(--err)] font-[600]' : ''}`}>
                    {ticket.dueDate
                      ? new Date(ticket.dueDate).toLocaleString('vi-VN', {
                          hour: '2-digit',
                          minute: '2-digit',
                          day: '2-digit',
                          month: '2-digit',
                          year: 'numeric'
                        })
                      : 'N/A'}
                  </span>
                </div>
              </div>

              {/* Nút hành động workflow */}
              <div className="space-y-2">
                {ticket.status === 'OPEN' && isAgentOrAdmin && (
                  <button
                    onClick={() => handleUpdateStatus('IN_PROGRESS', currentUser.id)}
                    disabled={updatingStatus}
                    className="w-full h-[34px] rounded-[6px] text-[13px] font-[500] text-white flex items-center justify-center gap-1.5 transition-colors disabled:opacity-50"
                    style={{ backgroundColor: 'var(--brand)' }}
                  >
                    <UserCheck className="w-3.5 h-3.5" />
                    <span>Tiếp nhận yêu cầu</span>
                  </button>
                )}

                {ticket.status === 'IN_PROGRESS' && isAgentOrAdmin && (
                  <button
                    onClick={() => handleUpdateStatus('RESOLVED')}
                    disabled={updatingStatus}
                    className="w-full h-[34px] rounded-[6px] text-[13px] font-[500] text-white flex items-center justify-center gap-1.5 transition-colors disabled:opacity-50"
                    style={{ backgroundColor: 'var(--ok)' }}
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Đánh dấu đã giải quyết</span>
                  </button>
                )}

                {ticket.status === 'RESOLVED' && (isCreator || role === 'ADMIN') && (
                  <button
                    onClick={() => handleUpdateStatus('CLOSED')}
                    disabled={updatingStatus}
                    className="w-full h-[34px] rounded-[6px] text-[13px] font-[500] text-white flex items-center justify-center gap-1.5 transition-colors disabled:opacity-50"
                    style={{ backgroundColor: 'var(--text)' }}
                  >
                    <Archive className="w-3.5 h-3.5" />
                    <span>Xác nhận & Đóng ticket</span>
                  </button>
                )}

                {ticket.status === 'RESOLVED' && isAgentOrAdmin && (
                  <button
                    onClick={() => handleUpdateStatus('IN_PROGRESS')}
                    disabled={updatingStatus}
                    className="w-full h-[34px] rounded-[6px] text-[13px] font-[500] border transition-colors flex items-center justify-center gap-1.5"
                    style={{ borderColor: 'var(--line)', color: 'var(--text)' }}
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>Mở lại yêu cầu</span>
                  </button>
                )}
              </div>

              {/* Timeline lịch sử xử lý & bình luận */}
              <div className="pt-3" style={{ borderTop: '1px solid var(--line)' }}>
                <div className="text-[13px] font-[600] mb-3" style={{ color: 'var(--text)' }}>
                  Lịch sử xử lý & Phản hồi ({comments.length})
                </div>

                <div className="relative pl-5 space-y-4 before:content-[''] before:absolute before:left-[7px] before:top-2 before:bottom-2 before:w-[2px] before:bg-[var(--line)]">
                  {/* Điểm bắt đầu tạo ticket */}
                  <div className="relative text-[12px]">
                    <span
                      className="absolute -left-[19px] top-1 w-[8px] h-[8px] rounded-full"
                      style={{ backgroundColor: 'var(--brand)' }}
                    />
                    <div className="font-[500]">{ticket.requester?.fullName} đã tạo yêu cầu</div>
                    <div style={{ color: 'var(--muted)' }}>
                      {new Date(ticket.createdAt).toLocaleString('vi-VN')}
                    </div>
                  </div>

                  {/* Bình luận */}
                  {comments.map((c) => (
                    <div key={c.id} className="relative text-[12px]">
                      <span
                        className="absolute -left-[19px] top-1 w-[8px] h-[8px] rounded-full"
                        style={{
                          backgroundColor: c.user?.role === 'AGENT' || c.user?.role === 'ADMIN'
                            ? 'var(--brand)'
                            : 'var(--ok)'
                        }}
                      />
                      <div className="flex items-center justify-between">
                        <span className="font-[600]">{c.user?.fullName}</span>
                        <span style={{ color: 'var(--muted)' }}>
                          {c.createdAt ? new Date(c.createdAt).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }) : ''}
                        </span>
                      </div>
                      <div
                        className="mt-1 p-2 rounded-[6px] leading-relaxed whitespace-pre-line"
                        style={{ backgroundColor: 'var(--bg)', color: 'var(--text)' }}
                      >
                        {c.content}
                      </div>
                    </div>
                  ))}
                  <div ref={commentsEndRef} />
                </div>
              </div>
            </>
          ) : null}
        </div>

        {/* Ô phản hồi cố định ở đáy */}
        <div
          className="p-3 shrink-0"
          style={{ borderTop: '1px solid var(--line)', backgroundColor: 'var(--surface)' }}
        >
          <form onSubmit={handleSendReply} className="flex gap-2">
            <input
              type="text"
              value={replyText}
              onChange={(e) => setReplyText(e.target.value)}
              placeholder="Nhập nội dung phản hồi..."
              className="flex-1 px-3 py-1.5 text-[13px] rounded-[6px] focus:outline-none"
              style={{
                backgroundColor: 'var(--bg)',
                border: '1px solid var(--line)',
                color: 'var(--text)'
              }}
            />
            <button
              type="submit"
              disabled={submittingReply || !replyText.trim()}
              className="h-[34px] px-3 rounded-[6px] text-[13px] font-[500] text-white flex items-center gap-1 transition-colors disabled:opacity-40"
              style={{ backgroundColor: 'var(--brand)' }}
            >
              {submittingReply ? (
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <>
                  <span>Gửi</span>
                  <Send className="w-3 h-3" />
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
