import React, { useState } from 'react';
import axiosClient from '../../api/axiosClient';
import { useAuth } from '../../context/AuthContext';
import {
  CheckCircle2,
  Archive,
  RotateCcw,
  Loader2,
  UserCheck,
  AlertCircle,
  HelpCircle,
  ShieldCheck
} from 'lucide-react';

export const TicketWorkflowActions = ({ ticket, onStatusUpdated }) => {
  const { currentUser } = useAuth();
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState('');

  if (!ticket || !currentUser) return null;

  const role = currentUser.role;
  const isAgentOrAdmin = role === 'AGENT' || role === 'ADMIN';
  const isCreator = ticket.requester?.id === currentUser.id;
  const status = ticket.status;

  const handleUpdateStatus = async (newStatus, assigneeId = null) => {
    setUpdating(true);
    setError('');

    try {
      const payload = {
        status: newStatus,
        assigneeId: assigneeId !== null ? assigneeId : (ticket.assignee?.id || null)
      };

      const updatedTicket = await axiosClient.patch(`/tickets/${ticket.id}/status`, payload);
      onStatusUpdated?.(updatedTicket);
    } catch (err) {
      console.error('Lỗi cập nhật trạng thái:', err);
      setError(typeof err === 'string' ? err : 'Không thể cập nhật tiến trình xử lý.');
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div
      className="p-4 rounded-[8px] space-y-3"
      style={{
        backgroundColor: 'var(--surface)',
        border: '1px solid var(--line)'
      }}
    >
      <div
        className="flex items-center justify-between pb-2.5"
        style={{ borderBottom: '1px solid var(--line)' }}
      >
        <h4 className="text-[13px] font-[600] flex items-center gap-1.5" style={{ color: 'var(--text)' }}>
          <ShieldCheck className="w-4 h-4" style={{ color: 'var(--brand)' }} />
          <span>Thao tác xử lý nghiệp vụ</span>
        </h4>
        <span
          className="text-[11px] font-[500] px-2 py-0.5 rounded-[10px]"
          style={{ backgroundColor: 'var(--gray-soft)', color: 'var(--muted)' }}
        >
          {role}
        </span>
      </div>

      {error && (
        <div
          className="p-2.5 rounded-[6px] text-[13px] flex items-center gap-1.5"
          style={{
            backgroundColor: 'var(--err-soft)',
            color: 'var(--err)',
            border: '1px solid var(--err)'
          }}
        >
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Trạng thái OPEN */}
      {status === 'OPEN' && (
        <div>
          {isAgentOrAdmin ? (
            <button
              onClick={() => handleUpdateStatus('IN_PROGRESS', currentUser.id)}
              disabled={updating}
              className="w-full h-[34px] px-3 text-white text-[13px] font-[500] rounded-[6px] flex items-center justify-center gap-1.5 transition-opacity disabled:opacity-50"
              style={{ backgroundColor: 'var(--brand)' }}
            >
              {updating ? (
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <>
                  <UserCheck className="w-3.5 h-3.5" />
                  <span>Tiếp nhận xử lý</span>
                </>
              )}
            </button>
          ) : (
            <div
              className="p-2.5 rounded-[6px] text-[13px] flex items-start gap-1.5"
              style={{
                backgroundColor: 'var(--bg)',
                border: '1px solid var(--line)',
                color: 'var(--muted)'
              }}
            >
              <HelpCircle className="w-4 h-4 shrink-0 mt-0.5" style={{ color: 'var(--brand)' }} />
              <span>Yêu cầu đang chờ kỹ thuật viên tiếp nhận phân công.</span>
            </div>
          )}
        </div>
      )}

      {/* Trạng thái IN_PROGRESS */}
      {status === 'IN_PROGRESS' && (
        <div className="space-y-2">
          {isAgentOrAdmin ? (
            <>
              <button
                onClick={() => handleUpdateStatus('RESOLVED')}
                disabled={updating}
                className="w-full h-[34px] px-3 text-white text-[13px] font-[500] rounded-[6px] flex items-center justify-center gap-1.5 transition-opacity disabled:opacity-50"
                style={{ backgroundColor: 'var(--ok)' }}
              >
                {updating ? (
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <>
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Đã giải quyết</span>
                  </>
                )}
              </button>

              {ticket.assignee?.id !== currentUser.id && (
                <button
                  onClick={() => handleUpdateStatus('IN_PROGRESS', currentUser.id)}
                  disabled={updating}
                  className="w-full h-[34px] px-2.5 text-[13px] font-[500] rounded-[6px] flex items-center justify-center gap-1 transition-colors"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)'
                  }}
                >
                  <UserCheck className="w-3.5 h-3.5" />
                  <span>Chuyển quyền phụ trách cho tôi</span>
                </button>
              )}
            </>
          ) : (
            <div
              className="p-2.5 rounded-[6px] text-[13px]"
              style={{
                backgroundColor: 'var(--warn-soft)',
                color: 'var(--warn)',
                border: '1px solid var(--warn)'
              }}
            >
              Kỹ thuật viên <strong>{ticket.assignee?.fullName || 'IT Support'}</strong> đang trong tiến trình xử lý sự cố.
            </div>
          )}
        </div>
      )}

      {/* Trạng thái RESOLVED */}
      {status === 'RESOLVED' && (
        <div className="space-y-2">
          {(isCreator || role === 'ADMIN') ? (
            <button
              onClick={() => handleUpdateStatus('CLOSED')}
              disabled={updating}
              className="w-full h-[34px] px-3 text-white text-[13px] font-[500] rounded-[6px] flex items-center justify-center gap-1.5 transition-opacity disabled:opacity-50"
              style={{ backgroundColor: 'var(--nav)' }}
            >
              {updating ? (
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <>
                  <Archive className="w-3.5 h-3.5" />
                  <span>Xác nhận đóng yêu cầu</span>
                </>
              )}
            </button>
          ) : (
            <div
              className="p-2.5 rounded-[6px] text-[13px]"
              style={{
                backgroundColor: 'var(--ok-soft)',
                color: 'var(--ok)',
                border: '1px solid var(--ok)'
              }}
            >
              Kỹ thuật viên đã xử lý xong. Chờ người yêu cầu ({ticket.requester?.fullName}) xác nhận để đóng.
            </div>
          )}

          {isAgentOrAdmin && (
            <button
              onClick={() => handleUpdateStatus('IN_PROGRESS')}
              disabled={updating}
              className="w-full h-[34px] px-2.5 text-[13px] font-[500] rounded-[6px] flex items-center justify-center gap-1 transition-colors"
              style={{
                backgroundColor: 'var(--surface)',
                border: '1px solid var(--line)',
                color: 'var(--text)'
              }}
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Mở lại yêu cầu</span>
            </button>
          )}
        </div>
      )}

      {/* Trạng thái CLOSED */}
      {status === 'CLOSED' && (
        <div className="space-y-2">
          <div
            className="p-2.5 rounded-[6px] text-[13px] flex items-center gap-1.5"
            style={{
              backgroundColor: 'var(--bg)',
              border: '1px solid var(--line)',
              color: 'var(--muted)'
            }}
          >
            <CheckCircle2 className="w-4 h-4 shrink-0" style={{ color: 'var(--ok)' }} />
            <span>Yêu cầu đã được đóng và lưu trữ hoàn tất.</span>
          </div>

          {role === 'ADMIN' && (
            <button
              onClick={() => handleUpdateStatus('IN_PROGRESS')}
              disabled={updating}
              className="w-full py-1 text-[12px] hover:underline flex items-center justify-center gap-1"
              style={{ color: 'var(--brand)' }}
            >
              <RotateCcw className="w-3 h-3" />
              <span>Mở lại yêu cầu này</span>
            </button>
          )}
        </div>
      )}
    </div>
  );
};
