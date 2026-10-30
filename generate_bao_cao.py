import os
import sys
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

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(14)
    r.font.name = 'Times New Roman'
    r.font.color.rgb = RGBColor(0, 51, 102)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(13)
    r.font.name = 'Times New Roman'
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.italic = True
    r.font.size = Pt(13)
    r.font.name = 'Times New Roman'
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_body_p(doc, text, bold_prefix="", indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.5
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.4)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(13)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    return p

def add_bullet_item(doc, text, bold_title=""):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.3
    r_bullet = p.add_run("• ")
    r_bullet.bold = True
    if bold_title:
        r_title = p.add_run(bold_title + ": ")
        r_title.bold = True
        r_title.font.name = 'Times New Roman'
        r_title.font.size = Pt(13)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    return p

def create_bao_cao_concise():
    print("Generating comprehensive and concise Bao cao thuc tap doanh nghiep updated to current product...")
    doc = docx.Document()

    # Căn lề chuẩn HUMG: Top 2.5cm, Bottom 2.5cm, Left 3.5cm, Right 2.5cm
    for s in doc.sections:
        s.top_margin = Inches(0.984)
        s.bottom_margin = Inches(0.984)
        s.left_margin = Inches(1.378)
        s.right_margin = Inches(0.984)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.line_spacing = 1.5

    # ==================== TRANG BÌA CHÍNH (BÌA 1) ====================
    p_b1 = doc.add_paragraph()
    p_b1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_b1.paragraph_format.line_spacing = 1.2
    r = p_b1.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\n")
    r.font.size = Pt(13)
    r.bold = True
    r2 = p_b1.add_run("TRƯỜNG ĐẠI HỌC MỎ - ĐỊA CHẤT\n")
    r2.font.size = Pt(14)
    r2.bold = True
    r3 = p_b1.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n------------------***------------------")
    r3.font.size = Pt(13)
    r3.bold = True

    for _ in range(4): doc.add_paragraph()

    p_b2 = doc.add_paragraph()
    p_b2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_b2.paragraph_format.line_spacing = 1.3
    r_bc = p_b2.add_run("BÁO CÁO THỰC TẬP DOANH NGHIỆP\n\n")
    r_bc.bold = True
    r_bc.font.size = Pt(20)
    r_bc.font.color.rgb = RGBColor(0, 51, 102)

    r_cn = p_b2.add_run("CHUYÊN NGÀNH: CÔNG NGHỆ PHẦN MỀM\n\n")
    r_cn.bold = True
    r_cn.font.size = Pt(14)

    r_dt = p_b2.add_run("ĐỀ TÀI:\n\"XÂY DỰNG HỆ THỐNG QUẢN LÝ YÊU CẦU HỖ TRỢ NỘI BỘ\n(IT HELPDESK TICKETING SYSTEM)\nTHEO KIẾN TRÚC SPRING BOOT VÀ REACTJS\"")
    r_dt.bold = True
    r_dt.font.size = Pt(15)

    for _ in range(5): doc.add_paragraph()

    p_b3 = doc.add_paragraph()
    p_b3.paragraph_format.left_indent = Inches(1.5)
    p_b3.paragraph_format.line_spacing = 1.3
    r_sv = p_b3.add_run("Sinh viên thực hiện:\t")
    r_sv.bold = True
    p_b3.add_run("[HỌ VÀ TÊN BẠN]\n")
    r_msv = p_b3.add_run("Mã sinh viên:\t\t")
    r_msv.bold = True
    p_b3.add_run("[MÃ SINH VIÊN CỦA BẠN]\n")
    r_lop = p_b3.add_run("Lớp:\t\t\t")
    r_lop.bold = True
    p_b3.add_run("DCCTPM65...\n")
    r_khoa = p_b3.add_run("Khóa:\t\t\t")
    r_khoa.bold = True
    p_b3.add_run("65 (2020 - 2025)")

    for _ in range(3): doc.add_paragraph()

    p_b4 = doc.add_paragraph()
    p_b4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_hn = p_b4.add_run("HÀ NỘI, THÁNG 10 NĂM 2026")
    r_hn.bold = True
    r_hn.font.size = Pt(13)

    # ==================== TRANG BÌA PHỤ (BÌA 2) ====================
    doc.add_page_break()
    p_bp1 = doc.add_paragraph()
    p_bp1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bp1.paragraph_format.line_spacing = 1.2
    r = p_bp1.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\n")
    r.font.size = Pt(13)
    r.bold = True
    r2 = p_bp1.add_run("TRƯỜNG ĐẠI HỌC MỎ - ĐỊA CHẤT\n")
    r2.font.size = Pt(14)
    r2.bold = True
    r3 = p_bp1.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n------------------***------------------")
    r3.font.size = Pt(13)
    r3.bold = True

    for _ in range(3): doc.add_paragraph()

    p_bp2 = doc.add_paragraph()
    p_bp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bp2.paragraph_format.line_spacing = 1.3
    r_bc = p_bp2.add_run("BÁO CÁO THỰC TẬP DOANH NGHIỆP\n\n")
    r_bc.bold = True
    r_bc.font.size = Pt(18)
    r_bc.font.color.rgb = RGBColor(0, 51, 102)

    r_cn = p_bp2.add_run("CHUYÊN NGÀNH: CÔNG NGHỆ PHẦN MỀM\n\n")
    r_cn.bold = True
    r_cn.font.size = Pt(13)

    r_dt = p_bp2.add_run("ĐỀ TÀI:\n\"XÂY DỰNG HỆ THỐNG QUẢN LÝ YÊU CẦU HỖ TRỢ NỘI BỘ\n(IT HELPDESK TICKETING SYSTEM)\nTHEO KIẾN TRÚC SPRING BOOT VÀ REACTJS\"")
    r_dt.bold = True
    r_dt.font.size = Pt(14)

    for _ in range(4): doc.add_paragraph()

    p_bp3 = doc.add_paragraph()
    p_bp3.paragraph_format.left_indent = Inches(1.0)
    p_bp3.paragraph_format.line_spacing = 1.3
    
    info_bp = [
        ("Sinh viên thực tập:", "[HỌ VÀ TÊN BẠN]"),
        ("Mã sinh viên:", "[MÃ SINH VIÊN CỦA BẠN]"),
        ("Công ty thực tập:", "Công ty TNHH JITS INOVATION LABS"),
        ("Người phụ trách tại công ty:", "Đào Văn Tâm (Quản lý dự án)"),
        ("Giảng viên hướng dẫn:", "ThS. Nguyễn Thế Lộc (Bộ môn CNPM)")
    ]
    for lbl, val in info_bp:
        r_lbl = p_bp3.add_run(f"{lbl}\t")
        r_lbl.bold = True
        p_bp3.add_run(f"{val}\n")

    for _ in range(3): doc.add_paragraph()

    p_bp4 = doc.add_paragraph()
    p_bp4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_hn = p_bp4.add_run("HÀ NỘI, THÁNG 10 NĂM 2026")
    r_hn.bold = True
    r_hn.font.size = Pt(13)

    # ==================== ĐỀ CƯƠNG THỰC TẬP DOANH NGHIỆP ====================
    doc.add_page_break()
    p_dc_h = doc.add_paragraph()
    p_dc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dc_h.add_run("ĐỀ CƯƠNG THỰC TẬP DOANH NGHIỆP\n")
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(0, 51, 102)

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.3
    p.add_run("1. Sinh viên thực tập:\n").bold = True
    p.add_run("   • Họ và tên: [HỌ VÀ TÊN BẠN]   -   Mã SV: [MÃ SINH VIÊN CỦA BẠN]\n"
              "   • Lớp: DCCTPM65...   -   Điện thoại: [Số điện thoại của bạn]\n"
              "   • Email: [Mã sinh viên]@student.humg.edu.vn\n\n")
    p.add_run("2. Giảng viên hướng dẫn:\n").bold = True
    p.add_run("   • Họ và tên: ThS. Nguyễn Thế Lộc (Mã CB: 0801-02) - Bộ môn Công nghệ phần mềm\n"
              "   • Điện thoại: 0983330682   -   Email: nguyentheloc@humg.edu.vn\n\n")
    p.add_run("3. Thông tin công ty thực tập:\n").bold = True
    p.add_run("   • Tên công ty: Công ty TNHH JITS INOVATION LABS\n"
              "   • Địa chỉ: Tầng 2, số 6 phố Phạm Tuấn Tài, P. Dịch Vọng Hậu, Q. Cầu Giấy, Hà Nội\n"
              "   • SĐT: 0338 355 571   -   Email: contact@jitsinnovationlabs.com   -   MST: 0107486223\n\n")
    p.add_run("4. Người hướng dẫn tại công ty:\n").bold = True
    p.add_run("   • Họ và tên: Đào Văn Tâm   -   Chức vụ: Quản lý dự án\n"
              "   • SĐT: 0357708915   -   Email: tamdv@jitsinnovationlabs.com\n\n")
    p.add_run("5. Tên đề tài thực tập:\n").bold = True
    p.add_run("   \"Xây dựng Hệ thống Quản lý Yêu cầu Hỗ trợ Nội bộ (IT Helpdesk Ticketing System) theo kiến trúc Spring Boot và ReactJS\"\n\n")
    p.add_run("6. Nhiệm vụ và yêu cầu kỹ thuật:\n").bold = True
    p.add_run("   • Tính năng: Đăng nhập 3 vai trò (Employee, Agent, Admin); Quản lý danh mục dịch vụ (/categories); Quản lý người dùng & phân quyền (/users); Quản lý chính sách SLA (/sla-policies); Tạo ticket tự động tính SLA; Danh sách yêu cầu đa góc nhìn (Tất cả, Của tôi, Chưa phân công); Ngăn trượt TicketDetailDrawer tương tác nhanh; Bảng điều khiển KPI và Báo cáo hiệu năng IT (/reports); Hệ thống thiết kế chuẩn doanh nghiệp 2D (IBM Plex Sans, Light/Dark mode).\n"
              "   • Yêu cầu: Validate dữ liệu đầu vào (Bean Validation), try-catch xử lý ngoại lệ tập trung, Clean Code, phân tầng Controller-Service-Repository, quản lý mã nguồn bằng Git/GitLab.\n\n")
    p.add_run("7. Kế hoạch thực hiện 10 tuần tóm tắt:\n").bold = True

    t_dc_plan = doc.add_table(rows=11, cols=2)
    t_dc_plan.style = 'Table Grid'
    t_dc_plan.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_dc_plan.columns[0].width = Inches(0.9)
    t_dc_plan.columns[1].width = Inches(5.1)

    t_dc_plan.cell(0, 0).text = "Tuần"
    t_dc_plan.cell(0, 0).paragraphs[0].runs[0].font.bold = True
    t_dc_plan.cell(0, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_cell_background(t_dc_plan.cell(0, 0), "EAEAEA")
    t_dc_plan.cell(0, 1).text = "Nội dung công việc"
    t_dc_plan.cell(0, 1).paragraphs[0].runs[0].font.bold = True
    t_dc_plan.cell(0, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_cell_background(t_dc_plan.cell(0, 1), "EAEAEA")

    weeks_summary = [
        ("Tuần 1", "Tìm hiểu văn hóa doanh nghiệp, kiến trúc Client-Server, RESTful API và cài đặt môi trường (Java 17, Maven, VS Code/IntelliJ, Node.js)"),
        ("Tuần 2", "Khảo sát quy trình IT Helpdesk nội bộ, phân tích yêu cầu nghiệp vụ và thiết kế biểu đồ Use Case cho 3 vai trò"),
        ("Tuần 3", "Thiết kế cơ sở dữ liệu quan hệ (ERD), khởi tạo Spring Boot 3 và cấu hình H2 Database lưu file local bền vững"),
        ("Tuần 4", "Xây dựng các Entity JPA (User, Category, SlaPolicy, Ticket, Comment), xử lý tránh đệ quy JSON và viết Service tính hạn SLA dueDate"),
        ("Tuần 5", "Xây dựng RESTful API cho Ticket, Category, SlaPolicy, User, Comment, Dashboard và cấu hình WebConfig mở CORS toàn cục"),
        ("Tuần 6", "Khởi tạo front-end ReactJS (Vite), Tailwind CSS, Axios, Router; thiết lập Design System chuẩn doanh nghiệp (Tokens, IBM Plex Sans, Light/Dark mode)"),
        ("Tuần 7", "Xây dựng trang Login (chuyển đổi nhanh 3 vai trò Demo), danh sách Ticket đa góc nhìn (Tất cả, Của tôi, Chưa phân công) và ngăn trượt TicketDetailDrawer"),
        ("Tuần 8", "Xây dựng Modal tạo Ticket tự động tính SLA; xây dựng các phân hệ Quản trị: Danh mục dịch vụ (/categories), Người dùng (/users), Chính sách SLA (/sla-policies)"),
        ("Tuần 9", "Triển khai SlaScheduler quét ngầm ticket quá hạn; xây dựng Dashboard KPI và Phân hệ Báo cáo phân tích hiệu năng IT (/reports) với Recharts"),
        ("Tuần 10", "Kiểm thử tích hợp hệ thống (E2E), tối ưu hóa giao diện 2D doanh nghiệp, đóng gói mã nguồn và hoàn thiện báo cáo thực tập")
    ]
    for idx, (wn, wt) in enumerate(weeks_summary, start=1):
        c0 = t_dc_plan.cell(idx, 0)
        c0.text = wn
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_margins(c0, 40, 40, 60, 60)
        c1 = t_dc_plan.cell(idx, 1)
        c1.text = wt
        set_cell_margins(c1, 40, 40, 80, 80)

    # ==================== MỤC LỤC ====================
    doc.add_page_break()
    p_ml = doc.add_paragraph()
    p_ml.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_ml.add_run("MỤC LỤC")
    r.bold = True
    r.font.size = Pt(16)
    p_ml.paragraph_format.space_after = Pt(12)

    toc_items = [
        ("ĐỀ CƯƠNG THỰC TẬP DOANH NGHIỆP", "3"),
        ("MỞ ĐẦU", "5"),
        ("CHƯƠNG 1: GIỚI THIỆU VỀ CÔNG TY VÀ VỊ TRÍ THỰC TẬP", "6"),
        ("  1.1 Giới thiệu về Công ty TNHH JITS INOVATION LABS", "6"),
        ("  1.2 Vị trí thực tập và nhiệm vụ được giao", "6"),
        ("  1.3 Đề tài thực tập", "7"),
        ("  1.4 Kế hoạch và tiến độ thực tập 10 tuần (Bảng 1-1)", "7"),
        ("CHƯƠNG 2: NỘI DUNG VÀ KẾT QUẢ THỰC TẬP", "9"),
        ("  2.1 Các công cụ và phần mềm đã tìm hiểu, sử dụng", "9"),
        ("  2.2 Các công nghệ, kỹ thuật mới và lý thuyết đã áp dụng", "10"),
        ("  2.3 Phân tích thiết kế hệ thống và cơ sở dữ liệu", "11"),
        ("  2.4 Các phân hệ chức năng đã xây dựng theo sản phẩm thực tế", "13"),
        ("    2.4.1 Phân hệ Đăng nhập và chuyển đổi nhanh 3 vai trò Demo", "13"),
        ("    2.4.2 Phân hệ Quản lý yêu cầu hỗ trợ (Tạo ticket, Danh sách đa góc nhìn, Drawer chi tiết)", "13"),
        ("    2.4.3 Phân hệ Quản trị Danh mục dịch vụ (Service Categories)", "14"),
        ("    2.4.4 Phân hệ Quản trị Người dùng & Phân quyền (User Management)", "15"),
        ("    2.4.5 Phân hệ Quản lý Chính sách cam kết dịch vụ (SLA Policies & SlaScheduler)", "15"),
        ("    2.4.6 Phân hệ Bảng điều khiển KPI và Báo cáo phân tích hiệu năng IT (Dashboard & Reports)", "16"),
        ("    2.4.7 Chuẩn hóa giao diện theo Hệ thống thiết kế doanh nghiệp (Design System 2D)", "17"),
        ("CHƯƠNG 3: ĐÁNH GIÁ KẾT QUẢ VÀ ĐỊNH HƯỚNG PHÁT TRIỂN", "18"),
        ("  3.1 Tự đánh giá kết quả quá trình thực tập", "18"),
        ("    3.1.1 Về mặt kiến thức chuyên môn", "18"),
        ("    3.1.2 Về mặt kỹ năng làm việc và kỹ năng mềm", "18"),
        ("    3.1.3 Khả năng đáp ứng công việc thực tế", "19"),
        ("  3.2 Đánh giá mức độ áp dụng kiến thức đào tạo tại HUMG", "19"),
        ("  3.3 Định hướng phát triển đề tài cho Đồ án tốt nghiệp", "20"),
        ("KẾT LUẬN", "21"),
        ("TÀI LIỆU THAM KHẢO", "22"),
        ("PHỤ LỤC", "23")
    ]
    for item, page in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.space_after = Pt(2)
        r_item = p_t.add_run(item)
        if item.startswith("CHƯƠNG") or item in ["ĐỀ CƯƠNG THỰC TẬP DOANH NGHIỆP", "MỞ ĐẦU", "KẾT LUẬN", "TÀI LIỆU THAM KHẢO", "PHỤ LỤC"]:
            r_item.bold = True
        dots_len = max(4, 75 - len(item))
        p_t.add_run(" " + "." * dots_len + " ")
        r_p = p_t.add_run(page)
        r_p.bold = True

    # ==================== MỞ ĐẦU ====================
    doc.add_page_break()
    add_heading_1(doc, "MỞ ĐẦU")
    
    add_body_p(doc, 
        "Trong các doanh nghiệp hiện nay, hệ thống công nghệ thông tin (CNTT) đóng vai trò then chốt trong hoạt động vận hành "
        "hàng ngày. Tuy nhiên, khi xảy ra sự cố kỹ thuật (hỏng máy tính, lỗi mạng, phần mềm không truy cập được), nhiều đơn vị vẫn tiếp nhận "
        "thông qua tin nhắn Zalo, Skype hoặc gọi điện trực tiếp. Quy trình thủ công này dễ dẫn đến tình trạng bỏ sót yêu cầu, "
        "không có cam kết thời gian hoàn thành (SLA) và cấp quản lý không đo lường được hiệu suất của đội ngũ hỗ trợ IT.")

    add_body_p(doc,
        "Nhận thức được vấn đề trên, trong kỳ thực tập tại Công ty TNHH JITS INOVATION LABS, sinh viên đã lựa chọn và thực hiện đề tài: "
        "\"Xây dựng Hệ thống Quản lý Yêu cầu Hỗ trợ Nội bộ (IT Helpdesk Ticketing System) theo kiến trúc Spring Boot và ReactJS\". "
        "Hệ thống nhằm số hóa toàn diện quy trình tiếp nhận, xử lý sự cố, tự động tính hạn SLA và trực quan hóa dữ liệu qua Dashboard.")

    add_body_p(doc,
        "Báo cáo gồm 3 chương chính:\n"
        "• Chương 1: Giới thiệu về công ty và vị trí thực tập (Tổng quan công ty, vị trí, đề tài và lịch làm việc 10 tuần).\n"
        "• Chương 2: Nội dung và kết quả thực tập (Các công cụ, công nghệ tìm hiểu, phân tích thiết kế, các phân hệ chức năng thực tế và chuẩn hóa giao diện Design System).\n"
        "• Chương 3: Đánh giá kết quả và định hướng phát triển (Tự đánh giá, liên hệ kiến thức môn học HUMG và hướng mở rộng Đồ án tốt nghiệp).")

    # ==================== CHƯƠNG 1 ====================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 1: GIỚI THIỆU VỀ CÔNG TY VÀ VỊ TRÍ THỰC TẬP")

    add_heading_2(doc, "1.1 Giới thiệu về Công ty TNHH JITS INOVATION LABS")
    add_body_p(doc,
        "Công ty TNHH JITS INOVATION LABS là doanh nghiệp công nghệ chuyên cung cấp các giải pháp phần mềm tài chính ngân hàng, "
        "Core Banking, cổng thanh toán số và các ứng dụng chuyển đổi số doanh nghiệp.")
    add_bullet_item(doc, "Tầng 2, số 6, phố Phạm Tuấn Tài, P. Dịch Vọng Hậu, Q. Cầu Giấy, TP. Hà Nội", "Địa chỉ trụ sở")
    add_bullet_item(doc, "0338 355 571   |   Email: contact@jitsinnovationlabs.com", "Điện thoại & Email")
    add_bullet_item(doc, "Ông Nguyễn Đức Hoàng   -   Mã số thuế: 0107486223", "Người đại diện & MST")
    add_bullet_item(doc, "Hơn 80 kỹ sư phần mềm, làm việc theo mô hình Agile/Scrum linh hoạt và hiện đại.", "Quy mô nhân sự")

    add_heading_2(doc, "1.2 Vị trí thực tập và nhiệm vụ được giao")
    add_body_p(doc,
        "Trong thời gian 10 tuần, sinh viên thực tập tại vị trí Thực tập sinh Kỹ sư phần mềm (Full-Stack Intern) "
        "dưới sự hướng dẫn trực tiếp của anh Đào Văn Tâm – Quản lý dự án tại công ty. Nhiệm vụ chính gồm:")
    add_bullet_item(doc, "Tìm hiểu quy trình hỗ trợ CNTT nội bộ và mô hình cam kết dịch vụ SLA.")
    add_bullet_item(doc, "Xây dựng Backend RESTful API sử dụng Java 17, Spring Boot 3 và Spring Data JPA.")
    add_bullet_item(doc, "Xây dựng Frontend Single Page Application bằng ReactJS, Tailwind CSS, Axios, Router và Recharts.")
    add_bullet_item(doc, "Áp dụng hệ thống thiết kế phần mềm doanh nghiệp chuẩn mực (2D, IBM Plex Sans, Light/Dark mode).")
    add_bullet_item(doc, "Kiểm thử tích hợp, hoàn thiện sản phẩm và viết báo cáo thực tập doanh nghiệp.")

    add_heading_2(doc, "1.3 Đề tài thực tập")
    add_body_p(doc,
        "• Tên đề tài: \"Xây dựng Hệ thống Quản lý Yêu cầu Hỗ trợ Nội bộ (IT Helpdesk Ticketing System) theo kiến trúc Spring Boot và ReactJS\".\n"
        "• Mục tiêu: Xây dựng một ứng dụng web hoàn chỉnh, độc lập, phân quyền 3 nhóm người dùng (Nhân viên, Kỹ thuật viên IT, Quản trị viên), "
        "hỗ trợ quản lý toàn diện vòng đời phiếu yêu cầu từ lúc tạo, tiếp nhận, xử lý đến khi đóng phiếu, tự động cảnh báo quá hạn SLA, "
        "đồng thời tích hợp đầy đủ các phân hệ quản trị danh mục, người dùng, chính sách SLA và báo cáo phân tích hiệu năng.")

    add_heading_2(doc, "1.4 Kế hoạch và tiến độ thực tập 10 tuần")
    add_body_p(doc, "Dưới đây là bảng phân công công việc chi tiết và mức độ hoàn thành trong 10 tuần thực tập của sinh viên:")

    # BẢNG 1-1 CHUẨN 5 CỘT THEO HƯỚNG DẪN HUMG
    p_cap1 = doc.add_paragraph()
    r = p_cap1.add_run("Bảng 1- 1 Lịch làm việc 10 tuần thực tập tại doanh nghiệp")
    r.bold = True
    p_cap1.paragraph_format.space_after = Pt(2)

    t_w10 = doc.add_table(rows=11, cols=5)
    t_w10.style = 'Table Grid'
    t_w10.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_w10.columns[0].width = Inches(0.6)
    t_w10.columns[1].width = Inches(2.8)
    t_w10.columns[2].width = Inches(1.1)
    t_w10.columns[3].width = Inches(1.1)
    t_w10.columns[4].width = Inches(0.8)

    headers_w10 = ["Tuần", "Nội dung công việc", "Người hướng dẫn", "Mức độ hoàn thành", "Ghi chú"]
    for c_i, h_txt in enumerate(headers_w10):
        cell = t_w10.cell(0, c_i)
        cell.text = h_txt
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, 50, 50, 50, 50)

    work_plan = [
        ("Tuần 1", "Tìm hiểu văn hóa doanh nghiệp, quy trình Agile/Scrum. Cài đặt công cụ: Java 17, Maven, VS Code/IntelliJ, Node.js, Git.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 2", "Khảo sát thực trạng quy trình IT Helpdesk nội bộ. Phân tích yêu cầu nghiệp vụ và vẽ biểu đồ Use Case cho 3 vai trò.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 3", "Thiết kế cơ sở dữ liệu quan hệ (ERD). Khởi tạo Spring Boot 3, cấu hình H2 Database lưu file local bền vững.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 4", "Tạo các Entity JPA (User, Category, SlaPolicy, Ticket, Comment), xử lý tránh đệ quy JSON. Viết Service tính hạn SLA dueDate.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 5", "Xây dựng các RESTful API (Ticket, Category, SlaPolicy, User, Comment, Dashboard). Cấu hình WebConfig mở CORS toàn cục.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 6", "Khởi tạo Frontend ReactJS (Vite), cấu hình Tailwind CSS, Axios, Router; thiết lập Design System chuẩn doanh nghiệp (Tokens, IBM Plex Sans, Light/Dark mode).", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 7", "Xây dựng trang Login (chuyển đổi nhanh 3 vai trò Demo), danh sách Ticket đa góc nhìn (Tất cả, Của tôi, Chưa phân công) và ngăn trượt TicketDetailDrawer.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 8", "Xây dựng Modal tạo Ticket tự động tính SLA; xây dựng các phân hệ Quản trị: Danh mục dịch vụ (/categories), Người dùng (/users), Chính sách SLA (/sla-policies).", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 9", "Triển khai SlaScheduler quét ngầm ticket quá hạn; xây dựng Dashboard KPI và Phân hệ Báo cáo phân tích hiệu năng IT (/reports) với Recharts.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 10", "Kiểm thử tích hợp hệ thống (E2E), tối ưu hóa trải nghiệm người dùng theo phong cách 2D hiện đại, đóng gói mã nguồn và hoàn thiện báo cáo thực tập.", "Đào Văn Tâm", "100%", "Hoàn thành xuất sắc")
    ]
    for row_idx, r_data in enumerate(work_plan, start=1):
        for col_idx, text_val in enumerate(r_data):
            c = t_w10.cell(row_idx, col_idx)
            c.text = text_val
            c.paragraphs[0].runs[0].font.size = Pt(9.5)
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if col_idx in [0, 2, 3, 4]:
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_cell_margins(c, 40, 40, 50, 50)

    # ==================== CHƯƠNG 2 ====================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 2: NỘI DUNG VÀ KẾT QUẢ THỰC TẬP")

    add_heading_2(doc, "2.1 Các công cụ và phần mềm đã tìm hiểu, sử dụng")
    add_body_p(doc, "Trong quá trình thực tập, sinh viên đã trực tiếp làm quen và sử dụng thành thạo bộ công cụ phát triển phần mềm gồm:")
    add_bullet_item(doc, "IDE chính để viết mã nguồn Backend Java Spring Boot và Frontend ReactJS, sử dụng các extension hỗ trợ format và debug.", "Visual Studio Code & IntelliJ IDEA")
    add_bullet_item(doc, "Hệ thống quản lý phiên bản mã nguồn phân tán, thực hiện tạo nhánh tính năng, commit và push mã nguồn định kỳ.", "Git & GitLab")
    add_bullet_item(doc, "Công cụ gửi request HTTP (GET, POST, PUT, PATCH, DELETE) kiểm thử dữ liệu JSON trả về từ các RESTful API trước khi ghép nối Frontend.", "Postman")
    add_bullet_item(doc, "Giao diện web trực quan của cơ sở dữ liệu H2 giúp kiểm tra nhanh các bảng dữ liệu và câu lệnh SQL tại đường dẫn http://localhost:8080/h2-console.", "H2 Web Console")

    add_heading_2(doc, "2.2 Các công nghệ, kỹ thuật mới và lý thuyết đã áp dụng")
    add_body_p(doc, "Bám sát các yêu cầu từ Mentor, sinh viên đã nghiên cứu và vận dụng các kiến thức kỹ thuật sau:")
    add_bullet_item(doc, "Sử dụng Java 17 LTS và framework Spring Boot 3.3.5 để xây dựng tầng dịch vụ dữ liệu RESTful API độc lập.", "Java 17 & Spring Boot 3")
    add_bullet_item(doc, "Khai báo các Interface kế thừa JpaRepository và JpaSpecificationExecutor để truy vấn dữ liệu động, loại bỏ việc viết câu lệnh SQL thủ công.", "Spring Data JPA & Hibernate")
    add_bullet_item(doc, "Cấu hình lưu cơ sở dữ liệu ra tệp vật lý './data/helpdesk_db' để dữ liệu không bị mất khi khởi động lại ứng dụng.", "H2 Persistent File Database")
    add_bullet_item(doc, "Xây dựng giao diện Single Page Application (SPA) với Vite, chuyển trang mượt mà không tải lại trang.", "ReactJS (Vite)")
    add_bullet_item(doc, "Áp dụng chuẩn thiết kế phần mềm doanh nghiệp (ServiceNow / Jira Service Management) với bộ CSS Tokens phẳng, font IBM Plex Sans và hỗ trợ Light/Dark mode.", "Enterprise 2D Design System & Tailwind CSS")
    add_bullet_item(doc, "Sử dụng slide-over drawer trượt từ cạnh phải để xem chi tiết và xử lý ticket nhanh chóng mà không làm mất ngữ cảnh bộ lọc danh sách.", "Drawer UX Pattern")
    add_bullet_item(doc, "Khái niệm cam kết thời gian hoàn thành theo 4 mức ưu tiên: Khẩn cấp (CRITICAL: 2h), Cao (HIGH: 8h), Trung bình (MEDIUM: 24h), Thấp (LOW: 48h) và quy trình leo thang sự cố.", "Quy trình ITIL & SLA Policy")
    add_bullet_item(doc, "Trực quan hóa chỉ số KPI bằng biểu đồ cột đôi và biểu đồ thanh đo mức độ tuân thủ SLA đổi màu theo ngưỡng cảnh báo.", "Thư viện Recharts")
    add_bullet_item(doc, "Giải quyết triệt để 3 bài toán kỹ thuật chuyên sâu: Ngắt đệ quy vô tận JSON Infinite Recursion bằng @JsonIgnoreProperties; Mở CORS toàn cục cho cổng 5173 bằng WebConfig; Quét tự động ticket quá hạn mỗi phút bằng @Scheduled(fixedRate = 60000).", "Các kỹ thuật chuyên sâu")

    add_heading_2(doc, "2.3 Phân tích thiết kế hệ thống và cơ sở dữ liệu")
    add_body_p(doc, 
        "Hệ thống được thiết kế theo kiến trúc phân tầng chuẩn mực (Layered Architecture): Tách biệt hoàn toàn máy chủ Backend (Port 8080) "
        "và máy khách Frontend (Port 5173), giao tiếp với nhau thuần túy qua giao thức HTTP REST API định dạng JSON.")

    add_body_p(doc, "Cơ sở dữ liệu gồm 5 thực thể chính:")
    add_bullet_item(doc, "Lưu thông tin tài khoản, mật khẩu (@JsonProperty(WRITE_ONLY)), họ tên, email, phòng ban và vai trò (EMPLOYEE, AGENT, ADMIN).", "Bảng users (Người dùng)")
    add_bullet_item(doc, "Lưu các nhóm sự cố kỹ thuật (Phần mềm & Bản quyền, Phần cứng & Thiết bị, Mạng nội bộ & Tài khoản, Email & Cloud).", "Bảng categories (Danh mục dịch vụ)")
    add_bullet_item(doc, "Quy định số giờ xử lý cam kết tương ứng với 4 cấp độ ưu tiên (CRITICAL 2h, HIGH 8h, MEDIUM 24h, LOW 48h).", "Bảng sla_policies (Chính sách SLA)")
    add_bullet_item(doc, "Lưu mã ticket (HD-xxxx), tiêu đề, mô tả, trạng thái (OPEN, IN_PROGRESS, RESOLVED, CLOSED), độ ưu tiên, người tạo, người xử lý, hạn dueDate và cờ isOverdue.", "Bảng tickets (Phiếu yêu cầu)")
    add_bullet_item(doc, "Lưu nội dung bình luận, người gửi và thời điểm trao đổi giữa người yêu cầu và nhân viên kỹ thuật.", "Bảng ticket_comments (Thảo luận sự cố)")

    add_heading_2(doc, "2.4 Các phân hệ chức năng đã xây dựng theo sản phẩm thực tế")
    add_body_p(doc, "Dựa trên kế hoạch 10 tuần, sinh viên đã hoàn thành đầy đủ các phân hệ chức năng chính của sản phẩm:")

    add_heading_3(doc, "2.4.1 Phân hệ Đăng nhập và chuyển đổi nhanh 3 vai trò Demo")
    add_body_p(doc,
        "Trang Đăng nhập (/login) được thiết kế theo chuẩn 2D doanh nghiệp. Ngoài form nhập tài khoản và mật khẩu, hệ thống cung cấp "
        "3 thẻ bấm 'Chuyển nhanh tài khoản Demo' đại diện cho 3 vai trò: Nhân viên (emp_nam), Kỹ thuật viên IT (agent_hoa), Quản trị viên (admin_quang). "
        "Khi bấm thẻ, hệ thống gọi API /api/auth/login, lưu thông tin người dùng vào localStorage qua React AuthContext và điều hướng mượt mà vào hệ thống.")

    add_heading_3(doc, "2.4.2 Phân hệ Quản lý yêu cầu hỗ trợ (Tạo ticket, Danh sách đa góc nhìn, Drawer chi tiết)")
    add_body_p(doc,
        "Phân hệ yêu cầu là trọng tâm của hệ thống, bao gồm 3 thành phần chính liên kết chặt chẽ:")
    add_bullet_item(doc, "Modal tạo yêu cầu hiển thị trực quan các mức ưu tiên cùng số giờ cam kết SLA. Backend tự động sinh mã phiếu (HD-xxxx) và cộng số giờ SLA vào thời điểm tạo để xác định chính xác hạn chót dueDate.", "Tạo yêu cầu mới (CreateTicketModal)")
    add_bullet_item(doc, "Hỗ trợ 3 góc nhìn tiện ích trên thanh Navbar: 'Tất cả ticket' (danh sách toàn bộ), 'Của tôi' (phiếu do bản thân tạo hoặc phụ trách kèm badge số đếm) và 'Chưa phân công' (phiếu mới đang chờ nhận xử lý kèm badge số đếm). Bảng dữ liệu có hàng cao chuẩn 44px, hỗ trợ tìm kiếm và lọc trạng thái kèm số đếm.", "Danh sách Ticket đa góc nhìn (TicketList)")
    add_bullet_item(doc, "Khi nhấp vào bất kỳ hàng nào trên bảng (hoặc nhấn phím Enter), ngăn chi tiết trượt ra từ cạnh phải màn hình (max 460px) có mask mờ và phím tắt Esc. Cho phép duyệt thông tin, thực hiện quy trình nghiệp vụ (Tiếp nhận -> Đã giải quyết -> Đóng phiếu -> Mở lại) và gửi bình luận trao đổi trực tiếp mà không cần chuyển trang.", "Ngăn trượt chi tiết (TicketDetailDrawer)")

    add_heading_3(doc, "2.4.3 Phân hệ Quản trị Danh mục dịch vụ (Service Categories)")
    add_body_p(doc,
        "Trang Quản lý danh mục (/categories) cho phép ban quản trị phân loại các nhóm sự cố kỹ thuật thường gặp. "
        "Hỗ trợ tìm kiếm nhanh theo tên hoặc mô tả dịch vụ, xem trạng thái áp dụng và tích hợp Modal thêm danh mục mới kết nối API Backend (POST /api/categories).")

    add_heading_3(doc, "2.4.4 Phân hệ Quản trị Người dùng & Phân quyền (User Management)")
    add_body_p(doc,
        "Trang Quản lý người dùng (/users) dành riêng cho vai trò ADMIN. Cung cấp danh sách toàn bộ nhân sự trong công ty, "
        "hỗ trợ tìm kiếm tức thời theo từ khóa và bộ lọc theo vai trò (Employee, Agent, Admin). Tích hợp Modal cấp tài khoản mới "
        "(họ tên, email, phòng ban, mật khẩu mặc định 123456) có cơ chế kiểm tra trùng lặp email/username, và nút xóa tài khoản có xác thực bảo vệ an toàn.")

    add_heading_3(doc, "2.4.5 Phân hệ Quản lý Chính sách cam kết dịch vụ (SLA Policies & SlaScheduler)")
    add_body_p(doc,
        "Trang Chính sách SLA (/sla-policies) công khai ma trận thời gian cam kết dịch vụ của doanh nghiệp: "
        "Khẩn cấp (phản hồi <= 15 phút, giải quyết <= 2 giờ); Cao (phản hồi <= 30 phút, giải quyết <= 8 giờ); "
        "Trung bình (phản hồi <= 2 giờ, giải quyết <= 24 giờ); Thấp (phản hồi <= 4 giờ, giải quyết <= 48 giờ) cùng quy định leo thang khi trễ hạn. "
        "Phía Backend, tiến trình SlaScheduler chạy ngầm định kỳ mỗi phút tự động kiểm tra và đánh dấu cờ isOverdue = true cho các phiếu quá hạn dueDate.")

    add_heading_3(doc, "2.4.6 Phân hệ Bảng điều khiển KPI và Báo cáo phân tích hiệu năng IT (Dashboard & Reports)")
    add_body_p(doc,
        "Hệ thống cung cấp 2 màn hình phân tích số liệu trực quan:")
    add_bullet_item(doc, "Màn hình Dashboard (/dashboard) hiển thị 4 thẻ KPI đo lường cốt lõi (Tổng yêu cầu, Chờ tiếp nhận, Đang xử lý, Quá hạn SLA), kết hợp biểu đồ cột đôi so sánh số lượng mới/đã giải quyết và thanh đo tỷ lệ tuân thủ SLA tự động đổi màu khi xuống dưới ngưỡng cảnh báo.", "Bảng điều khiển tác nghiệp (Dashboard)")
    add_bullet_item(doc, "Màn hình Báo cáo (/reports) đo lường các chỉ số quản lý chất lượng dịch vụ chuyên sâu: Tỷ lệ đạt chuẩn SLA (%), Thời gian phản hồi trung bình (MTTA), Thời gian khắc phục trung bình (MTTR), biểu đồ phân bổ yêu cầu theo danh mục dịch vụ và phân bổ sự cố theo từng phòng ban.", "Báo cáo phân tích hiệu năng (Reports)")

    add_heading_3(doc, "2.4.7 Chuẩn hóa giao diện theo Hệ thống thiết kế doanh nghiệp (Design System 2D)")
    add_body_p(doc,
        "Toàn bộ giao diện được chuẩn hóa theo Hệ thống thiết kế (Design System) hiện đại: "
        "Sử dụng font chữ duy nhất IBM Plex Sans hỗ trợ tiếng Việt; bảng mã màu phẳng tokens CSS không dùng gradient hay bóng đổ nặng; "
        "chỉ sử dụng duy nhất một màu nhấn chủ đạo (--brand #0b6bcb / #4c9dff); hỗ trợ chuyển đổi linh hoạt chế độ Sáng / Tối (Light / Dark mode) "
        "và thanh Sidebar 232px chuyên nghiệp với cấu trúc phân nhóm rõ ràng: Tổng quan, Yêu cầu, Quản trị.")

    # ==================== CHƯƠNG 3 ====================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 3: ĐÁNH GIÁ KẾT QUẢ VÀ ĐỊNH HƯỚNG PHÁT TRIỂN")

    add_heading_2(doc, "3.1 Tự đánh giá kết quả quá trình thực tập")
    add_heading_3(doc, "3.1.1 Về mặt kiến thức chuyên môn")
    add_body_p(doc,
        "Từ mức độ cơ bản nhập môn Java Spring, sau 10 tuần thực tập sinh viên đã làm chủ quy trình xây dựng Backend RESTful API hoàn chỉnh, "
        "hiểu rõ cách thức phân tầng Controller - Service - Repository, quản lý dữ liệu bằng Spring Data JPA và tích hợp tác vụ chạy ngầm định kỳ. "
        "Đồng thời thành thạo kỹ năng xây dựng giao diện người dùng hiện đại với ReactJS, Tailwind CSS và làm chủ tư duy thiết kế Design System doanh nghiệp.")

    add_heading_3(doc, "3.1.2 Về mặt kỹ năng làm việc và kỹ năng mềm")
    add_body_p(doc,
        "Sinh viên đã nâng cao rõ rệt kỹ năng tra cứu tài liệu kỹ thuật chính thống, đọc và phân tích lỗi (debug); "
        "thực hành quản lý mã nguồn bài bản với Git; rèn luyện tác phong làm việc kỷ luật, chủ động báo cáo tiến độ và tiếp thu góp ý từ người hướng dẫn.")

    add_heading_3(doc, "3.1.3 Khả năng đáp ứng công việc thực tế")
    add_body_p(doc,
        "Mặc dù đang làm việc trong lĩnh vực khác, nhưng với tinh thần tự học cao và sự hướng dẫn sát sao từ công ty, "
        "sinh viên đã hoàn thành 100% các mục tiêu công việc đề ra đúng tiến độ, chứng minh khả năng thích ứng tốt với môi trường phát triển phần mềm chuyên nghiệp.")

    add_heading_2(doc, "3.2 Đánh giá mức độ áp dụng kiến thức đào tạo tại HUMG")
    add_body_p(doc, "Quá trình thực tập đã giúp sinh viên củng cố và vận dụng trực tiếp các môn học cốt lõi tại Khoa CNTT - HUMG:")
    add_bullet_item(doc, "Tư duy lập trình hướng đối tượng, đóng gói và kế thừa là nền tảng cốt lõi để viết các Entity, Service và Repository trong Spring Boot.", "Lập trình Java / Hướng đối tượng (OOP)")
    add_bullet_item(doc, "Áp dụng kiến thức thiết kế bảng, khóa chính (PK), khóa ngoại (FK) và chuẩn hóa dữ liệu để xây dựng cơ sở dữ liệu tối ưu.", "Cơ sở dữ liệu & Hệ quản trị CSDL")
    add_bullet_item(doc, "Vẽ biểu đồ ca sử dụng (Use Case) và mô hình hóa thực thể quan hệ (ERD) cho bài toán IT Helpdesk.", "Phân tích thiết kế hệ thống thông tin")
    add_bullet_item(doc, "Hiểu rõ phương thức HTTP (GET, POST, PUT, PATCH, DELETE), mã phản hồi HTTP và cấu trúc JSON để kết nối giữa Frontend và Backend.", "Công nghệ Web")
    add_bullet_item(doc, "Hiểu rõ quy trình phát triển phần mềm Agile/Scrum, quản trị phiên bản với Git và tầm quan trọng của việc kiểm thử chất lượng mã nguồn.", "Công nghệ phần mềm")

    add_heading_2(doc, "3.3 Định hướng phát triển đề tài cho Đồ án tốt nghiệp")
    add_body_p(doc, "Để phát triển hệ thống thành Đồ án tốt nghiệp chuyên sâu, sinh viên định hướng các nội dung mở rộng sau:")
    add_bullet_item(doc, "Tích hợp Spring Security kết hợp JSON Web Token (JWT) để mã hóa phiên làm việc và phân quyền bảo mật chặt chẽ trên từng API.", "Nâng cấp bảo mật với Spring Security & JWT")
    add_bullet_item(doc, "Sử dụng Spring WebSocket để đẩy thông báo chuông và pop-up tức thì khi có ticket mới hoặc bình luận; gửi email tự động khi ticket sắp quá hạn SLA.", "Hệ thống thông báo thời gian thực (WebSocket & Email)")
    add_bullet_item(doc, "Viết tệp Dockerfile đóng gói Backend, Frontend và Database để triển khai đồng nhất lên nền tảng đám mây; nghiên cứu AI tự động gợi ý phân loại sự cố.", "Đóng gói Docker & Ứng dụng AI phân loại sự cố")

    # ==================== KẾT LUẬN ====================
    doc.add_page_break()
    add_heading_1(doc, "KẾT LUẬN")
    
    add_body_p(doc,
        "Kỳ thực tập doanh nghiệp tại Công ty TNHH JITS INOVATION LABS đã mang lại cho sinh viên những trải nghiệm thực tế vô cùng giá trị. "
        "Sinh viên đã hoàn thành toàn diện sản phẩm 'Hệ thống Quản lý Yêu cầu Hỗ trợ Nội bộ (IT Helpdesk Ticketing System)' đáp ứng đầy đủ "
        "các chức năng quản lý sự cố theo tiêu chuẩn SLA, phân quyền 3 vai trò, ngăn trượt TicketDetailDrawer, phân hệ quản trị danh mục/người dùng/chính sách SLA, "
        "và hệ thống báo cáo phân tích hiệu năng IT theo chuẩn thiết kế doanh nghiệp 2D.")

    add_body_p(doc,
        "Dự án không chỉ giúp sinh viên hệ thống hóa và áp dụng các kiến thức đã học tại Trường Đại học Mỏ - Địa chất, "
        "mà còn là nền tảng vững chắc để sinh viên tự tin tiếp tục hoàn thiện, phát triển thành Đồ án tốt nghiệp đại học trong giai đoạn tiếp theo.")

    add_body_p(doc,
        "Sinh viên xin bày tỏ lòng biết ơn chân thành tới thầy giáo hướng dẫn ThS. Nguyễn Thế Lộc (Khoa CNTT - HUMG) "
        "cùng anh Đào Văn Tâm và tập thể các anh chị tại Công ty TNHH JITS INOVATION LABS đã nhiệt tình hướng dẫn, "
        "hỗ trợ sinh viên hoàn thành tốt kỳ thực tập này.")

    # ==================== TÀI LIỆU THAM KHẢO ====================
    doc.add_page_break()
    add_heading_1(doc, "TÀI LIỆU THAM KHẢO")

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.3
    p.add_run("Tài liệu Tiếng Việt:\n").bold = True
    p.add_run("[1] Đoàn Văn Ban (2018), Giáo trình Kỹ thuật phần mềm, Nhà xuất bản Giáo dục Việt Nam, Hà Nội.\n"
              "[2] Đặng Văn Đức (2015), Phân tích và thiết kế hệ thống hướng đối tượng với UML, NXB Khoa học và Kỹ thuật.\n"
              "[3] Nguyễn Văn Ba (2019), Phát triển ứng dụng Web và kiến trúc RESTful API, NXB Đại học Quốc gia Hà Nội.\n\n")

    p.add_run("Tài liệu Tiếng Anh:\n").bold = True
    p.add_run("[4] Craig Walls (2022), Spring in Action, Sixth Edition, Manning Publications, New York.\n"
              "[5] Alex Banks and Eve Porcello (2020), Learning React: Modern Patterns for Developing React Apps, O'Reilly Media.\n"
              "[6] Robert C. Martin (2017), Clean Architecture: A Craftsman's Guide to Software Structure and Design, Prentice Hall.\n\n")

    p.add_run("Tài liệu từ Internet:\n").bold = True
    p.add_run("[7] Spring Boot Official Documentation, https://spring.io/projects/spring-boot, truy cập ngày 15/10/2026.\n"
              "[8] React Official Documentation, https://react.dev, truy cập ngày 18/10/2026.\n"
              "[9] Tailwind CSS Official Documentation, https://tailwindcss.com, truy cập ngày 20/10/2026.\n")

    # ==================== PHỤ LỤC ====================
    doc.add_page_break()
    add_heading_1(doc, "PHỤ LỤC: CẤU HÌNH VÀ THÀNH PHẦN HỆ THỐNG")

    add_heading_2(doc, "Phụ lục 1: Cấu hình mở CORS toàn cục trên Backend (WebConfig.java)")
    p_code1 = doc.add_paragraph()
    p_code1.paragraph_format.left_indent = Inches(0.2)
    p_code1.paragraph_format.line_spacing = 1.15
    r_c1 = p_code1.add_run(
        "@Configuration\n"
        "public class WebConfig implements WebMvcConfigurer {\n"
        "    @Override\n"
        "    public void addCorsMappings(CorsRegistry registry) {\n"
        "        registry.addMapping(\"/api/**\")\n"
        "                .allowedOrigins(\"http://localhost:5173\")\n"
        "                .allowedMethods(\"GET\", \"POST\", \"PUT\", \"PATCH\", \"DELETE\", \"OPTIONS\")\n"
        "                .allowedHeaders(\"*\")\n"
        "                .allowCredentials(true);\n"
        "    }\n"
        "}"
    )
    r_c1.font.name = 'Consolas'
    r_c1.font.size = Pt(10)

    add_heading_2(doc, "Phụ lục 2: Cấu hình kết nối HTTP Client trên Frontend (axiosClient.js)")
    p_code2 = doc.add_paragraph()
    p_code2.paragraph_format.left_indent = Inches(0.2)
    p_code2.paragraph_format.line_spacing = 1.15
    r_c2 = p_code2.add_run(
        "import axios from 'axios';\n"
        "\n"
        "const axiosClient = axios.create({\n"
        "    baseURL: 'http://localhost:8080/api',\n"
        "    headers: {\n"
        "        'Content-Type': 'application/json',\n"
        "    },\n"
        "});\n"
        "\n"
        "export default axiosClient;"
    )
    r_c2.font.name = 'Consolas'
    r_c2.font.size = Pt(10)

    add_heading_2(doc, "Phụ lục 3: Cấu hình hệ thống Design Tokens CSS (tokens.css)")
    p_code3 = doc.add_paragraph()
    p_code3.paragraph_format.left_indent = Inches(0.2)
    p_code3.paragraph_format.line_spacing = 1.15
    r_c3 = p_code3.add_run(
        ":root {\n"
        "  --bg: #f4f6f9; --surface: #ffffff; --line: #e2e7ee;\n"
        "  --text: #1b2433; --muted: #64708a; --nav: #0f1f3d;\n"
        "  --brand: #0b6bcb; --ok: #1a7f4b; --warn: #a15c00; --err: #c0262d;\n"
        "}\n"
        "[data-theme=\"dark\"] {\n"
        "  --bg: #0d1320; --surface: #151d2e; --line: #26304a;\n"
        "  --text: #e6ebf5; --muted: #8d9ab5; --nav: #090f1d;\n"
        "  --brand: #4c9dff; --ok: #4cc38a; --warn: #f0b04a; --err: #ff7a80;\n"
        "}"
    )
    r_c3.font.name = 'Consolas'
    r_c3.font.size = Pt(10)

    output_path = "Bao_cao_Thuc_tap_Doanh_nghiep_IT_Helpdesk.docx"
    try:
        doc.save(output_path)
        print(f"Successfully generated: {output_path}")
    except PermissionError:
        backup_path = "Bao_cao_Thuc_tap_Doanh_nghiep_IT_Helpdesk_CapNhat.docx"
        doc.save(backup_path)
        print(f"File {output_path} is currently locked by another program (e.g. Word). Saved to: {backup_path}")

if __name__ == "__main__":
    create_bao_cao_concise()
