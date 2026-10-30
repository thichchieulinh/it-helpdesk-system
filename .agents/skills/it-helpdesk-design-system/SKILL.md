---
name: it-helpdesk-design-system
description: Hệ thống thiết kế và quy ước code cho IT Helpdesk Ticketing System (Spring Boot + ReactJS). Dùng skill này mỗi khi tạo hoặc chỉnh sửa giao diện, component, trang hoặc API của dự án helpdesk, để giữ phong cách doanh nghiệp, gọn gàng, nhất quán.
---

# IT Helpdesk – Design System & Conventions

## Mục tiêu
Giao diện quản lý yêu cầu hỗ trợ kỹ thuật nội bộ theo phong cách phần mềm doanh nghiệp (tham chiếu: ServiceNow, Jira Service Management, Freshservice). Ưu tiên: **gọn, rõ thông tin, dễ quét mắt, nhất quán**. Không trang trí thừa.

## Tech stack
- Frontend: React 18 + Vite, React Router, TanStack Query, Axios, Ant Design 5 (tuỳ biến theme theo token bên dưới). Không dùng thêm UI library khác.
- Backend: Spring Boot 3, Spring Security + JWT, Spring Data JPA, Bean Validation, MySQL/PostgreSQL.
- Ngôn ngữ giao diện: **tiếng Việt**. Code, tên biến, tên API: tiếng Anh.

## Design tokens
Khai báo thành CSS variables ở `:root`, ghi đè trong `@media (prefers-color-scheme: dark)` và `[data-theme="dark"]`. Không hard-code màu trong component.

| Token | Light | Dark |
|---|---|---|
| --bg | #f4f6f9 | #0d1320 |
| --surface | #ffffff | #151d2e |
| --line | #e2e7ee | #26304a |
| --text | #1b2433 | #e6ebf5 |
| --muted | #64708a | #8d9ab5 |
| --nav (sidebar) | #0f1f3d | #090f1d |
| --nav-text | #aab6cf | #aab6cf |
| --brand | #0b6bcb | #4c9dff |
| --brand-soft | #e6f0fb | #16294a |
| --ok / --ok-soft | #1a7f4b / #e3f4ea | #4cc38a / #12301f |
| --warn / --warn-soft | #a15c00 / #fff1d6 | #f0b04a / #3a2a0d |
| --err / --err-soft | #c0262d / #fde8e8 | #ff7a80 / #3b1519 |
| --gray-soft | #eceff4 | #212b42 |

Quy tắc màu: chỉ **một** màu nhấn (`--brand`). Đỏ/cam/xanh lá chỉ dùng cho ngữ nghĩa trạng thái, mức ưu tiên, cảnh báo SLA. Không dùng gradient, không dùng bóng đổ nặng.

Ant Design theme mapping:
```js
theme={{ token: {
  colorPrimary: '#0b6bcb', borderRadius: 6, fontFamily: '"IBM Plex Sans", system-ui, sans-serif',
  colorBgLayout: '#f4f6f9', colorBorderSecondary: '#e2e7ee', fontSize: 14 } }}
```

## Typography
- Font duy nhất: **IBM Plex Sans** (400, 500, 600), hỗ trợ tiếng Việt. Fallback: system-ui, sans-serif.
- Cỡ chữ: 14px nội dung, 13px phụ/metadata, 12px nhãn bảng và badge, 16px tiêu đề panel, 20px tiêu đề trang, 26px số KPI.
- Viết hoa theo kiểu câu (sentence case). Không IN HOA toàn bộ nhãn, không letter-spacing rộng.

## Layout
- Shell: sidebar trái cố định 232px (nền `--nav`) + topbar cao 56px + vùng nội dung cuộn, padding 24px.
- Sidebar: logo, các nhóm menu có tiêu đề nhỏ (Tổng quan, Yêu cầu, Quản trị), badge đỏ đếm số lượng, khối thông tin người dùng ở đáy. Mục đang chọn: nền trắng 12% trong suốt, chữ trắng.
- Topbar: ô tìm kiếm (max 420px), nút chuyển giao diện sáng/tối, nút chính "+ Tạo yêu cầu".
- Trang Dashboard: hàng 4 thẻ KPI → lưới 2fr/1fr (biểu đồ + SLA) → bảng ticket.
- Card: nền `--surface`, viền 1px `--line`, bo góc 8px, không đổ bóng. Tiêu đề card 14px/600 có đường kẻ dưới.
- Responsive: dưới 900px ẩn sidebar (chuyển thành drawer menu), KPI 2 cột, lưới 1 cột. Bảng cuộn ngang trong container riêng, không để body cuộn ngang.
- Khoảng cách theo bội số của 4px (8, 12, 16, 24).

## Component specs
**KPI card:** viền trái 3px màu ngữ nghĩa, nhãn 13px muted, số 26px/600, ghi chú 12px muted. Không icon trang trí.

**Bảng ticket:** header nền `--bg`, chữ 12px muted; hàng cao ~44px, kẻ ngang 1px, hover nền `--bg`, click hàng mở drawer chi tiết, hỗ trợ Enter bằng bàn phím. Mã ticket (TK-1048) màu `--brand`, 500. Cột tiêu đề được xuống dòng, các cột khác không xuống dòng. Có tab lọc theo trạng thái kèm số đếm.

**Badge (trạng thái/ưu tiên):** pill bo 10px, chữ 12px/500, chấm tròn 6px đầu badge, nền `*-soft`, chữ và chấm màu đậm.
- Ưu tiên: Khẩn cấp = err, Cao = warn, Trung bình = brand, Thấp = muted.
- Trạng thái: Mới = brand, Đang xử lý = warn, Chờ phản hồi = muted, Đã giải quyết = ok, Đã đóng = muted.

**Drawer chi tiết ticket:** trượt từ phải, rộng tối đa 460px, có mask mờ, đóng bằng nút ✕, bấm mask hoặc phím Esc. Nội dung: mã + tiêu đề, danh sách thông tin (trạng thái, ưu tiên, người yêu cầu, danh mục, người phụ trách, hạn SLA), timeline lịch sử xử lý (đường dọc 2px, chấm tròn brand), ô phản hồi cố định ở đáy.

**Biểu đồ:** cột đôi (Mới = brand, Đã đóng = ok), lưới ngang nhạt, có chú giải, có `aria-label`. Dùng Recharts hoặc Ant Design Charts.

**Thanh SLA:** nhãn + phần trăm, thanh cao 6px bo tròn, màu `--brand`. Dưới ngưỡng cảnh báo đổi sang `--warn`/`--err`.

**Nút:** cao 34px, bo 6px. Nút chính nền `--brand` chữ trắng. Mỗi màn hình chỉ có một nút chính. Nhãn nút là động từ cụ thể: "Tạo yêu cầu", "Gửi phản hồi", "Lưu thay đổi" (không dùng "Submit/OK").

## Nội dung & microcopy (tiếng Việt)
- Ngắn gọn, động từ rõ ràng, nhất quán một thuật ngữ: dùng "yêu cầu/ticket" thống nhất, "Người yêu cầu", "Phụ trách", "Hạn SLA".
- Trạng thái rỗng phải hướng dẫn hành động: "Không có ticket phù hợp. Thử đổi bộ lọc hoặc từ khóa."
- Thông báo lỗi nêu rõ nguyên nhân và cách khắc phục, không xin lỗi dài dòng.
- Toast khớp tên hành động: bấm "Lưu thay đổi" → "Đã lưu thay đổi".
- Thời gian tương đối ở danh sách ("10 phút trước"), tuyệt đối ở chi tiết (dd/MM/yyyy HH:mm).

## Accessibility
- Focus hiển thị rõ: outline 2px `--brand`, offset 1px.
- Hàng bảng click được phải có `tabindex="0"` và xử lý Enter.
- Tương phản chữ đạt WCAG AA ở cả giao diện sáng và tối.
- Tôn trọng `prefers-reduced-motion`. Chuyển động chỉ dùng cho hành động của người dùng (mở drawer), không animation tự chạy.

## Cấu trúc frontend đề xuất
```
src/
  api/            # axios instance, interceptor JWT, hàm gọi API
  components/     # Sidebar, Topbar, KpiCard, StatusBadge, PriorityBadge, TicketTable, TicketDrawer, Timeline
  hooks/          # useTickets, useDashboardStats, useAuth, useTheme
  layouts/        # AppShell
  pages/          # Dashboard, TicketList, TicketCreate, Users, Categories, SlaPolicies, Reports, Login
  routes/         # ProtectedRoute theo role
  styles/         # tokens.css
```

## Quy ước backend
- Package: `controller`, `service`, `repository`, `entity`, `dto`, `security`, `exception`, `config`.
- Entity chính: `User`, `Role`, `Department`, `Category`, `Ticket`, `TicketComment`, `TicketHistory`, `Attachment`, `SlaPolicy`.
- Enum: `TicketStatus { NEW, IN_PROGRESS, WAITING, RESOLVED, CLOSED }`, `Priority { CRITICAL, HIGH, MEDIUM, LOW }`, `RoleName { EMPLOYEE, TECHNICIAN, ADMIN }`.
- Mã ticket dạng `TK-{số tăng dần}`.
- Luôn dùng DTO, không trả entity trực tiếp. Validate đầu vào bằng Bean Validation. Xử lý lỗi tập trung bằng `@RestControllerAdvice`, trả JSON `{ code, message, details }`.
- Mọi thay đổi trạng thái, phân công, bình luận phải ghi vào `ticket_history`.
- Phân quyền: EMPLOYEE chỉ xem và tạo ticket của mình; TECHNICIAN xử lý ticket được giao; ADMIN toàn quyền.

API chính:
```
POST  /api/auth/login
GET   /api/tickets            (lọc: status, priority, assignee, keyword, phân trang)
POST  /api/tickets
GET   /api/tickets/{id}
PATCH /api/tickets/{id}/assign
PATCH /api/tickets/{id}/status
POST  /api/tickets/{id}/comments
GET   /api/dashboard/stats
```

## Không làm
- Không thêm màu nhấn thứ hai, gradient, glassmorphism, hoặc bóng đổ lớn.
- Không dùng emoji làm icon giao diện; dùng icon Ant Design hoặc Lucide, nét mảnh.
- Không in hoa toàn bộ nhãn, không hiệu ứng xuất hiện tự động trên từng card.
- Không hard-code màu, cỡ chữ, khoảng cách ngoài token đã định nghĩa.
- Không tạo trang mới khi chưa dùng AppShell và các component dùng chung.
