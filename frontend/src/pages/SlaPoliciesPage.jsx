import React, { useState, useEffect } from 'react';
import axiosClient from '../api/axiosClient';
import {
  ShieldAlert,
  Clock,
  RefreshCw,
  CheckCircle,
  AlertTriangle,
  Info
} from 'lucide-react';

export const SlaPoliciesPage = () => {
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchPolicies = async () => {
    setLoading(true);
    try {
      const data = await axiosClient.get('/sla-policies');
      setPolicies(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Lỗi khi tải chính sách SLA:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  const slaTiers = [
    {
      priority: 'CRITICAL',
      label: 'Khẩn cấp (Critical)',
      badgeBg: 'var(--err-soft)',
      badgeColor: 'var(--err)',
      borderAccent: 'var(--err)',
      responseTime: '15 phút',
      resolutionHours: 2,
      description: 'Sự cố tê liệt toàn hệ thống hoặc gián đoạn hoạt động của cả phòng ban/chi nhánh.',
      escalation: 'Thông báo tự động tới Trưởng phòng CNTT và Ban Giám đốc nếu chưa tiếp nhận sau 15 phút.'
    },
    {
      priority: 'HIGH',
      label: 'Cao (High)',
      badgeBg: 'var(--warn-soft)',
      badgeColor: 'var(--warn)',
      borderAccent: 'var(--warn)',
      responseTime: '30 phút',
      resolutionHours: 8,
      description: 'Hỏng hóc thiết bị then chốt, nhân sự không thể tiếp tục công việc hàng ngày.',
      escalation: 'Điều chuyển ticket sang kỹ thuật viên cấp cao nếu quá 4 giờ chưa có phương án xử lý.'
    },
    {
      priority: 'MEDIUM',
      label: 'Trung bình (Medium)',
      badgeBg: 'var(--brand-soft)',
      badgeColor: 'var(--brand)',
      borderAccent: 'var(--brand)',
      responseTime: '2 giờ',
      resolutionHours: 24,
      description: 'Lỗi phần mềm thông thường, hiệu năng giảm một phần nhưng vẫn có giải pháp thay thế.',
      escalation: 'Nhắc nhở qua email khi thời gian giải quyết đạt 80% hạn cam kết SLA.'
    },
    {
      priority: 'LOW',
      label: 'Thấp (Low)',
      badgeBg: 'var(--gray-soft)',
      badgeColor: 'var(--muted)',
      borderAccent: 'var(--line)',
      responseTime: '4 giờ',
      resolutionHours: 48,
      description: 'Thắc mắc tư vấn sử dụng, yêu cầu cấp mới quyền hạn không khẩn cấp.',
      escalation: 'Được xử lý theo thứ tự FIFO trong giờ làm việc hành chính tiêu chuẩn.'
    }
  ];

  return (
    <div className="space-y-4">
      {/* Header trang */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-[20px] font-[600]" style={{ color: 'var(--text)' }}>
            Chính sách cam kết dịch vụ (SLA)
          </h1>
          <p className="text-[13px] mt-0.5" style={{ color: 'var(--muted)' }}>
            Quy định thời hạn phản hồi, giải quyết sự cố và quy trình leo thang theo cấp độ ưu tiên
          </p>
        </div>

        <button
          onClick={fetchPolicies}
          className="h-[34px] px-3 rounded-[6px] text-[13px] font-[500] flex items-center gap-1.5 transition-colors self-start sm:self-auto"
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

      {/* Thông tin nguyên tắc SLA */}
      <div
        className="p-4 rounded-[8px] flex items-start gap-3"
        style={{
          backgroundColor: 'var(--brand-soft)',
          border: '1px solid var(--line)',
          color: 'var(--brand)'
        }}
      >
        <Info className="w-5 h-5 shrink-0 mt-0.5" />
        <div className="text-[13px] leading-relaxed">
          <span className="font-[600]">Nguyên tắc tính hạn tự động: </span>
          Hệ thống IT Helpdesk tự động gắn hạn chót (Due Date) cho mỗi ticket ngay khi nhân viên tạo yêu cầu dựa theo ma trận mức độ ưu tiên bên dưới. Bất kỳ yêu cầu nào vượt quá thời hạn này sẽ lập tức kích hoạt nhãn đỏ <strong>Quá hạn SLA</strong> trên bảng điều khiển.
        </div>
      </div>

      {/* Lưới 4 Thẻ mức độ SLA */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {slaTiers.map((tier) => {
          const matchedDbPolicy = policies.find(
            (p) => p.priorityLevel === tier.priority
          );
          const hours = matchedDbPolicy ? matchedDbPolicy.resolutionTimeHours : tier.resolutionHours;

          return (
            <div
              key={tier.priority}
              className="p-5 rounded-[8px] space-y-4"
              style={{
                backgroundColor: 'var(--surface)',
                border: '1px solid var(--line)',
                borderLeft: `4px solid ${tier.borderAccent}`
              }}
            >
              <div className="flex items-center justify-between">
                <span
                  className="px-2.5 py-0.5 rounded-[10px] text-[12px] font-[600]"
                  style={{
                    backgroundColor: tier.badgeBg,
                    color: tier.badgeColor
                  }}
                >
                  {tier.label}
                </span>

                <div className="flex items-center gap-1.5 font-mono text-[13px] font-[600]" style={{ color: 'var(--text)' }}>
                  <Clock className="w-4 h-4" style={{ color: 'var(--muted)' }} />
                  <span>{hours} giờ cam kết</span>
                </div>
              </div>

              <p className="text-[13px] leading-relaxed" style={{ color: 'var(--text)' }}>
                {tier.description}
              </p>

              <div
                className="p-3 rounded-[6px] space-y-2 text-[12px]"
                style={{
                  backgroundColor: 'var(--bg)',
                  border: '1px solid var(--line)'
                }}
              >
                <div className="flex justify-between">
                  <span style={{ color: 'var(--muted)' }}>Thời gian phản hồi ban đầu:</span>
                  <span className="font-[600]" style={{ color: 'var(--text)' }}>
                    &le; {tier.responseTime}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span style={{ color: 'var(--muted)' }}>Thời gian hoàn thành dứt điểm:</span>
                  <span className="font-[600]" style={{ color: 'var(--text)' }}>
                    &le; {hours} giờ
                  </span>
                </div>
                <div className="pt-2 border-t" style={{ borderColor: 'var(--line)' }}>
                  <div className="text-[11px] font-[500] uppercase mb-0.5" style={{ color: 'var(--muted)' }}>
                    Quy trình leo thang:
                  </div>
                  <div className="text-[12px] leading-snug" style={{ color: 'var(--text)' }}>
                    {tier.escalation}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
