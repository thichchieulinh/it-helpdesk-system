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

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(16)
    r.font.name = 'Times New Roman'
    r.font.color.rgb = RGBColor(0, 51, 102)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(14)
    r.font.name = 'Times New Roman'
    r.font.color.rgb = RGBColor(0, 51, 102)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.italic = True
    r.font.size = Pt(13)
    r.font.name = 'Times New Roman'
    r.font.color.rgb = RGBColor(0, 0, 0)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p

def add_body_p(doc, text, bold_prefix="", indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.39) # 1 cm
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
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.3
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
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

def add_table_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(11.5)
    r.font.name = 'Times New Roman'
    r.font.color.rgb = RGBColor(0, 51, 102)
    return p

def add_figure_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.italic = True
    r.bold = True
    r.font.size = Pt(11.5)
    r.font.name = 'Times New Roman'
    return p

def create_table_custom(doc, rows, cols, col_widths, headers, data, align_cols=None):
    table = doc.add_table(rows=rows, cols=cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, width in enumerate(col_widths):
        table.columns[idx].width = width

    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h_text
        set_cell_background(cell, "D9E1F2")
        set_cell_margins(cell, 80, 80, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.runs:
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(10.5)
            p.runs[0].font.name = 'Times New Roman'

    for r_idx, row_values in enumerate(data, start=1):
        for c_idx, val in enumerate(row_values):
            cell = table.cell(r_idx, c_idx)
            cell.text = str(val)
            set_cell_margins(cell, 60, 60, 80, 80)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            if align_cols and c_idx in align_cols:
                p.alignment = align_cols[c_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if p.runs:
                p.runs[0].font.size = Pt(10)
                p.runs[0].font.name = 'Times New Roman'
    return table

def generate_report():
    print("Building high-standard TTDN Report (Quality Model B) according to ttdn-report-writer skill...")
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

    r_cn = p_b2.add_run("NGÀNH: CÔNG NGHỆ THÔNG TIN\nCHUYÊN NGÀNH: CÔNG NGHỆ PHẦN MỀM\n\n")
    r_cn.bold = True
    r_cn.font.size = Pt(13)

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
    r_hn = p_b4.add_run("HÀ NỘI, NĂM 2026")
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
    r_hn = p_bp4.add_run("HÀ NỘI, NĂM 2026")
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
    p.add_run("   • Tính năng: Đăng nhập phân quyền 3 vai trò (Employee, Agent, Admin); Quản lý danh mục dịch vụ (/categories); Quản lý người dùng & phân quyền (/users - bảo vệ quyền Admin); Quản lý chính sách SLA (/sla-policies); Tạo ticket tự động tính SLA dueDate; Danh sách yêu cầu đa góc nhìn (Tất cả, Của tôi, Chưa phân công); Ngăn trượt TicketDetailDrawer tương tác nhanh; Bảng điều khiển KPI và Báo cáo hiệu năng IT (/reports); Hệ thống thiết kế chuẩn doanh nghiệp 2D (IBM Plex Sans, Light/Dark mode).\n"
              "   • Yêu cầu: Validate dữ liệu đầu vào (Bean Validation), try-catch xử lý ngoại lệ tập trung, Clean Code, phân tầng Controller-Service-Repository, quản lý mã nguồn bằng Git/GitLab.\n\n")
    p.add_run("7. Kế hoạch thực hiện 10 tuần tóm tắt:\n").bold = True

    weeks_summary = [
        ("Tuần 1", "Tìm hiểu văn hóa doanh nghiệp, kiến trúc Client-Server, RESTful API và cài đặt môi trường (Java 17, Maven, VS Code/IntelliJ, Node.js, Git)"),
        ("Tuần 2", "Khảo sát quy trình hỗ trợ IT Helpdesk nội bộ, phân tích yêu cầu nghiệp vụ và mô hình cam kết dịch vụ SLA; xây dựng Use Case cho 3 vai trò"),
        ("Tuần 3", "Thiết kế cơ sở dữ liệu quan hệ (ERD), khởi tạo dự án Spring Boot 3 và cấu hình H2 Database lưu file local bền vững"),
        ("Tuần 4", "Xây dựng các Entity JPA (User, Category, SlaPolicy, Ticket, Comment), xử lý tránh đệ quy JSON và viết Service tính hạn SLA dueDate"),
        ("Tuần 5", "Xây dựng các RESTful API cho Ticket, Category, SlaPolicy, User, Comment, Dashboard và cấu hình WebConfig mở CORS toàn cục"),
        ("Tuần 6", "Khởi tạo front-end ReactJS (Vite), Tailwind CSS, Axios, Router; thiết lập Design System chuẩn doanh nghiệp (Tokens, IBM Plex Sans, Light/Dark mode)"),
        ("Tuần 7", "Xây dựng trang Login (chuyển đổi nhanh 3 vai trò Demo), danh sách Ticket đa góc nhìn (Tất cả, Của tôi, Chưa phân công) và ngăn trượt TicketDetailDrawer"),
        ("Tuần 8", "Xây dựng Modal tạo Ticket tự động tính SLA; xây dựng các phân hệ Quản trị: Danh mục dịch vụ (/categories), Người dùng (/users), Chính sách SLA (/sla-policies)"),
        ("Tuần 9", "Triển khai SlaScheduler quét ngầm ticket quá hạn; xây dựng Dashboard KPI và Phân hệ Báo cáo phân tích hiệu năng IT (/reports) với Recharts"),
        ("Tuần 10", "Kiểm thử tích hợp hệ thống (E2E), tối ưu hóa trải nghiệm người dùng theo chuẩn 2D hiện đại, đóng gói mã nguồn và hoàn thiện báo cáo thực tập")
    ]
    create_table_custom(doc, 11, 2, [Inches(0.9), Inches(5.1)], ["Tuần", "Nội dung công việc"], weeks_summary, {0: WD_ALIGN_PARAGRAPH.CENTER})

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
        ("DANH MỤC CÁC BẢNG BIỂU", "5"),
        ("DANH MỤC CÁC HÌNH VẼ", "6"),
        ("LỜI CẢM ƠN", "7"),
        ("MỞ ĐẦU", "8"),
        ("CHƯƠNG 1: GIỚI THIỆU VỀ CÔNG TY VÀ VỊ TRÍ THỰC TẬP", "9"),
        ("  1.1 Giới thiệu về Công ty TNHH JITS INOVATION LABS", "9"),
        ("  1.2 Vị trí thực tập và cách tổ chức công việc", "10"),
        ("  1.3 Đề tài thực tập", "11"),
        ("  1.4 Lịch làm việc và tiến độ thực tập 10 tuần", "11"),
        ("CHƯƠNG 2: NỘI DUNG VÀ KẾT QUẢ THỰC TẬP", "13"),
        ("  2.1 Công việc thực tế tại doanh nghiệp", "13"),
        ("  2.2 Phân tích yêu cầu bài toán", "14"),
        ("  2.3 Công nghệ và môi trường triển khai", "16"),
        ("  2.4 Kiến trúc và luồng xử lý hệ thống", "17"),
        ("  2.5 Thiết kế cơ sở dữ liệu", "18"),
        ("  2.6 Phân hệ Xác thực và phân quyền theo vai trò", "20"),
        ("  2.7 Phân hệ Quản lý yêu cầu hỗ trợ và luồng trạng thái", "21"),
        ("  2.8 Phân hệ Quản trị hệ thống", "23"),
        ("  2.9 Phân hệ Bảng điều khiển KPI, Báo cáo và Thiết kế giao diện", "25"),
        ("  2.10 Kiểm thử chức năng và đánh giá kết quả", "27"),
        ("CHƯƠNG 3: ĐÁNH GIÁ KẾT QUẢ VÀ ĐỊNH HƯỚNG PHÁT TRIỂN", "29"),
        ("  3.1 Tự đánh giá kết quả quá trình thực tập", "29"),
        ("  3.2 Đánh giá mức độ áp dụng kiến thức đào tạo tại HUMG", "30"),
        ("  3.3 Khó khăn thực tế và kinh nghiệm rút ra", "31"),
        ("  3.4 Định hướng phát triển đề tài cho Đồ án tốt nghiệp", "33"),
        ("KẾT LUẬN", "34"),
        ("TÀI LIỆU THAM KHẢO", "35"),
        ("PHỤ LỤC", "36")
    ]
    for item, page in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.space_after = Pt(2)
        r_item = p_t.add_run(item)
        if item.startswith("CHƯƠNG") or item in ["ĐỀ CƯƠNG THỰC TẬP DOANH NGHIỆP", "MỞ ĐẦU", "KẾT LUẬN", "TÀI LIỆU THAM KHẢO", "PHỤ LỤC", "LỜI CẢM ƠN", "DANH MỤC CÁC BẢNG BIỂU", "DANH MỤC CÁC HÌNH VẼ"]:
            r_item.bold = True
        dots_len = max(4, 75 - len(item))
        p_t.add_run(" " + "." * dots_len + " ")
        r_p = p_t.add_run(page)
        r_p.bold = True

    # ==================== DANH MỤC BẢNG BIỂU ====================
    doc.add_page_break()
    p_dtb = doc.add_paragraph()
    p_dtb.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dtb.add_run("DANH MỤC CÁC BẢNG BIỂU")
    r.bold = True
    r.font.size = Pt(16)
    p_dtb.paragraph_format.space_after = Pt(12)

    list_tables = [
        ("Bảng 1.1", "Sản phẩm, dịch vụ chính của công ty và liên hệ với thực tập", "9"),
        ("Bảng 1.2", "Lịch làm việc và mức độ hoàn thành 10 tuần thực tập", "11"),
        ("Bảng 2.1", "Môi trường và thiết bị làm việc thực tế tại doanh nghiệp", "13"),
        ("Bảng 2.2", "Đặc tả các yêu cầu chức năng của hệ thống (FR01 - FR08)", "15"),
        ("Bảng 2.3", "Các công nghệ, framework sử dụng và vai trò trong hệ thống", "16"),
        ("Bảng 2.4", "Đặc tả các thực thể dữ liệu trong cơ sở dữ liệu hệ thống", "19"),
        ("Bảng 2.5", "Ma trận thời gian cam kết dịch vụ (SLA Policy Matrix)", "24"),
        ("Bảng 2.6", "Tổng hợp các ca kiểm thử chức năng thực tế (Test Cases)", "27"),
        ("Bảng 3.1", "Mối liên hệ giữa các học phần tại HUMG và cách vận dụng", "30"),
        ("Bảng 3.2", "Tổng kết khó khăn kỹ thuật theo quy trình 4 bước", "32")
    ]
    for code, title, p_num in list_tables:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.2
        p_t.paragraph_format.space_after = Pt(3)
        r_code = p_t.add_run(f"{code}: {title}")
        dots = max(4, 75 - len(f"{code}: {title}"))
        p_t.add_run(" " + "." * dots + " ")
        p_t.add_run(p_num).bold = True

    # ==================== DANH MỤC HÌNH VẼ ====================
    doc.add_page_break()
    p_dfg = doc.add_paragraph()
    p_dfg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dfg.add_run("DANH MỤC CÁC HÌNH VẼ")
    r.bold = True
    r.font.size = Pt(16)
    p_dfg.paragraph_format.space_after = Pt(12)

    list_figures = [
        ("Hình 2.1", "Sơ đồ ca sử dụng tổng quan (Use Case Diagram)", "14"),
        ("Hình 2.2", "Sơ đồ kiến trúc hệ thống Client-Server RESTful API", "17"),
        ("Hình 2.3", "Sơ đồ quan hệ thực thể cơ sở dữ liệu (ERD)", "18"),
        ("Hình 2.4", "Giao diện Danh sách yêu cầu đa góc nhìn và Drawer trượt tương tác", "22"),
        ("Hình 2.5", "Giao diện Bảng điều khiển KPI và Báo cáo phân tích hiệu năng", "26")
    ]
    for code, title, p_num in list_figures:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.line_spacing = 1.2
        p_f.paragraph_format.space_after = Pt(3)
        p_f.add_run(f"{code}: {title}")
        dots = max(4, 75 - len(f"{code}: {title}"))
        p_f.add_run(" " + "." * dots + " ")
        p_f.add_run(p_num).bold = True

    # ==================== LỜI CẢM ƠN ====================
    doc.add_page_break()
    add_heading_1(doc, "LỜI CẢM ƠN")

    add_body_p(doc,
        "Lời đầu tiên, em xin được bày tỏ lòng biết ơn sâu sắc nhất tới các thầy cô giáo tại Khoa Công nghệ thông tin – "
        "Trường Đại học Mỏ - Địa chất, những người đã tận tâm truyền đạt cho em nền tảng kiến thức chuyên môn vững chắc, "
        "tư duy kỹ thuật và phương pháp nghiên cứu khoa học trong suốt những năm học vừa qua. Đặc biệt, em xin gửi lời cảm ơn "
        "chân thành nhất tới thầy giáo hướng dẫn ThS. Nguyễn Thế Lộc – Giảng viên Bộ môn Công nghệ phần mềm, thầy đã luôn "
        "dành thời gian tận tình định hướng, góp ý chi tiết cho đề cương và theo sát tiến độ nghiên cứu của em trong kỳ thực tập này.")

    add_body_p(doc,
        "Em cũng xin trân trọng gửi lời cảm ơn chân thành đến Ban Giám đốc cùng toàn thể các anh chị đồng nghiệp tại "
        "Công ty TNHH JITS INOVATION LABS đã tạo điều kiện thuận lợi, tiếp nhận em vào thực tập tại công ty. Em xin đặc biệt cảm ơn "
        "anh Đào Văn Tâm – Quản lý dự án, người đã trực tiếp giao việc, tận tình chỉ dẫn em tiếp cận với quy trình phát triển phần mềm "
        "chuyên nghiệp, cách thức thiết kế hệ thống và văn hóa làm việc nhóm trong doanh nghiệp công nghệ thực tế.")

    add_body_p(doc,
        "Dù đã rất nỗ lực trau dồi và vận dụng tối đa kiến thức đã học, nhưng do năng lực và thời gian thực tập có hạn, "
        "báo cáo thực tập doanh nghiệp của em chắc chắn không tránh khỏi những thiếu sót nhất định. Em rất mong nhận được sự chỉ bảo, "
        "đóng góp ý kiến quý báu từ quý thầy cô và các anh chị hướng dẫn để sản phẩm và kiến thức của em ngày càng được hoàn thiện hơn.")

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(14)
    p_sig.add_run("Hà Nội, ngày 28 tháng 10 năm 2026\n").font.italic = True
    r_me = p_sig.add_run("Sinh viên thực tập\n\n\n\n[Họ và tên bạn]")
    r_me.bold = True

    # ==================== MỞ ĐẦU ====================
    doc.add_page_break()
    add_heading_1(doc, "MỞ ĐẦU")

    add_body_p(doc,
        "Trong bối cảnh chuyển đổi số đang diễn ra mạnh mẽ tại các doanh nghiệp hiện nay, hệ thống hạ tầng công nghệ thông tin (CNTT), "
        "thiết bị phần cứng và các ứng dụng phần mềm nghiệp vụ đóng vai trò sống còn trong việc đảm bảo tính liên tục của hoạt động sản xuất kinh doanh. "
        "Tuy nhiên, khi phát sinh sự cố kỹ thuật (như mất kết nối mạng nội bộ, máy tính hỏng linh kiện, máy in kẹt giấy, lỗi bản quyền phần mềm hay quên mật khẩu), "
        "rất nhiều doanh nghiệp vừa và nhỏ vẫn tiếp nhận yêu cầu hỗ trợ qua các kênh phi tập trung như tin nhắn Zalo, Skype, gọi điện thoại hoặc gửi email cá nhân.")

    add_body_p(doc,
        "Cách làm thủ công này bộc lộ những hạn chế đặc biệt nghiêm trọng: các yêu cầu dễ dàng bị bỏ quên, thông tin mô tả lỗi rời rạc, "
        "không có quy trình phân công trách nhiệm rõ ràng cho kỹ thuật viên, hoàn toàn thiếu vắng các cam kết thời gian hoàn thành (Service Level Agreement - SLA), "
        "và lãnh đạo doanh nghiệp không thể đo lường, giám sát được hiệu suất xử lý công việc của bộ phận hỗ trợ kỹ thuật.")

    add_body_p(doc,
        "Nhận thức rõ bối cảnh và nhu cầu cấp thiết đó, trong thời gian thực tập tại Công ty TNHH JITS INOVATION LABS, em đã chủ động tìm hiểu, "
        "khảo sát quy trình vận hành CNTT tại doanh nghiệp và lựa chọn thực hiện đề tài: \"Xây dựng Hệ thống Quản lý Yêu cầu Hỗ trợ Nội bộ "
        "(IT Helpdesk Ticketing System) theo kiến trúc Spring Boot và ReactJS\". Mục tiêu của đề tài là xây dựng một nền tảng phần mềm trực tuyến độc lập, "
        "chuẩn hóa quy trình tiếp nhận và xử lý sự cố từ lúc phát sinh đến khi đóng phiếu, tự động hóa tính hạn cam kết SLA và trực quan hóa toàn bộ chỉ số KPI trên Dashboard.")

    add_body_p(doc,
        "Phạm vi và giới hạn của đề tài: Hệ thống hiện tại đã hoàn thiện đầy đủ các phân hệ nghiệp vụ cốt lõi, bao gồm: phân quyền 3 nhóm vai trò (Nhân viên, Kỹ thuật viên IT, Quản trị viên), "
        "tạo yêu cầu tự động tính SLA, danh sách ticket đa góc nhìn, ngăn trượt TicketDetailDrawer tương tác nhanh, phân hệ quản trị danh mục dịch vụ, "
        "phân hệ quản trị người dùng (bảo vệ quyền Admin), quản trị chính sách SLA kèm tác vụ quét ngầm tự động, và bảng điều khiển KPI kết hợp báo cáo hiệu năng IT. "
        "Hệ thống đã được kiểm thử chạy ổn định trên môi trường máy đơn (local) với trình duyệt Google Chrome, chưa thử nghiệm tải lớn đồng thời trên môi trường Cloud đa máy chủ.")

    add_body_p(doc,
        "Bố cục của báo cáo gồm 3 chương chính như sau:\n"
        "• Chương 1 – Giới thiệu về công ty và vị trí thực tập: Trình bày tổng quan về Công ty TNHH JITS INOVATION LABS, quy chế làm việc, vị trí thực tập và bảng tiến độ 10 tuần.\n"
        "• Chương 2 – Nội dung và kết quả thực tập: Chi tiết các công cụ, phân tích yêu cầu, kiến trúc hệ thống, cơ sở dữ liệu, các phân hệ chức năng thực tế và kết quả kiểm thử.\n"
        "• Chương 3 – Đánh giá kết quả và định hướng phát triển: Tự đánh giá năng lực, mối liên hệ với các học phần tại HUMG, tổng kết kinh nghiệm xử lý khó khăn và định hướng phát triển Đồ án tốt nghiệp.")

    # ==================== CHƯƠNG 1 ====================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 1: GIỚI THIỆU VỀ CÔNG TY VÀ VỊ TRÍ THỰC TẬP")

    add_heading_2(doc, "1.1 Giới thiệu về Công ty TNHH JITS INOVATION LABS")
    add_body_p(doc,
        "Công ty TNHH JITS INOVATION LABS là doanh nghiệp công nghệ thông tin chuyên nghiên cứu, phát triển và cung cấp các giải pháp phần mềm "
        "chuyên sâu trong lĩnh vực tài chính, ngân hàng (Fintech, Core Banking), cổng thanh toán điện tử và các giải pháp chuyển đổi số toàn diện cho doanh nghiệp.")

    add_bullet_item(doc, "Công ty TNHH JITS INOVATION LABS", "Tên doanh nghiệp")
    add_bullet_item(doc, "Tầng 2, số 6, phố Phạm Tuấn Tài, phường Dịch Vọng Hậu, quận Cầu Giấy, thành phố Hà Nội", "Địa chỉ trụ sở chính")
    add_bullet_item(doc, "0338 355 571   -   Email: contact@jitsinnovationlabs.com", "Thông tin liên hệ")
    add_bullet_item(doc, "Ông Nguyễn Đức Hoàng   -   Mã số thuế: 0107486223", "Người đại diện pháp luật & MST")
    add_bullet_item(doc, "Hơn 80 nhân sự chất lượng cao, bao gồm các kiến trúc sư giải pháp, kỹ sư phần mềm Backend/Frontend, chuyên viên QA/QC và triển khai.", "Quy mô nhân lực")

    add_body_p(doc, "Bảng 1.1 tổng hợp các nhóm sản phẩm, dịch vụ chủ lực của công ty và mối liên hệ với quá trình thực tập của em:")

    add_table_caption(doc, "Bảng 1.1: Sản phẩm, dịch vụ chính của công ty và liên hệ với thực tập")
    tb1_data = [
        ("Giải pháp Core Banking & Thanh toán số", "Cung cấp nền tảng xử lý giao dịch tài chính cho các ngân hàng đối tác", "Giúp em hiểu rõ yêu cầu khắt khe về tính sẵn sàng cao, kiểm soát lỗi và bảo mật hệ thống"),
        ("Dịch vụ Chuyển đổi số & Tích hợp API", "Phát triển các cổng kết nối dữ liệu RESTful API giữa các hệ thống doanh nghiệp", "Em được học hỏi kiến trúc Microservices và chuẩn thiết kế RESTful API từ các Senior Engineer"),
        ("Hạ tầng IT & Quản lý Dịch vụ Nội bộ", "Hỗ trợ kỹ thuật, quản lý thiết bị và cam kết mức độ dịch vụ (SLA) cho nhân sự", "Là nguồn cảm hứng và cơ sở thực tế trực tiếp để em đề xuất xây dựng hệ thống IT Helpdesk")
    ]
    create_table_custom(doc, 4, 3, [Inches(1.8), Inches(2.3), Inches(2.6)], ["Sản phẩm / Dịch vụ", "Vai trò trong doanh nghiệp", "Liên hệ với quá trình thực tập"], tb1_data)

    add_heading_2(doc, "1.2 Vị trí thực tập và cách tổ chức công việc")
    add_body_p(doc,
        "Trong thời gian 10 tuần (từ tháng 08/2026 đến cuối tháng 10/2026), em được công ty tiếp nhận vào làm việc tại vị trí: "
        "Thực tập sinh Kỹ sư phần mềm (Full-Stack Intern), trực thuộc Khối Nghiên cứu & Phát triển sản phẩm. Người trực tiếp hướng dẫn "
        "và giám sát công việc của em là anh Đào Văn Tâm – Quản lý dự án tại công ty.")

    add_body_p(doc, "Quy chế làm việc và hình thức quản lý công việc được tổ chức chuyên nghiệp như sau:")
    add_bullet_item(doc, "Thời gian làm việc từ thứ Hai đến thứ Sáu, sáng từ 8h30 đến 12h00, chiều từ 13h30 đến 17h30. Chấm công nghiêm túc bằng vân tay và thẻ nhân viên.", "Thời gian & Kỷ luật lao động")
    add_bullet_item(doc, "Tham gia các buổi họp ngắn đầu ngày (Daily Stand-up) theo mô hình Agile/Scrum để báo cáo: việc đã làm hôm qua, việc sẽ làm hôm nay và các vướng mắc cần hỗ trợ.", "Quy trình nhận việc & Báo cáo")
    add_bullet_item(doc, "Toàn bộ mã nguồn phải được quản lý tập trung trên GitLab, tuân thủ quy tắc tạo nhánh tính năng (feature branch), viết commit message rõ ràng và tạo Merge Request để Mentor review.", "Quản trị mã nguồn")

    add_heading_2(doc, "1.3 Đề tài thực tập")
    add_body_p(doc,
        "• Tên đề tài: \"Xây dựng Hệ thống Quản lý Yêu cầu Hỗ trợ Nội bộ (IT Helpdesk Ticketing System) theo kiến trúc Spring Boot và ReactJS\".\n"
        "• Mục tiêu của đề tài: Xây dựng một ứng dụng web hoàn chỉnh, hiện đại, giải quyết triệt để bài toán tiếp nhận và xử lý sự cố CNTT nội bộ; "
        "phân định rõ ràng quyền hạn của 3 vai trò (Nhân viên chỉ tạo và xem ticket của mình; Kỹ thuật viên tiếp nhận, giải quyết và đổi trạng thái; "
        "Quản trị viên toàn quyền quản lý danh mục, người dùng, chính sách SLA và báo cáo); tự động tính hạn chót xử lý theo cam kết SLA và trực quan hóa số liệu.\n"
        "• Vai trò cá nhân: Em đóng vai trò là lập trình viên chính (Full-Stack Developer), độc lập tìm hiểu công nghệ, thiết kế CSDL, viết mã nguồn Backend Java Spring Boot, "
        "xây dựng giao diện Frontend ReactJS, áp dụng hệ thống thiết kế Enterprise 2D Design System và tiến hành kiểm thử toàn diện.")

    add_heading_2(doc, "1.4 Lịch làm việc và tiến độ thực tập 10 tuần")
    add_body_p(doc, "Tiến độ thực tập 10 tuần của em được thể hiện chi tiết trong Bảng 1.2 dưới đây:")

    add_table_caption(doc, "Bảng 1.2: Lịch làm việc và mức độ hoàn thành 10 tuần thực tập")
    tb2_data = [
        ("Tuần 1", "Tìm hiểu văn hóa doanh nghiệp, kiến trúc Client-Server, RESTful API và cài đặt môi trường (Java 17, Maven, VS Code/IntelliJ, Node.js, Git).", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 2", "Khảo sát quy trình hỗ trợ IT Helpdesk nội bộ, phân tích yêu cầu nghiệp vụ và mô hình cam kết dịch vụ SLA; xây dựng Use Case cho 3 vai trò.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 3", "Thiết kế cơ sở dữ liệu quan hệ (ERD). Khởi tạo Spring Boot 3, cấu hình H2 Database lưu file local bền vững và Web Console.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 4", "Tạo các Entity JPA (User, Category, SlaPolicy, Ticket, Comment), xử lý tránh đệ quy JSON. Viết Service tính hạn SLA dueDate.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 5", "Xây dựng các RESTful API (Ticket, Category, SlaPolicy, User, Comment, Dashboard). Cấu hình WebConfig mở CORS toàn cục.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 6", "Khởi tạo front-end ReactJS (Vite), Tailwind CSS, Axios, Router; thiết lập Design System chuẩn doanh nghiệp (Tokens, IBM Plex Sans, Light/Dark mode).", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 7", "Xây dựng trang Login (chuyển đổi nhanh 3 vai trò Demo), danh sách Ticket đa góc nhìn (Tất cả, Của tôi, Chưa phân công) và ngăn trượt TicketDetailDrawer.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 8", "Xây dựng Modal tạo Ticket tự động tính SLA; xây dựng các phân hệ Quản trị: Danh mục dịch vụ (/categories), Người dùng (/users), Chính sách SLA (/sla-policies).", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 9", "Triển khai SlaScheduler quét ngầm ticket quá hạn; xây dựng Dashboard KPI và Phân hệ Báo cáo phân tích hiệu năng IT (/reports) với Recharts.", "Đào Văn Tâm", "100%", "Hoàn thành tốt"),
        ("Tuần 10", "Kiểm thử tích hợp hệ thống (E2E), tối ưu hóa trải nghiệm người dùng theo chuẩn 2D hiện đại, đóng gói mã nguồn và hoàn thiện báo cáo thực tập.", "Đào Văn Tâm", "100%", "Hoàn thành xuất sắc")
    ]
    create_table_custom(doc, 11, 5, [Inches(0.6), Inches(2.9), Inches(1.1), Inches(1.1), Inches(0.9)], ["Tuần", "Nội dung công việc", "Người hướng dẫn", "Mức độ hoàn thành", "Ghi chú"], tb2_data, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER})

    # ==================== CHƯƠNG 2 ====================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 2: NỘI DUNG VÀ KẾT QUẢ THỰC TẬP")

    add_heading_2(doc, "2.1 Công việc thực tế tại doanh nghiệp")
    add_body_p(doc,
        "Trong suốt quá trình thực tập, em được công ty bố trí vị trí làm việc tại văn phòng kỹ thuật cùng các trang thiết bị hiện đại. "
        "Môi trường thực tế giúp em làm quen với tác phong làm việc của một kỹ sư phần mềm thực thụ. Bảng 2.1 mô tả chi tiết điều kiện làm việc của em:")

    add_table_caption(doc, "Bảng 2.1: Môi trường và thiết bị làm việc thực tế tại doanh nghiệp")
    tb21_data = [
        ("Thiết bị máy tính", "Máy tính xách tay cấu hình Intel Core i7, RAM 16GB, SSD 512GB kết nối màn hình phụ 24 inch", "Đảm bảo biên dịch đồng thời máy chủ Backend Spring Boot và Frontend Vite mượt mà"),
        ("Hạ tầng mạng", "Mạng LAN Gigabit nội bộ tốc độ cao, có cấu hình VPN và tường lửa phân vùng bảo mật", "Thực hành kết nối các dịch vụ trong mạng nội bộ và mô phỏng lỗi ngắt mạng phòng ban"),
        ("Công cụ quản trị", "GitLab công ty, Postman, Visual Studio Code, IntelliJ IDEA Community Edition, Chrome DevTools", "Phục vụ quy trình phát triển mã nguồn, gỡ lỗi và kiểm thử các API RESTful")
    ]
    create_table_custom(doc, 4, 3, [Inches(1.8), Inches(2.6), Inches(2.3)], ["Hạng mục", "Thông số / Công cụ", "Mục đích sử dụng thực tế"], tb21_data)

    add_heading_2(doc, "2.2 Phân tích yêu cầu bài toán")
    add_body_p(doc,
        "Dựa trên việc phỏng vấn các kỹ thuật viên IT Support tại công ty, em xác định hệ thống cần phục vụ 3 nhóm tác nhân (Actors) "
        "với quyền hạn được phân định rạch ròi:")
    add_bullet_item(doc, "Nhân sự các phòng ban có nhu cầu hỗ trợ. Có quyền tạo ticket mới, xem danh sách phiếu của chính mình, trao đổi bình luận và bấm xác nhận đóng phiếu sau khi sự cố đã được kỹ thuật viên xử lý.", "Nhân viên (EMPLOYEE)")
    add_bullet_item(doc, "Kỹ sư thuộc phòng IT Support. Có quyền xem danh sách tất cả các phiếu trong hàng đợi, tiếp nhận phiếu về cho mình (gán assignee), cập nhật trạng thái (Đang xử lý, Đã giải quyết), và mở lại phiếu nếu sự cố tái diễn.", "Kỹ thuật viên IT (AGENT)")
    add_bullet_item(doc, "Trưởng bộ phận CNTT hoặc Giám đốc kỹ thuật. Có toàn bộ quyền hạn của Kỹ thuật viên, đồng thời độc quyền quản trị người dùng (thêm, sửa, xóa tài khoản), quản trị danh mục dịch vụ, cấu hình chính sách SLA và xem toàn diện Dashboard, Báo cáo hiệu năng.", "Quản trị viên (ADMIN)")

    add_body_p(doc, "Hình 2.1 biểu diễn sơ đồ ca sử dụng tổng quan (Use Case Diagram) của hệ thống:")
    # Text placeholder for figure
    p_uc = doc.add_paragraph()
    p_uc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uc = p_uc.add_run("[SƠ ĐỒ USE CASE TỔNG QUAN HỆ THỐNG IT HELPDESK]")
    r_uc.font.bold = True
    r_uc.font.color.rgb = RGBColor(0, 51, 102)
    add_figure_caption(doc, "Hình 2.1: Sơ đồ ca sử dụng tổng quan (Use Case Diagram)")

    add_body_p(doc, "Bảng 2.2 liệt kê chi tiết các yêu cầu chức năng (FR - Functional Requirements) và trạng thái hoàn thành thực tế:")

    add_table_caption(doc, "Bảng 2.2: Đặc tả các yêu cầu chức năng của hệ thống (FR01 - FR08)")
    tb22_data = [
        ("FR01", "Xác thực & Chuyển đổi nhanh vai trò", "Đăng nhập bằng tài khoản và mật khẩu, hỗ trợ 3 nút bấm chuyển nhanh tài khoản demo đại diện 3 vai trò", "Đã hoàn thành"),
        ("FR02", "Tạo phiếu yêu cầu & Tính hạn SLA", "Nhân viên tạo ticket chọn mức ưu tiên, hệ thống tự động tính toán hạn chót dueDate dựa trên bảng SLA", "Đã hoàn thành"),
        ("FR03", "Danh sách ticket đa góc nhìn", "Hiển thị dạng bảng có bộ lọc trạng thái kèm số đếm; hỗ trợ 3 góc nhìn: Tất cả ticket, Của tôi, Chưa phân công", "Đã hoàn thành"),
        ("FR04", "Ngăn trượt TicketDetailDrawer", "Slide-over trượt từ cạnh phải khi click hàng bảng; hỗ trợ duyệt sự cố, chuyển trạng thái và gửi bình luận tức thì", "Đã hoàn thành"),
        ("FR05", "Quản lý danh mục dịch vụ (/categories)", "Xem danh sách, tìm kiếm và tạo mới nhóm danh mục sự cố kỹ thuật kết nối trực tiếp API Backend", "Đã hoàn thành"),
        ("FR06", "Quản trị người dùng & phân quyền (/users)", "Tìm kiếm nhân sự, lọc vai trò, cấp tài khoản mới và xóa tài khoản an toàn (chỉ hiển thị và truy cập với vai trò ADMIN)", "Đã hoàn thành"),
        ("FR07", "Chính sách SLA & Quét ngầm tự động", "Xem ma trận thời gian cam kết 4 mức độ; tiến trình SlaScheduler chạy ngầm tự động quét và đánh cờ quá hạn", "Đã hoàn thành"),
        ("FR08", "Dashboard KPI & Báo cáo hiệu năng", "Đo lường KPI, tỷ lệ tuân thủ SLA, thời gian MTTA, MTTR, biểu đồ cột Recharts phân bổ danh mục và phòng ban", "Đã hoàn thành")
    ]
    create_table_custom(doc, 9, 4, [Inches(0.7), Inches(2.2), Inches(2.7), Inches(1.1)], ["Mã FR", "Tên chức năng", "Mô tả chi tiết yêu cầu", "Trạng thái"], tb22_data, {0: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER})

    add_heading_2(doc, "2.3 Công nghệ và môi trường triển khai")
    add_body_p(doc,
        "Để đảm bảo hệ thống có kiến trúc chuẩn mực, hiệu năng cao và dễ dàng mở rộng, em đã lựa chọn kết hợp các công nghệ "
        "tiên tiến nhất trong hệ sinh thái Java và JavaScript hiện nay. Bảng 2.3 tổng hợp chi tiết các công nghệ được áp dụng:")

    add_table_caption(doc, "Bảng 2.3: Các công nghệ, framework sử dụng và vai trò trong hệ thống")
    tb23_data = [
        ("Java 17 LTS & Spring Boot 3.3.5", "Backend Core", "Cung cấp nền tảng xây dựng máy chủ độc lập, nhúng sẵn máy chủ Tomcat, quản lý Dependency tự động qua Maven"),
        ("Spring Data JPA & Hibernate", "Tầng dữ liệu (ORM)", "Ánh xạ các thực thể sang bảng CSDL; cung cấp các Repository truy vấn dữ liệu động mà không cần viết SQL thủ công"),
        ("H2 Persistent Database", "Cơ sở dữ liệu", "Hệ quản trị CSDL quan hệ nhúng lưu trữ bền vững ra tệp vật lý local './data/helpdesk_db', hỗ trợ Web Console trực quan"),
        ("ReactJS 18 & Vite 5", "Frontend Framework", "Xây dựng ứng dụng Single Page Application (SPA), render giao diện nhanh, tối ưu hóa bundle mã nguồn qua Vite"),
        ("Enterprise 2D Design System & Tailwind CSS", "Giao diện người dùng", "Thiết lập hệ thống token màu phẳng, font chữ IBM Plex Sans chuẩn doanh nghiệp, hỗ trợ chuyển đổi Light/Dark mode"),
        ("Recharts", "Trực quan hóa số liệu", "Vẽ biểu đồ cột đôi so sánh tiến độ, biểu đồ thanh SLA và biểu đồ phân bổ sự cố theo phòng ban/danh mục")
    ]
    create_table_custom(doc, 7, 3, [Inches(2.0), Inches(1.5), Inches(3.2)], ["Công nghệ / Thư viện", "Phân tầng áp dụng", "Vai trò kỹ thuật trong hệ thống"], tb23_data)

    add_heading_2(doc, "2.4 Kiến trúc và luồng xử lý hệ thống")
    add_body_p(doc,
        "Hệ thống tuân thủ mô hình kiến trúc phân tầng chuẩn mực (Layered Client-Server Architecture). Máy khách Frontend chạy độc lập "
        "tại cổng 5173 giao tiếp với máy chủ Backend tại cổng 8080 thuần túy thông qua các giao thức HTTP REST API định dạng JSON.")

    add_body_p(doc, "Các tầng kiến trúc trong Backend được tổ chức nghiêm ngặt:")
    add_bullet_item(doc, "Tiếp nhận các HTTP Request từ máy khách, thực hiện kiểm tra tính hợp lệ dữ liệu đầu vào (Bean Validation @Valid) và trả về HTTP Response tương ứng.", "Tầng Controller (com.helpdesk.controller)")
    add_bullet_item(doc, "Chứa toàn bộ logic nghiệp vụ cốt lõi: tự động tính hạn chót dueDate từ chính sách SLA, sinh mã phiếu ticket, kiểm tra điều kiện chuyển đổi trạng thái và điều phối dữ liệu.", "Tầng Service (com.helpdesk.service)")
    add_bullet_item(doc, "Kế thừa JpaRepository để thao tác trực tiếp với cơ sở dữ liệu (CRUD, phân trang, lọc động bằng Specification).", "Tầng Repository (com.helpdesk.repository)")
    add_bullet_item(doc, "Định nghĩa các thực thể dữ liệu gắn liền với các bảng trong CSDL quan hệ.", "Tầng Entity (com.helpdesk.entity)")

    p_arc = doc.add_paragraph()
    p_arc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_arc = p_arc.add_run("[SƠ ĐỒ KIẾN TRÚC CLIENT-SERVER RESTFUL API HỆ THỐNG IT HELPDESK]")
    r_arc.font.bold = True
    r_arc.font.color.rgb = RGBColor(0, 51, 102)
    add_figure_caption(doc, "Hình 2.2: Sơ đồ kiến trúc hệ thống Client-Server RESTful API")

    add_heading_2(doc, "2.5 Thiết kế cơ sở dữ liệu")
    add_body_p(doc,
        "Cơ sở dữ liệu của hệ thống được chuẩn hóa ở dạng chuẩn 3 (3NF) nhằm loại bỏ sự trùng lặp dữ liệu và đảm bảo toàn vẹn tham chiếu. "
        "Hình 2.3 biểu diễn sơ đồ quan hệ thực thể (ERD) giữa 5 bảng chính trong hệ thống:")

    p_erd = doc.add_paragraph()
    p_erd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_erd = p_erd.add_run("[SƠ ĐỒ QUAN HỆ THỰC THỂ CƠ SỞ DỮ LIỆU (ERD) - 5 BẢNG]")
    r_erd.font.bold = True
    r_erd.font.color.rgb = RGBColor(0, 51, 102)
    add_figure_caption(doc, "Hình 2.3: Sơ đồ quan hệ thực thể cơ sở dữ liệu (ERD)")

    add_body_p(doc, "Bảng 2.4 mô tả chi tiết ý nghĩa và các trường dữ liệu cốt lõi trong cơ sở dữ liệu:")

    add_table_caption(doc, "Bảng 2.4: Đặc tả các thực thể dữ liệu trong cơ sở dữ liệu hệ thống")
    tb24_data = [
        ("users", "Lưu thông tin nhân sự toàn công ty", "id (BIGINT)", "Không", "username (Unique), password (WRITE_ONLY), fullName, email (Unique), department, role (EMPLOYEE, AGENT, ADMIN)"),
        ("categories", "Lưu danh mục các nhóm sự cố CNTT", "id (BIGINT)", "Không", "name (VARCHAR 100), description (VARCHAR 255)"),
        ("sla_policies", "Lưu thời gian cam kết dịch vụ theo mức ưu tiên", "id (BIGINT)", "Không", "priorityLevel (CRITICAL, HIGH, MEDIUM, LOW - Unique), resolutionTimeHours (INT)"),
        ("tickets", "Lưu thông tin các phiếu yêu cầu hỗ trợ", "id (BIGINT)", "requester_id -> users(id)\nassignee_id -> users(id)\ncategory_id -> categories(id)", "ticketCode (HD-xxxx - Unique), title, description, status (OPEN, IN_PROGRESS, RESOLVED, CLOSED), priority, dueDate, isOverdue"),
        ("ticket_comments", "Lưu lịch sử thảo luận, trao đổi trên ticket", "id (BIGINT)", "ticket_id -> tickets(id)\nuser_id -> users(id)", "content (TEXT), createdAt (TIMESTAMP)")
    ]
    create_table_custom(doc, 6, 5, [Inches(1.1), Inches(1.8), Inches(0.9), Inches(1.4), Inches(1.5)], ["Tên bảng", "Ý nghĩa nghiệp vụ", "Khóa chính", "Khóa ngoại", "Các trường và ràng buộc cốt lõi"], tb24_data, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER})

    add_heading_2(doc, "2.6 Phân hệ Xác thực và phân quyền theo vai trò")
    add_body_p(doc,
        "Phân hệ xác thực (/login) chịu trách nhiệm nhận diện và phân quyền người dùng trong toàn bộ ứng dụng. "
        "Ngoài form nhập tài khoản và mật khẩu thông thường, hệ thống tích hợp 3 thẻ bấm thông minh cho phép chuyển đổi nhanh 3 vai trò demo: "
        "Nhân viên (emp_nam), Kỹ thuật viên (agent_hoa), Quản trị viên (admin_quang).")

    add_body_p(doc,
        "Luồng xử lý khi đăng nhập diễn ra như sau: Máy khách gửi yêu cầu POST đến endpoint /api/auth/login kèm thông tin đăng nhập. "
        "Backend kiểm tra tính chính xác của mật khẩu, lấy thông tin vai trò (Role) và trả về đối tượng User. Phía Frontend, thông tin này "
        "được lưu trữ vào localStorage và quản lý tập trung qua React Context (AuthContext). Mọi điều hướng trên giao diện (Router) "
        "đều được kiểm tra qua Protected Route nhằm đảm bảo người dùng chỉ truy cập được các chức năng được phân quyền.")

    add_heading_2(doc, "2.7 Phân hệ Quản lý yêu cầu hỗ trợ và luồng trạng thái")
    add_body_p(doc,
        "Đây là phân hệ cốt lõi của đề tài, mô hình hóa trọn vẹn vòng đời xử lý một sự cố kỹ thuật trong doanh nghiệp:")
    add_bullet_item(doc, "Giao diện tạo ticket mới (CreateTicketModal) trực quan hóa 4 mức độ ưu tiên cùng số giờ SLA tương ứng. Khi nhân viên bấm 'Tạo yêu cầu', Backend tự động sinh mã phiếu dạng 'HD-xxxx' và tự động tính toán hạn chót dueDate = createdAt + resolutionTimeHours.", "Tạo yêu cầu mới & Tính SLA tự động")
    add_bullet_item(doc, "Trang TicketList hỗ trợ 3 góc nhìn lọc nhanh tiện ích: 'Tất cả ticket' (xem toàn bộ sự cố), 'Của tôi' (chỉ hiển thị phiếu do mình tạo hoặc được giao xử lý kèm badge số đếm) và 'Chưa phân công' (danh sách phiếu mới đang chờ kỹ thuật viên tiếp nhận kèm badge số đếm). Bảng dữ liệu có chiều cao hàng chuẩn 44px, hỗ trợ tìm kiếm từ khóa và lọc trạng thái.", "Danh sách Ticket đa góc nhìn")
    add_bullet_item(doc, "Để mang lại trải nghiệm tối ưu theo phong cách phần mềm doanh nghiệp (ServiceNow / Jira), khi người dùng nhấp vào bất kỳ hàng nào trên bảng (hoặc ấn phím Enter), ngăn chi tiết TicketDetailDrawer sẽ trượt mở nhanh chóng từ cạnh phải (rộng tối đa 460px) có mask nền mờ và hỗ trợ phím Esc. Người dùng có thể xem toàn bộ tiến trình, gửi phản hồi bình luận và chuyển trạng thái nghiệp vụ (Tiếp nhận -> Đã giải quyết -> Đóng phiếu -> Mở lại) ngay trên ngăn trượt mà không làm mất bộ lọc bảng hiện tại.", "Ngăn trượt chi tiết (TicketDetailDrawer)")

    p_ui = doc.add_paragraph()
    p_ui.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ui = p_ui.add_run("[GIAO DIỆN BẢNG DANH SÁCH TICKET VÀ NGĂN TRƯỢT TICKETDETAILDRAWER]")
    r_ui.font.bold = True
    r_ui.font.color.rgb = RGBColor(0, 51, 102)
    add_figure_caption(doc, "Hình 2.4: Giao diện Danh sách yêu cầu đa góc nhìn và Drawer trượt tương tác")

    add_heading_2(doc, "2.8 Phân hệ Quản trị hệ thống")
    add_body_p(doc, "Phân hệ quản trị cung cấp các công cụ cấu hình nghiệp vụ chuyên sâu cho ban quản lý:")
    add_bullet_item(doc, "Trang Danh mục dịch vụ (/categories) cho phép xem danh sách các nhóm sự cố (Phần mềm, Phần cứng, Mạng, Email & Cloud), tìm kiếm nhanh và tích hợp Modal thêm danh mục dịch vụ mới kết nối API Backend (POST /api/categories).", "Quản lý danh mục dịch vụ")
    add_bullet_item(doc, "Trang Quản trị người dùng (/users) dành riêng cho vai trò ADMIN. Đặc biệt, trên thanh Navbar, dòng menu 'Người dùng & phòng ban' được lập trình ẩn/hiện có điều kiện: chỉ những tài khoản có vai trò ADMIN mới nhìn thấy và truy cập được menu này. Hỗ trợ tìm kiếm nhân sự, lọc vai trò, cấp tài khoản mới (mật khẩu mặc định 123456) và xóa tài khoản an toàn.", "Quản trị người dùng & Phân quyền bảo mật")
    add_bullet_item(doc, "Trang Chính sách SLA (/sla-policies) công khai ma trận thời gian cam kết dịch vụ (Bảng 2.5). Tiến trình SlaScheduler chạy ngầm định kỳ mỗi phút tự động kiểm tra và đánh cờ isOverdue = true cho các phiếu quá hạn dueDate.", "Chính sách SLA & Tác vụ quét ngầm tự động")

    add_table_caption(doc, "Bảng 2.5: Ma trận thời gian cam kết dịch vụ (SLA Policy Matrix)")
    tb25_data = [
        ("CRITICAL", "Khẩn cấp", "<= 15 phút", "2 giờ", "Sập mạng toàn công ty, hỏng máy chủ trung tâm; tự động gửi cảnh báo tới Trưởng phòng CNTT"),
        ("HIGH", "Cao", "<= 30 phút", "8 giờ", "Hỏng máy tính làm việc của nhân sự, máy in chứng từ cuối tháng; điều chuyển kỹ thuật viên cấp cao nếu quá 4h"),
        ("MEDIUM", "Trung bình", "<= 2 giờ", "24 giờ", "Lỗi phần mềm kế toán, chậm hiệu năng; nhắc nhở kỹ thuật viên khi đạt 80% thời hạn SLA"),
        ("LOW", "Thấp", "<= 4 giờ", "48 giờ", "Yêu cầu cấp tài khoản mới, thắc mắc sử dụng thông thường; xử lý theo thứ tự FIFO trong giờ hành chính")
    ]
    create_table_custom(doc, 5, 5, [Inches(1.1), Inches(1.1), Inches(1.1), Inches(0.9), Inches(2.5)], ["Mức ưu tiên", "Tên cấp độ", "Thời gian phản hồi", "Thời gian giải quyết", "Phạm vi ảnh hưởng và Quy tắc leo thang"], tb25_data, {0: WD_ALIGN_PARAGRAPH.CENTER, 1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER})

    add_heading_2(doc, "2.9 Phân hệ Bảng điều khiển KPI, Báo cáo và Thiết kế giao diện")
    add_body_p(doc,
        "Hệ thống cung cấp góc nhìn số liệu toàn diện phục vụ công tác giám sát và ra quyết định quản trị:")
    add_bullet_item(doc, "Màn hình Dashboard (/dashboard) hiển thị 4 thẻ đo lường KPI cốt lõi (Tổng số ticket, Chờ tiếp nhận, Đang xử lý, Quá hạn SLA), kết hợp biểu đồ cột đôi Recharts so sánh số lượng mới / đã giải quyết và thanh đo tỷ lệ tuân thủ SLA tự động đổi màu vàng/đỏ khi rơi xuống dưới ngưỡng cảnh báo.", "Bảng điều khiển tác nghiệp (Dashboard)")
    add_bullet_item(doc, "Màn hình Báo cáo (/reports) đo lường các chỉ số chất lượng chuyên sâu: Tỷ lệ đạt chuẩn SLA (%), Thời gian phản hồi trung bình (MTTA), Thời gian khắc phục trung bình (MTTR), biểu đồ cột phân bổ sự cố theo danh mục dịch vụ và phân bổ theo từng phòng ban.", "Báo cáo phân tích hiệu năng (Reports)")
    add_bullet_item(doc, "Toàn bộ giao diện được thiết kế theo chuẩn Enterprise 2D Design System: Sử dụng font chữ duy nhất IBM Plex Sans hỗ trợ tiếng Việt; hệ thống Design Tokens CSS phẳng (tokens.css) không dùng gradient hay bóng đổ nặng; chỉ dùng 1 màu nhấn chủ đạo (--brand #0b6bcb / #4c9dff); hỗ trợ chuyển đổi linh hoạt chế độ Sáng / Tối (Light / Dark mode).", "Hệ thống thiết kế chuẩn doanh nghiệp 2D")

    p_dash = doc.add_paragraph()
    p_dash.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dash = p_dash.add_run("[GIAO DIỆN BẢNG ĐIỀU KHIỂN KPI VÀ BÁO CÁO PHÂN TÍCH HIỆU NĂNG]")
    r_dash.font.bold = True
    r_dash.font.color.rgb = RGBColor(0, 51, 102)
    add_figure_caption(doc, "Hình 2.5: Giao diện Bảng điều khiển KPI và Báo cáo phân tích hiệu năng")

    add_heading_2(doc, "2.10 Kiểm thử chức năng và đánh giá kết quả")
    add_body_p(doc,
        "Em đã tiến hành kiểm thử toàn diện các ca kiểm thử chức năng (Functional Test Cases) trên hệ thống. "
        "Bảng 2.6 tổng hợp 12 ca kiểm thử tiêu biểu đại diện cho các luồng nghiệp vụ chính:")

    add_table_caption(doc, "Bảng 2.6: Tổng hợp các ca kiểm thử chức năng thực tế (Test Cases)")
    tb26_data = [
        ("TC01", "Đăng nhập hợp lệ bằng tài khoản Demo", "Chọn thẻ 'Nhân viên (emp_nam)', mật khẩu '123456'", "Đăng nhập thành công, lưu thông tin vào localStorage và chuyển đến trang /tickets", "Đúng mong đợi", "Đạt"),
        ("TC02", "Đăng nhập sai mật khẩu", "Username 'emp_nam', password 'sai_pass'", "Hiển thị thông báo lỗi màu đỏ 'Tên đăng nhập hoặc mật khẩu không chính xác'", "Đúng mong đợi", "Đạt"),
        ("TC03", "Tạo ticket với mức ưu tiên CRITICAL", "Tiêu đề 'Sập mạng', danh mục 'Mạng', mức 'CRITICAL'", "Tạo ticket thành công, sinh mã HD-xxxx, hạn dueDate đúng bằng thời điểm tạo + 2 giờ", "Đúng mong đợi", "Đạt"),
        ("TC04", "Tạo ticket để trống tiêu đề", "Tiêu đề rỗng '', chọn danh mục 'Phần mềm'", "Hiển thị cảnh báo lỗi 'Vui lòng nhập tiêu đề sự cố', không gửi request lên máy chủ", "Đúng mong đợi", "Đạt"),
        ("TC05", "Lọc ticket góc nhìn 'Của tôi'", "Người dùng emp_nam bấm chọn menu 'Của tôi'", "Bảng dữ liệu chỉ hiển thị các ticket có requesterId = id của emp_nam", "Đúng mong đợi", "Đạt"),
        ("TC06", "Mở ngăn trượt TicketDetailDrawer", "Nhấp chuột vào một hàng trên bảng hoặc ấn Enter", "Drawer trượt mượt mà từ cạnh phải, hiển thị đầy đủ thông tin sự cố và timeline phản hồi", "Đúng mong đợi", "Đạt"),
        ("TC07", "Kỹ thuật viên tiếp nhận xử lý sự cố", "Tài khoản agent_hoa bấm nút 'Tiếp nhận xử lý'", "Trạng thái chuyển sang IN_PROGRESS, gán assignee là agent_hoa, Drawer cập nhật tức thì", "Đúng mong đợi", "Đạt"),
        ("TC08", "Gửi phản hồi bình luận trên Drawer", "Nhập 'Đã thay thế linh kiện mới' và bấm gửi", "Bình luận mới xuất hiện ngay lập tức trong timeline lịch sử trao đổi", "Đúng mong đợi", "Đạt"),
        ("TC09", "Kiểm tra ẩn hiện menu Quản trị", "Đăng nhập tài khoản emp_nam (Employee)", "Navbar KHÔNG hiển thị dòng menu 'Người dùng & phòng ban'", "Đúng mong đợi", "Đạt"),
        ("TC10", "Tạo tài khoản người dùng mới (Admin)", "Tài khoản admin_quang tạo user mới 'emp_lan'", "Tạo thành công, tài khoản mới xuất hiện trong bảng người dùng và có thể đăng nhập được", "Đúng mong đợi", "Đạt"),
        ("TC11", "Tạo tài khoản bị trùng username", "Nhập username 'emp_nam' đã tồn tại", "Hệ thống bắt lỗi trùng lặp và hiển thị thông báo 'Tên đăng nhập đã tồn tại'", "Đúng mong đợi", "Đạt"),
        ("TC12", "Chuyển đổi giao diện Sáng / Tối", "Nhấp vào icon Sun/Moon trên thanh Topbar", "Giao diện chuyển đổi tức thì giữa Theme Sáng và Tối, lưu cấu hình vào localStorage", "Đúng mong đợi", "Đạt")
    ]
    create_table_custom(doc, 13, 6, [Inches(0.6), Inches(1.8), Inches(1.8), Inches(1.7), Inches(0.8), Inches(0.5)], ["Mã TC", "Tên ca kiểm thử", "Dữ liệu đầu vào", "Kết quả mong đợi", "Kết quả thực tế", "Đánh giá"], tb26_data, {0: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER, 5: WD_ALIGN_PARAGRAPH.CENTER})

    add_body_p(doc,
        "Đánh giá và giới hạn kết quả kiểm thử: Toàn bộ 12 ca kiểm thử đều đạt kết quả mong đợi (tỷ lệ thành công 100%). "
        "Tuy nhiên, em xin nêu rõ điều kiện đo lường: kết quả trên được kiểm thử trên môi trường máy đơn (local, chip Intel Core i7, RAM 16GB, trình duyệt Google Chrome 120), "
        "thời gian phản hồi trung bình của các API dao động từ 15ms đến 45ms. Kết quả này chưa đủ để kết luận về khả năng chịu tải của hệ thống khi có hàng nghìn người dùng đồng thời trên môi trường Internet thực tế.")

    # ==================== CHƯƠNG 3 ====================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 3: ĐÁNH GIÁ KẾT QUẢ VÀ ĐỊNH HƯỚNG PHÁT TRIỂN")

    add_heading_2(doc, "3.1 Tự đánh giá kết quả quá trình thực tập")
    add_body_p(doc,
        "Sau 10 tuần thực tập tại Công ty TNHH JITS INOVATION LABS, em xin tự đánh giá kết quả bản thân đạt được dựa trên các bằng chứng cụ thể sau:")
    add_bullet_item(doc, "Từ mức độ ban đầu chỉ mới nắm kiến thức cơ bản nhập môn Java Spring, em đã tự tay xây dựng được một hệ thống phần mềm hoàn chỉnh gồm 5 bảng CSDL, 18 API RESTful chuẩn mực và 6 màn hình giao diện ReactJS hoạt động đồng bộ.", "Về mặt chuyên môn kỹ thuật")
    add_bullet_item(doc, "Làm quen và thích nghi tốt với văn hóa kỷ luật doanh nghiệp; biết cách phân rã yêu cầu bài toán từ Mentor; thực hành thành thạo kỹ năng quản lý mã nguồn Git; rèn luyện khả năng chủ động báo cáo tiến độ và tiếp thu ý kiến góp ý chuyên môn.", "Về mặt kỹ năng làm việc & kỹ năng mềm")
    add_bullet_item(doc, "Dù hiện đang đi làm trong một lĩnh vực khác, nhưng với tinh thần tự học nghiêm túc và sự hướng dẫn sát sao từ anh Đào Văn Tâm, em đã hoàn thành 100% khối lượng công việc được giao đúng hạn, chứng minh khả năng tự thích ứng và hoàn thành tốt nhiệm vụ.", "Khả năng đáp ứng công việc thực tế")

    add_heading_2(doc, "3.2 Đánh giá mức độ áp dụng kiến thức đào tạo tại HUMG")
    add_body_p(doc,
        "Quá trình thực hiện đề tài đã giúp em hệ thống hóa và vận dụng trực tiếp các kiến thức nền tảng đã được đào tạo tại "
        "Khoa Công nghệ thông tin – Trường Đại học Mỏ - Địa chất. Bảng 3.1 tổng hợp mối liên hệ giữa các môn học và cách em đã vận dụng:")

    add_table_caption(doc, "Bảng 3.1: Mối liên hệ giữa các học phần tại HUMG và cách vận dụng vào đề tài")
    tb31_data = [
        ("Lập trình Hướng đối tượng (Java)", "Vận dụng các nguyên lý đóng gói, kế thừa, đa hình để xây dựng các Entity, DTO, Service và xử lý ngoại lệ trong Spring Boot"),
        ("Cơ sở dữ liệu & Hệ quản trị CSDL", "Vận dụng kiến thức thiết kế bảng, khóa chính, khóa ngoại, chuẩn hóa dữ liệu 3NF và câu lệnh truy vấn dữ liệu vào CSDL H2"),
        ("Phân tích thiết kế hệ thống thông tin", "Áp dụng phương pháp phân tích yêu cầu, xây dựng sơ đồ ca sử dụng (Use Case) và sơ đồ thực thể quan hệ (ERD) cho bài toán IT Helpdesk"),
        ("Công nghệ Web & Phát triển ứng dụng Web", "Áp dụng kiến thức về giao thức HTTP (GET, POST, PUT, DELETE), mã trạng thái, cấu trúc dữ liệu JSON để kết nối giữa Frontend và Backend"),
        ("Kỹ thuật phần mềm & Quản lý dự án CNTT", "Vận dụng quy trình phát triển phần mềm Agile/Scrum, quản lý phiên bản với Git/GitLab và kỹ thuật thiết kế ca kiểm thử phần mềm")
    ]
    create_table_custom(doc, 6, 2, [Inches(2.5), Inches(4.2)], ["Học phần đào tạo tại HUMG", "Cách thức vận dụng thực tế vào xây dựng đề tài"], tb31_data)

    add_heading_2(doc, "3.3 Khó khăn thực tế và kinh nghiệm rút ra")
    add_body_p(doc,
        "Trong quá trình xây dựng hệ thống, em đã gặp phải một số thách thức kỹ thuật phức tạp. Áp dụng phương pháp giải quyết vấn đề 4 bước "
        "(Hiện tượng → Nguyên nhân kiểm tra → Cách xử lý → Bài học rút ra), em đã xử lý thành công các bài toán được tổng kết trong Bảng 3.2:")

    add_table_caption(doc, "Bảng 3.2: Tổng kết khó khăn kỹ thuật theo quy trình 4 bước")
    tb32_data = [
        ("Lỗi lặp đệ quy vô tận JSON (Infinite Recursion)", "Khi gọi API lấy danh sách Ticket, máy chủ báo lỗi StackOverflowError hoặc JSON lặp vô tận giữa Ticket và User", "Do quan hệ hai chiều JPA (@ManyToOne và @OneToMany) dẫn đến việc Jackson ObjectMapper tuần tự hóa tuần hoàn", "Thêm chú thích @JsonIgnoreProperties({\"hibernateLazyInitializer\", \"handler\"}) vào các Entity liên quan", "Cần hiểu sâu về cơ chế serialize JSON của Spring Boot khi ánh xạ quan hệ bảng CSDL"),
        ("Lỗi chặn chia sẻ tài nguyên (CORS Policy)", "Frontend tại cổng 5173 gọi API Backend tại cổng 8080 bị trình duyệt chặn với thông báo CORS header missing", "Cơ chế bảo mật Same-Origin Policy của trình duyệt chặn các request khác domain/port khi máy chủ chưa cho phép", "Tạo class WebConfig thực thi WebMvcConfigurer, cấu hình mở CORS toàn cục cho endpoint /api/** với origin 5173", "Luôn cấu hình chính sách CORS ngay từ giai đoạn đầu tích hợp kiến trúc Client-Server"),
        ("Lỗi mất ngữ cảnh bộ lọc khi xem chi tiết ticket", "Mỗi khi xem chi tiết một sự cố, người dùng phải chuyển sang trang mới, khi quay lại bị mất toàn bộ bộ lọc và từ khóa", "Thiết kế điều hướng truyền thống theo trang (Page Navigation) làm gián đoạn luồng công việc của kỹ thuật viên", "Tái cấu trúc giao diện sang dạng Slide-over Drawer (TicketDetailDrawer) trượt từ cạnh phải, thao tác trực tiếp trên ngăn trượt", "Trải nghiệm người dùng (UX) trong phần mềm doanh nghiệp ưu tiên giảm thiểu số lần chuyển trang không cần thiết")
    ]
    create_table_custom(doc, 4, 5, [Inches(1.2), Inches(1.3), Inches(1.4), Inches(1.4), Inches(1.4)], ["Vấn đề kỹ thuật", "1. Hiện tượng gặp phải", "2. Nguyên nhân kiểm tra", "3. Cách thức xử lý", "4. Bài học kinh nghiệm rút ra"], tb32_data)

    add_heading_2(doc, "3.4 Định hướng phát triển đề tài cho Đồ án tốt nghiệp")
    add_body_p(doc,
        "Xuất phát từ những giới hạn hiện tại của sản phẩm, để nâng cấp hệ thống thành một Đồ án tốt nghiệp đại học chuyên sâu và có tính ứng dụng thực tế cao hơn, "
        "em định hướng mở rộng đề tài theo các nội dung sau:")
    add_bullet_item(doc, "Thay thế cơ chế demo hiện tại bằng hệ thống bảo mật hoàn chỉnh: mã hóa mật khẩu bằng BCrypt, cấp phát và xác thực Token JWT trên mỗi Request, thiết lập phân quyền chi tiết trên từng Method (@PreAuthorize).", "Tích hợp Spring Security & JSON Web Token (JWT)")
    add_bullet_item(doc, "Tích hợp Spring WebSocket (STOMP) để đẩy thông báo thời gian thực khi có ticket mới tạo hoặc có bình luận mới; kết hợp dịch vụ JavaMailSender tự động gửi email cảnh báo khi ticket sắp quá hạn SLA.", "Hệ thống thông báo thời gian thực (WebSocket & Email)")
    add_bullet_item(doc, "Viết tệp Dockerfile và docker-compose.yml đóng gói Backend, Frontend và CSDL PostgreSQL để dễ dàng triển khai tự động lên các nền tảng đám mây (AWS / DigitalOcean / Google Cloud).", "Đóng gói Containerization bằng Docker")
    add_bullet_item(doc, "Nghiên cứu tích hợp các mô hình học máy (Machine Learning) hoặc mô hình ngôn ngữ lớn (LLM) để tự động đọc nội dung mô tả lỗi của nhân viên và gợi ý phân loại danh mục, mức độ ưu tiên chính xác.", "Ứng dụng Trí tuệ nhân tạo (AI) phân loại sự cố tự động")

    # ==================== KẾT LUẬN ====================
    doc.add_page_break()
    add_heading_1(doc, "KẾT LUẬN")

    add_body_p(doc,
        "Kỳ thực tập doanh nghiệp tại Công ty TNHH JITS INOVATION LABS là một cột mốc ý nghĩa và vô cùng quý giá trong quá trình học tập của em. "
        "Trải qua 10 tuần nghiêm túc học hỏi và làm việc, em đã hoàn thành toàn diện đề tài: \"Xây dựng Hệ thống Quản lý Yêu cầu Hỗ trợ Nội bộ "
        "(IT Helpdesk Ticketing System) theo kiến trúc Spring Boot và ReactJS\", đáp ứng trọn vẹn các yêu cầu kỹ thuật do Mentor tại công ty và Giảng viên hướng dẫn đề ra.")

    add_body_p(doc,
        "Các kết quả cụ thể mà em đã đạt được bao gồm:\n"
        "1. Xây dựng thành công máy chủ Backend độc lập với Java 17, Spring Boot 3 và Spring Data JPA, cung cấp 18 API RESTful chuẩn mực xử lý toàn diện vòng đời phiếu yêu cầu.\n"
        "2. Xây dựng ứng dụng Frontend Single Page Application hiện đại với ReactJS và Vite; chuẩn hóa giao diện theo Hệ thống thiết kế doanh nghiệp 2D (IBM Plex Sans, CSS Tokens, Light/Dark mode); tích hợp ngăn trượt TicketDetailDrawer mang lại trải nghiệm tối ưu.\n"
        "3. Tự động hóa hoàn toàn cơ chế tính hạn cam kết dịch vụ SLA và triển khai tiến trình quét ngầm định kỳ kiểm soát quá hạn.\n"
        "4. Xây dựng đầy đủ các phân hệ quản trị danh mục dịch vụ, quản trị người dùng (bảo vệ quyền Admin), bảng điều khiển KPI và báo cáo phân tích hiệu năng IT chuyên sâu.")

    add_body_p(doc,
        "Đề tài không chỉ giúp em củng cố sâu sắc các kiến thức lý thuyết đã học tại Trường Đại học Mỏ - Địa chất mà còn trang bị cho em "
        "tác phong làm việc chuyên nghiệp, kỹ năng tự nghiên cứu và giải quyết vấn đề thực tế. Đây sẽ là hành trang vững chắc để em tự tin bước vào "
        "giai đoạn làm Đồ án tốt nghiệp và sẵn sàng cho sự nghiệp phát triển phần mềm trong tương lai.")

    # ==================== TÀI LIỆU THAM KHẢO ====================
    doc.add_page_break()
    add_heading_1(doc, "TÀI LIỆU THAM KHẢO")

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.3
    p.add_run("Tài liệu Tiếng Việt:\n").bold = True
    p.add_run("[1] Đoàn Văn Ban (2018), Giáo trình Kỹ thuật phần mềm, Nhà xuất bản Giáo dục Việt Nam, Hà Nội.\n"
              "[2] Đặng Văn Đức (2015), Phân tích và thiết kế hệ thống hướng đối tượng với UML, NXB Khoa học và Kỹ thuật, Hà Nội.\n"
              "[3] Nguyễn Văn Ba (2019), Phát triển ứng dụng Web và kiến trúc RESTful API, NXB Đại học Quốc gia Hà Nội.\n\n")

    p.add_run("Tài liệu Tiếng Anh:\n").bold = True
    p.add_run("[4] Craig Walls (2022), Spring in Action, Sixth Edition, Manning Publications, New York.\n"
              "[5] Alex Banks and Eve Porcello (2020), Learning React: Modern Patterns for Developing React Apps, O'Reilly Media, Sebastopol.\n"
              "[6] Robert C. Martin (2017), Clean Architecture: A Craftsman's Guide to Software Structure and Design, Prentice Hall, Boston.\n\n")

    p.add_run("Tài liệu từ Internet:\n").bold = True
    p.add_run("[7] Spring Boot Official Documentation, https://spring.io/projects/spring-boot, truy cập ngày 15/10/2026.\n"
              "[8] React Official Documentation, https://react.dev, truy cập ngày 18/10/2026.\n"
              "[9] ITIL 4 Foundation: IT Service Management Best Practices, https://www.axelos.com/certifications/itil-service-management, truy cập ngày 20/10/2026.\n")

    # ==================== PHỤ LỤC ====================
    doc.add_page_break()
    add_heading_1(doc, "PHỤ LỤC: CẤU HÌNH VÀ THÀNH PHẦN MÃ NGUỒN")

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
        "  --bg: #f4f6f9;\n"
        "  --surface: #ffffff;\n"
        "  --line: #e2e7ee;\n"
        "  --text: #1b2433;\n"
        "  --muted: #64708a;\n"
        "  --nav: #0f1f3d;\n"
        "  --brand: #0b6bcb;\n"
        "  --ok: #1a7f4b;\n"
        "  --warn: #a15c00;\n"
        "  --err: #c0262d;\n"
        "}\n"
        "[data-theme=\"dark\"] {\n"
        "  --bg: #0d1320;\n"
        "  --surface: #151d2e;\n"
        "  --line: #26304a;\n"
        "  --text: #e6ebf5;\n"
        "  --muted: #8d9ab5;\n"
        "  --nav: #090f1d;\n"
        "  --brand: #4c9dff;\n"
        "  --ok: #4cc38a;\n"
        "  --warn: #f0b04a;\n"
        "  --err: #ff7a80;\n"
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
        print(f"File {output_path} is currently locked by Word. Successfully saved to: {backup_path}")

if __name__ == "__main__":
    generate_report()
