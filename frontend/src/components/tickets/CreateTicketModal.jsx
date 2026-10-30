import React, { useState, useEffect } from 'react';
import axiosClient from '../../api/axiosClient';
import { useAuth } from '../../context/AuthContext';
import { X, AlertCircle, Loader2, Check } from 'lucide-react';

export const CreateTicketModal = ({ isOpen, onClose, onSuccess }) => {
  const { currentUser } = useAuth();

  const [categories, setCategories] = useState([]);
  const [loadingCategories, setLoadingCategories] = useState(false);

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [priority, setPriority] = useState('MEDIUM');

  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Tải danh mục sự cố từ backend
  useEffect(() => {
    if (isOpen) {
      const fetchCategories = async () => {
        setLoadingCategories(true);
        try {
          const data = await axiosClient.get('/categories');
          setCategories(data);
          if (data && data.length > 0) {
            setCategoryId(data[0].id.toString());
          }
        } catch (err) {
          console.error('Lỗi khi tải danh mục:', err);
          setErrorMessage('Không thể tải danh mục sự cố từ máy chủ.');
        } finally {
          setLoadingCategories(false);
        }
      };
      fetchCategories();
      setTitle('');
      setDescription('');
      setPriority('MEDIUM');
      setErrorMessage('');
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const priorityOptions = [
    {
      value: 'LOW',
      label: 'Thấp',
      slaHours: 'SLA 48h',
      description: 'Yêu cầu không khẩn cấp, thắc mắc thông thường'
    },
    {
      value: 'MEDIUM',
      label: 'Trung bình',
      slaHours: 'SLA 24h',
      description: 'Sự cố ảnh hưởng một phần công việc cá nhân'
    },
    {
      value: 'HIGH',
      label: 'Cao',
      slaHours: 'SLA 8h',
      description: 'Hỏng hóc thiết bị, gián đoạn công việc'
    },
    {
      value: 'CRITICAL',
      label: 'Khẩn cấp',
      slaHours: 'SLA 2h',
      description: 'Sự cố tê liệt công việc phòng ban hoặc toàn hệ thống'
    }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setErrorMessage('Vui lòng nhập tiêu đề sự cố.');
      return;
    }
    if (!categoryId) {
      setErrorMessage('Vui lòng chọn danh mục sự cố.');
      return;
    }

    setSubmitting(true);
    setErrorMessage('');

    try {
      const payload = {
        title: title.trim(),
        description: description.trim(),
        priority,
        categoryId: Number(categoryId),
        requesterId: currentUser?.id
      };

      const createdTicket = await axiosClient.post('/tickets', payload);
      onSuccess?.(createdTicket);
      onClose();
    } catch (err) {
      console.error('Lỗi khi tạo ticket:', err);
      setErrorMessage(typeof err === 'string' ? err : 'Không thể gửi yêu cầu hỗ trợ.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-none">
      <div
        className="w-full max-w-xl overflow-hidden flex flex-col max-h-[90vh] rounded-[8px]"
        style={{
          backgroundColor: 'var(--surface)',
          border: '1px solid var(--line)'
        }}
      >
        {/* Modal Header */}
        <div
          className="px-5 py-3.5 flex items-center justify-between"
          style={{
            backgroundColor: 'var(--bg)',
            borderBottom: '1px solid var(--line)'
          }}
        >
          <div>
            <h2 className="text-[16px] font-[600]" style={{ color: 'var(--text)' }}>
              Tạo yêu cầu hỗ trợ mới
            </h2>
            <p className="text-[12px] mt-0.5" style={{ color: 'var(--muted)' }}>
              Hệ thống tự động tính toán thời hạn cam kết SLA dựa theo mức độ ưu tiên
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-[4px] transition-colors"
            style={{ color: 'var(--muted)' }}
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <form onSubmit={handleSubmit} className="p-5 overflow-y-auto space-y-4">
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

          {/* Chọn Danh mục */}
          <div>
            <label className="block text-[13px] font-[500] mb-1" style={{ color: 'var(--text)' }}>
              Danh mục sự cố *
            </label>
            {loadingCategories ? (
              <div className="text-[13px] py-1.5 flex items-center gap-1.5" style={{ color: 'var(--muted)' }}>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Đang tải danh mục...</span>
              </div>
            ) : (
              <select
                value={categoryId}
                onChange={(e) => setCategoryId(e.target.value)}
                className="w-full h-[34px] px-3 text-[13px] rounded-[6px] focus:outline-none"
                style={{
                  backgroundColor: 'var(--bg)',
                  border: '1px solid var(--line)',
                  color: 'var(--text)'
                }}
              >
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.name} — {cat.description}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* Chọn Mức độ ưu tiên */}
          <div>
            <label className="block text-[13px] font-[500] mb-1.5" style={{ color: 'var(--text)' }}>
              Mức độ ưu tiên & Cam kết SLA *
            </label>
            <div className="grid grid-cols-2 gap-2">
              {priorityOptions.map((opt) => {
                const isSelected = priority === opt.value;
                return (
                  <div
                    key={opt.value}
                    onClick={() => setPriority(opt.value)}
                    className="p-2.5 rounded-[6px] cursor-pointer transition-all"
                    style={{
                      border: isSelected ? '1px solid var(--brand)' : '1px solid var(--line)',
                      backgroundColor: isSelected ? 'var(--brand-soft)' : 'var(--bg)'
                    }}
                  >
                    <div className="flex items-center justify-between text-[13px]">
                      <span className="font-[600]" style={{ color: 'var(--text)' }}>
                        {opt.label} ({opt.slaHours})
                      </span>
                      {isSelected && <Check className="w-3.5 h-3.5" style={{ color: 'var(--brand)' }} />}
                    </div>
                    <p className="text-[11px] mt-0.5 line-clamp-1" style={{ color: 'var(--muted)' }}>
                      {opt.description}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Tiêu đề */}
          <div>
            <label className="block text-[13px] font-[500] mb-1" style={{ color: 'var(--text)' }}>
              Tiêu đề sự cố *
            </label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Ví dụ: Không thể kết nối VPN nội bộ, lỗi font chữ máy in..."
              className="w-full h-[34px] px-3 text-[13px] rounded-[6px] focus:outline-none"
              style={{
                backgroundColor: 'var(--bg)',
                border: '1px solid var(--line)',
                color: 'var(--text)'
              }}
            />
          </div>

          {/* Mô tả chi tiết */}
          <div>
            <label className="block text-[13px] font-[500] mb-1" style={{ color: 'var(--text)' }}>
              Mô tả chi tiết sự cố
            </label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Ghi rõ chi tiết mã lỗi, phần mềm hoặc vị trí bàn làm việc..."
              className="w-full p-2.5 text-[13px] rounded-[6px] focus:outline-none resize-none"
              style={{
                backgroundColor: 'var(--bg)',
                border: '1px solid var(--line)',
                color: 'var(--text)'
              }}
            />
          </div>

          <div
            className="p-2.5 rounded-[6px] text-[12px] flex justify-between"
            style={{
              backgroundColor: 'var(--bg)',
              border: '1px solid var(--line)',
              color: 'var(--muted)'
            }}
          >
            <span>Người tạo yêu cầu:</span>
            <span className="font-[500]" style={{ color: 'var(--text)' }}>
              {currentUser?.fullName} ({currentUser?.department})
            </span>
          </div>
        </form>

        {/* Modal Footer */}
        <div
          className="px-5 py-3 flex items-center justify-end gap-2"
          style={{
            backgroundColor: 'var(--bg)',
            borderTop: '1px solid var(--line)'
          }}
        >
          <button
            type="button"
            onClick={onClose}
            disabled={submitting}
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
            type="button"
            onClick={handleSubmit}
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
              <span>Tạo yêu cầu</span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
