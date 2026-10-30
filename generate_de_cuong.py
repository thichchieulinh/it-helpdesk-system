import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_de_cuong():
    print("Generating concise De cuong thuc tap doanh nghiep updated to current product...")
    doc = docx.Document()
    
    # Page setup: Margins
    for section in doc.sections:
        section.top_margin = Inches(0.98) # 2.5 cm
        section.bottom_margin = Inches(0.98) # 2.5 cm
        section.left_margin = Inches(1.18) # 3.0 cm
        section.right_margin = Inches(0.79) # 2.0 cm
        
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(2)

    # 1. Header Quốc hiệu & Trường
    table_hdr = doc.add_table(rows=1, cols=2)
    table_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_hdr.autofit = False
    table_hdr.columns[0].width = Inches(3.2)
    table_hdr.columns[1].width = Inches(3.5)
    
    cell_l = table_hdr.cell(0, 0)
    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_l.add_run("TRƯỜNG ĐẠI HỌC MỎ - ĐỊA CHẤT\n")
    r1.font.size = Pt(11)
    r2 = p_l.add_run("KHOA CÔNG NGHỆ THÔNG TIN")
    r2.bold = True
    r2.font.size = Pt(11)
    
    cell_r = table_hdr.cell(0, 1)
    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r3.bold = True
    r3.font.size = Pt(11)
    r4 = p_r.add_run("Độc lập - Tự do - Hạnh phúc")
    r4.bold = True
    r4.font.size = Pt(11)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(4)

    # 2. Tiêu đề
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("ĐỀ CƯƠNG THỰC TẬP DOANH NGHIỆP")
    r_t.bold = True
    r_t.font.size = Pt(14)
    p_title.paragraph_format.space_after = Pt(10)

    # 3. Mục 1: Sinh viên thực tập
    p1 = doc.add_paragraph()
    p1.add_run("1. Sinh viên thực tập").bold = True
    
    info_sv = [
        ("Mã sinh viên:", "[Điền Mã SV của bạn, ví dụ: 2021050548]"),
        ("Họ và tên:", "[Điền Họ và tên bạn, ví dụ: Nguyễn Văn A]"),
        ("Lớp:", "DCCTPM65..."),
        ("Điện thoại:", "[Số điện thoại của bạn]"),
        ("Email:", "[Mã sinh viên]@student.humg.edu.vn")
    ]
    for lbl, val in info_sv:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_after = Pt(1)
        p.add_run(f"{lbl} {val}")

    # 4. Mục 2: Giảng viên hướng dẫn
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(4)
    p2.add_run("2. Giảng viên hướng dẫn").bold = True
    
    info_gv = [
        ("Mã cán bộ:", "0801-02"),
        ("Họ và tên:", "ThS. Nguyễn Thế Lộc"),
        ("Đơn vị:", "Bộ môn Công nghệ phần mềm"),
        ("Điện thoại:", "0983330682"),
        ("Email:", "nguyentheloc@humg.edu.vn")
    ]
    for lbl, val in info_gv:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_after = Pt(1)
        p.add_run(f"{lbl} {val}")

    # 5. Mục 3: Thông tin công ty thực tập
    p3 = doc.add_paragraph()
    p3.paragraph_format.space_before = Pt(4)
    p3.add_run("3. Thông tin công ty thực tập").bold = True
    
    info_cty = [
        ("Tên công ty:", "Công ty TNHH JITS INOVATION LABS"),
        ("Địa chỉ:", "Tầng 2, số 6, phố Phạm Tuấn Tài, phường Dịch Vọng Hậu, Quận Cầu Giấy, Hà Nội, Việt Nam"),
        ("Số điện thoại:", "0338 355 571"),
        ("Email:", "contact@jitsinnovationlabs.com"),
        ("Họ và tên giám đốc:", "Nguyễn Đức Hoàng"),
        ("Mã số thuế:", "0107486223")
    ]
    for lbl, val in info_cty:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_after = Pt(1)
        p.add_run(f"{lbl} {val}")

    # 6. Mục 4: Người hướng dẫn thực tập tại công ty
    p4 = doc.add_paragraph()
    p4.paragraph_format.space_before = Pt(4)
    p4.add_run("4. Người hướng dẫn thực tập tại công ty").bold = True
    
    info_hd = [
        ("Họ và tên:", "Đào Văn Tâm"),
        ("Chức vụ:", "Quản lí"),
        ("Điện thoại:", "0357708915"),
        ("Email:", "tamdv@jitsinnovationlabs.com")
    ]
    for lbl, val in info_hd:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.space_after = Pt(1)
        p.add_run(f"{lbl} {val}")

    # 7. Mục 5: Tên đề tài hoặc dự án thực tập
    p5 = doc.add_paragraph()
    p5.paragraph_format.space_before = Pt(4)
    p5.add_run("5. Tên đề tài hoặc dự án thực tập").bold = True
    
    p5_txt = doc.add_paragraph()
    p5_txt.paragraph_format.left_indent = Inches(0.3)
    p5_txt.paragraph_format.space_after = Pt(2)
    p5_txt.add_run("Xây dựng Hệ thống Quản lý Yêu cầu Hỗ trợ Nội bộ (IT Helpdesk Ticketing System) theo kiến trúc Spring Boot và ReactJS")

    # 8. Mục 6: Các nhiệm vụ được giao thực hiện
    p6 = doc.add_paragraph()
    p6.paragraph_format.space_before = Pt(4)
    p6.add_run("6. Các nhiệm vụ được giao thực hiện").bold = True

    p6_1 = doc.add_paragraph()
    p6_1.paragraph_format.left_indent = Inches(0.2)
    p6_1.paragraph_format.space_after = Pt(1)
    p6_1.add_run("+ Các tính năng cần xây dựng theo sản phẩm thực tế:").bold = True

    tinh_nang = [
        "Xác thực phân quyền 3 vai trò (Employee, IT Agent, Admin) kèm tính năng chuyển đổi nhanh tài khoản demo",
        "Quản lý danh mục dịch vụ hỗ trợ (Category) & quản lý chính sách cam kết dịch vụ (SLA Policies: Khẩn cấp 2h, Cao 8h, Trung bình 24h, Thấp 48h)",
        "Quản lý tài khoản người dùng & phân quyền (User Management) dành riêng cho Admin, hỗ trợ tìm kiếm, lọc vai trò và cấp tài khoản mới",
        "Tạo phiếu yêu cầu hỗ trợ (Ticket), hệ thống tự động sinh mã phiếu (HD-xxxx) và tự động tính hạn chót xử lý (dueDate) dựa theo chính sách SLA",
        "Danh sách yêu cầu đa góc nhìn: Tất cả ticket, Của tôi, Chưa phân công; tích hợp thanh tìm kiếm và bộ lọc trạng thái kèm số đếm",
        "Ngăn trượt chi tiết Ticket (TicketDetailDrawer) trượt từ cạnh phải màn hình: xem thông tin sự cố, xử lý quy trình chuyển trạng thái (Open -> In Progress -> Resolved -> Closed), gửi thảo luận bình luận (Comments) và kiểm tra hạn SLA mà không cần chuyển trang",
        "Bảng điều khiển (Dashboard) đo lường chỉ số KPI, biểu đồ cột đôi theo dõi tiến độ và thanh đo tỷ lệ tuân thủ SLA tự động đổi màu cảnh báo",
        "Phân hệ Báo cáo phân tích hiệu năng IT (Reports): đo lường tỷ lệ đạt chuẩn SLA, thời gian phản hồi trung bình (MTTA), thời gian khắc phục trung bình (MTTR), biểu đồ phân bổ sự cố theo danh mục và phòng ban",
        "Hệ thống thiết kế chuẩn doanh nghiệp (Enterprise 2D Design System): sử dụng chuẩn màu phẳng tokens, font chữ IBM Plex Sans và hỗ trợ chuyển đổi giao diện Sáng / Tối (Light / Dark mode)"
    ]
    for tn in tinh_nang:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.space_after = Pt(1)
        p.add_run(f"- {tn}")

    p6_2 = doc.add_paragraph()
    p6_2.paragraph_format.left_indent = Inches(0.2)
    p6_2.paragraph_format.space_before = Pt(2)
    p6_2.paragraph_format.space_after = Pt(1)
    p6_2.add_run("+ Yêu cầu kỹ thuật & chất lượng:").bold = True

    yeu_cau = [
        "Tất cả các API RESTful phải validate dữ liệu đầu vào chặt chẽ (Bean Validation)",
        "Xử lý ngoại lệ tập trung (@RestControllerAdvice), bắt lỗi try-catch cẩn thận và trả về mã lỗi rõ ràng",
        "Quy ước đặt tên biến, hàm, package theo chuẩn quốc tế tiếng Anh có ý nghĩa, tuân thủ Clean Code",
        "Phân chia module nhỏ gọn, kiến trúc phân tầng rõ ràng (Controller - Service - Repository)",
        "Cơ sở dữ liệu H2 lưu file vật lý local bền vững, có thể thêm dữ liệu mẫu tự động phục vụ demo",
        "Quản lý mã nguồn bằng Git / GitLab theo quy trình chia nhánh tính năng chuyên nghiệp"
    ]
    for yq in yeu_cau:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.space_after = Pt(1)
        p.add_run(f"- {yq}")

    # 9. Mục 7: Kế hoạch thực hiện
    doc.add_page_break()
    p7 = doc.add_paragraph()
    p7.paragraph_format.space_before = Pt(4)
    p7.add_run("7. Kế hoạch thực hiện").bold = True

    t_plan = doc.add_table(rows=11, cols=2)
    t_plan.style = 'Table Grid'
    t_plan.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_plan.columns[0].width = Inches(1.0)
    t_plan.columns[1].width = Inches(5.7)

    c0 = t_plan.cell(0, 0)
    c0.text = "Tuần"
    c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c0.paragraphs[0].runs[0].font.bold = True
    set_cell_background(c0, "EAEAEA")
    set_cell_margins(c0, 80, 80, 100, 100)

    c1 = t_plan.cell(0, 1)
    c1.text = "Nội dung công việc"
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c1.paragraphs[0].runs[0].font.bold = True
    set_cell_background(c1, "EAEAEA")
    set_cell_margins(c1, 80, 80, 100, 100)

    weeks_concise = [
        ("1", "Tìm hiểu văn hóa doanh nghiệp, kiến trúc Client-Server, RESTful API và Spring Boot 3\nCài đặt môi trường phát triển (Java 17, Maven, VS Code/IntelliJ, Node.js, Git)"),
        ("2", "Khảo sát quy trình hỗ trợ IT Helpdesk nội bộ, phân tích yêu cầu nghiệp vụ và mô hình cam kết dịch vụ SLA\nXây dựng biểu đồ Use Case cho 3 nhóm tác nhân (Employee, Agent, Admin)"),
        ("3", "Thiết kế cơ sở dữ liệu quan hệ (ERD), khởi tạo dự án Spring Boot 3\nCấu hình H2 Database lưu file local bền vững và Web Console kiểm tra dữ liệu"),
        ("4", "Xây dựng các Entity JPA (User, Category, SlaPolicy, Ticket, Comment), xử lý tránh đệ quy JSON\nXây dựng tầng Repository và Service tự động tính hạn chót SLA dueDate khi tạo ticket"),
        ("5", "Xây dựng các RESTful API (Ticket, Category, SlaPolicy, User, Comment, Dashboard)\nCấu hình WebConfig mở CORS toàn cục cho máy khách Frontend"),
        ("6", "Cài đặt môi trường và xây dựng cấu trúc front-end với ReactJS (Vite), Tailwind CSS, Axios, Router\nThiết lập Design System doanh nghiệp (bộ Design Tokens CSS, font IBM Plex Sans, hỗ trợ Light/Dark mode)"),
        ("7", "Xây dựng trang Login (xác thực nhanh 3 vai trò Demo)\nXây dựng bảng Danh sách Ticket đa góc nhìn (Tất cả ticket, Của tôi, Chưa phân công) và ngăn trượt TicketDetailDrawer tương tác nhanh"),
        ("8", "Xây dựng Modal tạo Ticket với cam kết giờ SLA trực quan\nXây dựng các phân hệ Quản trị: Quản lý danh mục dịch vụ (/categories), Quản lý người dùng & phân quyền (/users), Chính sách SLA (/sla-policies)"),
        ("9", "Triển khai SlaScheduler quét ngầm tự động ticket quá hạn mỗi phút\nXây dựng Dashboard thống kê chỉ số KPI và Phân hệ Báo cáo phân tích hiệu năng IT (/reports) với biểu đồ Recharts"),
        ("10", "Kiểm thử tích hợp hệ thống (E2E), tối ưu hóa trải nghiệm người dùng theo phong cách 2D hiện đại\nĐóng gói mã nguồn và hoàn thiện quyển Báo cáo thực tập doanh nghiệp")
    ]

    for i, (w_num, w_task) in enumerate(weeks_concise, start=1):
        cell_w = t_plan.cell(i, 0)
        cell_w.text = w_num
        cell_w.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell_w.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins(cell_w, 60, 60, 80, 80)
        
        cell_t = t_plan.cell(i, 1)
        cell_t.text = w_task
        cell_t.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
        cell_t.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins(cell_t, 60, 60, 100, 100)

    # 10. Chữ ký xác nhận
    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(14)
    
    t_sign = doc.add_table(rows=2, cols=3)
    t_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sign.columns[0].width = Inches(2.2)
    t_sign.columns[1].width = Inches(2.3)
    t_sign.columns[2].width = Inches(2.2)

    headers_sign = [
        ("Sinh viên thực tập", "(Ký và ghi rõ họ tên)"),
        ("Người hướng dẫn tại công ty", "(Ký và ghi rõ họ tên)"),
        ("Giảng viên hướng dẫn", "(Ký và ghi rõ họ tên)")
    ]

    for col_idx, (t1, t2) in enumerate(headers_sign):
        c = t_sign.cell(0, col_idx)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f"{t1}\n")
        r1.bold = True
        r2 = p.add_run(t2)
        r2.font.italic = True
        r2.font.size = Pt(10)
        
        c_space = t_sign.cell(1, col_idx)
        p_sp = c_space.paragraphs[0]
        p_sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sp.add_run("\n\n\n\n")

    output_path = "De_cuong_Thuc_tap_Doanh_nghiep_IT_Helpdesk.docx"
    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    create_de_cuong()
