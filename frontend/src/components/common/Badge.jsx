import React from 'react';

export const StatusBadge = ({ status }) => {
  switch (status) {
    case 'OPEN':
      return (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-[10px] text-[12px] font-[500]"
          style={{ backgroundColor: 'var(--brand-soft)', color: 'var(--brand)' }}
        >
          <span className="w-[6px] h-[6px] rounded-full" style={{ backgroundColor: 'var(--brand)' }}></span>
          Mới
        </span>
      );
    case 'IN_PROGRESS':
      return (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-[10px] text-[12px] font-[500]"
          style={{ backgroundColor: 'var(--warn-soft)', color: 'var(--warn)' }}
        >
          <span className="w-[6px] h-[6px] rounded-full" style={{ backgroundColor: 'var(--warn)' }}></span>
          Đang xử lý
        </span>
      );
    case 'RESOLVED':
      return (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-[10px] text-[12px] font-[500]"
          style={{ backgroundColor: 'var(--ok-soft)', color: 'var(--ok)' }}
        >
          <span className="w-[6px] h-[6px] rounded-full" style={{ backgroundColor: 'var(--ok)' }}></span>
          Đã giải quyết
        </span>
      );
    case 'CLOSED':
      return (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-[10px] text-[12px] font-[500]"
          style={{ backgroundColor: 'var(--gray-soft)', color: 'var(--muted)' }}
        >
          <span className="w-[6px] h-[6px] rounded-full" style={{ backgroundColor: 'var(--muted)' }}></span>
          Đã đóng
        </span>
      );
    default:
      return (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-[10px] text-[12px] font-[500]"
          style={{ backgroundColor: 'var(--gray-soft)', color: 'var(--muted)' }}
        >
          <span className="w-[6px] h-[6px] rounded-full" style={{ backgroundColor: 'var(--muted)' }}></span>
          {status}
        </span>
      );
  }
};

export const PriorityBadge = ({ priority }) => {
  switch (priority) {
    case 'CRITICAL':
      return (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-[10px] text-[12px] font-[500]"
          style={{ backgroundColor: 'var(--err-soft)', color: 'var(--err)' }}
        >
          <span className="w-[6px] h-[6px] rounded-full" style={{ backgroundColor: 'var(--err)' }}></span>
          Khẩn cấp
        </span>
      );
    case 'HIGH':
      return (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-[10px] text-[12px] font-[500]"
          style={{ backgroundColor: 'var(--warn-soft)', color: 'var(--warn)' }}
        >
          <span className="w-[6px] h-[6px] rounded-full" style={{ backgroundColor: 'var(--warn)' }}></span>
          Cao
        </span>
      );
    case 'MEDIUM':
      return (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-[10px] text-[12px] font-[500]"
          style={{ backgroundColor: 'var(--brand-soft)', color: 'var(--brand)' }}
        >
          <span className="w-[6px] h-[6px] rounded-full" style={{ backgroundColor: 'var(--brand)' }}></span>
          Trung bình
        </span>
      );
    case 'LOW':
    default:
      return (
        <span
          className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-[10px] text-[12px] font-[500]"
          style={{ backgroundColor: 'var(--gray-soft)', color: 'var(--muted)' }}
        >
          <span className="w-[6px] h-[6px] rounded-full" style={{ backgroundColor: 'var(--muted)' }}></span>
          Thấp
        </span>
      );
  }
};

export const OverdueBadge = ({ isOverdue }) => {
  if (!isOverdue) return null;
  return (
    <span
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded-[10px] text-[11px] font-[600]"
      style={{ backgroundColor: 'var(--err-soft)', color: 'var(--err)', border: '1px solid var(--err)' }}
    >
      Trễ SLA
    </span>
  );
};
