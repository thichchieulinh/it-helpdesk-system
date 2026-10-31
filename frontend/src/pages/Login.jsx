import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import axiosClient from '../api/axiosClient';
import {
  Lock,
  User as UserIcon,
  AlertCircle,
  Loader2,
  Eye,
  EyeOff,
  Sun,
  Moon
} from 'lucide-react';

export const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim()) {
      setErrorMessage('Vui lòng nhập tên đăng nhập.');
      return;
    }
    if (!password) {
      setErrorMessage('Vui lòng nhập mật khẩu.');
      return;
    }

    setLoading(true);
    setErrorMessage('');

    try {
      const user = await axiosClient.post('/auth/login', {
        username: username.trim(),
        password
      });

      login(user);
      navigate('/tickets', { replace: true });
    } catch (err) {
      console.error('Đăng nhập thất bại:', err);
      if (typeof err === 'string') {
        setErrorMessage(err);
      } else if (err?.response?.data) {
        setErrorMessage(typeof err.response.data === 'string' ? err.response.data : 'Tên đăng nhập hoặc mật khẩu không chính xác.');
      } else {
        setErrorMessage('Tên đăng nhập hoặc mật khẩu không chính xác. Vui lòng thử lại.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen flex flex-col justify-center items-center py-12 px-4 sm:px-6 relative"
      style={{ backgroundColor: 'var(--bg)', color: 'var(--text)' }}
    >
      {/* Nút chuyển chế độ Sáng / Tối góc trên bên phải */}
      <div className="absolute top-4 right-4">
        <button
          type="button"
          onClick={toggleTheme}
          aria-label="Chuyển chế độ giao diện"
          className="w-[34px] h-[34px] rounded-[6px] flex items-center justify-center transition-colors"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)',
            color: 'var(--muted)'
          }}
        >
          {theme === 'dark' ? <Sun size={15} /> : <Moon size={15} />}
        </button>
      </div>

      <div className="w-full max-w-[400px] space-y-6">
        {/* Khối nhận diện hệ thống */}
        <div className="text-center space-y-2">
          <div
            className="inline-flex items-center justify-center w-10 h-10 rounded-[6px] font-[600] text-[15px] text-white shadow-none"
            style={{ backgroundColor: 'var(--brand)' }}
          >
            IT
          </div>
          <div>
            <h1 className="text-[20px] font-[600]" style={{ color: 'var(--text)' }}>
              Hệ thống IT Helpdesk
            </h1>
            <p className="mt-1 text-[13px]" style={{ color: 'var(--muted)' }}>
              Quản lý yêu cầu hỗ trợ kỹ thuật nội bộ và cam kết dịch vụ SLA
            </p>
          </div>
        </div>

        {/* Khung đăng nhập chuẩn Enterprise 2D Design */}
        <div
          className="p-6 rounded-[8px] space-y-5"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--line)'
          }}
        >
          <div className="pb-3 border-b" style={{ borderColor: 'var(--line)' }}>
            <h2 className="text-[14px] font-[600]" style={{ color: 'var(--text)' }}>
              Đăng nhập tài khoản
            </h2>
            <p className="text-[12px] mt-0.5" style={{ color: 'var(--muted)' }}>
              Nhập thông tin xác thực để truy cập hệ thống
            </p>
          </div>

          {/* Thông báo lỗi */}
          {errorMessage && (
            <div
              role="alert"
              className="p-3 rounded-[6px] text-[13px] flex items-start gap-2.5"
              style={{
                backgroundColor: 'var(--err-soft)',
                color: 'var(--err)',
                border: '1px solid var(--err)'
              }}
            >
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span className="leading-snug">{errorMessage}</span>
            </div>
          )}

          {/* Biểu mẫu đăng nhập */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label
                htmlFor="username-input"
                className="block text-[13px] font-[500] mb-1.5"
                style={{ color: 'var(--text)' }}
              >
                Tên đăng nhập
              </label>
              <div className="relative">
                <div
                  className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                  style={{ color: 'var(--muted)' }}
                >
                  <UserIcon size={15} />
                </div>
                <input
                  id="username-input"
                  type="text"
                  autoComplete="username"
                  autoFocus
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Nhập tên đăng nhập"
                  className="w-full pl-9 pr-3 h-[36px] text-[13px] rounded-[6px] focus:outline-none focus:ring-2 transition-colors"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)',
                    outlineColor: 'var(--brand)'
                  }}
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="password-input"
                className="block text-[13px] font-[500] mb-1.5"
                style={{ color: 'var(--text)' }}
              >
                Mật khẩu
              </label>
              <div className="relative">
                <div
                  className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                  style={{ color: 'var(--muted)' }}
                >
                  <Lock size={15} />
                </div>
                <input
                  id="password-input"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Nhập mật khẩu"
                  className="w-full pl-9 pr-9 h-[36px] text-[13px] rounded-[6px] focus:outline-none focus:ring-2 transition-colors"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)',
                    outlineColor: 'var(--brand)'
                  }}
                />
                <button
                  type="button"
                  tabIndex={-1}
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center transition-colors"
                  style={{ color: 'var(--muted)' }}
                  aria-label={showPassword ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'}
                >
                  {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full h-[36px] px-4 rounded-[6px] text-[13px] font-[500] text-white flex items-center justify-center gap-2 transition-opacity disabled:opacity-50 cursor-pointer"
              style={{ backgroundColor: 'var(--brand)' }}
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Đang xác thực...</span>
                </>
              ) : (
                <span>Đăng nhập</span>
              )}
            </button>
          </form>
        </div>

        {/* Thông tin chân trang */}
        <p className="text-center text-[12px]" style={{ color: 'var(--muted)' }}>
          Hệ thống Quản lý Yêu cầu Hỗ trợ Kỹ thuật Nội bộ • IT Helpdesk
        </p>
      </div>
    </div>
  );
};
