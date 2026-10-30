import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useTheme } from '../../context/ThemeContext';
import { useNavigate } from 'react-router-dom';
import {
  Search,
  Sun,
  Moon,
  Plus,
  LogOut,
  X
} from 'lucide-react';

export const Header = ({ onOpenCreateModal }) => {
  const { currentUser, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');

  if (!currentUser) return null;

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      navigate(`/tickets?search=${encodeURIComponent(searchTerm.trim())}`);
    }
  };

  return (
    <header
      className="h-[56px] px-6 flex items-center justify-between sticky top-0 z-20 shrink-0"
      style={{
        backgroundColor: 'var(--surface)',
        borderBottom: '1px solid var(--line)'
      }}
    >
      {/* Ô tìm kiếm toàn cục (max 420px theo Design System) */}
      <form onSubmit={handleSearchSubmit} className="flex-1 max-w-[420px]">
        <div className="relative">
          <Search
            className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
            style={{ color: 'var(--muted)' }}
          />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Tìm kiếm ticket theo mã hoặc từ khóa..."
            className="w-full h-[34px] pl-9 pr-8 text-[13px] rounded-[6px] focus:outline-none transition-colors"
            style={{
              backgroundColor: 'var(--bg)',
              border: '1px solid var(--line)',
              color: 'var(--text)'
            }}
          />
          {searchTerm && (
            <button
              type="button"
              onClick={() => setSearchTerm('')}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 p-0.5 text-slate-400 hover:text-slate-600"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </form>

      {/* Cụm công cụ bên phải */}
      <div className="flex items-center gap-3">
        {/* Nút chuyển giao diện sáng / tối */}
        <button
          onClick={toggleTheme}
          title={theme === 'dark' ? 'Chuyển sang giao diện Sáng' : 'Chuyển sang giao diện Tối'}
          className="h-[34px] w-[34px] rounded-[6px] flex items-center justify-center transition-colors"
          style={{
            border: '1px solid var(--line)',
            backgroundColor: 'var(--surface)',
            color: 'var(--text)'
          }}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
        </button>

        {/* Nút chính duy nhất: + Tạo yêu cầu (cao 34px, bo 6px, nền --brand) */}
        <button
          onClick={onOpenCreateModal}
          className="h-[34px] px-3.5 rounded-[6px] text-[13px] font-[500] text-white flex items-center gap-1.5 transition-colors cursor-pointer"
          style={{ backgroundColor: 'var(--brand)' }}
        >
          <Plus className="w-4 h-4" />
          <span>Tạo yêu cầu</span>
        </button>

        <div className="h-4 w-[1px] mx-1" style={{ backgroundColor: 'var(--line)' }} />

        {/* Nút Đăng xuất */}
        <button
          onClick={logout}
          title="Đăng xuất khỏi hệ thống"
          className="h-[34px] px-2.5 rounded-[6px] text-[13px] flex items-center gap-1.5 transition-colors"
          style={{
            border: '1px solid var(--line)',
            color: 'var(--muted)',
            backgroundColor: 'var(--surface)'
          }}
        >
          <LogOut className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Thoát</span>
        </button>
      </div>
    </header>
  );
};
