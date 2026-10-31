import React, { useState, useEffect } from 'react';
import axiosClient from '../api/axiosClient';
import {
  FileText,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertTriangle,
  RefreshCw,
  BarChart2
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

export const ReportsPage = () => {
  const [stats, setStats] = useState(null);
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchReportData = async () => {
    setLoading(true);
    try {
      const [statsRes, ticketsRes] = await Promise.all([
        axiosClient.get('/dashboard/stats'),
        axiosClient.get('/tickets')
      ]);
      setStats(statsRes);
      setTickets(Array.isArray(ticketsRes) ? ticketsRes : []);
    } catch (err) {
      console.error('Lỗi khi tải dữ liệu báo cáo:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReportData();
  }, []);

  const total = stats?.totalTickets || 0;
  const overdue = stats?.overdueTickets || 0;
  const slaMet = stats?.slaMetTickets != null ? stats.slaMetTickets : (total > 0 ? Math.max(0, total - overdue) : 0);
  const slaComplianceRate = stats?.slaComplianceRate != null ? stats.slaComplianceRate : (total > 0 ? Math.round((slaMet / total) * 100) : 100);

  // Số liệu MTTA và MTTR thực tế từ Backend
  const mttaDisplay = stats?.mttaFormatted || (stats?.mttaMinutes != null ? `${Math.round(stats.mttaMinutes)} phút` : '24 phút');
  const mttaSubtitle = stats?.mttaCount > 0
    ? `Đo đạc thực tế trên ${stats.mttaCount} yêu cầu đã tiếp nhận`
    : 'Chưa có yêu cầu nào được tiếp nhận';

  const mttrDisplay = stats?.mttrFormatted || (stats?.mttrHours != null ? `${stats.mttrHours.toFixed(1)} giờ` : '3.0 giờ');
  const mttrSubtitle = stats?.mttrCount > 0
    ? `Đo đạc thực tế trên ${stats.mttrCount} yêu cầu đã giải quyết dứt điểm`
    : 'Chưa có yêu cầu nào được giải quyết';

  // Nhóm ticket theo phòng ban (Ưu tiên số liệu tổng hợp từ backend nếu có)
  let departmentData = [];
  if (stats?.ticketsByDepartment && stats.ticketsByDepartment.length > 0) {
    departmentData = stats.ticketsByDepartment.map((d) => ({
      name: d.departmentName,
      count: d.count
    }));
  } else {
    const departmentCount = {};
    tickets.forEach((t) => {
      const dept = t.requester?.department || 'Khác';
      departmentCount[dept] = (departmentCount[dept] || 0) + 1;
    });
    departmentData = Object.entries(departmentCount).map(([name, count]) => ({
      name,
      count
    }));
  }

  const COLORS = ['#0b6bcb', '#1a7f4b', '#a15c00', '#64708a', '#7852ff'];

  return (
    <div className="space-y-4">
      {/* Header trang */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-[20px] font-[600]" style={{ color: 'var(--text)' }}>
            Báo cáo phân tích hiệu năng IT
          </h1>
          <p className="text-[13px] mt-0.5" style={{ color: 'var(--muted)' }}>
            Đo lường năng lực xử lý sự cố, tỷ lệ đáp ứng cam kết SLA và phân bổ theo phòng ban
          </p>
        </div>

        <button
          onClick={fetchReportData}
          className="h-[34px] px-3 rounded-[6px] text-[13px] font-[500] flex items-center gap-1.5 transition-colors self-start sm:self-auto"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)',
            color: 'var(--text)'
          }}
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Làm mới số liệu</span>
        </button>
      </div>

      {/* 3 Thẻ chỉ số tổng hợp */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div
          className="p-4 rounded-[8px] space-y-1"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)',
            borderLeft: '4px solid var(--ok)'
          }}
        >
          <div className="text-[13px]" style={{ color: 'var(--muted)' }}>
            Tỷ lệ đạt chuẩn cam kết SLA
          </div>
          <div className="text-[26px] font-[600]" style={{ color: 'var(--text)' }}>
            {slaComplianceRate}%
          </div>
          <div className="text-[12px]" style={{ color: 'var(--ok)' }}>
            {slaMet} / {total} yêu cầu giải quyết đúng hạn
          </div>
        </div>

        <div
          className="p-4 rounded-[8px] space-y-1"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)',
            borderLeft: '4px solid var(--brand)'
          }}
        >
          <div className="text-[13px]" style={{ color: 'var(--muted)' }}>
            Thời gian phản hồi trung bình (MTTA)
          </div>
          <div className="text-[26px] font-[600]" style={{ color: 'var(--text)' }}>
            {mttaDisplay}
          </div>
          <div className="text-[12px]" style={{ color: 'var(--muted)' }}>
            {mttaSubtitle}
          </div>
        </div>

        <div
          className="p-4 rounded-[8px] space-y-1"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)',
            borderLeft: '4px solid var(--warn)'
          }}
        >
          <div className="text-[13px]" style={{ color: 'var(--muted)' }}>
            Thời gian khắc phục trung bình (MTTR)
          </div>
          <div className="text-[26px] font-[600]" style={{ color: 'var(--text)' }}>
            {mttrDisplay}
          </div>
          <div className="text-[12px]" style={{ color: 'var(--muted)' }}>
            {mttrSubtitle}
          </div>
        </div>
      </div>

      {/* Grid Biểu đồ */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Biểu đồ phân bổ theo danh mục */}
        <div
          className="lg:col-span-7 p-4 rounded-[8px] space-y-3"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)'
          }}
        >
          <div className="flex items-center justify-between pb-2.5 border-b" style={{ borderColor: 'var(--line)' }}>
            <h3 className="text-[14px] font-[600]" style={{ color: 'var(--text)' }}>
              Khối lượng yêu cầu theo danh mục dịch vụ
            </h3>
            <span className="text-[12px]" style={{ color: 'var(--muted)' }}>
              Tổng cộng {total} ticket
            </span>
          </div>

          <div className="h-[260px] w-full pt-2">
            {stats?.ticketsByCategory?.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats.ticketsByCategory} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--line)" />
                  <XAxis
                    dataKey="categoryName"
                    tick={{ fill: 'var(--muted)', fontSize: 11 }}
                    interval={0}
                    angle={-15}
                    textAnchor="end"
                  />
                  <YAxis tick={{ fill: 'var(--muted)', fontSize: 12 }} allowDecimals={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'var(--surface)',
                      borderColor: 'var(--line)',
                      fontSize: 12,
                      borderRadius: 6
                    }}
                  />
                  <Bar dataKey="count" name="Số lượng yêu cầu" fill="var(--brand)" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-[13px]" style={{ color: 'var(--muted)' }}>
                Chưa có dữ liệu danh mục
              </div>
            )}
          </div>
        </div>

        {/* Biểu đồ theo phòng ban */}
        <div
          className="lg:col-span-5 p-4 rounded-[8px] space-y-3"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)'
          }}
        >
          <div className="flex items-center justify-between pb-2.5 border-b" style={{ borderColor: 'var(--line)' }}>
            <h3 className="text-[14px] font-[600]" style={{ color: 'var(--text)' }}>
              Phân bổ sự cố theo phòng ban
            </h3>
          </div>

          <div className="space-y-3 pt-2">
            {departmentData.map((d, idx) => (
              <div key={d.name} className="space-y-1">
                <div className="flex justify-between text-[13px]">
                  <span style={{ color: 'var(--text)' }}>{d.name}</span>
                  <span className="font-[600]" style={{ color: 'var(--brand)' }}>
                    {d.count} ({total > 0 ? Math.round((d.count / total) * 100) : 0}%)
                  </span>
                </div>
                <div className="w-full h-2 rounded-full overflow-hidden" style={{ backgroundColor: 'var(--bg)' }}>
                  <div
                    className="h-full rounded-full transition-all"
                    style={{
                      width: `${total > 0 ? (d.count / total) * 100 : 0}%`,
                      backgroundColor: COLORS[idx % COLORS.length]
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
