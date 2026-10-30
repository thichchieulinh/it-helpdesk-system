import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import axiosClient from '../api/axiosClient';
import { StatusBadge, PriorityBadge, OverdueBadge } from '../components/common/Badge';
import { CommentSection } from '../components/tickets/CommentSection';
import { TicketWorkflowActions } from '../components/tickets/TicketWorkflowActions';
import {
  ArrowLeft,
  Clock,
  User as UserIcon,
  Tag,
  AlertTriangle,
  RefreshCw,
  Mail,
  Building,
  CheckCircle2,
  Share2
} from 'lucide-react';

export const TicketDetail = () => {
  const { id } = useParams();

  const [ticket, setTicket] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [copied, setCopied] = useState(false);

  const fetchTicketData = useCallback(async () => {
    setLoading(true);
    setErrorMessage('');
    try {
      const [ticketRes, commentsRes] = await Promise.all([
        axiosClient.get(`/tickets/${id}`),
        axiosClient.get(`/tickets/${id}/comments`)
      ]);
      setTicket(ticketRes);
      setComments(commentsRes || []);
    } catch (err) {
      console.error('Lỗi khi tải chi tiết ticket:', err);
      setErrorMessage('Không thể tải thông tin yêu cầu hoặc phiếu này không tồn tại.');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchTicketData();
  }, [fetchTicketData]);

  const handleStatusUpdated = (updatedTicket) => {
    setTicket(updatedTicket);
  };

  const handleCommentAdded = (newComment) => {
    setComments((prev) => [...prev, newComment]);
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) {
    return (
      <div className="py-20 text-center text-[13px]" style={{ color: 'var(--muted)' }}>
        Đang tải thông tin chi tiết yêu cầu...
      </div>
    );
  }

  if (errorMessage || !ticket) {
    return (
      <div className="max-w-md mx-auto py-16 text-center space-y-3">
        <AlertTriangle className="w-8 h-8 mx-auto" style={{ color: 'var(--err)' }} />
        <h2 className="text-[16px] font-[600]" style={{ color: 'var(--text)' }}>
          Không tìm thấy yêu cầu
        </h2>
        <p className="text-[13px]" style={{ color: 'var(--muted)' }}>
          {errorMessage || 'Mã yêu cầu không hợp lệ hoặc đã bị xoá.'}
        </p>
        <Link
          to="/tickets"
          className="inline-flex items-center gap-1.5 px-3.5 h-[34px] text-white text-[13px] font-[500] rounded-[6px]"
          style={{ backgroundColor: 'var(--brand)' }}
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Quay lại danh sách</span>
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Top Bar */}
      <div
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-3"
        style={{ borderBottom: '1px solid var(--line)' }}
      >
        <div className="flex items-center gap-2.5">
          <Link
            to="/tickets"
            className="p-1.5 rounded-[6px] transition-colors"
            style={{
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--line)',
              color: 'var(--text)'
            }}
            title="Quay lại danh sách"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono font-[600] text-[15px]" style={{ color: 'var(--brand)' }}>
                {ticket.ticketCode}
              </span>
              <StatusBadge status={ticket.status} />
              <PriorityBadge priority={ticket.priority} />
              <OverdueBadge isOverdue={ticket.isOverdue} />
            </div>
            <div className="text-[12px] mt-0.5 flex items-center gap-2" style={{ color: 'var(--muted)' }}>
              <span>Tạo lúc: {new Date(ticket.createdAt).toLocaleString('vi-VN')}</span>
              <span>•</span>
              <span>Danh mục: {ticket.category?.name}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopyLink}
            className="inline-flex items-center gap-1.5 px-3 h-[34px] text-[13px] font-[500] rounded-[6px] transition-colors"
            style={{
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--line)',
              color: 'var(--text)'
            }}
          >
            {copied ? (
              <>
                <CheckCircle2 className="w-3.5 h-3.5" style={{ color: 'var(--ok)' }} />
                <span style={{ color: 'var(--ok)' }}>Đã chép link</span>
              </>
            ) : (
              <>
                <Share2 className="w-3.5 h-3.5" />
                <span>Chia sẻ link</span>
              </>
            )}
          </button>

          <button
            onClick={fetchTicketData}
            title="Làm mới"
            className="p-2 rounded-[6px] transition-colors"
            style={{
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--line)',
              color: 'var(--muted)'
            }}
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Grid 2 Cột */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 items-start">
        {/* Cột trái (8/12) */}
        <div className="lg:col-span-8 space-y-4">
          <div
            className="p-5 rounded-[8px] space-y-3"
            style={{
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--line)'
            }}
          >
            <div>
              <div className="text-[12px] font-[500] mb-1" style={{ color: 'var(--muted)' }}>
                Tiêu đề sự cố
              </div>
              <h1 className="text-[18px] font-[600] leading-snug" style={{ color: 'var(--text)' }}>
                {ticket.title}
              </h1>
            </div>

            <div className="pt-3" style={{ borderTop: '1px solid var(--line)' }}>
              <div className="text-[12px] font-[500] mb-1.5" style={{ color: 'var(--muted)' }}>
                Mô tả chi tiết
              </div>
              <div
                className="text-[13px] leading-relaxed whitespace-pre-line p-3 rounded-[6px]"
                style={{
                  backgroundColor: 'var(--bg)',
                  border: '1px solid var(--line)',
                  color: 'var(--text)'
                }}
              >
                {ticket.description || 'Không có mô tả chi tiết.'}
              </div>
            </div>
          </div>

          <CommentSection
            ticketId={ticket.id}
            comments={comments}
            onCommentAdded={handleCommentAdded}
          />
        </div>

        {/* Cột phải (4/12) */}
        <div className="lg:col-span-4 space-y-4">
          <TicketWorkflowActions
            ticket={ticket}
            onStatusUpdated={handleStatusUpdated}
          />

          {/* Thuộc tính phiếu */}
          <div
            className="p-4 rounded-[8px] space-y-3 text-[13px]"
            style={{
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--line)'
            }}
          >
            <h4
              className="font-[600] text-[13px] pb-2"
              style={{
                color: 'var(--text)',
                borderBottom: '1px solid var(--line)'
              }}
            >
              Thông tin SLA & người gửi
            </h4>

            {/* Hạn SLA */}
            <div className="space-y-1">
              <span style={{ color: 'var(--muted)' }}>Hạn cam kết (SLA Deadline):</span>
              {ticket.dueDate ? (
                <div
                  className="p-2.5 rounded-[6px] flex items-center justify-between"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)'
                  }}
                >
                  <div className="flex items-center gap-1.5 font-[500]">
                    <Clock className="w-3.5 h-3.5" style={{ color: 'var(--muted)' }} />
                    <span style={{ color: ticket.isOverdue ? 'var(--err)' : 'var(--text)' }}>
                      {new Date(ticket.dueDate).toLocaleString('vi-VN')}
                    </span>
                  </div>
                  <OverdueBadge isOverdue={ticket.isOverdue} />
                </div>
              ) : (
                <span style={{ color: 'var(--muted)' }}>Chưa xác định</span>
              )}
            </div>

            {/* Kỹ thuật viên */}
            <div className="pt-2 space-y-1" style={{ borderTop: '1px solid var(--line)' }}>
              <span style={{ color: 'var(--muted)' }}>Kỹ thuật viên tiếp nhận:</span>
              {ticket.assignee ? (
                <div
                  className="p-2.5 rounded-[6px]"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)'
                  }}
                >
                  <div className="font-[600]" style={{ color: 'var(--text)' }}>
                    {ticket.assignee.fullName}
                  </div>
                  <div className="text-[12px] font-mono" style={{ color: 'var(--muted)' }}>
                    {ticket.assignee.email}
                  </div>
                </div>
              ) : (
                <div
                  className="p-2 rounded-[6px] text-center text-[12px] italic"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--muted)'
                  }}
                >
                  Chưa có kỹ thuật viên tiếp nhận
                </div>
              )}
            </div>

            {/* Người tạo */}
            <div className="pt-2 space-y-1" style={{ borderTop: '1px solid var(--line)' }}>
              <span style={{ color: 'var(--muted)' }}>Người gửi yêu cầu:</span>
              <div
                className="p-2.5 rounded-[6px] space-y-1"
                style={{
                  backgroundColor: 'var(--bg)',
                  border: '1px solid var(--line)'
                }}
              >
                <div className="font-[600] flex items-center gap-1.5" style={{ color: 'var(--text)' }}>
                  <UserIcon className="w-3.5 h-3.5" style={{ color: 'var(--muted)' }} />
                  <span>{ticket.requester?.fullName}</span>
                </div>
                <div className="text-[12px] flex items-center gap-1.5" style={{ color: 'var(--muted)' }}>
                  <Building className="w-3.5 h-3.5" />
                  <span>{ticket.requester?.department}</span>
                </div>
                <div className="text-[12px] flex items-center gap-1.5 font-mono" style={{ color: 'var(--muted)' }}>
                  <Mail className="w-3.5 h-3.5" />
                  <span>{ticket.requester?.email}</span>
                </div>
              </div>
            </div>

            {/* Danh mục */}
            <div className="pt-2 space-y-1" style={{ borderTop: '1px solid var(--line)' }}>
              <span style={{ color: 'var(--muted)' }}>Danh mục sự cố:</span>
              <div className="font-[500] flex items-center gap-1.5" style={{ color: 'var(--text)' }}>
                <Tag className="w-3.5 h-3.5" style={{ color: 'var(--muted)' }} />
                <span>{ticket.category?.name}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
