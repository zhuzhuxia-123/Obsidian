from pathlib import Path
import json
import re
import hashlib
from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.table import Table

root = Path(__file__).resolve().parents[1]
source = root / 'Grounding_DINO_组会汇报.docx'
target = root / 'Grounding_DINO_组会汇报.md'
assets = root / '组会资料' / 'md_images'
assets.mkdir(parents=True, exist_ok=True)
doc = Document(source)
lines = []
images = {}
chapter_started = False
table_count = 0
paragraph_count = 0
math_count = 0

equations = {
    'S = Xᵢ Xₜᵀ     sᵢ = maxⱼ Sᵢⱼ     I = TopKIndices(s, 900)':
        r'S = X_I X_T^{\mathsf T},\qquad s_i = \max_j S_{ij},\qquad I = \operatorname{TopKIndices}(s,900)',
    'L = Lcls + 5 Lₗ₁ + 2 LGIoU':
        r'\mathcal L = \mathcal L_{\mathrm{cls}} + 5\mathcal L_{\mathrm{L1}} + 2\mathcal L_{\mathrm{GIoU}}',
}

def clean(text):
    return text.replace('\xa0', ' ').strip()

def cell_text(cell):
    text = '<br>'.join(clean(p.text) for p in cell.paragraphs)
    return text.replace('|', r'\|')

for element in doc.element.body:
    if element.tag == qn('w:p'):
        paragraph = Paragraph(element, doc)
        text = clean(paragraph.text)
        for blip in element.iter(qn('a:blip')):
            rid = blip.get(qn('r:embed'))
            if not rid:
                continue
            part = doc.part.related_parts[rid]
            digest = hashlib.sha256(part.blob).hexdigest()
            if digest not in images:
                extension = Path(str(part.partname)).suffix
                image_path = assets / f'figure_{len(images)+1:02d}{extension}'
                image_path.write_bytes(part.blob)
                images[digest] = image_path
            image_path = images[digest]
            following = element.getnext()
            caption = ''
            if following is not None and following.tag == qn('w:p'):
                following_paragraph = Paragraph(following, doc)
                if following_paragraph.style.name == 'Caption':
                    caption = clean(following_paragraph.text)
            alt = caption or f'论文原图 {len(images)}'
            lines.extend([f'![{alt}]({image_path.relative_to(root).as_posix()})', ''])
        if not text:
            continue
        paragraph_count += 1
        if text in equations:
            lines.extend(['$$', equations[text], '$$', ''])
            math_count += 1
            continue
        style = paragraph.style.name
        if style == 'Title':
            text = '# ' + text
        elif style == 'Subtitle':
            text = '> ' + text
        elif style == 'Heading 1':
            text = '## ' + text
            chapter_started = True
        elif style == 'Heading 2':
            text = ('### ' if chapter_started else '## ') + text
        elif style == 'Caption':
            text = '*' + text + '*'
        elif all(run.bold for run in paragraph.runs if run.text.strip()):
            text = '**' + text + '**'
        else:
            text = text.replace('Nᵢ', '$N_I$').replace('Nₜ', '$N_T$')
            text = re.sub(r'https://[^\s]+', lambda m: '[' + ('论文原文' if 'arxiv.org' in m[0] else '作者代码仓库') + '](' + m[0] + ')', text)
            text = text.replace('\n', '  \n')
        lines.extend([text, ''])
    elif element.tag == qn('w:tbl'):
        table = Table(element, doc)
        rows = [[cell_text(c) for c in row.cells] for row in table.rows]
        lines.append('| ' + ' | '.join(rows[0]) + ' |')
        lines.append('| ' + ' | '.join('---' for _ in rows[0]) + ' |')
        lines.extend('| ' + ' | '.join(row) + ' |' for row in rows[1:])
        lines.append('')
        table_count += 1

content = '\n'.join(lines).rstrip() + '\n'
target.write_text(content, encoding='utf-8')
assert content.count('\n$$\n') == 4
assert table_count == len(doc.tables) == 11
assert len(images) == len(doc.inline_shapes) == 3
assert len(re.findall(r'^# ', content, re.M)) == 1
assert paragraph_count == len([p for p in doc.paragraphs if p.text.strip()])
for path in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', content):
    assert (root / path).is_file(), path
result = {'source': source.name, 'target': target.name, 'paragraphs_preserved': paragraph_count,
          'tables_preserved': table_count, 'images_preserved': len(images),
          'equations_converted_to_latex': math_count,
          'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'output_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
(root/'组会资料'/'md_conversion_checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
