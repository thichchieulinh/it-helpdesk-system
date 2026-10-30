import React, { useState, useEffect } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axiosClient from '../api/axiosClient';
import { KpiCard } from '../components/common/KpiCard';
import { StatusBadge, PriorityBadge } from '../components/common/Badge';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { RefreshCw, ArrowRight } from 'lucide-react';

export const DashboardPage = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();

  // Phân quyền: Nhân viên không vào Dashboard phân tích
  if (!currentUser || currentUser.role === 'EMPLOYEE') {
    return <Navigate to="/tickets" replace />;
  }

  const [stats, setStats] = useState(null);
  const [recentTickets, setRecentTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [statsData, ticketsData] = await Promise.all([
        axiosClient.get('/dashboard/stats'),
        axiosClient.get('/tickets')
      ]);
      setStats(statsData);
      setRecentTickets(ticketsData.slice(0, 5)); // Lấy 5 ticket mới nhất
    } catch (err) {
      console.error('Lỗi tải dữ liệu dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const total = stats?.totalTickets || 0;
  const inProgressCount = stats?.inProgressTickets || 0;
  const overdueCount = stats?.overdueTickets || 0;
  const completedCount = (stats?.resolvedTickets || 0) + (stats?.closedTickets || 0);

  // Tỷ lệ tuân thủ SLA (giả lập hoặc tính theo số ticket không bị quá hạn)
  const slaComplianceRate = total > 0 ? Math.max(0, Math.round(((total - overdueCount) / total) * 100)) : 100;

  // Dữ liệu biểu đồ cột đôi theo đặc tả Design System (Mới = brand, Đã đóng = ok)
  const chartData = [
    {
      name: 'Hôm nay',
      newCount: stats?.openTickets || 0,
      closedCount: stats?.closedTickets || 0
    },
    {
      name: 'Đang mở',
      newCount: inProgressCount,
      closedCount: stats?.resolvedTickets || 0
    },
    {
      name: 'Tổng quan',
      newCount: total,
      closedCount: completedCount
    }
  ];

  const getSlaColor = (rate) => {
    if (rate >= 90) return 'var(--brand)';
    if (rate >= 75) return 'var(--warn)';
    return 'var(--err)';
  };

  return (
    <div className="space-y-6">
      {/* Tiêu đề trang 20px */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-[20px] font-[600]" style={{ color: 'var(--text)' }}>
            Tổng quan hiệu suất hỗ trợ
          </h1>
          <p className="text-[13px] mt-0.5" style={{ color: 'var(--muted)' }}>
            Theo dõi khối lượng yêu cầu, tiến độ xử lý và cam kết mức độ dịch vụ (SLA)
          </p>
        </div>

        <button
          onClick={fetchDashboardData}
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

      {/* Hàng 4 thẻ KPI theo chuẩn Design System */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          label="Tổng yêu cầu ghi nhận"
          value={total}
          note="Toàn bộ lịch sử hỗ trợ"
          colorType="brand"
        />
        <KpiCard
          label="Đang trong tiến trình"
          value={inProgressCount}
          note={`${stats?.openTickets || 0} mới • ${inProgressCount} đang làm`}
          colorType="warn"
        />
        <KpiCard
          label="Đã giải quyết & Đóng"
          value={completedCount}
          note="Sự cố đã được khắc phục"
          colorType="ok"
        />
        <KpiCard
          label="Vi phạm cam kết SLA"
          value={overdueCount}
          note="Vượt quá thời hạn quy định"
          colorType="err"
        />
      </div>

      {/* Lưới 2fr / 1fr (Biểu đồ + Khối giám sát SLA) theo đúng Layout spec */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Card Biểu đồ cột đôi (2fr ~ 2 cols) */}
        <div
          className="lg:col-span-2 rounded-[8px] p-4 flex flex-col justify-between"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)'
          }}
        >
          <div
            className="text-[14px] font-[600] pb-2.5 flex items-center justify-between"
            style={{ borderBottom: '1px solid var(--line)', color: 'var(--text)' }}
          >
            <span>Phân bổ luồng xử lý yêu cầu</span>
            <span className="text-[12px] font-[400]" style={{ color: 'var(--muted)' }}>
              Cột đôi: Mới & Đã hoàn thành
            </span>
          </div>

          <div className="h-[240px] w-full pt-4" aria-label="Biểu đồ phân bổ luồng xử lý">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--line)" />
                <XAxis
                  dataKey="name"
                  tick={{ fontSize: 12, fill: 'var(--muted)' }}
                  axisLine={{ stroke: 'var(--line)' }}
                  tickLine={false}
                />
                <YAxis
                  allowDecimals={false}
                  tick={{ fontSize: 12, fill: 'var(--muted)' }}
                  axisLine={{ stroke: 'var(--line)' }}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--surface)',
                    borderColor: 'var(--line)',
                    color: 'var(--text)',
                    borderRadius: '6px',
                    fontSize: '12px'
                  }}
                />
                <Legend
                  verticalAlign="top"
                  align="right"
                  iconType="circle"
                  iconSize={8}
                  wrapperStyle={{ fontSize: 12, paddingBottom: 10 }}
                />
                <Bar name="Yêu cầu tiếp nhận" dataKey="newCount" fill="var(--brand)" radius={[4, 4, 0, 0]} maxBarSize={36} />
                <Bar name="Đã xử lý xong" dataKey="closedCount" fill="var(--ok)" radius={[4, 4, 0, 0]} maxBarSize={36} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Card Giám sát SLA (1fr ~ 1 col) */}
        <div
          className="rounded-[8px] p-4 flex flex-col justify-between"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)'
          }}
        >
          <div>
            <div
              className="text-[14px] font-[600] pb-2.5 flex items-center justify-between"
              style={{ borderBottom: '1px solid var(--line)', color: 'var(--text)' }}
            >
              <span>Giám sát cam kết SLA</span>
              <span className="text-[12px] font-[600]" style={{ color: getSlaColor(slaComplianceRate) }}>
                {slaComplianceRate}%
              </span>
            </div>

            {/* Thanh SLA Spec: nhãn + phần trăm, cao 6px bo tròn */}
            <div className="pt-3 space-y-4 text-[13px]">
              <div>
                <div className="flex items-center justify-between mb-1.5 text-[12px]">
                  <span style={{ color: 'var(--muted)' }}>Tuân thủ hạn xử lý chung</span>
                  <span className="font-[600]" style={{ color: 'var(--text)' }}>{slaComplianceRate}%</span>
                </div>
                <div className="w-full h-[6px] rounded-[3px] bg-slate-200 overflow-hidden" style={{ backgroundColor: 'var(--gray-soft)' }}>
                  <div
                    className="h-full rounded-[3px] transition-all"
                    style={{
                      width: `${slaComplianceRate}%`,
                      backgroundColor: getSlaColor(slaComplianceRate)
                    }}
                  />
                </div>
              </div>

              {/* Định mức từng cấp độ ưu tiên */}
              <div className="space-y-2 pt-2 text-[12px]" style={{ borderTop: '1px solid var(--line)' }}>
                <div className="flex items-center justify-between">
                  <span style={{ color: 'var(--muted)' }}>Khẩn cấp (CRITICAL)</span>
                  <span className="font-[600] font-mono text-[var(--err)]">2 giờ</span>
                </div>
                <div className="flex items-center justify-between">
                  <span style={{ color: 'var(--muted)' }}>Cao (HIGH)</span>
                  <span className="font-[600] font-mono text-[var(--warn)]">8 giờ</span>
                </div>
                <div className="flex items-center justify-between">
                  <span style={{ color: 'var(--muted)' }}>Trung bình (MEDIUM)</span>
                  <span className="font-[600] font-mono text-[var(--brand)]">24 giờ</span>
                </div>
                <div className="flex items-center justify-between">
                  <span style={{ color: 'var(--muted)' }}>Thấp (LOW)</span>
                  <span className="font-[600] font-mono text-[var(--muted)]">48 giờ</span>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-3 text-[12px]" style={{ color: 'var(--muted)', borderTop: '1px solid var(--line)' }}>
            Quét nền tự động: <strong>60 giây/lần</strong>
          </div>
        </div>
      </div>

      {/* Bảng Ticket gần đây */}
      <div
        className="rounded-[8px] overflow-hidden"
        style={{
          backgroundColor: 'var(--surface)',
          border: '1px solid var(--line)'
        }}
      >
        <div
          className="p-3.5 flex items-center justify-between"
          style={{ borderBottom: '1px solid var(--line)' }}
        >
          <span className="text-[14px] font-[600]" style={{ color: 'var(--text)' }}>
            Yêu cầu mới tiếp nhận gần đây
          </span>
          <button
            onClick={() => navigate('/tickets')}
            className="text-[12px] font-[500] flex items-center gap-1 transition-colors"
            style={{ color: 'var(--brand)' }}
          >
            <span>Xem tất cả</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

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
                <th className="py-2.5 px-3.5">Tiêu đề</th>
                <th className="py-2.5 px-3.5">Ưu tiên</th>
                <th className="py-2.5 px-3.5">Trạng thái</th>
                <th className="py-2.5 px-3.5">Người gửi</th>
                <th className="py-2.5 px-3.5">Hạn SLA</th>
              </tr>
            </thead>
            <tbody>
              {recentTickets.map((t) => (
                <tr
                  key={t.id}
                  onClick={() => navigate('/tickets')}
                  className="cursor-pointer transition-colors"
                  style={{ borderBottom: '1px solid var(--line)', height: '42px' }}
                  onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--bg)')}
                  onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
                >
                  <td className="py-2 px-3.5 font-mono font-[500]" style={{ color: 'var(--brand)' }}>
                    {t.ticketCode}
                  </td>
                  <td className="py-2 px-3.5 font-[500]" style={{ color: 'var(--text)' }}>
                    {t.title}
                  </td>
                  <td className="py-2 px-3.5">
                    <PriorityBadge priority={t.priority} />
                  </td>
                  <td className="py-2 px-3.5">
                    <StatusBadge status={t.status} />
                  </td>
                  <td className="py-2 px-3.5" style={{ color: 'var(--text)' }}>
                    {t.requester?.fullName}
                  </td>
                  <td className="py-2 px-3.5 text-[12px]" style={{ color: 'var(--muted)' }}>
                    {t.dueDate ? new Date(t.dueDate).toLocaleDateString('vi-VN') : 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
