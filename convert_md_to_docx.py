import re
import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_FILE = os.path.join(BASE_DIR, "Vision_Series_Test_Plan.md")
OUT_FILE = os.path.join(BASE_DIR, "Vision_Series_Test_Plan.docx")

doc = Document()

style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)
font.color.rgb = RGBColor(0x1a, 0x23, 0x32)

for level in range(1, 5):
    hs = doc.styles[f'Heading {level}']
    hs.font.name = 'Calibri'
    hs.font.color.rgb = RGBColor(0x1a, 0x23, 0x32)

section = doc.sections[0]
section.top_margin = Cm(2.5)
section.bottom_margin = Cm(2.5)
section.left_margin = Cm(2.5)
section.right_margin = Cm(2.5)

with open(MD_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

def add_image(path_rel, caption=None):
    img_path = os.path.join(BASE_DIR, path_rel.replace("/", os.sep))
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        try:
            run.add_picture(img_path, width=Inches(5.5))
        except Exception:
            run.add_picture(img_path, width=Inches(4.5))
        if caption:
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_cap = cap.add_run(caption)
            run_cap.italic = True
            run_cap.font.size = Pt(9)
            run_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)
    else:
        p = doc.add_paragraph(f"[Image not found: {path_rel}]")
        p.runs[0].font.color.rgb = RGBColor(0xff, 0x00, 0x00)

STAGE_COL_NAMES = {"FT", "TRIM", "OT", "VIS", "VI", "VER", "CONN"}
STAGE_COL_WIDTH = Cm(1.1)
TEST_PROC_COL_WIDTH = Cm(3.0)
PAGE_CONTENT_WIDTH = Cm(16)  # 21cm A4 minus 2 × 2.5cm margins

def add_table(header_line, rows):
    cols = [c.strip() for c in header_line.strip().strip("|").split("|")]
    clean_cols = [c.replace("**", "") for c in cols]
    num_cols = len(cols)
    table = doc.add_table(rows=1, cols=num_cols, style='Light Grid Accent 1')
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    is_test_proc_table = "Description" in clean_cols
    col_widths = None
    stage_col_indices = set()

    if is_test_proc_table:
        table.autofit = False
        tbl_pr = table._tbl.tblPr
        layout_el = OxmlElement('w:tblLayout')
        layout_el.set(qn('w:type'), 'fixed')
        tbl_pr.append(layout_el)

        col_widths = []
        fixed_total = Cm(0)
        flex_count = 0
        for ci, name in enumerate(clean_cols):
            if name in STAGE_COL_NAMES:
                col_widths.append(STAGE_COL_WIDTH)
                fixed_total += STAGE_COL_WIDTH
                stage_col_indices.add(ci)
            elif name == "Test procedure":
                col_widths.append(TEST_PROC_COL_WIDTH)
                fixed_total += TEST_PROC_COL_WIDTH
            else:
                col_widths.append(None)
                flex_count += 1
        remaining = PAGE_CONTENT_WIDTH - fixed_total
        if flex_count > 0:
            each = int(remaining) // flex_count
            col_widths = [w if w is not None else each for w in col_widths]

    for i, col in enumerate(cols):
        cell = table.rows[0].cells[i]
        cell.text = ""
        run = cell.paragraphs[0].add_run(col.replace("**", ""))
        run.bold = True
        run.font.size = Pt(10)
        run.font.name = 'Calibri'
        if col_widths:
            cell.width = col_widths[i]
        if i in stage_col_indices:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for row_text in rows:
        cells_text = [c.strip() for c in row_text.strip().strip("|").split("|")]
        row = table.add_row()
        for i, ct in enumerate(cells_text):
            if i < num_cols:
                clean = ct.replace("**", "")
                row.cells[i].text = clean
                if col_widths:
                    row.cells[i].width = col_widths[i]
                for para in row.cells[i].paragraphs:
                    for run in para.runs:
                        run.font.size = Pt(10)
                        run.font.name = 'Calibri'
                if i in stage_col_indices:
                    for para in row.cells[i].paragraphs:
                        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()

def parse_inline(text):
    """Returns list of (text, bold, italic) tuples."""
    parts = []
    pattern = re.compile(r'\*\*(.+?)\*\*')
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            parts.append((text[last:m.start()], False, False))
        parts.append((m.group(1), True, False))
        last = m.end()
    if last < len(text):
        parts.append((text[last:], False, False))
    return parts

i = 0
table_header = None
table_rows = []
in_table = False

while i < len(lines):
    line = lines[i].rstrip("\n")

    if line.startswith("|") and "---" not in line:
        if not in_table:
            in_table = True
            table_header = line
            table_rows = []
            i += 1
            if i < len(lines) and "---" in lines[i]:
                i += 1
            continue
        else:
            table_rows.append(line)
            i += 1
            continue
    else:
        if in_table:
            add_table(table_header, table_rows)
            in_table = False
            table_header = None
            table_rows = []

    if line.strip() == "---":
        doc.add_paragraph()
        i += 1
        continue

    if line.startswith("# ") and not line.startswith("## "):
        doc.add_heading(line[2:].strip(), level=0)
        i += 1
        continue

    if line.startswith("## "):
        doc.add_heading(line[3:].strip(), level=1)
        i += 1
        continue

    if line.startswith("### "):
        doc.add_heading(line[4:].strip(), level=2)
        i += 1
        continue

    if line.startswith("##### "):
        doc.add_heading(line[6:].strip(), level=4)
        i += 1
        continue

    if line.startswith("#### "):
        doc.add_heading(line[5:].strip(), level=3)
        i += 1
        continue

    img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
    if img_match:
        alt_text = img_match.group(1)
        img_path = img_match.group(2)
        caption = None
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            cap_match = re.match(r'^\*(.+)\*$', next_line)
            if cap_match:
                caption = cap_match.group(1)
                i += 1
        add_image(img_path, caption)
        i += 1
        continue

    cap_match = re.match(r'^\*(.+)\*$', line.strip())
    if cap_match and not line.strip().startswith("*Production") and not line.strip().startswith("*Trim") and not line.strip().startswith("*Stand") and not line.strip().startswith("*VIS Sub") and not line.strip().startswith("*(Similar") and not line.strip().startswith("*PSU") and not line.strip().startswith("*VIS4"):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(cap_match.group(1))
        run.italic = True
        run.font.size = Pt(9)
        i += 1
        continue

    if line.startswith("- **") or line.startswith("- *"):
        content = line[2:].strip()
        p = doc.add_paragraph(style='List Bullet')
        for text, bold, italic in parse_inline(content):
            run = p.add_run(text)
            run.bold = bold
            run.font.size = Pt(11)
            run.font.name = 'Calibri'
        i += 1
        continue

    if line.startswith("- "):
        content = line[2:].strip()
        p = doc.add_paragraph(style='List Bullet')
        for text, bold, italic in parse_inline(content):
            run = p.add_run(text)
            run.bold = bold
            run.font.size = Pt(11)
            run.font.name = 'Calibri'
        i += 1
        continue

    if line.strip().startswith("*") and line.strip().endswith("*"):
        text = line.strip().strip("*")
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.italic = True
        run.font.size = Pt(11)
        run.font.name = 'Calibri'
        i += 1
        continue

    if line.strip():
        p = doc.add_paragraph()
        for text, bold, italic in parse_inline(line.strip()):
            run = p.add_run(text)
            run.bold = bold
            run.font.size = Pt(11)
            run.font.name = 'Calibri'
        i += 1
        continue

    i += 1

if in_table:
    add_table(table_header, table_rows)

doc.save(OUT_FILE)
print(f"Word document saved to: {OUT_FILE}")
