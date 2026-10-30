# KẾ HOẠCH DỰ ÁN: HỆ THỐNG QUẢN LÝ YÊU CẦU HỖ TRỢ NỘI BỘ (IT HELPDESK & TICKETING SYSTEM)
> Đề tài Báo cáo Thực tập Doanh nghiệp ngành CNTT  
> Kiến trúc: Tách biệt Backend (Java Spring Boot 3 REST API) & Frontend (ReactJS SPA)  
> Phương pháp tiếp cận: Inside-Out (Database -> Repository -> Service -> Controller -> API -> React Page)

---

## 1. TỔNG QUAN KIẾN TRÚC & QUY TẮC PHÁT TRIỂN

### 1.1. Cấu trúc thư mục Monorepo
Dự án được quản lý trong một thư mục gốc duy nhất với 2 phần tách biệt:
- `/backend`: Mã nguồn Java Spring Boot (chạy tại port 8080).
- `/frontend`: Mã nguồn ReactJS + Vite + Tailwind CSS (chạy tại port 5173).

### 1.2. Tech Stack chuẩn
- **Backend:** Java 17/21, Spring Boot 3.x, Spring Data JPA, Lombok, H2 Database (lưu file local `./data/helpdesk_db` để duy trì dữ liệu khi khởi động lại), Java Scheduling (`@Scheduled`).
- **Frontend:** ReactJS (Vite), Tailwind CSS (tối giản, sắc nét), Axios, React Router DOM v6, Lucide React (Icons), Recharts (Biểu đồ).
- **Ngôn ngữ & Chuẩn giao tiếp:** RESTful API qua HTTP/JSON; Xử lý triệt để bài toán CORS giữa `localhost:5173` và `localhost:8080`.

### 1.3. Quy tắc "Bất di bất dịch" cho AI Agent (Antigravity Rules)
1. **Tuân thủ thứ tự Inside-Out:** Tuyệt đối không sinh file Controller hay React Component khi chưa hoàn thiện Entity/Repository/Service.
2. **Thực hiện từng giai đoạn (Milestone-based):** Hoàn thành đúng phạm vi của giai đoạn hiện tại. Dừng lại để kiểm thử (Review) trước khi chuyển sang giai đoạn kế tiếp.
3. **Phòng chống vòng lặp JSON:** Khi thiết lập quan hệ `@ManyToOne` và `@OneToMany`, sử dụng `@JsonIgnore` hoặc DTO để ngăn lỗi `JsonInfiniteRecursionException`.
4. **Phong cách giao diện:** Minimalist & Modern SaaS (nền `bg-slate-50`, card trắng `bg-white`, border `border-slate-200`, bo góc `rounded-xl`, chữ sắc nét, khoảng trắng thoáng).

---

## 2. LỘ TRÌNH 6 GIAI ĐOẠN TRIỂN KHAI CHI TIẾT
---

### GIAI ĐOẠN 1: Khởi tạo Backend & Cơ sở dữ liệu (Entities & Repositories)

#### 1. Mục tiêu kỹ thuật
- Dựng khung dự án `/backend` bằng Maven.
- Thiết lập kết nối H2 Database lưu file.
- Cấu hình mở CORS toàn cục cho `http://localhost:5173`.
- Khởi tạo 5 Entity nòng cốt và các JpaRepository tương ứng.
- Viết `DataInitializer` sinh dữ liệu mẫu sẵn có.

#### 2. Các file cần tạo theo thứ tự chuẩn
1. `backend/pom.xml`: Khai báo các dependency: `spring-boot-starter-web`, `spring-boot-starter-data-jpa`, `h2`, `lombok`.
2. `backend/src/main/resources/application.properties`: Cấu hình H2 file: `jdbc:h2:file:./data/helpdesk_db`, `ddl-auto=update`, mở H2 Console tại `/h2-console`.
3. `backend/src/main/java/.../config/WebConfig.java`: Cấu hình `CorsRegistry` cho phép `http://localhost:5173` gọi toàn bộ method (`GET, POST, PUT, PATCH, DELETE, OPTIONS`).
4. `backend/src/main/java/.../entity/`:
   - `User.java`: `id`, `username`, `password`, `fullName`, `email`, `department`, `role` (Enum: `EMPLOYEE`, `AGENT`, `ADMIN`).
   - `Category.java`: `id`, `name`, `description`.
   - `SlaPolicy.java`: `id`, `priorityLevel` (Enum: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), `resolutionTimeHours` (int).
   - `Ticket.java`: `id`, `ticketCode`, `title`, `description` (TEXT), `status` (Enum: `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`), `priority` (Enum: `LOW, MEDIUM, HIGH, CRITICAL`), `requester` (`@ManyToOne User`), `assignee` (`@ManyToOne User`), `category` (`@ManyToOne Category`), `createdAt`, `dueDate`, `isOverdue` (boolean).
   - `TicketComment.java`: `id`, `ticket` (`@ManyToOne Ticket` với `@JsonIgnore`), `user` (`@ManyToOne User`), `content`, `createdAt`.
5. `backend/src/main/java/.../repository/`:
   - `UserRepository`, `CategoryRepository`, `SlaPolicyRepository`, `TicketRepository`, `TicketCommentRepository` (kế thừa `JpaRepository`).
6. `backend/src/main/java/.../config/DataInitializer.java`:
   - Chèn sẵn 3 User (1 Employee, 1 Agent, 1 Admin).
   - Chèn 4 Category (Phần cứng, Phần mềm, Mạng, Quyền truy cập).
   - Chèn 4 mức SLA Policy (LOW: 24h, MEDIUM: 8h, HIGH: 4h, CRITICAL: 2h).
   - Chèn 5 Ticket mẫu đủ các trạng thái và độ ưu tiên.

#### 3. Tiêu chí nghiệm thu (Checklist)
- [ ] Chạy Backend thành công ở port `8080`.
- [ ] Truy cập `http://localhost:8080/h2-console` thấy đầy đủ các bảng dữ liệu đã có sẵn dữ liệu mẫu.

#### 4. Kiến thức vấn đáp cốt lõi
- **Hỏi:** *Tại sao dùng `@Entity` và `@ManyToOne`?*  
  **Trả lời:** `@Entity` để Hibernate ánh xạ class Java thành bảng trong cơ sở dữ liệu. `@ManyToOne` thể hiện quan hệ Nhiều - Một giữa các bảng (ví dụ: nhiều Ticket được tạo bởi một User).
- **Hỏi:** *CORS là gì và tại sao phải cấu hình?*  
  **Trả lời:** Là cơ chế bảo mật của trình duyệt chặn các request từ domain/port khác. Cần cấu hình CORS tại Spring Boot để cho phép Frontend ở port `5173` gọi API sang port `8080`.

---

### GIAI ĐOẠN 2: Xây dựng Service, Logic SLA & RESTful API Endpoints

#### 1. Mục tiêu kỹ thuật
- Tách biệt logic nghiệp vụ tại tầng Service.
- Tự động hóa sinh mã ticket (`TK-xxxx`) và tính toán `dueDate` dựa trên SLA Policy.
- Cung cấp toàn bộ các REST Controller trả dữ liệu chuẩn JSON.

#### 2. Các file cần tạo theo thứ tự chuẩn
1. `backend/src/main/java/.../dto/`:
   - `LoginRequest.java`, `TicketCreateRequest.java`, `CommentCreateRequest.java`, `StatusUpdateRequest.java`.
2. `backend/src/main/java/.../service/`:
   - `TicketService.java`:
     - `getAllTickets(status, priority, search, requesterId)`: Lọc động; tự động kiểm tra nếu `now > dueDate` và status chưa xong thì set `isOverdue = true`.
     - `getTicketById(Long id)`.
     - `createTicket(TicketCreateRequest req)`: Tìm SLA Policy theo `priority` $\rightarrow$ gán `dueDate = createdAt + resolutionTimeHours` $\rightarrow$ sinh mã `ticketCode` $\rightarrow$ lưu trạng thái `OPEN`.
     - `updateStatus(Long id, StatusUpdateRequest req)`: Đổi trạng thái, gán `assigneeId` khi Agent nhận việc.
   - `CommentService.java`: Thêm và lấy bình luận theo Ticket ID.
   - `DashboardService.java`: Tính toán các chỉ số: tổng số ticket, số lượng theo trạng thái, số lượng quá hạn, và nhóm theo category.
3. `backend/src/main/java/.../controller/`:
   - `AuthController.java`: `POST /api/auth/login` (Xác thực đơn giản/Demo Switch).
   - `CategoryController.java`: `GET /api/categories`.
   - `TicketController.java`:
     - `GET /api/tickets`
     - `GET /api/tickets/{id}`
     - `POST /api/tickets`
     - `PATCH /api/tickets/{id}/status`
     - `GET /api/tickets/{id}/comments`
     - `POST /api/tickets/{id}/comments`
   - `DashboardController.java`: `GET /api/dashboard/stats`.

#### 3. Tiêu chí nghiệm thu (Checklist)
- [x] Gửi GET tới `http://localhost:8080/api/tickets` nhận về chuỗi JSON chứa danh sách ticket.
- [x] Gửi GET tới `http://localhost:8080/api/dashboard/stats` nhận về đầy đủ các chỉ số thống kê.

#### 4. Kiến thức vấn đáp cốt lõi
- **Hỏi:** *Tại sao tách riêng `Service` mà không viết thẳng vào `Controller`?*  
  **Trả lời:** Để tuân thủ nguyên lý Single Responsibility. Controller chỉ điều hướng request/response HTTP; Service đảm nhận toàn bộ quy tắc nghiệp vụ (tính SLA, sinh mã, kiểm tra quá hạn), giúp code dễ kiểm thử và tái sử dụng.
- **Hỏi:** *Khác biệt giữa `@PostMapping` và `@PatchMapping`?*  
  **Trả lời:** `@PostMapping` dùng để tạo mới hoàn toàn một bản ghi (tạo ticket), còn `@PatchMapping` dùng để cập nhật một phần dữ liệu (chỉ sửa trạng thái hoặc người xử lý của ticket).

---

### GIAI ĐOẠN 3: Khởi tạo Frontend ReactJS & Cơ chế Đăng nhập Demo

#### 1. Mục tiêu kỹ thuật
- Khởi tạo ứng dụng ReactJS bằng Vite trong `/frontend`.
- Cài đặt Tailwind CSS, Axios, React Router DOM, Lucide React.
- Xây dựng Layout chuẩn Minimalist: Sidebar, Header, Theme Slate/White.
- Tạo `AuthContext` và trang Login hỗ trợ 3 nút chuyển nhanh tài khoản Demo.

#### 2. Các file cần tạo theo thứ tự chuẩn
1. Khởi tạo project: `npm create vite@latest frontend -- --template react`.
2. Cài đặt dependencies: `axios`, `react-router-dom`, `lucide-react`, `tailwindcss`, `postcss`, `autoprefixer`.
3. `frontend/src/api/axiosClient.js`: Cấu hình Axios với `baseURL: 'http://localhost:8080/api'`.
4. `frontend/src/context/AuthContext.jsx`: Quản lý `currentUser`, lưu `localStorage`, cung cấp hàm `login(user)` và `logout()`.
5. `frontend/src/components/layout/`:
   - `Sidebar.jsx`: Menu điều hướng tối giản (Dashboard, Tickets, My Requests) hiển thị theo Role.
   - `Header.jsx`: Hiển thị thông tin người dùng, Badge Role, nút Đăng xuất.
   - `MainLayout.jsx`: Ghép Sidebar, Header và `<Outlet />`.
6. `frontend/src/pages/Login.jsx`: Màn hình đăng nhập tối giản có 3 card bấm nhanh tài khoản Demo:
   - "Đăng nhập với vai trò Nhân viên (Employee)"
   - "Đăng nhập với vai trò Kỹ thuật viên (IT Agent)"
   - "Đăng nhập với vai trò Quản lý (Admin)"
7. `frontend/src/App.jsx`: Cấu hình React Router (Public route: `/login`, Protected layout routes: `/`, `/tickets`, `/dashboard`).

#### 3. Tiêu chí nghiệm thu (Checklist)
- [x] Chạy Frontend tại `http://localhost:5173`.
- [x] Bấm vào từng nút Demo trên trang Login, hệ thống lưu User vào state/storage và chuyển vào MainLayout không cần reload trang.

#### 4. Kiến thức vấn đáp cốt lõi
- **Hỏi:** *SPA (Single Page Application) là gì và hoạt động ra sao?*  
  **Trả lời:** Là ứng dụng web tải một trang HTML duy nhất ban đầu. Khi người dùng chuyển trang, React Router sẽ chặn hành vi tải lại của trình duyệt và chỉ render lại component tương ứng, tạo trải nghiệm chuyển trang tức thì.
- **Hỏi:** *Vai trò của `AuthContext` trong React?*  
  **Trả lời:** Dùng React Context API để chia sẻ trạng thái người dùng đăng nhập cho toàn bộ component trong cây DOM mà không cần truyền props qua nhiều tầng trung gian (tránh Prop Drilling).

---

### GIAI ĐOẠN 4: Giao diện Danh sách Ticket & Modal Tạo Ticket (User Flow)

#### 1. Mục tiêu kỹ thuật
- Xây dựng trang `/tickets` hiển thị bảng danh sách ticket chuẩn thiết kế tối giản.
- Thanh công cụ lọc: Tìm kiếm theo từ khóa, lọc theo Status, lọc theo Priority.
- Modal tạo mới Ticket: Tự động lấy danh mục từ Backend, người dùng chọn mức ưu tiên và nhập mô tả.
- Hiển thị trực quan nhãn quá hạn SLA (`isOverdue`).

#### 2. Các file cần tạo theo thứ tự chuẩn
1. `frontend/src/components/common/Badge.jsx`: Component hiển thị nhãn màu pastel cho Status và Priority.
2. `frontend/src/components/tickets/CreateTicketModal.jsx`:
   - Dùng `useEffect` gọi `GET /api/categories` lấy danh sách danh mục sự cố.
   - Form chọn: Danh mục, Mức ưu tiên (ghi chú rõ cam kết giờ SLA), Tiêu đề, Mô tả.
   - Xử lý submit gọi `POST /api/tickets`, hiển thị thông báo thành công và đóng modal.
3. `frontend/src/pages/TicketList.jsx`:
   - Khai báo state: `tickets`, `loading`, `filterStatus`, `filterPriority`, `searchTerm`, `isModalOpen`.
   - `useEffect` gọi `GET /api/tickets` kèm query params tương ứng.
   - Bảng hiển thị: Mã (`ticketCode`), Tiêu đề, Người tạo, Ngày tạo, Hạn xử lý (`dueDate`), Độ ưu tiên, Trạng thái.
   - Nếu `isOverdue === true` và trạng thái chưa xong: Hiển thị badge màu đỏ "Quá hạn SLA".

#### 3. Tiêu chí nghiệm thu (Checklist)
- [x] Đăng nhập tài khoản Nhân viên, bấm tạo ticket mới $\rightarrow$ Ticket mới xuất hiện trên bảng ngay lập tức với đầy đủ `dueDate`.
- [x] Nhập từ khóa vào ô tìm kiếm hoặc bấm lọc trạng thái $\rightarrow$ Bảng tự động cập nhật dữ liệu tương ứng.

#### 4. Kiến thức vấn đáp cốt lõi
- **Hỏi:** *`useState` và `useEffect` hoạt động như thế nào trong trang này?*  
  **Trả lời:** `useState` lưu trữ dữ liệu danh sách ticket và trạng thái bộ lọc. `useEffect` lắng nghe sự thay đổi của bộ lọc để kích hoạt gọi Axios lấy dữ liệu mới từ Backend về cập nhật lại state.
- **Hỏi:** *Làm thế nào để hiển thị dữ liệu dạng danh sách trong React?*  
  **Trả lời:** Sử dụng hàm `tickets.map((ticket) => (...))` để duyệt qua từng phần tử mảng và render ra thẻ JSX tương ứng, mỗi phần tử được gắn một `key={ticket.id}` duy nhất để React tối ưu thuật toán đối soát Virtual DOM.

---

### GIAI ĐOẠN 5: Trang Chi tiết Ticket, Luồng Xử lý IT & Trao đổi (Agent Flow)

#### 1. Mục tiêu kỹ thuật
- Xây dựng trang `/tickets/:id` với layout 2 cột hiện đại.
- Cột trái: Nội dung chi tiết sự cố và khung bình luận (Comments Timeline).
- Cột phải: Thông tin SLA, Người tạo, Kỹ thuật viên phụ trách và cụm nút thao tác (Workflow Actions).
- Phân quyền giao diện theo Role: Chỉ IT Agent/Admin mới thấy nút "Tiếp nhận" và "Đã giải quyết".

#### 2. Các file cần tạo theo thứ tự chuẩn
1. `frontend/src/components/tickets/CommentSection.jsx`:
   - Hiển thị danh sách bình luận (phân biệt màu nền giữa phản hồi của IT và Nhân viên).
   - Form nhập bình luận và nút gửi gọi `POST /api/tickets/{id}/comments`.
2. `frontend/src/components/tickets/TicketWorkflowActions.jsx`:
   - Nút "Tiếp nhận xử lý" (chỉ hiện khi status là `OPEN` và role là `AGENT`/`ADMIN`): gọi PATCH cập nhật `assignee` và đổi sang `IN_PROGRESS`.
   - Nút "Đã giải quyết" (chỉ hiện khi status là `IN_PROGRESS`): đổi sang `RESOLVED`.
   - Nút "Đóng phiếu" (hiện khi status là `RESOLVED` cho cả Nhân viên và IT).
3. `frontend/src/pages/TicketDetail.jsx`:
   - Lấy `id` từ URL qua `useParams()`.
   - Gọi song song `GET /api/tickets/{id}` và `GET /api/tickets/{id}/comments`.
   - Dựng layout 2 cột (Cột chính 2/3, Cột thuộc tính 1/3).

#### 3. Tiêu chí nghiệm thu (Checklist)
- [x] Bấm vào 1 dòng trong bảng danh sách $\rightarrow$ Chuyển sang `/tickets/:id` hiển thị đúng chi tiết ticket đó.
- [x] Dùng tài khoản IT Agent bấm "Tiếp nhận xử lý" $\rightarrow$ Trạng thái chuyển thành `IN_PROGRESS` và tên người phụ trách hiển thị tên IT hiện tại.
- [x] Gửi bình luận trao đổi $\rightarrow$ Bình luận mới xuất hiện ngay lập tức trong dòng thời gian.

#### 4. Kiến thức vấn đáp cốt lõi
- **Hỏi:** *Làm thế nào lấy được ID của Ticket từ đường dẫn trình duyệt?*  
  **Trả lời:** Sử dụng hook `useParams()` của `react-router-dom` để trích xuất tham số động `:id` được định nghĩa trong cấu hình router `/tickets/:id`.
- **Hỏi:** *Conditional Rendering trong React là gì?*  
  **Trả lời:** Là kỹ thuật render có điều kiện (sử dụng toán tử 3 ngôi `condition ? <A /> : <B />` hoặc `condition && <A />`) để ẩn/hiện các nút thao tác nghiệp vụ dựa theo trạng thái ticket và quyền hạn của người dùng đăng nhập.

---

### GIAI ĐOẠN 6: Dashboard Thống kê Biểu đồ & Tác vụ Quét SLA Chạy ngầm

#### 1. Mục tiêu kỹ thuật
- Trang `/dashboard` bố cục Bento Grid hiển thị 4 KPI Cards và 2 biểu đồ trực quan dùng thư viện `recharts`.
- Backend bật `@EnableScheduling`, chạy tác vụ ngầm mỗi 60 giây kiểm tra các ticket vi phạm thời hạn SLA.

#### 2. Các file cần tạo theo thứ tự chuẩn
1. `backend/src/main/java/.../scheduler/SlaScheduler.java`:
   - Đánh dấu `@Component` và `@Scheduled(fixedRate = 60000)`.
   - Quét các ticket có status `OPEN` hoặc `IN_PROGRESS`.
   - Nếu `LocalDateTime.now().isAfter(ticket.getDueDate())` và `!ticket.isOverdue()`, cập nhật `ticket.setOverdue(true)` và lưu xuống Database, in log cảnh báo ra console.
2. `backend/src/main/java/.../BackendApplication.java`: Thêm annotation `@EnableScheduling`.
3. `frontend/src/pages/Dashboard.jsx`:
   - Cài đặt `npm install recharts`.
   - Gọi API `GET /api/dashboard/stats`.
   - Hàng trên: 4 Metric Cards (Tổng số yêu cầu, Đang xử lý, Đã hoàn thành, Quá hạn SLA).
   - Hàng dưới:
     - `BarChart`: Thống kê số lượng ticket theo từng Trạng thái.
     - `PieChart`: Tỷ lệ phần trăm sự cố phân bổ theo từng Danh mục (Phần cứng, Mạng, Phần mềm...).

#### 3. Tiêu chí nghiệm thu (Checklist)
- [x] Màn hình Dashboard hiển thị biểu đồ sắc nét, số liệu khớp chính xác với dữ liệu trong database.
- [x] Cửa sổ console của Spring Boot in log quét SLA mỗi 1 phút một lần.

#### 4. Kiến thức vấn đáp cốt lõi
- **Hỏi:** *Cơ chế hoạt động của `@Scheduled` trong Spring Boot?*  
  **Trả lời:** Khi bật `@EnableScheduling`, Spring Boot tạo ra một TaskScheduler ngầm quản lý luồng thực thi (Background Thread). Hàm được đánh dấu `@Scheduled` sẽ tự động kích hoạt theo chu kỳ thời gian định sẵn mà không cần người dùng gửi request từ trình duyệt.
- **Hỏi:** *Tại sao dùng biểu đồ Dashboard trong hệ thống nội bộ doanh nghiệp?*  
  **Trả lời:** Dashboard chuyển đổi dữ liệu thô thành thông tin trực quan hỗ trợ ra quyết định: giúp nhà quản lý nhận diện nhanh điểm nghẽn quy trình, đánh giá hiệu suất hỗ trợ kỹ thuật và xác định nhóm lỗi xuất hiện nhiều nhất để có giải pháp hạ tầng căn cơ.

---

## 3. CHECKLIST TỔNG HỢP TRƯỚC KHI BẢO VỆ THỰC TẬP

- [x] Backend chạy mượt mà tại `localhost:8080`, không có lỗi Compile hoặc Warning nghiêm trọng.
- [x] Frontend chạy mượt mà tại `localhost:5173`, không có lỗi console đỏ (F12).
- [x] Kiểm tra toàn bộ luồng nghiệp vụ khép kín:
  1. Employee đăng nhập $\rightarrow$ Tạo ticket mới (SLA tự động tính).
  2. Agent đăng nhập $\rightarrow$ Xem danh sách $\rightarrow$ Nhận xử lý $\rightarrow$ Gửi bình luận phản hồi $\rightarrow$ Đánh dấu giải quyết.
  3. Employee xác nhận hoàn tất $\rightarrow$ Đóng phiếu.
  4. Admin vào Dashboard $\rightarrow$ Xem biểu đồ biến động theo dữ liệu vừa tạo.
- [x] Đọc kỹ các câu hỏi - câu trả lời vấn đáp ở cuối mỗi giai đoạn để tự tin phản xạ trước hội đồng chấm thi.