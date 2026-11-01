# IT Helpdesk Ticketing System

> Hệ thống Quản lý Yêu cầu Hỗ trợ Kỹ thuật Nội bộ (Báo cáo Thực tập Doanh nghiệp - CNTT HUMG)

Hệ thống hỗ trợ tiếp nhận sự cố kỹ thuật CNTT, phân loại danh mục dịch vụ, tự động tính toán thời hạn cam kết chất lượng dịch vụ (SLA), phân quyền xử lý theo 3 vai trò và giám sát hiệu năng vận hành qua Dashboard & Báo cáo.

---

## 🛠 Công nghệ sử dụng

- **Backend**:
  - Java 17 LTS, Spring Boot 3.3.5
  - Spring Data JPA, Hibernate
  - PostgreSQL 18 (Database: `helpdesk_db`, Port 5432)
  - Jakarta Bean Validation, Lombok
  - Spring Task Scheduling (`@Scheduled`)
- **Frontend**:
  - React 18, Vite 5
  - Tailwind CSS, Enterprise 2D Design Tokens (`tokens.css`)
  - React Router DOM v7
  - Axios Client
  - Recharts (Biểu đồ phân tích SLA, MTTA, MTTR)
  - Lucide React (Icons)

---

## 🚀 Tính năng nổi bật

1. **Phân quyền 3 vai trò (RBAC)**:
   - **Employee (Nhân viên)**: Tạo yêu cầu hỗ trợ, theo dõi tiến độ, trao đổi bình luận, xác nhận đóng ticket.
   - **Agent (Kỹ thuật viên IT)**: Tiếp nhận ticket toàn công ty, cập nhật trạng thái xử lý, trao đổi kỹ thuật.
   - **Admin (Quản trị viên)**: Độc quyền quản trị người dùng & phòng ban, quản lý danh mục dịch vụ, thiết lập chính sách SLA, xem báo cáo phân tích.
2. **Quy trình SLA tự động**:
   - Tự động gán thời hạn giải quyết (`dueDate = createdAt + resolutionTimeHours`) theo mức ưu tiên:
     - `CRITICAL`: 2 giờ
     - `HIGH`: 8 giờ
     - `MEDIUM`: 24 giờ
     - `LOW`: 48 giờ
   - Tiến trình ngầm định kỳ quét và đánh dấu cờ quá hạn (`isOverdue`).
3. **Trải nghiệm người dùng 2D Enterprise**:
   - Ngăn trượt chi tiết `TicketDetailDrawer` từ cạnh phải màn hình.
   - Hàng đợi đa góc nhìn (*Tất cả ticket*, *Của tôi*, *Chưa phân công*).
   - Bộ chuyển nhanh tài khoản demo 1-click tại trang đăng nhập.
   - Hỗ trợ chế độ Giao diện Sáng / Tối (Light / Dark mode).

---

## 📦 Hướng dẫn cài đặt & khởi chạy

### Yêu cầu môi trường
- JDK 17+
- Node.js 18+ & npm
- Maven 3.8+ (hoặc dùng Maven wrapper)

### Khởi chạy nhanh (1-Click trên Windows)
Chạy trực tiếp file script:
```cmd
run-project.bat
```

### Khởi chạy thủ công

**1. Khởi chạy Backend:**
```bash
cd backend
./mvnw spring-boot:run
# Backend lắng nghe tại: http://localhost:8080
# Kết nối PostgreSQL tại: localhost:5432/helpdesk_db (User: postgres, Password: 1)
```

**2. Khởi chạy Frontend:**
```bash
cd frontend
npm install
npm run dev
# Frontend truy cập tại: http://localhost:5173
```

---

## 👤 Tài khoản thử nghiệm (Demo Accounts)

| Vai trò | Tên đăng nhập | Mật khẩu | Phạm vi quyền |
|---|---|---|---|
| **Quản trị viên (Admin)** | `admin` | `admin` | Toàn quyền hệ thống, quản trị User & SLA |
| **Kỹ thuật viên (Agent)** | `agent` | `agent` | Xử lý hàng đợi ticket, xem Dashboard |
| **Nhân viên (Employee)** | `emp` | `emp` | Tạo ticket cá nhân, bình luận, đóng ticket |

---

## 📄 Cấu trúc thư mục

```
ProjectTTDN/
├── backend/                   # Spring Boot 3 REST API
│   ├── src/main/java/com/helpdesk/
│   │   ├── config/            # Cấu hình CORS WebConfig
│   │   ├── controller/        # REST Controllers (Auth, Ticket, User, Category, SLA, Dashboard)
│   │   ├── entity/            # JPA Entities & Enums
│   │   ├── repository/        # Spring Data JPA Repositories
│   │   ├── scheduler/         # SLA Overdue Scheduler
│   │   └── service/           # Business Logic Layer
│   └── pom.xml
├── frontend/                  # React Vite SPA
│   ├── src/
│   │   ├── api/               # Axios client instance
│   │   ├── components/        # Layout, Drawer, Modal, Common UI
│   │   ├── context/           # AuthContext, ThemeContext
│   │   ├── pages/             # Dashboard, Tickets, Users, SLA, Reports
│   │   └── styles/            # Enterprise 2D Tokens CSS
│   └── package.json
├── PROJECT_BUILD_SUMMARY.md   # Tài liệu tổng hợp kiến trúc hệ thống
├── run-project.bat            # Script khởi chạy đồng thời Backend + Frontend
└── README.md
```
