"""Genera la bitácora Word desde su Markdown. Solo documentación, no I1."""
from pathlib import Path
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.top_margin = sec.bottom_margin = Inches(0.7)
sec.left_margin = sec.right_margin = Inches(0.85)
normal = doc.styles['Normal']
normal.font.name = 'Calibri'
normal.font.size = Pt(11)
normal.paragraph_format.space_after = Pt(7)
normal.paragraph_format.line_spacing = 1.05
for name, size in [('Title', 24), ('Heading 1', 18), ('Heading 2', 13), ('Heading 3', 11)]:
    style = doc.styles[name]
    style.font.name = 'Calibri'
    style.font.size = Pt(size)
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.space_before = Pt(10)
    style.paragraph_format.space_after = Pt(7)
    style.paragraph_format.keep_with_next = True

def inline(paragraph, text):
    for part in re.split(r'(\*\*.*?\*\*)', text):
        run = paragraph.add_run(part[2:-2] if part.startswith('**') else part)
        run.bold = part.startswith('**')

code = False
for line in (ROOT / 'docs/BITACORA_JARVIS.md').read_text(encoding='utf-8').splitlines():
    if line == '<!-- page -->':
        doc.add_page_break()
    elif line.startswith('```'):
        code = not code
    elif code:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_together = True
        run = p.add_run(line)
        run.font.name = 'Consolas'
        run.font.size = Pt(9)
    elif line.startswith('# '):
        doc.add_paragraph(line[2:], 'Title')
    elif line.startswith('## '):
        doc.add_paragraph(line[3:], 'Heading 1')
    elif line.startswith('### '):
        doc.add_paragraph(line[4:], 'Heading 2')
    elif line.strip():
        inline(doc.add_paragraph(), line)

# Número discreto para poder localizar entradas en una bitácora acumulativa.
p = sec.footer.paragraphs[0]
p.alignment = 2
field = OxmlElement('w:fldSimple')
field.set(qn('w:instr'), 'PAGE')
p._p.append(field)
doc.core_properties.title = 'Bitácora de desarrollo de JARVIS'
doc.core_properties.author = 'Proyecto JARVIS'
doc.core_properties.subject = 'Preparación y seguimiento didáctico del desarrollo'
output = ROOT / 'docs/Bitacora_JARVIS.docx'
doc.save(output)
print(output)
