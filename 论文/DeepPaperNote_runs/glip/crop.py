import json, hashlib
from pathlib import Path
import pymupdf
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
decisions = json.loads((root/'decisions.json').read_text(encoding='utf-8'))
pdf_path = json.loads((root/'manifest.json').read_text(encoding='utf-8'))['pdf']['path']
doc = pymupdf.open(pdf_path)
# Bounds measured against the 816×1056 source-page previews.
crops = {
    'Figure 1': (2, 68, 124, 580, 323),
    'Figure 2': (2, 592, 81, 730, 323),
    'Figure 3': (7, 434, 94, 710, 283),
    'Figure 4': (8, 96, 94, 352, 208),
    'Figure 5': (8, 434, 95, 707, 283),
    'Table 2': (6, 64, 212, 383, 391),
    'Table 3': (6, 410, 93, 729, 221),
}
sheet = Image.new('RGB', (1200, 1500), '#eeeeee')
for i, item in enumerate(decisions['decisions']):
    key = item['source_id']
    if key in crops:
        page_no, x0, y0, x1, y1 = crops[key]
        page = doc[page_no-1]
        normalized = [x0/816, y0/1056, x1/816, y1/1056]
        bounds = [normalized[j]*(page.rect.width if j%2==0 else page.rect.height) for j in range(4)]
        path = root/'assets'/'images'/('glip_'+key.lower().replace(' ','_')+'.png')
        page.get_pixmap(dpi=300,clip=pymupdf.Rect(bounds),alpha=False).save(path)
        item.update(source_image_path=str(path), source_image_filename=path.name,
                    relative_markdown_embed=f'![{key}](images/{path.name})',
                    materialization_status='pending', visual_quality_status='usable_candidate',
                    review_evidence=dict(candidate_path=str(path),page_preview_path=str(root/'assets'/'page_previews'/f'page_{page_no:03d}.png'),
                      source_pdf_path=pdf_path,source_page=page_no,caption=item['caption'],bbox_pt=bounds,normalized_bbox=normalized,render_dpi=300))
    path = Path(item['source_image_path'])
    item['source_image_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    item['decision'] = 'review_pending'
    im = Image.open(path).convert('RGB')
    im.thumbnail((575,265))
    x, y = i%2*600, i//2*300
    sheet.paste(im,(x,y+22))
    ImageDraw.Draw(sheet).text((x+5,y+3),key,fill='black')
sheet.save(root/'review.png')
(root/'review_decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2),encoding='utf-8')
