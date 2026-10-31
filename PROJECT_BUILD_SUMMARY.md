# TỔNG HỢP KIẾN TRÚC VÀ QUÁ TRÌNH XÂY DỰNG DỰ ÁN IT HELPDESK TICKETING SYSTEM

Tài liệu này tổng hợp toàn bộ thông tin kỹ thuật, kiến trúc hệ thống, cơ sở dữ liệu, API, quy trình nghiệp vụ và cách thức triển khai của dự án **IT Helpdesk Ticketing System (Spring Boot 3 + ReactJS Vite)**. Tài liệu được cấu trúc chuẩn mực để có thể nạp trực tiếp vào Claude hoặc các mô hình AI khác phục vụ việc viết báo cáo, tài liệu kỹ thuật hoặc đồ án tốt nghiệp.

---

## 1. TỔNG QUAN DỰ ÁN

- **Tên đề tài**: Phân tích, thiết kế và xây dựng Hệ thống Quản lý Yêu cầu Hỗ trợ Kỹ thuật Nội bộ (IT Helpdesk Ticketing System).
- **Mục tiêu**: Xây dựng phần mềm hỗ trợ doanh nghiệp số hóa quy trình tiếp nhận sự cố CNTT, phân loại danh mục dịch vụ, tự động tính toán thời hạn cam kết dịch vụ (SLA - Service Level Agreement), phân quyền xử lý theo vai trò và giám sát hiệu năng qua Dashboard & Báo cáo.
- **Phong cách thiết kế**: Enterprise 2D Design System (tham chiếu chuẩn mực ServiceNow, Jira Service Management, Freshservice). Giao diện phẳng, tinh gọn, không gradient rườm rà, sử dụng font chữ **IBM Plex Sans** và hỗ trợ 2 chế độ **Sáng / Tối (Light / Dark mode)**.

---

## 2. STACK CÔNG NGHỆ VÀ MÔI TRƯỜNG

### 2.1. Backend (Máy chủ API - Port 8080)
- **Ngôn ngữ**: Java 17 LTS.
- **Framework**: Spring Boot 3.3.5.
- **Tầng dữ liệu (ORM)**: Spring Data JPA, Hibernate.
- **Cơ sở dữ liệu**: H2 Database cấu hình lưu trữ bền vững dạng file cục bộ (`jdbc:h2:file:./data/helpdesk_db`).
  - H2 Web Console: `http://localhost:8080/h2-console` (User: `sa`, Password: rỗng).
- **Thư viện bổ trợ**:
  - `Lombok`: Giảm thiểu boilerplate code (`@Getter`, `@Setter`, `@Builder`, `@RequiredArgsConstructor`).
  - `Jakarta Validation`: Kiểm tra ràng buộc dữ liệu đầu vào (`@NotBlank`, `@NotNull`, `@Valid`).
  - `Spring Task Scheduling`: Quét ngầm tự động định kỳ (`@EnableScheduling`, `@Scheduled`).
- **Cấu hình CORS toàn cục**: `WebConfig.java` cho phép cổng `http://localhost:5173` gọi các phương thức `GET, POST, PUT, PATCH, DELETE, OPTIONS`.

### 2.2. Frontend (Giao diện người dùng - Port 5173)
- **Nền tảng**: React 18, xây dựng với **Vite 5**.
- **Định tuyến**: `react-router-dom` v6/v7 (SPA - Single Page Application).
- **HTTP Client**: `axios` cấu hình tập trung tại `axiosClient.js` (`baseURL: 'http://localhost:8080/api'`).
- **Styling**: Tailwind CSS kết hợp bộ CSS Variables tokens thuần (`tokens.css`).
- **Biểu đồ số liệu**: `recharts` (BarChart, ResponsiveContainer, Tooltip, CartesianGrid).
- **Biểu tượng**: `lucide-react`.

---

## 3. THIẾT KẾ CƠ SỞ DỮ LIỆU (5 THỰC THỂ CHÍNH)

Hệ thống được thiết kế dạng CSDL quan hệ chuẩn 3NF:

### 3.1. Bảng `users` (Nhân sự & Tài khoản)
- `id` (BIGINT, PK, Auto Increment)
- `username` (VARCHAR(50), Unique, Not Null): Tên đăng nhập.
- `password` (VARCHAR(255), Not Null): Mật khẩu (được đánh dấu `@JsonProperty(access = Access.WRITE_ONLY)` để không lộ ra JSON).
- `fullName` (VARCHAR(100), Not Null): Họ và tên nhân viên.
- `email` (VARCHAR(100), Unique, Not Null): Email liên hệ.
- `department` (VARCHAR(100)): Phòng ban làm việc (Kế toán, IT Support, Kinh doanh, Ban Giám đốc...).
- `role` (VARCHAR(20), Enum: `EMPLOYEE`, `AGENT`, `ADMIN`): Vai trò hệ thống.

### 3.2. Bảng `categories` (Danh mục dịch vụ CNTT)
- `id` (BIGINT, PK, Auto Increment)
- `name` (VARCHAR(100), Not Null): Tên danh mục (Phần mềm & Bản quyền, Phần cứng & Thiết bị, Hạ tầng mạng & Tài khoản, Email & Lưu trữ Cloud...).
- `description` (VARCHAR(255)): Phạm vi hỗ trợ của nhóm dịch vụ.

### 3.3. Bảng `sla_policies` (Chính sách cam kết dịch vụ SLA)
- `id` (BIGINT, PK, Auto Increment)
- `priorityLevel` (VARCHAR(20), Enum: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, Unique, Not Null).
- `resolutionTimeHours` (INT, Not Null): Số giờ cam kết giải quyết dứt điểm sự cố:
  - `CRITICAL`: 2 giờ (Phản hồi <= 15 phút).
  - `HIGH`: 8 giờ (Phản hồi <= 30 phút).
  - `MEDIUM`: 24 giờ (Phản hồi <= 2 giờ).
  - `LOW`: 48 giờ (Phản hồi <= 4 giờ).

### 3.4. Bảng `tickets` (Phiếu yêu cầu hỗ trợ)
- `id` (BIGINT, PK, Auto Increment)
- `ticketCode` (VARCHAR(30), Unique, Not Null): Mã phiếu duy nhất tự sinh (`HD-2026-xxxx`).
- `title` (VARCHAR(255), Not Null): Tiêu đề sự cố ngắn gọn.
- `description` (TEXT): Mô tả chi tiết sự cố, vị trí bàn làm việc, mã lỗi.
- `status` (VARCHAR(20), Enum: `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`): Trạng thái phiếu.
- `priority` (VARCHAR(20), Enum: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
- `category_id` (BIGINT, FK -> `categories.id`): Nhóm danh mục sự cố.
- `requester_id` (BIGINT, FK -> `users.id`): Người tạo yêu cầu.
- `assignee_id` (BIGINT, FK -> `users.id`, Nullable): Kỹ thuật viên IT phụ trách.
- `createdAt` (TIMESTAMP): Thời điểm gửi yêu cầu.
- `dueDate` (TIMESTAMP): Hạn chót hoàn thành theo cam kết SLA (`dueDate = createdAt + resolutionTimeHours`).
- `acknowledgedAt` (TIMESTAMP, Nullable): Thời điểm kỹ thuật viên tiếp nhận xử lý lần đầu (chuyển sang `IN_PROGRESS` hoặc gán KTV). Phục vụ tính MTTA.
- `resolvedAt` (TIMESTAMP, Nullable): Thời điểm kỹ thuật viên đánh dấu hoàn tất (`RESOLVED` hoặc `CLOSED`). Phục vụ tính MTTR.
- `closedAt` (TIMESTAMP, Nullable): Thời điểm người yêu cầu hoặc Admin đóng phiếu.
- `isOverdue` (BOOLEAN, Default: false): Cờ đánh dấu sự cố bị trễ hạn SLA.

### 3.5. Bảng `ticket_comments` (Thảo luận & Lịch sử xử lý)
- `id` (BIGINT, PK, Auto Increment)
- `ticket_id` (BIGINT, FK -> `tickets.id`): Gắn liền với ticket cụ thể.
- `user_id` (BIGINT, FK -> `users.id`): Người gửi phản hồi (Nhân viên hoặc Kỹ thuật viên).
- `content` (TEXT, Not Null): Nội dung trao đổi, ghi chú kỹ thuật, giải pháp xử lý.
- `createdAt` (TIMESTAMP): Thời điểm bình luận.

---

## 4. HỆ THỐNG RESTFUL API (BACKEND ENDPOINTS)

### 4.1. Xác thực (`/api/auth`)
- `POST /api/auth/login`: Xác thực đăng nhập bằng `{ username, password }`. Trả về thông tin User và Role.

### 4.2. Quản lý Ticket (`/api/tickets`)
- `GET /api/tickets`: Lấy danh sách ticket. Hỗ trợ lọc theo:
  - `status`: `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`.
  - `priority`: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
  - `search`: Tìm kiếm tương đối theo mã ticket, tiêu đề, mô tả.
  - `requesterId`: Lọc theo người gửi.
- `GET /api/tickets/{id}`: Xem chi tiết 1 ticket (tự động cập nhật cờ `isOverdue`).
- `POST /api/tickets`: Tạo ticket mới. Nhận `{ title, description, priority, categoryId, requesterId }`. Backend tự động tính `dueDate` và sinh mã `HD-xxxx`.
- `PATCH /api/tickets/{id}/status`: Cập nhật trạng thái và kỹ thuật viên tiếp nhận:
  - Tiếp nhận: `status = IN_PROGRESS`, gán `assigneeId`.
  - Giải quyết: `status = RESOLVED`, cập nhật `resolvedAt`.
  - Đóng phiếu: `status = CLOSED`, cập nhật `closedAt`.
  - Mở lại: `status = IN_PROGRESS`.
- `GET /api/tickets/{id}/comments`: Lấy danh sách bình luận thảo luận theo ticket.
- `POST /api/tickets/{id}/comments`: Gửi bình luận mới `{ userId, content }`.

### 4.3. Quản lý Danh mục (`/api/categories`)
- `GET /api/categories`: Danh sách tất cả nhóm dịch vụ.
- `GET /api/categories/{id}`: Chi tiết 1 danh mục.
- `POST /api/categories`: Tạo danh mục dịch vụ mới `{ name, description }`.

### 4.4. Quản lý Người dùng (`/api/users`)
- `GET /api/users`: Lấy danh sách tất cả nhân sự.
- `POST /api/users`: Tạo tài khoản mới `{ username, password, fullName, email, department, role }`. Có kiểm tra trùng lặp `username` và `email`.
- `DELETE /api/users/{id}`: Xóa tài khoản nhân sự (có cơ chế chặn Admin tự xóa chính mình).

### 4.5. Chính sách SLA (`/api/sla-policies`)
- `GET /api/sla-policies`: Lấy danh sách 4 mức cam kết SLA.
- `PUT /api/sla-policies/{id}`: Cập nhật số giờ xử lý cam kết.

### 4.6. Bảng điều khiển & Báo cáo (`/api/dashboard`)
- `GET /api/dashboard/stats`: Thống kê tổng hợp số liệu thực tế:
  - `totalTickets`, `openTickets`, `inProgressTickets`, `resolvedTickets`, `closedTickets`, `overdueTickets`.
  - `slaComplianceRate` (% tỷ lệ giải quyết đúng hạn thực tế, ví dụ `80.0%`), `slaMetTickets` (số phiếu đúng hạn).
  - `mttaMinutes` (số phút phản hồi trung bình), `mttaFormatted` (`25 phút`), `mttaCount` (số ticket tính MTTA).
  - `mttrHours` (số giờ khắc phục trung bình), `mttrFormatted` (`3.0 giờ`), `mttrCount` (số ticket tính MTTR).
  - Thống kê mảng `ticketsByStatus` (số lượng theo trạng thái).
  - Thống kê mảng `ticketsByCategory` (số lượng theo nhóm dịch vụ).
  - Thống kê mảng `ticketsByDepartment` (số lượng theo từng phòng ban).

---

## 5. CÁC PHÂN HỆ VÀ TÍNH NĂNG ĐẶC SẮC TRÊN FRONTEND

### 5.1. Phân quyền vai trò (Role-Based Access Control)
Hệ thống thiết lập 3 vai trò có phân chia màn hình và quyền hạn chặt chẽ:
1. **EMPLOYEE (Nhân viên - Demo: `emp_nam` / `123456`)**:
   - Chỉ xem và quản lý các yêu cầu do chính mình tạo.
   - Gửi yêu cầu hỗ trợ mới qua Modal.
   - Tham gia bình luận sự cố và bấm nút "Xác nhận đóng phiếu" khi hài lòng.
   - **Bảo mật Navbar**: Không nhìn thấy menu "Người dùng & phòng ban".
2. **AGENT (Kỹ thuật viên IT - Demo: `agent_hoa` / `123456`)**:
   - Xem hàng đợi sự cố toàn công ty (*Tất cả ticket*, *Của tôi*, *Chưa phân công*).
   - Nút thao tác nghiệp vụ: "Tiếp nhận xử lý" (gán cho tôi), "Đánh dấu Đã giải quyết", "Mở lại yêu cầu".
   - Trao đổi bình luận kỹ thuật với người dùng.
   - Xem Dashboard KPI và Danh mục dịch vụ.
   - **Bảo mật Navbar**: Không nhìn thấy menu "Người dùng & phòng ban".
3. **ADMIN (Quản trị viên - Demo: `admin_quang` / `123456`)**:
   - Toàn bộ quyền của Agent.
   - **Độc quyền quản trị**: Được phép nhìn thấy và truy cập menu **"Người dùng & phòng ban" (`/users`)** để cấp tài khoản mới và xóa tài khoản.
   - Xem toàn bộ Báo cáo phân tích hiệu năng (`/reports`), Dashboard KPI và quản lý chính sách SLA (`/sla-policies`).

### 5.2. Ngăn trượt chi tiết Ticket (TicketDetailDrawer)
- Thay vì chuyển trang truyền thống làm mất ngữ cảnh và bộ lọc danh sách, khi nhấp vào bất kỳ hàng nào trên bảng (hoặc ấn `Enter`), ngăn chi tiết trượt ra từ cạnh phải màn hình (rộng tối đa 460px).
- Có mask nền mờ, đóng nhanh bằng nút ✕, click mask hoặc ấn phím `Esc`.
- Tích hợp đầy đủ thông tin: Mã ticket, tiêu đề, mô tả, mức ưu tiên, hạn SLA, người yêu cầu, kỹ thuật viên phụ trách, timeline bình luận và ô gửi phản hồi cố định ở đáy.
- Cho phép xử lý chuyển đổi trạng thái (Tiếp nhận -> Đã giải quyết -> Đóng) ngay trên ngăn trượt.

### 5.3. Hàng đợi Ticket đa góc nhìn
- **Tất cả ticket** (`/tickets`): Danh sách toàn bộ phiếu trong hệ thống.
- **Của tôi** (`/tickets?view=my`): Lọc phiếu do chính người đăng nhập tạo hoặc được giao phụ trách (kèm badge tròn đỏ hiển thị số lượng).
- **Chưa phân công** (`/tickets?view=unassigned`): Lọc phiếu mới đang chờ kỹ thuật viên tiếp nhận (kèm badge tròn đỏ hiển thị số lượng).

### 5.4. Tính toán SLA và Quét ngầm định kỳ (SLA Scheduler)
- **Tự động tính hạn chót**: Ngay khi tạo phiếu, Backend lấy cấu hình SLA của mức ưu tiên tương ứng và tính `dueDate = createdAt + resolutionTimeHours`.
- **Tác vụ quét ngầm (`SlaScheduler.java`)**: Sử dụng `@Scheduled(fixedRate = 60000)` chạy ngầm mỗi phút một lần. Tự động kiểm tra các ticket chưa hoàn tất (`status != RESOLVED && status != CLOSED`) mà thời gian hiện tại `now.isAfter(dueDate)`, tự động kích hoạt cờ `isOverdue = true`.
- **Thanh đo tuân thủ SLA**: Trên Dashboard hiển thị thanh đo tỷ lệ giải quyết đúng hạn (% compliance). Thanh cao 6px bo tròn, tự động đổi màu xanh (`--ok`) -> vàng (`--warn`) -> đỏ (`--err`) khi tỷ lệ rơi xuống dưới ngưỡng tiêu chuẩn.

### 5.5. Phân hệ Báo cáo phân tích hiệu năng (`/reports`)
- Chỉ số chất lượng dịch vụ tính toán thực tế từ hệ CSDL:
  - **Tỷ lệ đạt chuẩn SLA (%)**: Tính toán động từ tỷ lệ phiếu hoàn tất đúng hạn: $\text{SLA Compliance} = \frac{\text{Tổng ticket} - \text{Ticket quá hạn}}{\text{Tổng ticket}} \times 100\%$ (đạt 80.0% trên tập dữ liệu kiểm thử, 4/5 ticket tuân thủ).
  - **MTTA (Mean Time to Acknowledge)**: Thời gian phản hồi trung bình ban đầu từ khi tạo ticket đến khi kỹ thuật viên tiếp nhận xử lý: $\text{MTTA} = \frac{1}{N} \sum (t_{\text{acknowledged}} - t_{\text{created}})$ (đạt 25 phút trên 4 ticket đã tiếp nhận, nhanh hơn ngưỡng tiêu chuẩn <= 30 phút).
  - **MTTR (Mean Time to Resolve)**: Thời gian khắc phục trung bình sự cố từ khi tạo đến khi giải quyết dứt điểm: $\text{MTTR} = \frac{1}{M} \sum (t_{\text{resolved}} - t_{\text{created}})$ (đạt 3.0 giờ trên các ticket đã xử lý dứt điểm).
- Trực quan hóa dữ liệu với `recharts`: Biểu đồ cột phân bổ yêu cầu theo danh mục dịch vụ và biểu đồ thanh phân bổ sự cố theo phòng ban đồng bộ từ API.

### 5.6. Enterprise 2D Design System (tokens.css)
- Bộ biến màu CSS tokens chuẩn mực:
  - `--bg`: Nền tổng thể (`#f4f6f9` sáng / `#0d1320` tối).
  - `--surface`: Nền thẻ, panel, bảng (`#ffffff` sáng / `#151d2e` tối).
  - `--line`: Viền phân cách phẳng 1px (`#e2e7ee` sáng / `#26304a` tối).
  - `--text` & `--muted`: Chữ nội dung và chữ phụ (`#1b2433` / `#64708a`).
  - `--nav`: Nền thanh bên Sidebar cố định 232px màu xanh navy đậm (`#0f1f3d` sáng / `#090f1d` tối).
  - `--brand`: Màu nhấn chủ đạo duy nhất (`#0b6bcb` sáng / `#4c9dff` tối).
  - `--ok`, `--warn`, `--err`: Màu ngữ nghĩa trạng thái và cảnh báo SLA.
- Typography: Font duy nhất **IBM Plex Sans**, cỡ chữ phân cấp rõ ràng (26px KPI, 20px tiêu đề trang, 16px section, 14px body, 12px badge).

---

## 6. CẤU TRÚC THƯ MỤC MÃ NGUỒN DỰ ÁN

```
ProjectTTDN/
├── backend/
│   ├── src/main/java/com/helpdesk/
│   │   ├── config/              # WebConfig.java (CORS configuration)
│   │   ├── controller/          # REST Controllers (Auth, Ticket, Category, User, SlaPolicy, Dashboard)
│   │   ├── dto/                 # Request/Response Data Transfer Objects
│   │   ├── entity/              # JPA Entities (User, Category, SlaPolicy, Ticket, TicketComment)
│   │   │   └── enums/           # Role.java, Priority.java, TicketStatus.java
│   │   ├── initializer/         # DataInitializer.java (Seed dữ liệu mẫu ban đầu)
│   │   ├── repository/          # Spring Data JPA Repositories
│   │   ├── scheduler/           # SlaScheduler.java (Quét ngầm tự động ticket quá hạn)
│   │   └── service/             # Business Logic Layer (UserService, TicketService, CategoryService, DashboardService)
│   ├── src/main/resources/
│   │   └── application.properties # Cấu hình H2 persistent db, port 8080
│   └── pom.xml                  # Maven dependencies
├── frontend/
│   ├── src/
│   │   ├── api/                 # axiosClient.js (Axios instance baseURL /api)
│   │   ├── components/
│   │   │   ├── common/          # Badge.jsx (Pill trạng thái 6px dot), KpiCard.jsx (Viền trái 3px)
│   │   │   ├── layout/          # MainLayout.jsx, Header.jsx (Topbar 56px), Sidebar.jsx (Navbar 232px)
│   │   │   └── tickets/         # CreateTicketModal.jsx, TicketDetailDrawer.jsx, CommentSection.jsx, TicketWorkflowActions.jsx
│   │   ├── context/             # AuthContext.jsx (Xác thực & phân quyền), ThemeContext.jsx (Light/Dark mode)
│   │   ├── pages/               # Login.jsx, TicketList.jsx, TicketDetail.jsx, DashboardPage.jsx, UserManagement.jsx, ServiceCategories.jsx, SlaPoliciesPage.jsx, ReportsPage.jsx
│   │   ├── styles/              # tokens.css (Enterprise 2D CSS tokens)
│   │   ├── App.jsx              # React Router registration & Protected routes
│   │   └── main.jsx             # Entry point
│   ├── package.json
│   └── vite.config.js
└── run-project.bat              # Script 1-click khởi động song song Backend và Frontend
```

---

## 7. DỮ LIỆU KIỂM THỬ THỰC TẾ & KẾT QUẢ ĐO LƯỜNG

- **Môi trường thử nghiệm**: Máy trạm phát triển local (Intel Core i7, RAM 16GB, Windows 11, Google Chrome v120).
- **Bộ kiểm thử chức năng**: 12/12 ca kiểm thử cốt lõi (TC01 -> TC12) đạt kết quả 100%.
- **Thời gian phản hồi API (Latency)**: Đo đạc thực tế qua Chrome Network Tab dao động từ **15ms đến 45ms** trên môi trường local.
- **Khả năng tự phục hồi**: Tắt máy chủ và khởi động lại, cơ sở dữ liệu H2 lưu file vật lý bền vững `./data/helpdesk_db` giữ nguyên 100% dữ liệu ticket, người dùng và lịch sử bình luận.
- **Hạn chế kỹ thuật cần ghi nhận**: Chưa thử nghiệm tải đồng thời hàng nghìn kết nối qua mạng Internet công cộng; chưa tích hợp mã hóa JWT có thời hạn hết hạn ngắn (hiện dùng phiên đăng nhập Context).
