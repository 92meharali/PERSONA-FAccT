"""Build the team protocol and separate blinded assessor packet."""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent


def table(doc, lines):
    rows = [[cell.strip() for cell in line.strip().strip('|').split('|')]
            for line in lines if not set(line.replace('|', '').replace('-', '').strip()) == set()]
    t = doc.add_table(rows=1, cols=len(rows[0]))
    t.autofit = False
    widths = [2.0, 4.9] if len(rows[0]) == 2 else [2.35, 1.8, 2.75]
    for col, width in zip(t.columns, widths):
        col.width = Inches(width)
    for r, row in enumerate(rows):
        cells = t.rows[0].cells if r == 0 else t.add_row().cells
        for j, value in enumerate(row):
            cells[j].width = Inches(widths[j])
            cells[j].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cells[j].text = value
            pr = cells[j]._tc.get_or_add_tcPr()
            margins = OxmlElement('w:tcMar')
            for side in ('top', 'left', 'bottom', 'right'):
                el = OxmlElement('w:' + side)
                el.set(qn('w:w'), '90')
                el.set(qn('w:type'), 'dxa')
                margins.append(el)
            pr.append(margins)
            for p in cells[j].paragraphs:
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.line_spacing = 1.05
                for run in p.runs:
                    run.font.size = Pt(10)
                    run.bold = r == 0
            if r == 0:
                shading = OxmlElement('w:shd')
                shading.set(qn('w:fill'), 'E8EDF0')
                pr.append(shading)
        trpr = t.rows[r]._tr.get_or_add_trPr()
        trpr.append(OxmlElement('w:cantSplit'))
        if r == 0:
            trpr.append(OxmlElement('w:tblHeader'))
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + edge)
        e.set(qn('w:val'), 'single')
        e.set(qn('w:sz'), '4')
        e.set(qn('w:color'), 'D9D9D9')
        borders.append(e)
    t._tbl.tblPr.append(borders)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def build(source, output):
    doc = Document()
    for border in list(doc.styles.element.iter(qn('w:pBdr'))):
        border.getparent().remove(border)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.top_margin = sec.bottom_margin = Inches(.65)
    sec.left_margin = sec.right_margin = Inches(.8)
    sec.footer_distance = Inches(.3)
    for name in ('Normal', 'Title', 'Heading 1', 'Heading 2', 'List Bullet', 'List Number'):
        s = doc.styles[name]
        s.font.name = 'Calibri'
        s.font.color.rgb = RGBColor(0, 0, 0)
        s.font.size = Pt(11)
        s.paragraph_format.space_after = Pt(6)
        s.paragraph_format.line_spacing = 1.08
    doc.styles['Title'].font.size = Pt(23)
    doc.styles['Title'].font.bold = True
    doc.styles['Title'].paragraph_format.space_after = Pt(9)
    doc.styles['Heading 1'].font.size = Pt(15)
    doc.styles['Heading 1'].font.bold = True
    doc.styles['Heading 1'].paragraph_format.space_before = Pt(9)
    doc.styles['Heading 2'].font.size = Pt(12)
    doc.styles['Heading 2'].font.bold = True
    doc.styles['Heading 2'].paragraph_format.space_before = Pt(7)
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.add_run('Page ').font.size = Pt(9)
    f = OxmlElement('w:fldSimple')
    f.set(qn('w:instr'), 'PAGE')
    footer._p.append(f)
    lines = source.read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('|'):
            end = i
            while end < len(lines) and lines[end].strip().startswith('|'):
                end += 1
            table(doc, lines[i:end])
            i = end
            continue
        if line == '---':
            if source.name == 'assessor_packet.md':
                doc.add_page_break()
        elif line.startswith('# '):
            doc.add_paragraph(line[2:], 'Title')
        elif line.startswith('## '):
            title = line[3:]
            doc.add_paragraph(title, 'Heading 1' if title[0].isdigit() else 'Heading 2')
        elif line.startswith('- '):
            doc.add_paragraph(line[2:], 'List Bullet')
        else:
            # Keep explicit numbering to preserve restart semantics per checklist.
            doc.add_paragraph(line)
        i += 1
    doc.core_properties.title = lines[0][2:]
    doc.core_properties.subject = 'Proposed independent annotation follow-up for PERSONA'
    doc.core_properties.author = 'PERSONA research team'
    doc.save(output)
    print(output)


if __name__ == '__main__':
    build(ROOT / 'protocol.md', ROOT / 'PERSONA_Independent_Annotation_Protocol.docx')
    build(ROOT / 'assessor_packet.md', ROOT / 'PERSONA_Assessor_Instructions.docx')
