import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axiosClient from '../api/axiosClient';
import {
  Briefcase,
  Headphones,
  Shield,
  ArrowRight,
  Lock,
  User as UserIcon,
  AlertCircle,
  Loader2
} from 'lucide-react';

export const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('123456');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // 3 tài khoản Demo đại diện cho 3 Role
  const demoAccounts = [
    {
      role: 'EMPLOYEE',
      roleLabel: 'Nhân viên',
      username: 'emp_nam',
      name: 'Nguyễn Văn Nam',
      department: 'Phòng Kế toán',
      description: 'Chỉ xem và gửi các yêu cầu hỗ trợ của chính mình.',
      icon: Briefcase,
      badgeBg: 'var(--gray-soft)',
      badgeColor: 'var(--muted)'
    },
    {
      role: 'AGENT',
      roleLabel: 'Kỹ thuật viên IT',
      username: 'agent_hoa',
      name: 'Trần Thị Hoa',
      department: 'Phòng IT Support',
      description: 'Xem tất cả yêu cầu trong hàng đợi, tiếp nhận xử lý và cam kết SLA.',
      icon: Headphones,
      badgeBg: 'var(--warn-soft)',
      badgeColor: 'var(--warn)'
    },
    {
      role: 'ADMIN',
      roleLabel: 'Quản trị viên',
      username: 'admin_quang',
      name: 'Lê Nhật Quang',
      department: 'Ban Quản trị CNTT',
      description: 'Toàn quyền: Giám sát KPI Dashboard và Quản lý tài khoản người dùng.',
      icon: Shield,
      badgeBg: 'var(--brand-soft)',
      badgeColor: 'var(--brand)'
    }
  ];

  const handleLogin = async (loginUsername, loginPassword = '123456') => {
    setLoading(true);
    setErrorMessage('');

    try {
      const user = await axiosClient.post('/auth/login', {
        username: loginUsername.trim(),
        password: loginPassword
      });

      login(user);
      navigate('/tickets', { replace: true });
    } catch (err) {
      console.error('Đăng nhập thất bại:', err);
      setErrorMessage(typeof err === 'string' ? err : 'Tên đăng nhập hoặc mật khẩu không chính xác.');
    } finally {
      setLoading(false);
    }
  };

  const handleManualSubmit = (e) => {
    e.preventDefault();
    if (!username.trim()) {
      setErrorMessage('Vui lòng nhập tên đăng nhập.');
      return;
    }
    handleLogin(username, password);
  };

  return (
    <div
      className="min-h-screen flex flex-col justify-center py-12 px-4 sm:px-6"
      style={{ backgroundColor: 'var(--bg)', color: 'var(--text)' }}
    >
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div
          className="inline-flex items-center justify-center w-10 h-10 rounded-[6px] font-[600] text-[14px] text-white mb-2"
          style={{ backgroundColor: 'var(--nav)' }}
        >
          IT
        </div>
        <h1 className="text-[20px] font-[600]" style={{ color: 'var(--text)' }}>
          Hệ thống IT Helpdesk
        </h1>
        <p className="mt-1 text-[13px]" style={{ color: 'var(--muted)' }}>
          Quản lý yêu cầu hỗ trợ kỹ thuật và cam kết dịch vụ (SLA)
        </p>
      </div>

      <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-[460px]">
        <div
          className="py-6 px-6 sm:px-7 rounded-[8px] space-y-5"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)'
          }}
        >
          {/* Thông báo lỗi */}
          {errorMessage && (
            <div
              className="p-3 rounded-[6px] text-[13px] flex items-center gap-2"
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

          {/* Form đăng nhập */}
          <form onSubmit={handleManualSubmit} className="space-y-4">
            <div>
              <label className="block text-[13px] font-[500] mb-1" style={{ color: 'var(--text)' }}>
                Tên đăng nhập
              </label>
              <div className="relative">
                <div
                  className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                  style={{ color: 'var(--muted)' }}
                >
                  <UserIcon className="w-4 h-4" />
                </div>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Ví dụ: emp_nam, agent_hoa, admin_quang..."
                  className="w-full pl-9 pr-3 h-[36px] text-[13px] rounded-[6px] focus:outline-none"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)'
                  }}
                />
              </div>
            </div>

            <div>
              <label className="block text-[13px] font-[500] mb-1" style={{ color: 'var(--text)' }}>
                Mật khẩu
              </label>
              <div className="relative">
                <div
                  className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                  style={{ color: 'var(--muted)' }}
                >
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Mật khẩu (mặc định: 123456)"
                  className="w-full pl-9 pr-3 h-[36px] text-[13px] rounded-[6px] focus:outline-none"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)'
                  }}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full h-[36px] px-4 rounded-[6px] text-[13px] font-[500] text-white flex items-center justify-center gap-2 transition-opacity disabled:opacity-50"
              style={{ backgroundColor: 'var(--brand)' }}
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Đang kết nối...</span>
                </>
              ) : (
                <>
                  <span>Đăng nhập</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Dòng phân cách */}
          <div className="relative pt-2">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full" style={{ borderTop: '1px solid var(--line)' }}></div>
            </div>
            <div className="relative flex justify-center text-[12px]">
              <span
                className="px-2"
                style={{ backgroundColor: 'var(--surface)', color: 'var(--muted)' }}
              >
                Chuyển nhanh tài khoản demo
              </span>
            </div>
          </div>

          {/* 3 Thẻ chuyển nhanh Demo */}
          <div className="space-y-2 pt-1">
            {demoAccounts.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.role}
                  type="button"
                  disabled={loading}
                  onClick={() => handleLogin(item.username, '123456')}
                  className="w-full p-2.5 rounded-[6px] text-left flex items-start gap-3 transition-colors group"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = 'var(--brand)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'var(--line)';
                  }}
                >
                  <div
                    className="p-1.5 rounded-[4px] shrink-0 mt-0.5"
                    style={{
                      backgroundColor: 'var(--surface)',
                      border: '1px solid var(--line)',
                      color: 'var(--text)'
                    }}
                  >
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-1">
                      <span className="text-[13px] font-[600]" style={{ color: 'var(--text)' }}>
                        {item.name}
                      </span>
                      <span
                        className="text-[11px] font-[500] px-2 py-0.5 rounded-[10px]"
                        style={{
                          backgroundColor: item.badgeBg,
                          color: item.badgeColor
                        }}
                      >
                        {item.roleLabel}
                      </span>
                    </div>
                    <div className="text-[12px] font-mono mt-0.5" style={{ color: 'var(--muted)' }}>
                      {item.username} • {item.department}
                    </div>
                    <p className="text-[11px] mt-0.5 leading-snug line-clamp-1" style={{ color: 'var(--muted)' }}>
                      {item.description}
                    </p>
                  </div>
                  <div className="self-center" style={{ color: 'var(--muted)' }}>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        <p className="mt-4 text-center text-[12px]" style={{ color: 'var(--muted)' }}>
          Hệ thống IT Helpdesk Doanh nghiệp • Spring Boot 3 & React
        </p>
      </div>
    </div>
  );
};
