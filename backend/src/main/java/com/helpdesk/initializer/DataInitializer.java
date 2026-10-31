package com.helpdesk.initializer;

import com.helpdesk.entity.*;
import com.helpdesk.entity.enums.Priority;
import com.helpdesk.entity.enums.Role;
import com.helpdesk.entity.enums.TicketStatus;
import com.helpdesk.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final CategoryRepository categoryRepository;
    private final SlaPolicyRepository slaPolicyRepository;
    private final TicketRepository ticketRepository;
    private final TicketCommentRepository commentRepository;

    @Override
    @Transactional
    public void run(String... args) {
        if (userRepository.count() > 0) {
            log.info("Du lieu mau da ton tai trong co so du lieu H2 local, bo qua buoc khoi tao.");
            return;
        }

        log.info("Bat dau khoi tao du lieu mau cho he thong IT Helpdesk...");

        // 1. Khoi tao 3 User dai dien 3 Role
        User employee = User.builder()
                .username("emp_nam")
                .password("123456")
                .fullName("Nguyễn Văn Nam")
                .email("nam.nv@company.com")
                .department("Kế toán")
                .role(Role.EMPLOYEE)
                .build();

        User agent = User.builder()
                .username("agent_hoa")
                .password("123456")
                .fullName("Trần Thị Hoa")
                .email("hoa.tt@company.com")
                .department("IT Support")
                .role(Role.AGENT)
                .build();

        User admin = User.builder()
                .username("admin_quang")
                .password("123456")
                .fullName("Lê Nhật Quang")
                .email("admin@company.com")
                .department("IT Management")
                .role(Role.ADMIN)
                .build();

        userRepository.saveAll(List.of(employee, agent, admin));
        log.info("Da khoi tao 3 User thanh cong.");

        // 2. Khoi tao 4 Category
        Category catSoftware = Category.builder()
                .name("Phần mềm & Bản quyền")
                .description("Sự cố cài đặt hệ điều hành, bản quyền Office, phần mềm kế toán, ERP")
                .build();

        Category catHardware = Category.builder()
                .name("Phần cứng & Thiết bị")
                .description("Hỏng màn hình, kẹt giấy máy in, chuột, bàn phím, hỏng linh kiện máy tính")
                .build();

        Category catNetwork = Category.builder()
                .name("Hạ tầng mạng & Tài khoản")
                .description("Mất kết nối LAN/Wifi, cấu hình VPN, cấp quyền tài khoản nội bộ, reset mật khẩu")
                .build();

        Category catCloud = Category.builder()
                .name("Email & Lưu trữ Cloud")
                .description("Lỗi Outlook, hòm thư đầy dung lượng, phân quyền thư mục OneDrive, Google Drive")
                .build();

        categoryRepository.saveAll(List.of(catSoftware, catHardware, catNetwork, catCloud));
        log.info("Da khoi tao 4 Category thanh cong.");

        // 3. Khoi tao 4 muc SlaPolicy
        SlaPolicy slaCritical = SlaPolicy.builder()
                .priorityLevel(Priority.CRITICAL)
                .resolutionTimeHours(2)
                .build();

        SlaPolicy slaHigh = SlaPolicy.builder()
                .priorityLevel(Priority.HIGH)
                .resolutionTimeHours(8)
                .build();

        SlaPolicy slaMedium = SlaPolicy.builder()
                .priorityLevel(Priority.MEDIUM)
                .resolutionTimeHours(24)
                .build();

        SlaPolicy slaLow = SlaPolicy.builder()
                .priorityLevel(Priority.LOW)
                .resolutionTimeHours(48)
                .build();

        slaPolicyRepository.saveAll(List.of(slaCritical, slaHigh, slaMedium, slaLow));
        log.info("Da khoi tao 4 SLA Policy thanh cong.");

        // 4. Khoi tao 5 Ticket mau da dang trang thai
        LocalDateTime now = LocalDateTime.now();

        // Ticket 1: OPEN - CRITICAL - Qua han (isOverdue = true, chua tiep nhan)
        Ticket ticket1 = Ticket.builder()
                .ticketCode("HD-2026-0001")
                .title("Sập kết nối mạng Internet và LAN tầng 3 văn phòng kế toán")
                .description("Toàn bộ máy tính phòng kế toán mất kết nối mạng nội bộ lúc 9h sáng, không xuất được hóa đơn điện tử cho khách hàng.")
                .status(TicketStatus.OPEN)
                .priority(Priority.CRITICAL)
                .category(catNetwork)
                .requester(employee)
                .assignee(null)
                .createdAt(now.minusHours(4))
                .dueDate(now.minusHours(2)) // Qua han 2 gio
                .acknowledgedAt(null)
                .resolvedAt(null)
                .closedAt(null)
                .isOverdue(true)
                .build();

        // Ticket 2: IN_PROGRESS - HIGH - Chua qua han (tiep nhan sau 24 phut)
        Ticket ticket2 = Ticket.builder()
                .ticketCode("HD-2026-0002")
                .title("Máy in HP LaserJet phòng kế toán kẹt giấy liên tục và báo lỗi Drum")
                .description("Khi in chứng từ cuối tháng, máy in phát ra tiếng kêu cọc cạch và kẹt giấy ngay khay cuốn giấy, cần thay hộp mực hoặc cụm sấy.")
                .status(TicketStatus.IN_PROGRESS)
                .priority(Priority.HIGH)
                .category(catHardware)
                .requester(employee)
                .assignee(agent)
                .createdAt(now.minusHours(3))
                .dueDate(now.plusHours(5))
                .acknowledgedAt(now.minusHours(3).plusMinutes(24))
                .resolvedAt(null)
                .closedAt(null)
                .isOverdue(false)
                .build();

        // Ticket 3: IN_PROGRESS - MEDIUM - Chua qua han (tiep nhan sau 18 phut)
        Ticket ticket3 = Ticket.builder()
                .ticketCode("HD-2026-0003")
                .title("Cài đặt và cấu hình phần mềm MISA SME 2026 cho nhân sự mới")
                .description("Nhân viên mới phòng kế toán cần cài đặt phần mềm và phân quyền truy cập máy chủ dữ liệu nội bộ.")
                .status(TicketStatus.IN_PROGRESS)
                .priority(Priority.MEDIUM)
                .category(catSoftware)
                .requester(employee)
                .assignee(agent)
                .createdAt(now.minusHours(8))
                .dueDate(now.plusHours(16))
                .acknowledgedAt(now.minusHours(8).plusMinutes(18))
                .resolvedAt(null)
                .closedAt(null)
                .isOverdue(false)
                .build();

        // Ticket 4: RESOLVED - LOW (tiep nhan sau 32 phut, giai quyet sau 3.75h)
        Ticket ticket4 = Ticket.builder()
                .ticketCode("HD-2026-0004")
                .title("Tài khoản email Outlook báo dung lượng hòm thư vượt mức 95%")
                .description("Hòm thư nhận cảnh báo sắp đầy, không nhận được thư mới có đính kèm file dung lượng lớn.")
                .status(TicketStatus.RESOLVED)
                .priority(Priority.LOW)
                .category(catCloud)
                .requester(employee)
                .assignee(agent)
                .createdAt(now.minusDays(2))
                .dueDate(now.minusHours(10))
                .acknowledgedAt(now.minusDays(2).plusMinutes(32))
                .resolvedAt(now.minusDays(2).plusHours(3).plusMinutes(45))
                .closedAt(null)
                .isOverdue(false)
                .build();

        // Ticket 5: CLOSED - HIGH (tiep nhan sau 26 phut, giai quyet sau 2h 15m, dong sau 2.5h)
        Ticket ticket5 = Ticket.builder()
                .ticketCode("HD-2026-0005")
                .title("Cấp lại quyền truy cập và mở khóa VPN làm việc từ xa")
                .description("Tài khoản VPN bị khóa do nhập sai mật khẩu quá 5 lần khi truy cập từ nhà.")
                .status(TicketStatus.CLOSED)
                .priority(Priority.HIGH)
                .category(catNetwork)
                .requester(employee)
                .assignee(admin)
                .createdAt(now.minusDays(3))
                .dueDate(now.minusDays(2))
                .acknowledgedAt(now.minusDays(3).plusMinutes(26))
                .resolvedAt(now.minusDays(3).plusHours(2).plusMinutes(15))
                .closedAt(now.minusDays(3).plusHours(2).plusMinutes(30))
                .isOverdue(false)
                .build();

        ticketRepository.saveAll(List.of(ticket1, ticket2, ticket3, ticket4, ticket5));

        // Them Comment mau vao Ticket de kiem tra quan he 1-N va JsonManagedReference / JsonBackReference
        TicketComment comment1 = TicketComment.builder()
                .ticket(ticket2)
                .user(agent)
                .content("IT Support đã tiếp nhận yêu cầu, kỹ thuật viên Hoa đang mang hộp mực mới và bộ vệ sinh sấy lên tầng 3.")
                .createdAt(LocalDateTime.now().minusHours(2))
                .build();

        TicketComment comment2 = TicketComment.builder()
                .ticket(ticket3)
                .user(agent)
                .content("Đã cài xong bộ cài đặt MISA, đang chờ nhân sự cung cấp mã license để kích hoạt bản quyền.")
                .createdAt(LocalDateTime.now().minusHours(4))
                .build();

        TicketComment comment3 = TicketComment.builder()
                .ticket(ticket4)
                .user(agent)
                .content("Đã hoàn tất hỗ trợ: Đã lưu trữ (Archive) email cũ sang file .pst ngoại tuyến và dọn dẹp thư mục rác.")
                .createdAt(LocalDateTime.now().minusDays(1))
                .build();

        TicketComment comment4 = TicketComment.builder()
                .ticket(ticket5)
                .user(admin)
                .content("Đã mở khóa tài khoản Active Directory và gửi mật khẩu tạm thời qua SMS của nhân viên.")
                .createdAt(LocalDateTime.now().minusDays(3).plusHours(2))
                .build();

        commentRepository.saveAll(List.of(comment1, comment2, comment3, comment4));

        log.info("Da khoi tao 5 Ticket mau va cac Comment tuong ung thanh cong.");
    }
}
