"""Build the study implementation handoff from its maintained Markdown source."""
from pathlib import Path
import re

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'implementation_2026-10-24.md'
OUTPUT = ROOT / 'PERSONA_Capability_Study_Implementation_Plan.docx'


def make_table(doc, rows):
    table = doc.add_table(rows=0, cols=len(rows[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    widths = [2.2, 4.3] if len(rows[0]) == 2 else ([1.4, 2.8, 2.3] if len(rows[0]) == 3 else [1.2, 1.6, 1.3, 2.4])
    for col, width in zip(table.columns, widths):
        col.width = Inches(width)
    for i, row in enumerate(rows):
        cells = table.add_row().cells
        for cell, text, width in zip(cells, row, widths):
            cell.width = Inches(width)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            props = cell._tc.get_or_add_tcPr()
            borders = OxmlElement('w:tcBorders')
            for edge in ('top', 'left', 'bottom', 'right'):
                e = OxmlElement('w:' + edge)
                for key, value in [('val','single'), ('sz','4'), ('color','D9D9D9')]:
                    e.set(qn('w:' + key), value)
                borders.append(e)
            props.append(borders)
            margins = OxmlElement('w:tcMar')
            for edge in ('top', 'left', 'bottom', 'right'):
                e = OxmlElement('w:' + edge)
                e.set(qn('w:w'), '80')
                e.set(qn('w:type'), 'dxa')
                margins.append(e)
            props.append(margins)
            shade = OxmlElement('w:shd')
            shade.set(qn('w:fill'), 'E9EEF2' if i == 0 else 'FFFFFF')
            props.append(shade)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.02
            run = p.add_run(text)
            run.font.size = Pt(9)
            run.bold = i == 0
        props = table.rows[-1]._tr.get_or_add_trPr()
        props.append(OxmlElement('w:cantSplit'))
        if i == 0:
            props.append(OxmlElement('w:tblHeader'))
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def main():
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Inches(8.5), Inches(11.7)
    section.top_margin = section.bottom_margin = Inches(.65)
    section.left_margin = section.right_margin = Inches(1)
    for name in ['Normal', 'Title', 'Subtitle', 'Heading 1', 'Heading 2', 'Heading 3', 'List Bullet', 'List Number']:
        style = doc.styles[name]
        style.font.name = 'Calibri'
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.font.size = Pt(10.5)
    for style in doc.styles:
        for border in list(style.element.iter(qn('w:pBdr'))):
            border.getparent().remove(border)
    normal = doc.styles['Normal'].paragraph_format
    normal.space_after = Pt(6)
    normal.line_spacing = 1.08
    doc.styles['Title'].font.size = Pt(24)
    doc.styles['Heading 1'].font.size = Pt(17)
    doc.styles['Heading 2'].font.size = Pt(12)
    for name in ['Heading 1', 'Heading 2']:
        doc.styles[name].paragraph_format.space_before = Pt(8)
        doc.styles[name].paragraph_format.space_after = Pt(6)
    footer = section.footer.paragraphs[0]
    footer.alignment = 2
    run = footer.add_run('PERSONA study plan  |  ')
    run.font.size = Pt(8)
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'), 'PAGE')
    footer._p.append(field)
    doc.core_properties.title = 'Implementing Capability Grounded Review Allocation'
    doc.core_properties.author = ''
    doc.core_properties.subject = 'Prospective PERSONA study implementation plan'
    lines = SOURCE.read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        if line == '<!-- PAGE -->':
            doc.add_page_break()
        elif line.startswith('|'):
            rows = [[v.strip() for v in line.strip('|').split('|')]]
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = [v.strip() for v in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+', v) for v in row):
                    rows.append(row)
                i += 1
            make_table(doc, rows)
        elif line.startswith('# '):
            doc.add_paragraph(line[2:], 'Title')
        elif line.startswith('## '):
            doc.add_paragraph(line[3:], 'Heading 1')
        elif line.startswith('### '):
            doc.add_paragraph(line[4:], 'Heading 2')
        elif line.startswith('- '):
            doc.add_paragraph(line[2:], 'List Bullet')
        elif re.match(r'^\d+\. ', line):
            doc.add_paragraph(line, 'Normal')
        else:
            doc.add_paragraph(line)
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == '__main__':
    main()
