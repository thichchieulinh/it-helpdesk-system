import React, { useState, useEffect } from 'react';
import axiosClient from '../api/axiosClient';
import {
  FolderPlus,
  RefreshCw,
  Search,
  CheckCircle,
  X,
  Loader2,
  AlertCircle
} from 'lucide-react';

export const ServiceCategories = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [submitting, setSubmitting] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [formError, setFormError] = useState('');

  const fetchCategories = async () => {
    setLoading(true);
    try {
      const data = await axiosClient.get('/categories');
      setCategories(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Lỗi khi tải danh mục dịch vụ:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const handleCreateCategory = async (e) => {
    e.preventDefault();
    if (!formData.name.trim()) {
      setFormError('Vui lòng nhập tên danh mục dịch vụ.');
      return;
    }

    setSubmitting(true);
    setFormError('');
    try {
      await axiosClient.post('/categories', {
        name: formData.name.trim(),
        description: formData.description.trim()
      });
      setIsModalOpen(false);
      setFormData({ name: '', description: '' });
      setToastMessage('Đã thêm danh mục dịch vụ thành công.');
      setTimeout(() => setToastMessage(''), 3000);
      fetchCategories();
    } catch (err) {
      setFormError(err.response?.data?.message || 'Không thể tạo danh mục dịch vụ.');
    } finally {
      setSubmitting(false);
    }
  };

  const filteredCategories = categories.filter(
    (c) =>
      c.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-4">
      {/* Toast thông báo */}
      {toastMessage && (
        <div
          className="fixed top-4 right-4 z-50 px-3.5 py-2.5 rounded-[6px] text-[13px] font-[500] text-white shadow-md flex items-center gap-2"
          style={{ backgroundColor: 'var(--ok)' }}
        >
          <CheckCircle className="w-4 h-4" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Header trang */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-[20px] font-[600]" style={{ color: 'var(--text)' }}>
            Danh mục dịch vụ
          </h1>
          <p className="text-[13px] mt-0.5" style={{ color: 'var(--muted)' }}>
            Phân loại các nhóm sự cố kỹ thuật và danh mục yêu cầu hỗ trợ người dùng
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchCategories}
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
            <FolderPlus className="w-4 h-4" />
            <span>Thêm danh mục</span>
          </button>
        </div>
      </div>

      {/* Tìm kiếm */}
      <div
        className="p-3 rounded-[8px] flex items-center gap-3"
        style={{
          backgroundColor: 'var(--surface)',
          border: '1px solid var(--line)'
        }}
      >
        <div className="relative flex-1">
          <Search
            className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none"
            style={{ color: 'var(--muted)' }}
          />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Tìm kiếm danh mục theo tên hoặc mô tả dịch vụ..."
            className="w-full h-[34px] pl-9 pr-3 text-[13px] rounded-[6px] focus:outline-none"
            style={{
              backgroundColor: 'var(--bg)',
              border: '1px solid var(--line)',
              color: 'var(--text)'
            }}
          />
        </div>
      </div>

      {/* Bảng danh mục dịch vụ */}
      <div
        className="rounded-[8px] overflow-hidden"
        style={{
          backgroundColor: 'var(--surface)',
          border: '1px solid var(--line)'
        }}
      >
        {loading ? (
          <div className="py-16 text-center text-[13px]" style={{ color: 'var(--muted)' }}>
            Đang tải danh mục dịch vụ...
          </div>
        ) : filteredCategories.length === 0 ? (
          <div className="py-16 text-center text-[13px]" style={{ color: 'var(--muted)' }}>
            Không tìm thấy danh mục phù hợp.
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
                  <th className="py-2.5 px-3.5 w-16">Mã</th>
                  <th className="py-2.5 px-3.5 w-64">Tên nhóm dịch vụ</th>
                  <th className="py-2.5 px-3.5">Mô tả chi tiết</th>
                  <th className="py-2.5 px-3.5 w-32 text-center">Trạng thái</th>
                </tr>
              </thead>
              <tbody>
                {filteredCategories.map((cat) => (
                  <tr
                    key={cat.id}
                    className="transition-colors"
                    style={{ borderBottom: '1px solid var(--line)', height: '44px' }}
                    onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--bg)')}
                    onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
                  >
                    <td className="py-2.5 px-3.5 font-mono font-[500]" style={{ color: 'var(--brand)' }}>
                      #{cat.id}
                    </td>
                    <td className="py-2.5 px-3.5 font-[600]" style={{ color: 'var(--text)' }}>
                      {cat.name}
                    </td>
                    <td className="py-2.5 px-3.5" style={{ color: 'var(--muted)' }}>
                      {cat.description || 'Chưa có mô tả chi tiết'}
                    </td>
                    <td className="py-2.5 px-3.5 text-center">
                      <span
                        className="px-2 py-0.5 rounded-[10px] text-[11px] font-[500]"
                        style={{ backgroundColor: 'var(--ok-soft)', color: 'var(--ok)' }}
                      >
                        Đang áp dụng
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal Thêm danh mục */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40">
          <div
            className="w-full max-w-md rounded-[8px] overflow-hidden flex flex-col shadow-lg"
            style={{
              backgroundColor: 'var(--surface)',
              border: '1px solid var(--line)'
            }}
          >
            <div
              className="px-5 py-3.5 flex items-center justify-between"
              style={{
                backgroundColor: 'var(--bg)',
                borderBottom: '1px solid var(--line)'
              }}
            >
              <h2 className="text-[15px] font-[600]" style={{ color: 'var(--text)' }}>
                Thêm danh mục dịch vụ mới
              </h2>
              <button
                onClick={() => setIsModalOpen(false)}
                className="p-1 rounded text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleCreateCategory} className="p-5 space-y-4">
              {formError && (
                <div
                  className="p-2.5 rounded-[6px] text-[13px] flex items-center gap-1.5"
                  style={{
                    backgroundColor: 'var(--err-soft)',
                    color: 'var(--err)',
                    border: '1px solid var(--err)'
                  }}
                >
                  <AlertCircle className="w-4 h-4 shrink-0" />
                  <span>{formError}</span>
                </div>
              )}

              <div>
                <label className="block text-[13px] font-[500] mb-1" style={{ color: 'var(--text)' }}>
                  Tên danh mục dịch vụ *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Ví dụ: Thiết bị mạng & Wifi, Bản quyền Microsoft..."
                  className="w-full h-[34px] px-3 text-[13px] rounded-[6px] focus:outline-none"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)'
                  }}
                />
              </div>

              <div>
                <label className="block text-[13px] font-[500] mb-1" style={{ color: 'var(--text)' }}>
                  Mô tả danh mục
                </label>
                <textarea
                  rows={3}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Ghi rõ phạm vi hỗ trợ của nhóm dịch vụ này..."
                  className="w-full p-2.5 text-[13px] rounded-[6px] focus:outline-none resize-none"
                  style={{
                    backgroundColor: 'var(--bg)',
                    border: '1px solid var(--line)',
                    color: 'var(--text)'
                  }}
                />
              </div>

              <div className="pt-2 flex items-center justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="h-[34px] px-3.5 text-[13px] font-[500] rounded-[6px] transition-colors"
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
                  className="h-[34px] px-4 text-[13px] font-[500] text-white rounded-[6px] flex items-center gap-1.5 transition-opacity disabled:opacity-50"
                  style={{ backgroundColor: 'var(--brand)' }}
                >
                  {submitting ? (
                    <>
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      <span>Đang lưu...</span>
                    </>
                  ) : (
                    <span>Lưu danh mục</span>
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
