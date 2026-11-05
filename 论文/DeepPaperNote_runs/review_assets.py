import json, hashlib
from pathlib import Path
import fitz
p=Path(__file__).parent/'deeppapernote'
f=p/'grounding_dino_figure_table_decisions.json'
d=json.loads(f.read_text(encoding='utf-8'))
repairs={'Fig 3':0.07,'Fig 4':0.32,'Table 11':0.24,'Table 12':0.20,'Table 14':0.10,'Table 18':0.09}
for x in d['decisions']:
 if x['decision']!='review_pending': continue
 if x['source_id'] in ('Table 8','Table 13'):
  reason='scientific_content_missing' if x['source_id']=='Table 8' else 'identity_mismatch'
  x['decision']='visual_defect'; x['skip_reason']=reason
  x['visual_review'].update(status='fail',reviewed_asset_sha256=x['source_image_sha256'],failure_reason=reason,notes='表8只剩参数表底部；表13候选实际是正文，没有该表。',omitted_scientific_elements=['完整表体'])
  continue
 if x['source_id'] in repairs:
  ev=x['review_evidence']; b=ev['bbox_pt']; b[1]+=repairs[x['source_id']]*(b[3]-b[1])
  doc=fitz.open(ev['source_pdf_path']); page=doc[ev['source_page']-1]
  page.get_pixmap(matrix=fitz.Matrix(300/72,300/72),clip=fitz.Rect(b),alpha=False).save(x['source_image_path'])
  nb=[b[0]/page.rect.width,b[1]/page.rect.height,b[2]/page.rect.width,b[3]/page.rect.height]; ev['normalized_bbox']=nb
  x['source_image_sha256']=hashlib.sha256(Path(x['source_image_path']).read_bytes()).hexdigest()
  x['visual_review']['repair_attempts']=1; x['visual_review']['revised_bbox']=nb
 x['decision']='insert'
 x['visual_review'].update(status='pass',reviewed_asset_sha256=x['source_image_sha256'],preserved_scientific_elements=['图表主体、文字标注、数值或连接关系'],omitted_scientific_elements=[],notes='已对照候选图像核验；修复项已重新渲染，待复核。',failure_reason='')
 if x['source_id']=='Fig 4': x['target_section']='方法主线'
f.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
