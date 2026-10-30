import React from 'react';

/**
 * KPI card theo đặc tả IT Helpdesk Design System:
 * - Viền trái 3px màu ngữ nghĩa
 * - Nền --surface, viền 1px --line, bo góc 8px, không đổ bóng
 * - Nhãn 13px muted
 * - Số 26px/600
 * - Ghi chú 12px muted
 * - Không icon trang trí
 */
export const KpiCard = ({ label, value, note, colorType = 'brand' }) => {
  const getColor = () => {
    switch (colorType) {
      case 'err':
        return 'var(--err)';
      case 'warn':
        return 'var(--warn)';
      case 'ok':
        return 'var(--ok)';
      case 'brand':
      default:
        return 'var(--brand)';
    }
  };

  return (
    <div
      className="p-4 rounded-[8px] flex flex-col justify-between"
      style={{
        backgroundColor: 'var(--surface)',
        border: '1px solid var(--line)',
        borderLeft: `3px solid ${getColor()}`,
        borderRadius: '8px'
      }}
    >
      <div className="text-[13px]" style={{ color: 'var(--muted)' }}>
        {label}
      </div>
      <div className="text-[26px] font-[600] my-1" style={{ color: 'var(--text)' }}>
        {value ?? '--'}
      </div>
      {note && (
        <div className="text-[12px]" style={{ color: 'var(--muted)' }}>
          {note}
        </div>
      )}
    </div>
  );
};
