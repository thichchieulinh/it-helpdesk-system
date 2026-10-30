import React, { useState } from 'react';
import axiosClient from '../../api/axiosClient';
import { useAuth } from '../../context/AuthContext';
import {
  MessageSquare,
  Send,
  Loader2,
  Clock,
  AlertCircle
} from 'lucide-react';

export const CommentSection = ({ ticketId, comments = [], onCommentAdded }) => {
  const { currentUser } = useAuth();
  const [content, setContent] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) {
      setErrorMessage('Vui lòng nhập nội dung phản hồi.');
      return;
    }

    setSubmitting(true);
    setErrorMessage('');

    try {
      const payload = {
        userId: currentUser?.id,
        content: content.trim()
      };

      const newComment = await axiosClient.post(`/tickets/${ticketId}/comments`, payload);
      setContent('');
      onCommentAdded?.(newComment);
    } catch (err) {
      console.error('Lỗi khi gửi bình luận:', err);
      setErrorMessage(typeof err === 'string' ? err : 'Không thể gửi phản hồi.');
    } finally {
      setSubmitting(false);
    }
  };

  const getRoleBadge = (role) => {
    switch (role) {
      case 'ADMIN':
        return (
          <span
            className="text-[11px] font-[500] px-2 py-0.5 rounded-[10px]"
            style={{ backgroundColor: 'var(--brand-soft)', color: 'var(--brand)' }}
          >
            Quản trị viên
          </span>
        );
      case 'AGENT':
        return (
          <span
            className="text-[11px] font-[500] px-2 py-0.5 rounded-[10px]"
            style={{ backgroundColor: 'var(--warn-soft)', color: 'var(--warn)' }}
          >
            Kỹ thuật viên
          </span>
        );
      case 'EMPLOYEE':
      default:
        return (
          <span
            className="text-[11px] font-[500] px-2 py-0.5 rounded-[10px]"
            style={{ backgroundColor: 'var(--gray-soft)', color: 'var(--muted)' }}
          >
            Người yêu cầu
          </span>
        );
    }
  };

  return (
    <div
      className="p-5 rounded-[8px] space-y-4"
      style={{
        backgroundColor: 'var(--surface)',
        border: '1px solid var(--line)'
      }}
    >
      {/* Section Header */}
      <div
        className="flex items-center justify-between pb-3"
        style={{ borderBottom: '1px solid var(--line)' }}
      >
        <div className="flex items-center gap-2">
          <MessageSquare className="w-4 h-4" style={{ color: 'var(--brand)' }} />
          <h3 className="text-[14px] font-[600]" style={{ color: 'var(--text)' }}>
            Lịch sử trao đổi ({comments.length})
          </h3>
        </div>
        <span className="text-[12px]" style={{ color: 'var(--muted)' }}>
          Phản hồi và ghi chú xử lý
        </span>
      </div>

      {/* Danh sách bình luận */}
      <div className="space-y-3">
        {comments.length === 0 ? (
          <div className="py-8 text-center text-[13px]" style={{ color: 'var(--muted)' }}>
            Chưa có phản hồi nào. Hãy nhập nội dung trao đổi bên dưới.
          </div>
        ) : (
          comments.map((comment) => {
            const isStaff = comment.user?.role === 'AGENT' || comment.user?.role === 'ADMIN';
            return (
              <div
                key={comment.id}
                className="p-3 rounded-[6px]"
                style={{
                  backgroundColor: isStaff ? 'var(--brand-soft)' : 'var(--bg)',
                  border: '1px solid var(--line)'
                }}
              >
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <div className="flex items-center gap-2">
                    <span className="text-[13px] font-[600]" style={{ color: 'var(--text)' }}>
                      {comment.user?.fullName || 'Người dùng'}
                    </span>
                    {getRoleBadge(comment.user?.role)}
                    <span className="text-[12px] font-mono" style={{ color: 'var(--muted)' }}>
                      ({comment.user?.department || 'Nội bộ'})
                    </span>
                  </div>

                  {comment.createdAt && (
                    <div className="flex items-center gap-1 text-[11px]" style={{ color: 'var(--muted)' }}>
                      <Clock className="w-3 h-3" />
                      <span>
                        {new Date(comment.createdAt).toLocaleString('vi-VN', {
                          hour: '2-digit',
                          minute: '2-digit',
                          day: '2-digit',
                          month: '2-digit'
                        })}
                      </span>
                    </div>
                  )}
                </div>

                <div className="text-[13px] leading-relaxed whitespace-pre-line" style={{ color: 'var(--text)' }}>
                  {comment.content}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Form nhập bình luận mới */}
      <form onSubmit={handleSubmit} className="pt-3 space-y-2.5" style={{ borderTop: '1px solid var(--line)' }}>
        {errorMessage && (
          <div
            className="p-2.5 rounded-[6px] text-[13px] flex items-center gap-1.5"
            style={{
              backgroundColor: 'var(--err-soft)',
              color: 'var(--err)',
              border: '1px solid var(--err)'
            }}
          >
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        <textarea
          rows={3}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder={`Nhập phản hồi với tư cách ${currentUser?.fullName || ''}...`}
          className="w-full p-2.5 text-[13px] rounded-[6px] focus:outline-none resize-none"
          style={{
            backgroundColor: 'var(--bg)',
            border: '1px solid var(--line)',
            color: 'var(--text)'
          }}
        />

        <div className="flex items-center justify-between">
          <span className="text-[12px]" style={{ color: 'var(--muted)' }}>
            Nội dung trao đổi sẽ được lưu vào lịch sử yêu cầu.
          </span>
          <button
            type="submit"
            disabled={submitting || !content.trim()}
            className="h-[34px] px-3.5 text-[13px] font-[500] text-white rounded-[6px] flex items-center gap-1.5 transition-opacity disabled:opacity-40"
            style={{ backgroundColor: 'var(--brand)' }}
          >
            {submitting ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Đang gửi...</span>
              </>
            ) : (
              <>
                <span>Gửi phản hồi</span>
                <Send className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
