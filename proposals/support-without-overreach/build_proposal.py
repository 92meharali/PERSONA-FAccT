"""Build the proposal from its Markdown source with python-docx."""

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.opc.constants import RELATIONSHIP_TYPE


ROOT = Path(__file__).resolve().parent
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.top_margin = sec.bottom_margin = Inches(0.7)
sec.left_margin = sec.right_margin = Inches(0.8)
sec.footer_distance = Inches(0.3)

for style in doc.styles:
    for border in style.element.xpath('.//w:pBdr'):
        border.getparent().remove(border)

for name in ('Normal', 'Title', 'Subtitle', 'Heading 1', 'Heading 2', 'List Bullet'):
    style = doc.styles[name]
    style.font.name = 'Calibri'
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.widow_control = True

normal = doc.styles['Normal']
normal.font.size = Pt(11)
normal.paragraph_format.space_after = Pt(7)
normal.paragraph_format.line_spacing = 1.06
doc.styles['Title'].font.size = Pt(25)
doc.styles['Title'].paragraph_format.space_after = Pt(10)
doc.styles['Heading 1'].font.size = Pt(16)
doc.styles['Heading 1'].paragraph_format.space_before = Pt(10)
doc.styles['Heading 1'].paragraph_format.space_after = Pt(8)
doc.styles['Heading 2'].font.size = Pt(12)
doc.styles['Heading 2'].paragraph_format.space_before = Pt(9)
doc.styles['Heading 2'].paragraph_format.space_after = Pt(5)
doc.styles['List Bullet'].paragraph_format.space_after = Pt(5)


def add_link(paragraph, value):
    link = OxmlElement('w:hyperlink')
    link.set(qn('r:id'), paragraph.part.relate_to(value, RELATIONSHIP_TYPE.HYPERLINK, is_external=True))
    run = OxmlElement('w:r')
    props = OxmlElement('w:rPr')
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '254D65')
    props.append(color)
    size = OxmlElement('w:sz')
    size.set(qn('w:val'), '19')
    props.append(size)
    run.append(props)
    text = OxmlElement('w:t')
    text.text = value
    run.append(text)
    link.append(run)
    paragraph._p.append(link)


def add_text(paragraph, text):
    for part in re.split(r'(\*\*.*?\*\*|https?://\S+)', text):
        if part.startswith('**'):
            paragraph.add_run(part[2:-2]).bold = True
        elif part.startswith('http'):
            add_link(paragraph, part)
        else:
            paragraph.add_run(part)


def add_table(lines):
    rows = [[c.strip() for c in line.strip('|').split('|')] for line in lines]
    rows = [r for r in rows if not all(re.fullmatch(r'[-: ]+', c) for c in r)]
    table = doc.add_table(rows=0, cols=len(rows[0]))
    table.autofit = False
    widths = [2.05, 4.85] if len(rows[0]) == 2 else [1.6, 1.65, 3.65]
    for col, width in zip(table.columns, widths):
        col.width = Inches(width)
    for i, row in enumerate(rows):
        cells = table.add_row().cells
        for j, value in enumerate(row):
            cells[j].width = Inches(widths[j])
            p = cells[j].paragraphs[0]
            p.paragraph_format.space_before = Pt(5)
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.line_spacing = 1.02
            add_text(p, value)
            for run in p.runs:
                run.font.size = Pt(10.5)
                run.bold = i == 0
            if i == 0:
                shading = OxmlElement('w:shd')
                shading.set(qn('w:fill'), 'E8ECEF')
                cells[j]._tc.get_or_add_tcPr().append(shading)
        no_split = OxmlElement('w:cantSplit')
        table.rows[i]._tr.get_or_add_trPr().append(no_split)
    repeat = OxmlElement('w:tblHeader')
    table.rows[0]._tr.get_or_add_trPr().append(repeat)


lines = (ROOT / 'proposal.md').read_text().splitlines()
i = 0
next_page = False
while i < len(lines):
    line = lines[i].strip()
    i += 1
    if not line:
        continue
    if line == '<!-- PAGE -->':
        next_page = True
    elif line.startswith('|'):
        table_lines = [line]
        while i < len(lines) and lines[i].startswith('|'):
            table_lines.append(lines[i])
            i += 1
        add_table(table_lines)
    elif line.startswith('# '):
        doc.add_paragraph(line[2:], 'Title')
    elif line.startswith('## '):
        p = doc.add_paragraph(line[3:], 'Heading 1')
        if next_page:
            p.paragraph_format.page_break_before = True
            next_page = False
    elif line.startswith('### '):
        doc.add_paragraph(line[4:], 'Heading 2')
    else:
        p = doc.add_paragraph(style='List Bullet' if line.startswith('- ') else 'Normal')
        add_text(p, line[2:] if line.startswith('- ') else line)
        if re.match(r'^\[\d\]', line):
            p.paragraph_format.space_after = Pt(6)
            for run in p.runs:
                run.font.size = Pt(9.5)

footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
field = OxmlElement('w:fldSimple')
field.set(qn('w:instr'), 'PAGE')
footer._p.append(field)
doc.core_properties.title = 'Chatbot Design and Contextual Appropriateness in Supportive Conversations'
doc.core_properties.subject = 'Joint research proposal'
doc.core_properties.author = ''
doc.save(ROOT / 'Joint_Research_Proposal.docx')
print(ROOT / 'Joint_Research_Proposal.docx')
