import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Navigate } from 'react-router-dom';
import axiosClient from '../api/axiosClient';
import {
  Users,
  UserPlus,
  Search,
  Trash2,
  X,
  AlertCircle,
  RefreshCw,
  Loader2
} from 'lucide-react';

export const UserManagement = () => {
  const { currentUser } = useAuth();

  // Chỉ ADMIN mới có quyền truy cập trang này
  if (!currentUser || currentUser.role !== 'ADMIN') {
    return <Navigate to="/tickets" replace />;
  }

  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState('');

  // State Modal tạo tài khoản
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    fullName: '',
    email: '',
    department: 'Phòng Kế toán',
    role: 'EMPLOYEE'
  });
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState('');
  const [toastMessage, setToastMessage] = useState('');

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const data = await axiosClient.get('/users');
      setUsers(data);
    } catch (err) {
      console.error('Lỗi khi tải người dùng:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleCreateUser = async (e) => {
    e.preventDefault();
    setFormError('');

    if (!formData.username.trim()) {
      setFormError('Vui lòng nhập tên đăng nhập.');
      return;
    }
    if (!formData.fullName.trim()) {
      setFormError('Vui lòng nhập họ và tên.');
      return;
    }
    if (!formData.email.trim()) {
      setFormError('Vui lòng nhập email.');
      return;
    }

    setSubmitting(true);
    try {
      await axiosClient.post('/users', {
        username: formData.username.trim(),
        password: formData.password || '123456',
        fullName: formData.fullName.trim(),
        email: formData.email.trim(),
        department: formData.department.trim(),
        role: formData.role
      });

      setIsModalOpen(false);
      setFormData({
        username: '',
        password: '',
        fullName: '',
        email: '',
        department: 'Phòng Kế toán',
        role: 'EMPLOYEE'
      });
      setToastMessage(`Đã tạo tài khoản "${formData.username}" thành công.`);
      setTimeout(() => setToastMessage(''), 3000);
      fetchUsers();
    } catch (err) {
      const msg = err.response?.data?.message || err.message || 'Không thể tạo tài khoản.';
      setFormError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteUser = async (userId, username) => {
    if (userId === currentUser.id) {
      alert('Bạn không thể tự xóa tài khoản của chính mình.');
      return;
    }
    if (!window.confirm(`Xác nhận xóa tài khoản "${username}"?`)) {
      return;
    }

    try {
      await axiosClient.delete(`/users/${userId}`);
      setToastMessage(`Đã xóa tài khoản "${username}".`);
      setTimeout(() => setToastMessage(''), 3000);
      fetchUsers();
    } catch (err) {
      alert('Lỗi xóa: ' + (err.response?.data?.message || err.message));
    }
  };

  const filteredUsers = users.filter((u) => {
    const matchSearch =
      u.username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      u.fullName?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      u.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      u.department?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchRole = filterRole ? u.role === filterRole : true;
    return matchSearch && matchRole;
  });

  const getRoleBadge = (role) => {
    switch (role) {
      case 'ADMIN':
        return (
          <span
            className="px-2 py-0.5 rounded-[10px] text-[12px] font-[500]"
            style={{ backgroundColor: 'var(--brand-soft)', color: 'var(--brand)' }}
          >
            Quản trị viên
          </span>
        );
      case 'AGENT':
        return (
          <span
            className="px-2 py-0.5 rounded-[10px] text-[12px] font-[500]"
            style={{ backgroundColor: 'var(--warn-soft)', color: 'var(--warn)' }}
          >
            Kỹ thuật viên IT
          </span>
        );
      case 'EMPLOYEE':
      default:
        return (
          <span
            className="px-2 py-0.5 rounded-[10px] text-[12px] font-[500]"
            style={{ backgroundColor: 'var(--gray-soft)', color: 'var(--muted)' }}
          >
            Nhân viên
          </span>
        );
    }
  };

  return (
    <div className="space-y-4">
      {/* Toast thông báo */}
      {toastMessage && (
        <div
          className="fixed top-4 right-4 z-50 px-3.5 py-2.5 rounded-[6px] text-[13px] font-[500] text-white shadow-lg"
          style={{ backgroundColor: 'var(--ok)' }}
        >
          {toastMessage}
        </div>
      )}

      {/* Header trang */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-[20px] font-[600]" style={{ color: 'var(--text)' }}>
            Quản lý tài khoản & phân quyền
          </h1>
          <p className="text-[13px] mt-0.5" style={{ color: 'var(--muted)' }}>
            Danh sách nhân sự, phân vai trò người dùng và cấp tài khoản mới
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchUsers}
            className="h-[34px] px-3 rounded-[6px] text-[13px] font-[500] flex items-center gap-1.5 transition-colors"
            style={{
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--line)',
              color: 'var(--text)'
            }}
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Làm mới</span>
          </button>

          <button
            onClick={() => setIsModalOpen(true)}
            className="h-[34px] px-3.5 rounded-[6px] text-[13px] font-[500] text-white flex items-center gap-1.5 transition-colors"
            style={{ backgroundColor: 'var(--brand)' }}
          >
            <UserPlus className="w-4 h-4" />
            <span>Tạo tài khoản</span>
          </button>
        </div>
      </div>

      {/* Ô tìm kiếm & Bộ lọc */}
      <div
        className="p-3 rounded-[8px] flex flex-col sm:flex-row items-center gap-3"
        style={{
          backgroundColor: 'var(--surface)',
          border: '1px solid var(--line)'
        }}
      >
        <div className="relative flex-1 w-full">
          <Search
            className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
            style={{ color: 'var(--muted)' }}
          />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Tìm theo tên đăng nhập, họ tên, email hoặc phòng ban..."
            className="w-full h-[34px] pl-9 pr-3 text-[13px] rounded-[6px] focus:outline-none"
            style={{
              backgroundColor: 'var(--bg)',
              border: '1px solid var(--line)',
              color: 'var(--text)'
            }}
          />
        </div>

        <div className="w-full sm:w-48">
          <select
            value={filterRole}
            onChange={(e) => setFilterRole(e.target.value)}
            className="w-full h-[34px] px-2.5 text-[13px] rounded-[6px] focus:outline-none"
            style={{
              backgroundColor: 'var(--bg)',
              border: '1px solid var(--line)',
              color: 'var(--text)'
            }}
          >
            <option value="">Tất cả vai trò</option>
            <option value="EMPLOYEE">Nhân viên (EMPLOYEE)</option>
            <option value="AGENT">Kỹ thuật viên IT (AGENT)</option>
            <option value="ADMIN">Quản trị viên (ADMIN)</option>
          </select>
        </div>
      </div>

      {/* Bảng dữ liệu người dùng */}
      <div
        className="rounded-[8px] overflow-hidden"
        style={{
          backgroundColor: 'var(--surface)',
          border: '1px solid var(--line)'
        }}
      >
        {loading ? (
          <div className="py-16 text-center text-[13px]" style={{ color: 'var(--muted)' }}>
            Đang tải dữ liệu...
          </div>
        ) : filteredUsers.length === 0 ? (
          <div className="py-16 text-center text-[13px]" style={{ color: 'var(--muted)' }}>
            Không tìm thấy người dùng phù hợp.
          </div>
        ) : (
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
                  <th className="py-2.5 px-3.5">Tài khoản</th>
                  <th className="py-2.5 px-3.5">Họ và tên</th>
                  <th className="py-2.5 px-3.5">Email</th>
                  <th className="py-2.5 px-3.5">Phòng ban</th>
                  <th className="py-2.5 px-3.5">Vai trò</th>
                  <th className="py-2.5 px-3.5 text-right">Thao tác</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map((u) => (
                  <tr
                    key={u.id}
                    className="transition-colors"
                    style={{ borderBottom: '1px solid var(--line)', height: '44px' }}
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--bg)')}
                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
                  >
                    <td className="py-2.5 px-3.5 font-mono font-[500]" style={{ color: 'var(--brand)' }}>
                      {u.username}
                      {u.id === currentUser.id && (
                        <span
                          className="ml-1.5 text-[10px] px-1.5 py-0.2 rounded font-sans"
                          style={{ backgroundColor: 'var(--brand-soft)', color: 'var(--brand)' }}
                        >
                          Bạn
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 px-3.5 font-[500]" style={{ color: 'var(--text)' }}>
                      {u.fullName}
                    </td>
                    <td className="py-2.5 px-3.5 font-mono text-[12px]" style={{ color: 'var(--muted)' }}>
                      {u.email}
                    </td>
                    <td className="py-2.5 px-3.5" style={{ color: 'var(--text)' }}>
                      {u.department || 'Nội bộ'}
                    </td>
                    <td className="py-2.5 px-3.5">
                      {getRoleBadge(u.role)}
                    </td>
                    <td className="py-2.5 px-3.5 text-right">
                      {u.id !== currentUser.id ? (
                        <button
                          onClick={() => handleDeleteUser(u.id, u.username)}
                          title="Xóa tài khoản"
                          className="p-1.5 rounded-[4px] hover:bg-slate-100 text-slate-400 hover:text-[var(--err)] transition-colors"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      ) : (
                        <span className="text-[11px] italic" style={{ color: 'var(--muted)' }}>
                          Hiện tại
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div
          className="p-3 text-[12px] flex items-center justify-between"
          style={{
            backgroundColor: 'var(--bg)',
            color: 'var(--muted)',
            borderTop: '1px solid var(--line)'
          }}
        >
          <span>Tổng cộng: <strong>{filteredUsers.length}</strong> tài khoản</span>
          <span className="font-mono text-[11px]">Database: H2 Local Persistent</span>
        </div>
      </div>

      {/* Modal Tạo Tài Khoản Mới */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40">
          <div
            className="rounded-[8px] w-full max-w-md shadow-xl overflow-hidden"
            style={{
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--line)',
              color: 'var(--text)'
            }}
          >
            {/* Modal Header */}
            <div
              className="px-4 py-3 flex items-center justify-between"
              style={{ borderBottom: '1px solid var(--line)', backgroundColor: 'var(--bg)' }}
            >
              <span className="text-[14px] font-[600]">Tạo tài khoản mới</span>
              <button onClick={() => setIsModalOpen(false)} className="p-1 rounded text-slate-400 hover:text-slate-700">
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Modal Form */}
            <form onSubmit={handleCreateUser} className="p-4 space-y-3">
              {formError && (
                <div
                  className="p-2.5 rounded-[6px] text-[12px] flex items-center gap-1.5"
                  style={{ backgroundColor: 'var(--err-soft)', color: 'var(--err)' }}
                >
                  <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                  <span>{formError}</span>
                </div>
              )}

              <div>
                <label className="block text-[12px] font-[500] mb-1" style={{ color: 'var(--muted)' }}>
                  Tên đăng nhập (Username) *
                </label>
                <input
                  type="text"
                  required
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  placeholder="Ví dụ: it_hoang, hr_lan..."
                  className="w-full h-[34px] px-3 text-[13px] rounded-[6px] font-mono focus:outline-none"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)'
                  }}
                />
              </div>

              <div>
                <label className="block text-[12px] font-[500] mb-1" style={{ color: 'var(--muted)' }}>
                  Mật khẩu
                </label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  placeholder="Mặc định: 123456"
                  className="w-full h-[34px] px-3 text-[13px] rounded-[6px] font-mono focus:outline-none"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)'
                  }}
                />
              </div>

              <div>
                <label className="block text-[12px] font-[500] mb-1" style={{ color: 'var(--muted)' }}>
                  Họ và tên *
                </label>
                <input
                  type="text"
                  required
                  value={formData.fullName}
                  onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                  placeholder="Ví dụ: Hoàng Văn An"
                  className="w-full h-[34px] px-3 text-[13px] rounded-[6px] focus:outline-none"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)'
                  }}
                />
              </div>

              <div>
                <label className="block text-[12px] font-[500] mb-1" style={{ color: 'var(--muted)' }}>
                  Địa chỉ Email *
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder="Ví dụ: an.hoang@company.vn"
                  className="w-full h-[34px] px-3 text-[13px] rounded-[6px] focus:outline-none"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)'
                  }}
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[12px] font-[500] mb-1" style={{ color: 'var(--muted)' }}>
                    Phòng ban
                  </label>
                  <select
                    value={formData.department}
                    onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                    className="w-full h-[34px] px-2.5 text-[13px] rounded-[6px] focus:outline-none"
                    style={{
                      backgroundColor: 'var(--bg)',
                      border: '1px solid var(--line)',
                      color: 'var(--text)'
                    }}
                  >
                    <option value="Phòng IT Support">Phòng IT Support</option>
                    <option value="Phòng Kế toán">Phòng Kế toán</option>
                    <option value="Phòng Nhân sự">Phòng Nhân sự</option>
                    <option value="Phòng Kinh doanh">Phòng Kinh doanh</option>
                    <option value="Ban Giám đốc">Ban Giám đốc</option>
                  </select>
                </div>

                <div>
                  <label className="block text-[12px] font-[500] mb-1" style={{ color: 'var(--muted)' }}>
                    Vai trò (Role) *
                  </label>
                  <select
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                    className="w-full h-[34px] px-2.5 text-[13px] rounded-[6px] font-[500] focus:outline-none"
                    style={{
                      backgroundColor: 'var(--bg)',
                      border: '1px solid var(--line)',
                      color: 'var(--text)'
                    }}
                  >
                    <option value="EMPLOYEE">Nhân viên (EMPLOYEE)</option>
                    <option value="AGENT">Kỹ thuật viên IT (AGENT)</option>
                    <option value="ADMIN">Quản trị viên (ADMIN)</option>
                  </select>
                </div>
              </div>

              {/* Modal Footer */}
              <div className="pt-3 flex items-center justify-end gap-2" style={{ borderTop: '1px solid var(--line)' }}>
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="h-[34px] px-3 rounded-[6px] text-[13px] font-[500] transition-colors"
                  style={{
                    backgroundColor: 'var(--surface)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)'
                  }}
                >
                  Hủy bỏ
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="h-[34px] px-3.5 rounded-[6px] text-[13px] font-[500] text-white flex items-center gap-1.5 transition-colors disabled:opacity-50"
                  style={{ backgroundColor: 'var(--brand)' }}
                >
                  {submitting ? (
                    <>
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      <span>Đang lưu...</span>
                    </>
                  ) : (
                    <span>Lưu tài khoản</span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
