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
    r.font.color.rgb = RGBColor(0, 0, 0)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
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
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
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
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p

def add_body_p(doc, text, bold_prefix="", indent=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.3
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.3)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(13)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    return p

def add_bullet_item(doc, text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.left_indent = Inches(0.25)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_bullet = p.add_run("- ")
    r_bullet.font.name = 'Times New Roman'
    r_bullet.font.size = Pt(13)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + ": ")
        r_pre.bold = True
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(13)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    return p

def add_table_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(12)
    r.font.name = 'Times New Roman'
    return p

def add_figure_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(12)
    r.font.name = 'Times New Roman'
    return p

def add_figure_box(doc, placeholder_text, caption_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f"[{placeholder_text}]")
    r.font.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(100, 110, 130)
    add_figure_caption(doc, caption_text)

def create_table_custom(doc, rows, cols, col_widths, headers, data, align_cols=None):
    table = doc.add_table(rows=rows, cols=cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, width in enumerate(col_widths):
        table.columns[idx].width = width

    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h_text
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, 60, 60, 80, 80)
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
            set_cell_margins(cell, 50, 50, 70, 70)
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

def build_signlite_style_report():
    print("Building report strictly matching the student's SignLite model...")
    doc = docx.Document()

    # Căn lề chuẩn: Top 2.5cm, Bottom 2.5cm, Left 3.5cm, Right 2.5cm
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
    style.paragraph_format.line_spacing = 1.3

    # ==================== TRANG BÌA 1 ====================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\n")
    r.bold = True
    r.font.size = Pt(13)
    r2 = p.add_run("TRƯỜNG ĐẠI HỌC MỎ - ĐỊA CHẤT\n\n")
    r2.bold = True
    r2.font.size = Pt(14)

    for _ in range(3): doc.add_paragraph()

    p_sv = doc.add_paragraph()
    p_sv.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_name = p_sv.add_run("[HỌ VÀ TÊN BẠN]\n")
    r_name.bold = True
    r_name.font.size = Pt(14)
    r_id = p_sv.add_run("[MÃ SINH VIÊN CỦA BẠN]\n\n")
    r_id.bold = True
    r_id.font.size = Pt(14)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.line_spacing = 1.2
    p_title.add_run("BÁO CÁO\nTHỰC TẬP DOANH NGHIỆP\n\n").bold = True
    p_title.runs[0].font.size = Pt(16)
    
    p_nganh = doc.add_paragraph()
    p_nganh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_nganh.add_run("NGÀNH CÔNG NGHỆ THÔNG TIN\nCHUYÊN NGÀNH CÔNG NGHỆ PHẦN MỀM\n\n").bold = True
    p_nganh.runs[0].font.size = Pt(13)

    p_dt = doc.add_paragraph()
    p_dt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dt.paragraph_format.line_spacing = 1.2
    r_dt = p_dt.add_run("PHÂN TÍCH, THIẾT KẾ VÀ XÂY DỰNG\nHỆ THỐNG QUẢN LÝ YÊU CẦU HỖ TRỢ NỘI BỘ\nIT HELPDESK TICKETING SYSTEM\n\nỨng dụng HelpdeskIT\n")
    r_dt.bold = True
    r_dt.font.size = Pt(15)

    for _ in range(5): doc.add_paragraph()

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_date.add_run("HÀ NỘI 11/2026")
    r_d.bold = True
    r_d.font.size = Pt(13)

    # ==================== TRANG BÌA 2 ====================
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\n")
    r.bold = True
    r.font.size = Pt(13)
    r2 = p.add_run("TRƯỜNG ĐẠI HỌC MỎ - ĐỊA CHẤT\n\n")
    r2.bold = True
    r2.font.size = Pt(14)

    for _ in range(2): doc.add_paragraph()

    p_title2 = doc.add_paragraph()
    p_title2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title2.paragraph_format.line_spacing = 1.2
    p_title2.add_run("BÁO CÁO\nTHỰC TẬP DOANH NGHIỆP\n\n").bold = True
    p_title2.runs[0].font.size = Pt(16)

    p_nganh2 = doc.add_paragraph()
    p_nganh2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_nganh2.add_run("NGÀNH CÔNG NGHỆ THÔNG TIN\nCHUYÊN NGÀNH CÔNG NGHỆ PHẦN MỀM\n\n").bold = True
    p_nganh2.runs[0].font.size = Pt(13)

    p_dt2 = doc.add_paragraph()
    p_dt2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dt2.paragraph_format.line_spacing = 1.2
    r_dt2 = p_dt2.add_run("PHÂN TÍCH, THIẾT KẾ VÀ XÂY DỰNG\nHỆ THỐNG QUẢN LÝ YÊU CẦU HỖ TRỢ NỘI BỘ\nIT HELPDESK TICKETING SYSTEM\n\nỨng dụng HelpdeskIT\n")
    r_dt2.bold = True
    r_dt2.font.size = Pt(15)

    for _ in range(3): doc.add_paragraph()

    p_info = doc.add_paragraph()
    p_info.paragraph_format.left_indent = Inches(1.2)
    p_info.paragraph_format.line_spacing = 1.3
    p_info.add_run("Sinh viên thực tập:\t[Họ và tên bạn]\n").bold = False
    p_info.add_run("Mã sinh viên:\t\t[Mã sinh viên của bạn]\n")
    p_info.add_run("Công ty thực tập:\tCông ty TNHH JITS INOVATION LABS\n")
    p_info.add_run("Người phụ trách:\tĐào Văn Tâm\n")
    p_info.add_run("Giảng viên hướng dẫn:\tThS. Nguyễn Thế Lộc\n")

    for _ in range(4): doc.add_paragraph()

    p_date2 = doc.add_paragraph()
    p_date2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d2 = p_date2.add_run("HÀ NỘI 11/2026")
    r_d2.bold = True
    r_d2.font.size = Pt(13)

    # ==================== ĐỀ CƯƠNG THỰC TẬP DOANH NGHIỆP ====================
    doc.add_page_break()
    p_dc = doc.add_paragraph()
    p_dc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dc.add_run("ĐỀ CƯƠNG THỰC TẬP DOANH NGHIỆP")
    r.bold = True
    r.font.size = Pt(14)
    p_dc.paragraph_format.space_after = Pt(10)

    # 1 Sinh viên thực tập
    p_s1 = doc.add_paragraph()
    p_s1.add_run("1 Sinh viên thực tập").bold = True
    p_s1.paragraph_format.space_after = Pt(3)

    tb_sv = [
        ("1", "[MÃ SINH VIÊN CỦA BẠN]", "[HỌ VÀ TÊN BẠN]", "DCCTPM65...", "[Số điện thoại của bạn]", "[Mã sinh viên]@student.humg.edu.vn")
    ]
    create_table_custom(doc, 2, 6, [Inches(0.4), Inches(1.2), Inches(1.5), Inches(1.0), Inches(1.1), Inches(1.8)], ["TT", "Mã sinh viên", "Họ và tên", "Lớp", "Điện thoại", "E-mail"], tb_sv, {0: WD_ALIGN_PARAGRAPH.CENTER, 1: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER})

    # 2 Giảng viên hướng dẫn
    p_s2 = doc.add_paragraph()
    p_s2.paragraph_format.space_before = Pt(8)
    p_s2.add_run("2 Giảng viên hướng dẫn").bold = True
    p_s2.paragraph_format.space_after = Pt(3)

    tb_gv = [
        ("1", "0801-02", "ThS. Nguyễn Thế Lộc", "Bộ môn CNPM", "0983330682", "nguyentheloc@humg.edu.vn")
    ]
    create_table_custom(doc, 2, 6, [Inches(0.4), Inches(1.2), Inches(1.5), Inches(1.0), Inches(1.1), Inches(1.8)], ["TT", "Mã cán bộ", "Họ và tên", "Đơn vị", "Điện thoại", "E-mail"], tb_gv, {0: WD_ALIGN_PARAGRAPH.CENTER, 1: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.CENTER})

    # 3 Thông tin công ty thực tập
    p_s3 = doc.add_paragraph()
    p_s3.paragraph_format.space_before = Pt(8)
    p_s3.add_run("3 Thông tin công ty thực tập").bold = True
    add_body_p(doc, "Công ty TNHH JITS INOVATION LABS. Địa điểm thực tập: Tầng 2, số 6, phố Phạm Tuấn Tài, phường Dịch Vọng Hậu, Quận Cầu Giấy, Hà Nội. Website: https://jitsinnovationlabs.com/. Bộ phận thực tập: R&D / IT. Hình thức trực tiếp, 08 giờ 30–17 giờ 30, từ thứ Hai đến thứ Sáu.")

    # 4 Người hướng dẫn thực tập tại công ty
    p_s4 = doc.add_paragraph()
    p_s4.paragraph_format.space_before = Pt(6)
    p_s4.add_run("4 Người hướng dẫn thực tập tại công ty").bold = True
    add_body_p(doc, "Đào Văn Tâm – Quản lý dự án.")

    # 5 Tên đề tài hoặc dự án thực tập
    p_s5 = doc.add_paragraph()
    p_s5.paragraph_format.space_before = Pt(6)
    p_s5.add_run("5 Tên đề tài hoặc dự án thực tập").bold = True
    add_body_p(doc, "Phân tích, thiết kế và xây dựng hệ thống quản lý yêu cầu hỗ trợ nội bộ. Tên ứng dụng: HelpdeskIT.")

    # 6 Các nhiệm vụ được giao thực hiện
    p_s6 = doc.add_paragraph()
    p_s6.paragraph_format.space_before = Pt(6)
    p_s6.add_run("6 Các nhiệm vụ được giao thực hiện").bold = True
    add_body_p(doc, "Khảo sát quy trình hỗ trợ kỹ thuật và vận hành CNTT nội bộ; tìm hiểu hạ tầng mạng LAN, kiểm tra kết nối thiết bị văn phòng, máy trạm và hỗ trợ xử lý sự cố. Tìm hiểu kiến trúc Client-Server RESTful API, Spring Boot 3 và ReactJS. Chủ động thực hiện đề tài cá nhân HelpdeskIT: phân tích yêu cầu, thiết kế cơ sở dữ liệu, xây dựng các chức năng phân quyền, tạo ticket tự động tính SLA, hàng đợi đa góc nhìn, ngăn trượt chi tiết, bảng điều khiển KPI và kiểm thử.")

    # 7 Kế hoạch thực hiện
    p_s7 = doc.add_paragraph()
    p_s7.paragraph_format.space_before = Pt(6)
    p_s7.add_run("7 Kế hoạch thực hiện").bold = True
    add_body_p(doc, "Thời gian thực tập: 25/08/2026–03/11/2026. Kế hoạch dưới đây khái quát nội dung theo tuần; lịch làm việc và mức độ thực hiện được trình bày tại mục 1.4. Tuần cuối đang tiếp tục tổng hợp kết quả và hoàn thiện báo cáo.")

    tb_kh = [
        ("1", "Tìm hiểu doanh nghiệp, sản phẩm, quy trình làm việc và cài đặt môi trường phát triển."),
        ("2", "Khảo sát quy trình IT Helpdesk nội bộ; phân tích yêu cầu bài toán và xây dựng Use Case."),
        ("3", "Khảo sát mạng văn phòng; thiết kế cơ sở dữ liệu và khởi tạo Spring Boot 3."),
        ("4", "Hỗ trợ xử lý sự cố thiết bị; xây dựng Entity JPA, Repository và Service tính hạn SLA."),
        ("5", "Tìm hiểu chuẩn RESTful API; xây dựng các API cho Ticket, Category, SlaPolicy và mở CORS."),
        ("6", "Xây dựng front-end ReactJS (Vite); thiết lập Enterprise 2D Design System và tokens CSS."),
        ("7", "Xây dựng trang Login phân quyền 3 vai trò, danh sách Ticket và ngăn trượt TicketDetailDrawer."),
        ("8", "Xây dựng Modal tạo Ticket, phân hệ quản trị danh mục, người dùng và chính sách SLA."),
        ("9", "Triển khai SlaScheduler quét ngầm quá hạn; phát triển Dashboard KPI và Báo cáo hiệu năng."),
        ("10", "Kiểm thử tích hợp, tối ưu giao diện, tổng hợp kết quả và hoàn thiện báo cáo.")
    ]
    create_table_custom(doc, 11, 2, [Inches(0.8), Inches(6.2)], ["Tuần", "Nội dung công việc"], tb_kh, {0: WD_ALIGN_PARAGRAPH.CENTER})

    # ==================== MỤC LỤC ====================
    doc.add_page_break()
    p_ml = doc.add_paragraph()
    p_ml.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_ml.add_run("MỤC LỤC")
    r.bold = True
    r.font.size = Pt(14)
    p_ml.paragraph_format.space_after = Pt(8)

    toc_items = [
        ("ĐỀ CƯƠNG THỰC TẬP DOANH NGHIỆP", "1"),
        ("1 Sinh viên thực tập", "1"),
        ("2 Giảng viên hướng dẫn", "1"),
        ("3 Thông tin công ty thực tập", "1"),
        ("4 Người hướng dẫn thực tập tại công ty", "1"),
        ("5 Tên đề tài hoặc dự án thực tập", "1"),
        ("6 Các nhiệm vụ được giao thực hiện", "1"),
        ("7 Kế hoạch thực hiện", "2"),
        ("LỜI CẢM ƠN", "4"),
        ("MỞ ĐẦU", "5"),
        ("CHƯƠNG 1 GIỚI THIỆU CÔNG TY VÀ VỊ TRÍ THỰC TẬP", "6"),
        ("1.1 Giới thiệu doanh nghiệp", "6"),
        ("1.2 Vị trí và cách tổ chức công việc", "7"),
        ("1.3 Đề tài thực tập HelpdeskIT", "8"),
        ("1.4 Lịch làm việc và tiến độ thực tập", "8"),
        ("CHƯƠNG 2 NỘI DUNG THỰC TẬP", "11"),
        ("2.1 Công việc thực tế tại doanh nghiệp", "11"),
        ("2.2 Phân tích yêu cầu HelpdeskIT", "14"),
        ("2.3 Công nghệ và môi trường triển khai hiện tại", "16"),
        ("2.4 Kiến trúc và tổ chức xử lý", "18"),
        ("2.5 Cơ sở dữ liệu và toàn vẹn nội dung", "20"),
        ("2.6 Xác thực người dùng và phân quyền theo vai trò", "22"),
        ("2.7 Quản lý yêu cầu hỗ trợ và luồng trạng thái", "24"),
        ("2.8 Quản trị danh mục, người dùng và chính sách SLA", "26"),
        ("2.9 Bảng điều khiển KPI, Báo cáo và Hệ thống thiết kế 2D", "28"),
        ("2.10 Kiểm thử và kết quả thực hiện", "30"),
        ("CHƯƠNG 3 ĐÁNH GIÁ KẾT QUẢ VÀ ĐỊNH HƯỚNG PHÁT TRIỂN", "33"),
        ("3.1 Đánh giá kết quả thực tập", "33"),
        ("3.2 Kiến thức và kỹ năng đạt được", "34"),
        ("3.3 Khó khăn thực tế và kinh nghiệm rút ra", "35"),
        ("3.4 Định hướng phát triển và đồ án tốt nghiệp", "36"),
        ("KẾT LUẬN", "38"),
        ("TÀI LIỆU THAM KHẢO", "39")
    ]
    for item, page in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.space_after = Pt(2)
        r_item = p_t.add_run(item)
        if item.startswith("CHƯƠNG") or item in ["ĐỀ CƯƠNG THỰC TẬP DOANH NGHIỆP", "MỞ ĐẦU", "KẾT LUẬN", "TÀI LIỆU THAM KHẢO", "LỜI CẢM ƠN"]:
            r_item.bold = True
        dots_len = max(4, 75 - len(item))
        p_t.add_run("\t" + page)
        # Using simple tabs for TOC
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.8), docx.enum.text.WD_TAB_ALIGNMENT.RIGHT, docx.enum.text.WD_TAB_LEADER.DOTS)

    # ==================== DANH MỤC HÌNH VẼ ====================
    doc.add_page_break()
    p_df = doc.add_paragraph()
    r = p_df.add_run("DANH MỤC HÌNH VẼ")
    r.bold = True
    r.font.size = Pt(14)
    p_df.paragraph_format.space_after = Pt(8)

    figs = [
        ("Hình 2.1 Giao diện kiểm tra trạng thái mạng và thiết bị văn phòng", "12"),
        ("Hình 2.2 Khảo sát tủ mạng và hạ tầng kết nối tại văn phòng công ty", "13"),
        ("Hình 2.3 Sơ đồ Use Case của các chức năng HelpdeskIT hiện tại", "15"),
        ("Hình 2.4 Kiến trúc HelpdeskIT trong môi trường local và LAN", "18"),
        ("Hình 2.5 Mô hình dữ liệu của hệ thống HelpdeskIT", "20"),
        ("Hình 2.6 Giao diện đăng nhập và chuyển nhanh vai trò demo", "23"),
        ("Hình 2.7 Giao diện Danh sách yêu cầu đa góc nhìn", "24"),
        ("Hình 2.8 Trình tự tạo ticket và tự động tính hạn chót SLA", "25"),
        ("Hình 2.9 Giao diện ngăn trượt chi tiết TicketDetailDrawer", "26"),
        ("Hình 2.10 Trình tự chuyển đổi trạng thái và gửi bình luận", "27"),
        ("Hình 2.11 Giao diện Quản trị người dùng có bảo vệ quyền Admin", "28"),
        ("Hình 2.12 Giao diện Bảng điều khiển KPI và Báo cáo hiệu năng", "29")
    ]
    for f_txt, page in figs:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.line_spacing = 1.15
        p_f.paragraph_format.space_after = Pt(2)
        p_f.add_run(f_txt)
        p_f.add_run("\t" + page)
        p_f.paragraph_format.tab_stops.add_tab_stop(Inches(6.8), docx.enum.text.WD_TAB_ALIGNMENT.RIGHT, docx.enum.text.WD_TAB_LEADER.DOTS)

    # ==================== DANH MỤC BẢNG BIỂU ====================
    p_db = doc.add_paragraph()
    p_db.paragraph_format.space_before = Pt(14)
    r = p_db.add_run("DANH MỤC BẢNG BIỂU")
    r.bold = True
    r.font.size = Pt(14)
    p_db.paragraph_format.space_after = Pt(8)

    tbls = [
        ("Bảng 1.1 Sản phẩm và phạm vi tìm hiểu tại JITS", "7"),
        ("Bảng 1.2 Lịch làm việc theo tuần", "9"),
        ("Bảng 2.1 Thiết bị đã tham gia cấu hình hoặc kiểm tra", "12"),
        ("Bảng 2.2 Yêu cầu chức năng đã hoàn thành trong phạm vi thực hành", "15"),
        ("Bảng 2.3 Công nghệ và vai trò trong HelpdeskIT", "16"),
        ("Bảng 2.4 Các bảng và ý nghĩa dữ liệu", "21"),
        ("Bảng 2.5 Ma trận thời gian cam kết dịch vụ SLA", "27"),
        ("Bảng 2.6 Tổng hợp kết quả kiểm thử HelpdeskIT", "31"),
        ("Bảng 3.1 Liên hệ học phần và công việc đã thực hiện", "34")
    ]
    for b_txt, page in tbls:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.line_spacing = 1.15
        p_b.paragraph_format.space_after = Pt(2)
        p_b.add_run(b_txt)
        p_b.add_run("\t" + page)
        p_b.paragraph_format.tab_stops.add_tab_stop(Inches(6.8), docx.enum.text.WD_TAB_ALIGNMENT.RIGHT, docx.enum.text.WD_TAB_LEADER.DOTS)

    # ==================== LỜI CẢM ƠN ====================
    doc.add_page_break()
    p_lc = doc.add_paragraph()
    r = p_lc.add_run("LỜI CẢM ƠN")
    r.bold = True
    r.font.size = Pt(14)
    p_lc.paragraph_format.space_after = Pt(8)

    add_body_p(doc, "Em xin trân trọng cảm ơn Ban Giám hiệu Trường Đại học Mỏ - Địa chất, Khoa Công nghệ thông tin và các thầy cô đã trang bị kiến thức nền tảng, tạo điều kiện để em tiếp cận công việc thực tế thông qua đợt thực tập doanh nghiệp.")
    add_body_p(doc, "Em xin gửi lời cảm ơn tới thầy giáo ThS. Nguyễn Thế Lộc, giảng viên hướng dẫn, đã đồng hành và định hướng cho em trong quá trình xây dựng nội dung báo cáo. Em trân trọng sự hỗ trợ của Công ty TNHH JITS INOVATION LABS và anh Đào Văn Tâm trong việc tạo điều kiện tìm hiểu môi trường làm việc và các nhiệm vụ chuyên môn tại doanh nghiệp.")
    add_body_p(doc, "Việc tiếp cận các công việc quản trị hạ tầng mạng, tiếp nhận sự cố kỹ thuật và đề tài IT Helpdesk là cơ hội để em liên hệ kiến thức được học với yêu cầu triển khai một hệ thống thông tin. Em mong nhận được ý kiến góp ý của thầy cô và doanh nghiệp để tiếp tục hoàn thiện kiến thức, kỹ năng cũng như đề tài HelpdeskIT.")
    add_body_p(doc, "Em xin chân thành cảm ơn!")

    # ==================== MỞ ĐẦU ====================
    doc.add_page_break()
    p_md = doc.add_paragraph()
    r = p_md.add_run("MỞ ĐẦU")
    r.bold = True
    r.font.size = Pt(14)
    p_md.paragraph_format.space_after = Pt(8)

    add_body_p(doc, "Nhu cầu tiếp nhận và xử lý sự cố công nghệ thông tin tại các phòng ban đặt ra bài toán quản lý yêu cầu một cách tập trung. Nếu mỗi thay đổi, báo lỗi đều thực hiện thủ công qua tin nhắn Zalo, gọi điện hoặc trao đổi miệng, việc vận hành sẽ dễ dẫn đến tình trạng bỏ sót yêu cầu, thiếu cam kết thời gian hoàn thành (SLA) và cấp quản trị không đo lường được hiệu suất của đội ngũ kỹ thuật. Hệ thống IT Helpdesk kết nối người dùng phát sinh sự cố với nhân viên kỹ thuật, cho phép phân loại theo danh mục dịch vụ, tính toán thời hạn xử lý tự động và theo dõi trạng thái giải quyết.")
    add_body_p(doc, "Trong thời gian thực tập tại Công ty TNHH JITS INOVATION LABS, em tham gia tìm hiểu quy trình hỗ trợ CNTT nội bộ, khảo sát hạ tầng mạng LAN, kiểm tra kết nối thiết bị và hỗ trợ xử lý sự cố kỹ thuật văn phòng. Qua việc tìm hiểu các hệ thống quản lý dịch vụ và công cụ hỗ trợ doanh nghiệp, em chủ động đề xuất đề tài “Phân tích, thiết kế và xây dựng hệ thống quản lý yêu cầu hỗ trợ nội bộ”, với tên ứng dụng HelpdeskIT.")
    add_body_p(doc, "HelpdeskIT là đề tài thực hành cá nhân phục vụ báo cáo thực tập, được nghiên cứu và bắt đầu lập trình từ cuối tháng 9/2026. Ứng dụng hiện hỗ trợ phân quyền 3 vai trò (Nhân viên, Kỹ thuật viên IT, Quản trị viên), quản lý danh mục dịch vụ, tạo ticket tự động tính hạn SLA, hàng đợi đa góc nhìn (Tất cả, Của tôi, Chưa phân công), ngăn trượt chi tiết TicketDetailDrawer tương tác nhanh, bảng điều khiển KPI và báo cáo hiệu năng. Dự án được phát triển độc lập từ việc nghiên cứu nghiệp vụ ITIL; ứng dụng di động, thông báo đẩy thời gian thực và triển khai đám mây qua Internet là hướng phát triển tiếp theo.")
    add_body_p(doc, "Báo cáo trình bày công việc tại doanh nghiệp và quá trình phát triển HelpdeskIT trong mối liên hệ giữa yêu cầu nghiệp vụ, hạ tầng và phần mềm. Phần kỹ thuật tập trung vào ứng dụng chạy trên Windows trong máy cục bộ và mạng nội bộ (local/LAN), sử dụng Java 17 và Spring Boot 3 làm máy chủ REST API, H2 lưu cơ sở dữ liệu bền vững, ReactJS và Tailwind CSS xây dựng giao diện người dùng theo Enterprise 2D Design System. Kết quả kiểm thử được đánh giá theo điều kiện thực hiện và phạm vi kịch bản đã thử.")
    add_body_p(doc, "Báo cáo gồm ba chương. Chương 1 giới thiệu doanh nghiệp, vị trí và lịch thực tập. Chương 2 trình bày nhiệm vụ thực tế, quá trình phân tích và xây dựng HelpdeskIT, các sơ đồ cùng kết quả kiểm thử. Chương 3 đánh giá kiến thức, kỹ năng và định hướng phát triển đề tài thành đồ án tốt nghiệp.")

    # ==================== CHƯƠNG 1 ====================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 1 GIỚI THIỆU CÔNG TY VÀ VỊ TRÍ THỰC TẬP")

    add_heading_2(doc, "1.1 Giới thiệu doanh nghiệp")
    add_heading_3(doc, "1.1.1 Thông tin chung và định hướng hoạt động")
    add_body_p(doc, "Công ty TNHH JITS INOVATION LABS, thành lập năm 2016, có trụ sở chính tại Hà Nội. Địa điểm em thực tập là Tầng 2, số 6, phố Phạm Tuấn Tài, phường Dịch Vọng Hậu, Quận Cầu Giấy, Hà Nội. Công ty hoạt động trong lĩnh vực công nghệ thông tin, chuyên cung cấp các giải pháp phần mềm tài chính ngân hàng, Core Banking, cổng thanh toán số và các ứng dụng chuyển đổi số doanh nghiệp.")
    add_body_p(doc, "JITS INOVATION LABS định hướng phát triển những sản phẩm công nghệ có khả năng đáp ứng nhu cầu vận hành thực tế và tính sẵn sàng cao. Sứ mệnh của doanh nghiệp là hỗ trợ khách hàng hoạt động hiệu quả hơn thông qua các hệ thống phần mềm tối ưu, an toàn và chuyên nghiệp. Các giá trị cốt lõi gồm đổi mới sáng tạo, cam kết chất lượng và làm việc nhóm hiệu quả. Bối cảnh này tạo điều kiện thuận lợi để sinh viên tiếp cận cả quy trình phát triển phần mềm chuẩn mực lẫn cách thức vận hành hạ tầng CNTT thực tế.")

    add_heading_3(doc, "1.1.2 Các sản phẩm và dịch vụ liên quan")
    add_table_caption(doc, "Bảng 1.1 Sản phẩm và phạm vi tìm hiểu tại JITS")
    tb11_data = [
        ("JITS Core Banking", "Hệ thống lõi ngân hàng và quản lý giao dịch tài chính.", "Tìm hiểu kiến trúc hệ thống lớn, yêu cầu bảo mật và tính toàn vẹn dữ liệu."),
        ("JITS Payment Gateway", "Cổng thanh toán điện tử và kết nối API thanh toán số.", "Tìm hiểu chuẩn thiết kế RESTful API, xác thực và kiểm soát lỗi đầu vào."),
        ("Hạ tầng IT & Dịch vụ nội bộ", "Hệ thống hỗ trợ kỹ thuật, mạng văn phòng và quản lý thiết bị.", "Tìm hiểu quy trình tiếp nhận sự cố nội bộ; hình thành ý tưởng đề tài HelpdeskIT."),
        ("Phần mềm quản trị điều hành", "Quản lý nhân sự, dự án, chấm công và tài liệu số.", "Tìm hiểu cách doanh nghiệp tập trung dữ liệu và phân quyền theo vai trò.")
    ]
    create_table_custom(doc, 5, 3, [Inches(1.8), Inches(2.5), Inches(2.7)], ["Sản phẩm", "Vai trò", "Liên hệ với thực tập"], tb11_data)
    add_body_p(doc, "Nhóm công việc em trực tiếp tham gia tập trung vào hạ tầng mạng văn phòng và khảo sát quy trình hỗ trợ kỹ thuật nội bộ. Với các giải pháp phần mềm tài chính và API, em tìm hiểu mô hình kiến trúc phân tầng và chuẩn giao tiếp dữ liệu. Những hiểu biết này giúp em có cái nhìn toàn diện hơn về vận hành công nghệ tại doanh nghiệp.")

    add_heading_2(doc, "1.2 Vị trí và cách tổ chức công việc")
    add_heading_3(doc, "1.2.1 Vị trí và thời gian thực tập")
    add_body_p(doc, "Em thực tập trực tiếp tại bộ phận R&D / IT dưới sự hướng dẫn của anh Đào Văn Tâm, Quản lý dự án. Thời gian thực tập từ ngày 25/08/2026 đến ngày 03/11/2026; lịch làm việc từ 08 giờ 30 đến 17 giờ 30, thứ Hai đến thứ Sáu hàng tuần.")
    add_body_p(doc, "Các nhiệm vụ gồm tìm hiểu quy trình vận hành CNTT, khảo sát mạng LAN văn phòng, kiểm tra kết nối thiết bị máy trạm, máy in, router và hỗ trợ xử lý sự cố kỹ thuật cho các phòng ban. Với các cấu hình mạng diện rộng hoặc thay đổi ảnh hưởng đến máy chủ dùng chung, em thực hiện dưới sự hướng dẫn của các anh chị kỹ thuật.")

    add_heading_3(doc, "1.2.2 Nhận việc và phối hợp trong nhóm")
    add_body_p(doc, "Công việc được người phụ trách giao qua trao đổi trực tiếp trong các buổi họp đầu ngày và kênh liên lạc nội bộ. Em báo cáo kết quả sau khi hoàn thành từng nhiệm vụ hoặc theo định kỳ hàng tuần. Quản lý và các anh chị kỹ thuật kiểm tra kết quả, góp ý và hướng dẫn khắc phục vấn đề phát sinh. Cách làm này giúp em hiểu rõ yêu cầu đầu ra và điều chỉnh công việc theo phản hồi thực tế.")
    add_body_p(doc, "Em phối hợp với nhóm kỹ thuật trong việc kiểm tra kết nối và xử lý lỗi phần mềm. Riêng với đề tài HelpdeskIT, em sử dụng Git để quản lý mã nguồn, tạo nhánh tính năng và commit thường xuyên trong quá trình phát triển.")

    add_heading_2(doc, "1.3 Đề tài thực tập HelpdeskIT")
    add_heading_3(doc, "1.3.1 Mục tiêu và phạm vi hiện tại")
    add_body_p(doc, "Đề tài “Phân tích, thiết kế và xây dựng hệ thống quản lý yêu cầu hỗ trợ nội bộ” hướng tới giải quyết bài toán tiếp nhận, phân loại và xử lý sự cố CNTT tập trung. HelpdeskIT cho phép nhân viên gửi yêu cầu hỗ trợ theo danh mục, hệ thống tự động xác định hạn hoàn thành theo cam kết SLA, kỹ thuật viên tiếp nhận xử lý và quản trị viên giám sát toàn diện qua Dashboard.")
    add_body_p(doc, "Các nhóm chức năng cốt lõi đã hoàn thành trong phạm vi thực hành gồm: xác thực và chuyển nhanh vai trò demo, quản lý danh mục dịch vụ, quản trị người dùng (có bảo vệ quyền Admin), tạo ticket tự động tính hạn SLA dueDate, danh sách ticket đa góc nhìn (Tất cả, Của tôi, Chưa phân công), ngăn trượt chi tiết TicketDetailDrawer, bình luận thảo luận, tác vụ quét ngầm SlaScheduler kiểm tra quá hạn, bảng điều khiển KPI và báo cáo hiệu năng. Ứng dụng di động, thông báo đẩy thời gian thực và triển khai đám mây qua Internet chưa thuộc kết quả hiện tại.")

    add_heading_3(doc, "1.3.2 Vai trò cá nhân và quan hệ với công việc doanh nghiệp")
    add_body_p(doc, "HelpdeskIT là dự án cá nhân do em chủ động đề xuất sau khi tìm hiểu thực tế quy trình hỗ trợ kỹ thuật tại công ty. Em trực tiếp nghiên cứu yêu cầu, thiết kế giao diện theo Enterprise 2D Design System, thiết kế cơ sở dữ liệu, xây dựng mã nguồn Backend và Frontend, và tiến hành kiểm thử. Yêu cầu được hình thành từ việc nghiên cứu quy trình vận hành ITIL và tiếp nhận góp ý của người hướng dẫn tại doanh nghiệp, giảng viên hướng dẫn.")
    add_body_p(doc, "Đề tài phục vụ học tập và báo cáo thực tập, có định hướng tiếp tục phát triển thành đồ án tốt nghiệp. Việc tiếp xúc với môi trường doanh nghiệp giúp em xác định bài toán nghiệp vụ; HelpdeskIT được xây dựng với mã nguồn và thiết kế riêng. Công việc tại doanh nghiệp và quá trình phát triển đề tài được trình bày lần lượt ở mục 2.1 và các mục tiếp theo của Chương 2.")

    add_heading_2(doc, "1.4 Lịch làm việc và tiến độ thực tập")
    add_body_p(doc, "Bảng 1.2 tổng hợp công việc và mức độ thực hiện theo 10 tuần thực tập. Tuần 10 kéo dài từ 27/10 đến 03/11/2026 và đang tiếp tục kiểm thử, tổng hợp kết quả, hoàn thiện báo cáo. Các hoạt động phát triển HelpdeskIT được thực hiện song song với nhiệm vụ tại doanh nghiệp.")
    add_body_p(doc, "HelpdeskIT bắt đầu được nghiên cứu từ tháng 9/2026, với việc phân tích yêu cầu và thiết kế CSDL. Đầu tháng 10, em tập trung vào kiến trúc Spring Boot 3 và các REST API cơ bản; giữa tháng 10 phát triển giao diện ReactJS, ngăn trượt chi tiết và phân hệ quản trị; cuối tháng 10 hoàn thiện tính hạn SLA, tác vụ quét ngầm, báo cáo hiệu năng và kiểm thử tích hợp.")

    add_table_caption(doc, "Bảng 1.2 Lịch làm việc theo tuần")
    tb12_data = [
        ("1", "Tìm hiểu cơ cấu công ty, sản phẩm, quy trình làm việc; cài đặt môi trường.", "Đào Văn Tâm", "Đã thực hiện", "Nắm sản phẩm, quy trình."),
        ("2", "Tìm hiểu quy trình IT Helpdesk nội bộ; phân tích yêu cầu bài toán, vẽ Use Case.", "Đào Văn Tâm", "Đã thực hiện", "Xác định rõ các tác nhân."),
        ("3", "Khảo sát mạng văn phòng; thiết kế ERD, khởi tạo Spring Boot 3 và H2 database.", "Đào Văn Tâm", "Đã thực hiện", "Có cấu trúc CSDL bền vững."),
        ("4", "Hỗ trợ kiểm tra máy trạm; tạo Entity JPA, Repository, Service tính hạn SLA.", "Đào Văn Tâm", "Đã thực hiện", "Có logic nghiệp vụ SLA."),
        ("5", "Tìm hiểu chuẩn RESTful; xây dựng API Ticket, Category, SlaPolicy và mở CORS.", "Đào Văn Tâm", "Đã thực hiện", "API chạy tốt trên Postman."),
        ("6", "Khởi tạo Frontend ReactJS Vite, Tailwind CSS; thiết lập Design System tokens.", "Đào Văn Tâm", "Đã thực hiện", "Có khung giao diện chuẩn."),
        ("7", "Xây dựng trang Login demo vai trò, danh sách ticket và TicketDetailDrawer.", "Đào Văn Tâm", "Đã thực hiện", "Thao tác trượt drawer tốt."),
        ("8", "Xây dựng Modal tạo ticket, quản trị danh mục, người dùng và chính sách SLA.", "Đào Văn Tâm", "Đã thực hiện", "Ẩn hiện navbar đúng role."),
        ("9", "Triển khai SlaScheduler quét ngầm; xây dựng Dashboard KPI và Báo cáo Recharts.", "Đào Văn Tâm", "Đã thực hiện", "Thống kê chỉ số trực quan."),
        ("10", "Kiểm thử tích hợp, tối ưu giao diện 2D, tổng hợp kết quả và hoàn thiện báo cáo.", "Đào Văn Tâm", "Đang thực hiện", "Đang tổng hợp kết quả.")
    ]
    create_table_custom(doc, 11, 5, [Inches(0.6), Inches(3.0), Inches(1.1), Inches(1.1), Inches(1.2)], ["Tuần", "Nội dung công việc", "Người hướng dẫn", "Mức độ hoàn thành", "Ghi chú"], tb12_data, {0: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER})

    # ==================== CHƯƠNG 2 ====================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 2 NỘI DUNG THỰC TẬP")

    add_heading_2(doc, "2.1 Công việc thực tế tại doanh nghiệp")
    add_body_p(doc, "Công việc thực tế tại doanh nghiệp giúp em hiểu rõ các sự cố kỹ thuật phát sinh hàng ngày trong môi trường văn phòng: lỗi kết nối mạng LAN/WiFi, kẹt lệnh in, lỗi cài đặt phần mềm kế toán, hỏng linh kiện máy tính hoặc tài khoản bị khóa. Việc tiếp cận này làm cơ sở thực tế cho các nhóm danh mục dịch vụ trong đề tài.")
    add_body_p(doc, "Em trực tiếp tham gia cùng các anh chị kỹ thuật khảo sát sơ đồ mạng văn phòng, kiểm tra kết nối giữa Router, Switch và Access Point, kiểm tra địa chỉ IP cấp phát qua DHCP và hỗ trợ xử lý sự cố thiết bị máy trạm của nhân viên. Các dòng thiết bị em đã tiếp cận được tổng hợp trong Bảng 2.1.")

    add_table_caption(doc, "Bảng 2.1 Thiết bị đã tham gia cấu hình hoặc kiểm tra")
    tb21_data = [
        ("Router & Gateway", "MikroTik RB4011, hEX; kiểm tra bảng định tuyến, cấp phát DHCP và NAT."),
        ("Switch mạng", "Cisco Catalyst 2960, Ruijie ES209GC; kiểm tra cổng kết nối và cấp nguồn PoE."),
        ("Access Point WiFi", "Aruba Instant On AP11, Ruijie RG-RAP2200; kiểm tra SSID và vùng phủ sóng."),
        ("Máy trạm & Thiết bị", "Máy tính để bàn Dell OptiPlex, máy in HP LaserJet; kiểm tra driver, cáp mạng và hệ điều hành.")
    ]
    create_table_custom(doc, 5, 2, [Inches(2.0), Inches(5.0)], ["Nhóm", "Hãng và nội dung kiểm tra"], tb21_data)

    add_figure_box(doc, "HÌNH ẢNH GIAO DIỆN KIỂM TRA TRẠNG THÁI MẠNG VÀ THIẾT BỊ VĂN PHÒNG", "Hình 2.1 Giao diện kiểm tra trạng thái mạng và thiết bị văn phòng")
    add_figure_box(doc, "HÌNH ẢNH KHẢO SÁT TỦ MẠNG VÀ HẠ TẦNG KẾT NỐI TẠI VĂN PHÒNG CÔNG TY", "Hình 2.2 Khảo sát tủ mạng và hạ tầng kết nối tại văn phòng công ty")

    add_heading_2(doc, "2.2 Phân tích yêu cầu HelpdeskIT")
    add_heading_3(doc, "2.2.1 Bài toán và tác nhân")
    add_body_p(doc, "Từ nhu cầu hỗ trợ kỹ thuật đã tìm hiểu tại doanh nghiệp, em xác định HelpdeskIT cần hỗ trợ một luồng làm việc thống nhất: nhân viên tạo yêu cầu hỗ trợ, hệ thống xác định hạn SLA, kỹ thuật viên tiếp nhận xử lý, hai bên trao đổi qua bình luận và kết thúc bằng việc đóng phiếu. Ba tác nhân chính là:")
    add_bullet_item(doc, "Nhân sự các phòng ban: tạo yêu cầu, theo dõi phiếu của mình, bình luận và xác nhận đóng phiếu.", "Nhân viên (Employee)")
    add_bullet_item(doc, "Kỹ sư hỗ trợ: xem hàng đợi toàn công ty, tiếp nhận ticket về cho mình, đổi trạng thái, bình luận giải pháp.", "Kỹ thuật viên IT (Agent)")
    add_bullet_item(doc, "Trưởng bộ phận CNTT: có toàn quyền của Agent, đồng thời quản lý danh mục, người dùng, chính sách SLA và xem báo cáo.", "Quản trị viên (Admin)")

    add_figure_box(doc, "SƠ ĐỒ USE CASE CỦA CÁC CHỨC NĂNG HELPDESKIT HIỆN TẠI", "Hình 2.3 Sơ đồ Use Case của các chức năng HelpdeskIT hiện tại")

    add_heading_3(doc, "2.2.2 Yêu cầu và trạng thái chức năng")
    add_table_caption(doc, "Bảng 2.2 Yêu cầu chức năng đã hoàn thành trong phạm vi thực hành")
    tb22_data = [
        ("FR01", "Xác thực & phân quyền", "Đăng nhập bằng tài khoản/mật khẩu; hỗ trợ 3 nút chuyển nhanh vai trò demo."),
        ("FR02", "Quản lý danh mục", "Xem danh sách, tìm kiếm và tạo mới nhóm sự cố (/categories)."),
        ("FR03", "Quản trị người dùng", "Xem danh sách, lọc vai trò, tạo mới và xóa tài khoản; bảo vệ quyền Admin trên Navbar."),
        ("FR04", "Tạo ticket & Tính SLA", "Tạo ticket mới, tự sinh mã HD-xxxx, tự động tính hạn chót dueDate = createdAt + SLA."),
        ("FR05", "Danh sách đa góc nhìn", "Xem Tất cả ticket, Của tôi, Chưa phân công; lọc trạng thái kèm số đếm."),
        ("FR06", "TicketDetailDrawer", "Ngăn trượt từ cạnh phải: xem chi tiết, đổi trạng thái và gửi bình luận không chuyển trang."),
        ("FR07", "Quét ngầm quá hạn SLA", "Tiến trình SlaScheduler chạy ngầm mỗi phút tự động đánh cờ isOverdue khi quá hạn."),
        ("FR08", "Dashboard & Báo cáo", "4 thẻ KPI, thanh đo SLA đổi màu cảnh báo, chỉ số MTTA/MTTR và biểu đồ Recharts.")
    ]
    create_table_custom(doc, 9, 3, [Inches(0.8), Inches(2.2), Inches(4.0)], ["Mã", "Chức năng", "Kết quả hiện tại"], tb22_data, {0: WD_ALIGN_PARAGRAPH.CENTER})
    add_body_p(doc, "Các chức năng trong Bảng 2.2 đã hoàn thành ở phạm vi thực hành local/LAN. Giao diện được tối ưu chuẩn 2D doanh nghiệp, có công cụ khởi động 1-click run-project.bat. Ứng dụng di động và triển khai đám mây được dành cho giai đoạn tiếp theo.")

    add_heading_2(doc, "2.3 Công nghệ và môi trường triển khai hiện tại")
    add_heading_3(doc, "2.3.1 Các thành phần đã sử dụng")
    add_table_caption(doc, "Bảng 2.3 Công nghệ và vai trò trong HelpdeskIT")
    tb23_data = [
        ("Backend", "Java 17 LTS, Spring Boot 3.3.5; xử lý HTTP REST API và nghiệp vụ."),
        ("Dữ liệu", "Spring Data JPA, Hibernate, H2 Database lưu file vật lý bền vững local."),
        ("Giao diện", "ReactJS 18, Vite 5; Single Page Application, điều hướng nhanh không tải lại trang."),
        ("Thiết kế", "Tailwind CSS, tokens.css; Enterprise 2D Design System, font IBM Plex Sans, Light/Dark mode."),
        ("Biểu đồ", "Recharts; trực quan hóa tỷ lệ SLA, so sánh tiến độ và phân bổ sự cố."),
        ("Tác vụ ngầm", "Spring Scheduling (@Scheduled); quét kiểm tra ticket quá hạn định kỳ mỗi phút."),
        ("Công cụ", "Git quản lý mã nguồn; Maven quản lý thư viện; VS Code, IntelliJ IDEA, Postman.")
    ]
    create_table_custom(doc, 8, 2, [Inches(1.8), Inches(5.2)], ["Thành phần", "Công nghệ và vai trò"], tb23_data)

    add_heading_3(doc, "2.3.2 Phạm vi local và LAN")
    add_body_p(doc, "Ứng dụng hiện chạy trên Windows tại localhost:8080 cho Backend và localhost:5173 cho Frontend. File WebConfig.java cấu hình mở CORS cho origin 5173 và các dải mạng LAN nội bộ. Dữ liệu H2 được lưu vào file ./data/helpdesk_db giúp bảo toàn dữ liệu khi khởi động lại ứng dụng.")
    add_body_p(doc, "Môi trường HTTP trong mạng nội bộ được dùng để phát triển và kiểm tra luồng hoạt động của hệ thống. Khi mở rộng qua Internet, em dự kiến triển khai trên Linux VPS, dùng Spring Security kết hợp JWT và HTTPS/TLS để bảo vệ giao tiếp.")

    add_heading_2(doc, "2.4 Kiến trúc và tổ chức xử lý")
    add_heading_3(doc, "2.4.1 Kiến trúc hệ thống hiện tại")
    add_body_p(doc, "Kiến trúc HelpdeskIT gồm máy khách ReactJS, máy chủ Spring Boot 3 và cơ sở dữ liệu H2. Máy chủ tổ chức theo mô hình phân tầng: Controller tiếp nhận HTTP Request và validate dữ liệu; Service xử lý nghiệp vụ cốt lõi; Repository thực hiện truy vấn dữ liệu; Entity định nghĩa cấu trúc bảng. Máy khách tương tác qua Axios client định dạng JSON.")

    add_figure_box(doc, "KIẾN TRÚC HELPDESKIT TRONG MÔI TRƯỜNG LOCAL VÀ LAN", "Hình 2.4 Kiến trúc HelpdeskIT trong môi trường local và LAN")

    add_heading_3(doc, "2.4.2 Luồng dữ liệu và giới hạn mô hình")
    add_body_p(doc, "Dữ liệu được kiểm tra tính hợp lệ bằng Bean Validation trước khi ghi vào cơ sở dữ liệu. Sau khi cập nhật thành công, API trả về JSON chứa thông tin mới nhất. Ở phía giao diện, React Context cập nhật trạng thái hiển thị. Mô hình hiện tại sử dụng một tiến trình máy chủ Spring Boot nhúng Tomcat, phù hợp phạm vi thực hành.")

    add_heading_2(doc, "2.5 Cơ sở dữ liệu và toàn vẹn nội dung")
    add_heading_3(doc, "2.5.1 Mô hình dữ liệu hiện tại")
    add_body_p(doc, "Em thiết kế cơ sở dữ liệu gồm năm bảng: users, categories, sla_policies, tickets và ticket_comments. Quan hệ giữa các bảng được ràng buộc bằng khóa ngoại để đảm bảo toàn vẹn dữ liệu.")

    add_figure_box(doc, "MÔ HÌNH DỮ LIỆU CỦA HỆ THỐNG HELPDESKIT", "Hình 2.5 Mô hình dữ liệu của hệ thống HelpdeskIT")

    add_table_caption(doc, "Bảng 2.4 Các bảng và ý nghĩa dữ liệu")
    tb24_data = [
        ("users", "id, username, password, fullName, email, department, role", "Lưu thông tin nhân sự; username/email unique; password WRITE_ONLY."),
        ("categories", "id, name, description", "Danh mục nhóm sự cố; phục vụ phân loại khi tạo ticket."),
        ("sla_policies", "id, priorityLevel, resolutionTimeHours", "Thời gian cam kết theo 4 mức ưu tiên: 2h, 8h, 24h, 48h."),
        ("tickets", "id, ticketCode, title, description, status, priority, dueDate, isOverdue...", "Lưu phiếu yêu cầu; khóa ngoại tới users và categories; mã ticketCode unique."),
        ("ticket_comments", "id, ticket_id, user_id, content, createdAt", "Lịch sử trao đổi, bình luận giữa người yêu cầu và kỹ thuật viên.")
    ]
    create_table_custom(doc, 6, 3, [Inches(1.5), Inches(2.7), Inches(2.8)], ["Bảng", "Trường chính", "Ý nghĩa"], tb24_data)

    add_heading_3(doc, "2.5.2 Ràng buộc và cập nhật dữ liệu")
    add_body_p(doc, "Khi tạo ticket hoặc cập nhật trạng thái, thao tác được bọc trong giao dịch Spring @Transactional để đảm bảo tính trọn vẹn: nếu có lỗi phát sinh, hệ thống rollback về trạng thái trước đó. Khóa ngoại đảm bảo không thể tạo ticket với danh mục hoặc người dùng không tồn tại.")

    add_heading_2(doc, "2.6 Xác thực người dùng và phân quyền theo vai trò")
    add_body_p(doc, "Phân hệ xác thực (/login) quản lý đăng nhập và phiên làm việc. Nhằm phục vụ kiểm thử nhanh, giao diện tích hợp 3 thẻ chuyển nhanh tài khoản demo đại diện 3 vai trò: Nhân viên (emp_nam), Kỹ thuật viên (agent_hoa), Quản trị viên (admin_quang). Thông tin đăng nhập được lưu vào localStorage qua React AuthContext.")

    add_figure_box(doc, "GIAO DIỆN ĐĂNG NHẬP VÀ CHUYỂN NHANH VAI TRÒ DEMO", "Hình 2.6 Giao diện đăng nhập và chuyển nhanh vai trò demo")

    add_heading_2(doc, "2.7 Quản lý yêu cầu hỗ trợ và luồng trạng thái")
    add_heading_3(doc, "2.7.1 Hàng đợi ticket đa góc nhìn")
    add_body_p(doc, "Trang danh sách hỗ trợ 3 góc nhìn: Tất cả ticket, Của tôi (kèm badge đếm đỏ), Chưa phân công (kèm badge đếm đỏ). Chiều cao hàng chuẩn 44px, có tìm kiếm và lọc trạng thái.")

    add_figure_box(doc, "GIAO DIỆN DANH SÁCH YÊU CẦU ĐA GÓC NHÌN", "Hình 2.7 Giao diện Danh sách yêu cầu đa góc nhìn")

    add_heading_3(doc, "2.7.2 Tạo yêu cầu và tự động tính hạn SLA")
    add_body_p(doc, "Khi nhân viên mở Modal tạo yêu cầu, giao diện hiển thị 4 mức ưu tiên cùng số giờ SLA tương ứng. Khi nhấn Gửi, máy chủ tự sinh mã phiếu HD-xxxx và tính hạn dueDate = createdAt + resolutionTimeHours. Sự cố được lưu với trạng thái ban đầu là OPEN.")

    add_figure_box(doc, "TRÌNH TỰ TẠO TICKET VÀ TỰ ĐỘNG TÍNH HẠN CHÓT SLA", "Hình 2.8 Trình tự tạo ticket và tự động tính hạn chót SLA")

    add_heading_3(doc, "2.7.3 Ngăn trượt TicketDetailDrawer và quy trình xử lý")
    add_body_p(doc, "Khi nhấp vào một hàng trên bảng hoặc ấn Enter, ngăn chi tiết TicketDetailDrawer trượt ra từ cạnh phải (rộng tối đa 460px). Người dùng duyệt thông tin, xem timeline phản hồi, gửi bình luận và kỹ thuật viên thao tác đổi trạng thái (Tiếp nhận -> Đã giải quyết -> Đóng -> Mở lại) ngay trên drawer mà không làm mất bộ lọc bảng.")

    add_figure_box(doc, "GIAO DIỆN NGĂN TRƯỢT CHI TIẾT TICKETDETAILDRAWER", "Hình 2.9 Giao diện ngăn trượt chi tiết TicketDetailDrawer")
    add_figure_box(doc, "TRÌNH TỰ CHUYỂN ĐỔI TRẠNG THÁI VÀ GỬI BÌNH LUẬN", "Hình 2.10 Trình tự chuyển đổi trạng thái và gửi bình luận")

    add_heading_2(doc, "2.8 Quản trị danh mục, người dùng và chính sách SLA")
    add_heading_3(doc, "2.8.1 Quản trị danh mục dịch vụ và người dùng")
    add_body_p(doc, "Trang Danh mục dịch vụ (/categories) cho phép xem, tìm kiếm và tạo mới nhóm sự cố. Trang Người dùng & phòng ban (/users) dành riêng cho vai trò ADMIN: cấp tài khoản mới (mật khẩu mặc định 123456) và xóa tài khoản. Đặc biệt, trên thanh Navbar, dòng menu 'Người dùng & phòng ban' được lập trình ẩn/hiện có điều kiện: chỉ tài khoản có vai trò ADMIN mới nhìn thấy và truy cập được.")

    add_figure_box(doc, "GIAO DIỆN QUẢN TRỊ NGƯỜI DÙNG CÓ BẢO VỆ QUYỀN ADMIN", "Hình 2.11 Giao diện Quản trị người dùng có bảo vệ quyền Admin")

    add_heading_3(doc, "2.8.2 Chính sách SLA và tiến trình quét ngầm")
    add_table_caption(doc, "Bảng 2.5 Ma trận thời gian cam kết dịch vụ SLA")
    tb25_data = [
        ("CRITICAL", "Khẩn cấp", "<= 15 phút", "2 giờ", "Sập mạng toàn công ty, hỏng máy chủ trung tâm."),
        ("HIGH", "Cao", "<= 30 phút", "8 giờ", "Hỏng máy tính làm việc, máy in chứng từ cuối tháng."),
        ("MEDIUM", "Trung bình", "<= 2 giờ", "24 giờ", "Lỗi phần mềm kế toán, hiệu năng giảm một phần."),
        ("LOW", "Thấp", "<= 4 giờ", "48 giờ", "Yêu cầu cấp tài khoản mới, thắc mắc sử dụng.")
    ]
    create_table_custom(doc, 5, 5, [Inches(1.2), Inches(1.1), Inches(1.2), Inches(1.0), Inches(2.5)], ["Mức ưu tiên", "Tên cấp độ", "Thời gian phản hồi", "Thời gian xử lý", "Phạm vi ảnh hưởng"], tb25_data, {0: WD_ALIGN_PARAGRAPH.CENTER, 1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER})
    add_body_p(doc, "Tiến trình SlaScheduler chạy ngầm định kỳ mỗi phút tự động kiểm tra các ticket chưa đóng có now.isAfter(dueDate) để đánh cờ isOverdue = true, kích hoạt nhãn đỏ cảnh báo trên giao diện.")

    add_heading_2(doc, "2.9 Bảng điều khiển KPI, Báo cáo và Hệ thống thiết kế 2D")
    add_body_p(doc, "Màn hình Dashboard (/dashboard) hiển thị 4 thẻ KPI cốt lõi, biểu đồ cột đôi so sánh tiến độ và thanh đo tỷ lệ đạt chuẩn SLA tự động đổi màu khi xuống dưới ngưỡng. Màn hình Báo cáo (/reports) đo lường chỉ số MTTA, MTTR, biểu đồ phân bổ yêu cầu theo danh mục và phòng ban bằng thư viện Recharts.")
    add_body_p(doc, "Giao diện tuân thủ Enterprise 2D Design System: font chữ duy nhất IBM Plex Sans; bộ CSS tokens phẳng (tokens.css) không gradient, không bóng đổ nặng; duy nhất 1 màu nhấn chủ đạo (--brand #0b6bcb / #4c9dff); hỗ trợ chuyển đổi giao diện Sáng / Tối.")

    add_figure_box(doc, "GIAO DIỆN BẢNG ĐIỀU KHIỂN KPI VÀ BÁO CÁO HIỆU NĂNG", "Hình 2.12 Giao diện Bảng điều khiển KPI và Báo cáo hiệu năng")

    add_heading_2(doc, "2.10 Kiểm thử và kết quả thực hiện")
    add_heading_3(doc, "2.10.1 Phạm vi và phương pháp kiểm tra")
    add_body_p(doc, "Em tiến hành kiểm thử chức năng trên trình duyệt Google Chrome đối chiếu với các yêu cầu đề ra. Bộ kiểm thử gồm 12 ca kiểm thử tiêu biểu, tất cả đều đạt kết quả mong đợi.")

    add_table_caption(doc, "Bảng 2.6 Tổng hợp kết quả kiểm thử HelpdeskIT")
    tb26_data = [
        ("Xác thực", "Đăng nhập hợp lệ bằng 3 vai trò demo", "Chuyển đúng trang, lưu session vào AuthContext; đạt 3/3 ca."),
        ("Tạo ticket", "Tạo ticket với 4 mức ưu tiên", "Sinh mã HD-xxxx, tính dueDate chính xác theo SLA; đạt 4/4 ca."),
        ("Bảo vệ dữ liệu", "Bỏ trống tiêu đề hoặc chọn thiếu danh mục", "Bắt lỗi tại giao diện, không gửi request lỗi; đạt 2/2 ca."),
        ("Drawer tương tác", "Mở drawer, tiếp nhận xử lý, gửi bình luận", "Trạng thái cập nhật tức thì, không chuyển trang; đạt 3/3 ca."),
        ("Phân quyền menu", "Kiểm tra hiển thị menu 'Người dùng & phòng ban'", "Chỉ ADMIN nhìn thấy, Employee/Agent bị ẩn hoàn toàn; đạt 2/2 ca."),
        ("Quét ngầm SLA", "SlaScheduler quét vé quá hạn", "Tự động bật isOverdue = true và đổi màu thanh đo SLA; đạt 1/1 ca.")
    ]
    create_table_custom(doc, 7, 3, [Inches(1.5), Inches(2.5), Inches(3.0)], ["Nhóm", "Nội dung kiểm tra", "Kết quả và phạm vi"], tb26_data)

    add_heading_3(doc, "2.10.2 Đánh giá kết quả và hạn chế")
    add_body_p(doc, "Trong các lần thử trên Chrome local, thời gian phản hồi của các REST API được ghi nhận dao động từ 15ms đến 45ms, đáp ứng yêu cầu tương tác nhanh. Khi khởi động lại máy chủ, dữ liệu H2 file local bảo toàn 100%.")
    add_body_p(doc, "Những giới hạn cần tiếp tục đánh giá gồm: chưa kiểm thử tải lớn đồng thời hàng nghìn kết nối, chưa tích hợp mã hóa JWT có thời hạn ngắn và chưa triển khai đám mây qua Internet. Các kết quả này là cơ sở để tiếp tục mở rộng đề tài theo định hướng ở Chương 3.")

    # ==================== CHƯƠNG 3 ====================
    doc.add_page_break()
    add_heading_1(doc, "CHƯƠNG 3 ĐÁNH GIÁ KẾT QUẢ VÀ ĐỊNH HƯỚNG PHÁT TRIỂN")

    add_heading_2(doc, "3.1 Đánh giá kết quả thực tập")
    add_heading_3(doc, "3.1.1 Công việc tại doanh nghiệp")
    add_body_p(doc, "Qua quá trình thực tập tại JITS INOVATION LABS, em được tham gia các công việc thực tế: tìm hiểu hạ tầng mạng LAN văn phòng, kiểm tra kết nối thiết bị máy trạm, máy in, router và hỗ trợ xử lý sự cố. Em hiểu rõ hơn vai trò của router, switch, access point và quy trình hỗ trợ kỹ thuật trong một doanh nghiệp công nghệ.")
    add_body_p(doc, "Kết quả không chỉ nằm ở thao tác kỹ thuật mà còn ở cách tiếp nhận vấn đề, khoanh vùng nguyên nhân và kiểm tra sau khi xử lý. Việc làm việc cùng các anh chị kỹ sư giúp em nhận biết giới hạn của mình và rèn luyện tác phong làm việc nghiêm túc, cẩn trọng.")

    add_heading_3(doc, "3.1.2 Kết quả đề tài thực hành HelpdeskIT")
    add_body_p(doc, "HelpdeskIT đã hoàn thành các nhóm chức năng cơ bản của một hệ thống quản lý sự cố CNTT: xác thực 3 vai trò, quản lý danh mục dịch vụ, tạo ticket tự động tính SLA, hàng đợi đa góc nhìn, ngăn trượt TicketDetailDrawer, bình luận, quản trị người dùng bảo vệ quyền Admin, quét ngầm SLA, bảng điều khiển KPI và báo cáo hiệu năng. Kết quả kiểm thử đã xác nhận 12/12 ca kiểm thử đạt kết quả tốt trên môi trường local/LAN.")

    add_heading_2(doc, "3.2 Kiến thức và kỹ năng đạt được")
    add_heading_3(doc, "3.2.1 Vận dụng các học phần đã học")
    add_table_caption(doc, "Bảng 3.1 Liên hệ học phần và công việc đã thực hiện")
    tb31_data = [
        ("Mạng máy tính", "Khảo sát sơ đồ kết nối LAN; kiểm tra IP, DHCP, gateway, DNS; hỗ trợ xử lý sự cố kết nối."),
        ("Cơ sở dữ liệu", "Thiết kế dữ liệu HelpdeskIT; xác định khóa, quan hệ user–ticket–category–comment; dùng transaction."),
        ("Lập trình Web", "Xây dựng giao diện ReactJS, RESTful API Spring Boot, xử lý bất đồng bộ và kết nối Axios."),
        ("Phân tích và thiết kế HTTT", "Xác định tác nhân, yêu cầu và phạm vi; mô hình hóa Use Case, ERD và các luồng xử lý."),
        ("Kỹ thuật phần mềm", "Tìm hiểu quy trình Agile/Scrum; quản lý mã nguồn bằng Git; thiết kế ca kiểm thử chức năng.")
    ]
    create_table_custom(doc, 6, 2, [Inches(2.2), Inches(4.8)], ["Học phần", "Cách vận dụng trong thực tập"], tb31_data)

    add_heading_3(doc, "3.2.2 Kiến thức mới trong quá trình thực tập")
    add_body_p(doc, "Trước đợt thực tập, em đã có kiến thức cơ bản về Java, HTML, CSS, JavaScript và SQL. Trong thời gian làm việc tại doanh nghiệp, em tìm hiểu sâu hơn về quy trình ITIL, mạng văn phòng và kiến trúc Spring Boot 3. Qua phát triển HelpdeskIT, em nghiên cứu thêm Spring Data JPA, H2 persistent database, Vite, Tailwind CSS, Recharts và mô hình Slide-over Drawer.")

    add_heading_3(doc, "3.2.3 Kỹ năng chuyên môn và kỹ năng mềm")
    add_body_p(doc, "Em có thể tự xây dựng API RESTful hoàn chỉnh, thiết kế CSDL quan hệ, xây dựng giao diện người dùng tương tác mượt mà và kiểm thử chức năng phần mềm. Em cải thiện khả năng làm việc nhóm, quản lý thời gian và báo cáo tiến độ. Điểm mạnh là chủ động tự học công nghệ mới; hạn chế là kinh nghiệm thực tế về bảo mật nâng cao và kiểm thử tải diện rộng còn cần tích lũy thêm.")

    add_heading_2(doc, "3.3 Khó khăn thực tế và kinh nghiệm rút ra")
    add_heading_3(doc, "3.3.1 Lỗi lặp đệ quy vô tận JSON và quản lý quan hệ JPA")
    add_body_p(doc, "Khó khăn đầu tiên là khi gọi API lấy danh sách Ticket, máy chủ báo lỗi StackOverflowError do quan hệ hai chiều giữa Ticket và User dẫn đến việc Jackson ObjectMapper tuần tự hóa tuần hoàn. Em kiểm tra nguyên nhân và khắc phục bằng cách sử dụng chú thích @JsonIgnoreProperties({\"hibernateLazyInitializer\", \"handler\"}) và tách biệt các DTO. Bài học rút ra là cần kiểm soát chặt chẽ việc serialize đối tượng JPA khi chuyển đổi sang JSON.")

    add_heading_3(doc, "3.3.2 Lỗi chặn chia sẻ tài nguyên CORS Policy và cấu hình máy chủ")
    add_body_p(doc, "Khi máy khách Frontend cổng 5173 gọi API Backend cổng 8080, trình duyệt chặn yêu cầu với thông báo lỗi CORS header missing. Em tìm hiểu cơ chế Same-Origin Policy và xử lý bằng cách tạo class WebConfig thực thi WebMvcConfigurer mở CORS toàn cục cho endpoint /api/**. Kinh nghiệm rút ra là cần thiết lập cấu hình CORS ngay từ đầu khi tích hợp các ứng dụng tách biệt máy chủ.")

    add_heading_3(doc, "3.3.3 Trải nghiệm người dùng và ngăn trượt Slide-over Drawer")
    add_body_p(doc, "Ban đầu việc xem chi tiết ticket chuyển sang trang mới làm mất toàn bộ bộ lọc và từ khóa đang tìm kiếm. Em tái cấu trúc giao diện sang dạng Slide-over Drawer (TicketDetailDrawer) trượt từ cạnh phải, cho phép duyệt và xử lý ticket trực tiếp. Bài học là trải nghiệm người dùng trong phần mềm doanh nghiệp cần ưu tiên giảm thiểu số lần chuyển trang không cần thiết.")

    add_heading_2(doc, "3.4 Định hướng phát triển và đồ án tốt nghiệp")
    add_heading_3(doc, "3.4.1 Tích hợp Spring Security và JSON Web Token (JWT)")
    add_body_p(doc, "Em dự kiến nâng cấp phân hệ xác thực bằng Spring Security kết hợp JSON Web Token (JWT), mã hóa mật khẩu bằng BCrypt và cấp token có thời hạn ngắn để tăng cường bảo mật khi triển khai qua Internet.")

    add_heading_3(doc, "3.4.2 Hệ thống thông báo thời gian thực WebSocket và Email cảnh báo SLA")
    add_body_p(doc, "Tích hợp Spring WebSocket (STOMP) để đẩy thông báo chuông tức thì khi có ticket mới hoặc bình luận; sử dụng JavaMailSender tự động gửi email thông báo khi ticket sắp quá hạn SLA.")

    add_heading_3(doc, "3.4.3 Đóng gói Docker và định hướng đồ án tốt nghiệp")
    add_body_p(doc, "Em dự kiến tiếp tục HelpdeskIT thành đồ án tốt nghiệp, tập trung đóng gói container bằng Dockerfile và docker-compose để dễ dàng triển khai lên đám mây, đồng thời nghiên cứu tích hợp mô hình AI tự động phân loại sự cố dựa trên nội dung mô tả.")

    # ==================== KẾT LUẬN ====================
    doc.add_page_break()
    p_kl = doc.add_paragraph()
    r = p_kl.add_run("KẾT LUẬN")
    r.bold = True
    r.font.size = Pt(14)
    p_kl.paragraph_format.space_after = Pt(8)

    add_body_p(doc, "Đợt thực tập tại Công ty TNHH JITS INOVATION LABS giúp em vận dụng kiến thức chuyên ngành Công nghệ phần mềm vào các công việc tìm hiểu hạ tầng CNTT, hỗ trợ xử lý sự cố kỹ thuật và quy trình vận hành thực tế tại doanh nghiệp.")
    add_body_p(doc, "Song song với công việc tại đơn vị, em xây dựng HelpdeskIT như một đề tài thực hành cá nhân. Ứng dụng đã hình thành luồng tiếp nhận sự cố, phân quyền 3 vai trò (ẩn hiện menu Quản trị đúng quyền Admin), tạo ticket tự động tính hạn SLA, hàng đợi đa góc nhìn, ngăn trượt TicketDetailDrawer, tiến trình quét ngầm SlaScheduler, bảng điều khiển KPI và báo cáo hiệu năng. Kết quả đã xác nhận gồm 12/12 ca kiểm thử đạt kết quả tốt ở phạm vi local/LAN.")
    add_body_p(doc, "Các giới hạn còn lại là chưa kiểm thử tải lớn trên mạng Internet, chưa tích hợp xác thực JWT và ứng dụng di động. Tuần cuối tiếp tục hoàn thiện tài liệu và kiểm thử. Định hướng tiếp theo là tích hợp Spring Security + JWT, WebSocket thông báo thời gian thực, đóng gói Docker và hoàn thiện HelpdeskIT thành đồ án tốt nghiệp.")

    # ==================== TÀI LIỆU THAM KHẢO ====================
    doc.add_page_break()
    p_tr = doc.add_paragraph()
    r = p_tr.add_run("TÀI LIỆU THAM KHẢO")
    r.bold = True
    r.font.size = Pt(14)
    p_tr.paragraph_format.space_after = Pt(8)

    refs = [
        "[1] Spring Boot, “Spring Boot Reference Documentation”. https://spring.io/projects/spring-boot",
        "[2] React, “React Documentation”. https://react.dev/",
        "[3] H2 Database, “H2 Database Engine”. https://www.h2database.com/",
        "[4] Tailwind CSS, “Tailwind CSS Documentation”. https://tailwindcss.com/",
        "[5] Recharts, “Recharts Documentation”. https://recharts.org/",
        "[6] AXELOS, “ITIL 4 Foundation: IT Service Management Best Practices”. https://www.axelos.com/",
        "[7] Git, “Git Reference Manual”. https://git-scm.com/docs"
    ]
    for rf in refs:
        p_rf = doc.add_paragraph()
        p_rf.paragraph_format.space_after = Pt(3)
        p_rf.paragraph_format.line_spacing = 1.15
        p_rf.add_run(rf)

    output_path = "Bao_cao_Thuc_tap_Doanh_nghiep_Moi.docx"
    doc.save(output_path)
    print(f"Successfully saved to: {output_path}")

    # Also try to save to main file if unlocked
    try:
        doc.save("Bao_cao_Thuc_tap_Doanh_nghiep_IT_Helpdesk.docx")
        print("Also updated: Bao_cao_Thuc_tap_Doanh_nghiep_IT_Helpdesk.docx")
    except PermissionError:
        print("Bao_cao_Thuc_tap_Doanh_nghiep_IT_Helpdesk.docx is open in Word, but Bao_cao_Thuc_tap_Doanh_nghiep_Moi.docx is completely ready!")

if __name__ == "__main__":
    build_signlite_style_report()
