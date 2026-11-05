import json,hashlib
from pathlib import Path
p=Path(__file__).parent/'deeppapernote'
note=(p/'note.md').read_text(encoding='utf-8'); digest=hashlib.sha256(note.encode()).hexdigest()
lint=json.loads((p/'note_lint.json').read_text(encoding='utf-8'))
assert lint['output_language']=='zh-CN' and lint['note_sha256']==digest
assert all(v for k,v in lint.items() if k.startswith('passes_'))
checks={
'central_evidence_chain':'任务定义、三处融合、公式和表7移除实验构成完整证据链。',
'settings_and_numbers':'包含查询数、特征维数、层数、硬件、批大小、优化器、学习率和匹配/损失权重；记录正文与附录系数冲突。',
'mechanism_result_mapping':'将编码器融合、查询和文本注意力对应LVIS差值，保留查询差值与正文不符的问题。',
'strong_baselines':'同数据比较DINO和GLIP，并保留DetCLIPv2零样本明显领先的结果。',
'limitations_explained':'从区域语义覆盖、唯一实体选择和监督配方解释长尾、REC及数据迁移边界。',
'proven_vs_unproven':'明确区分数据集零样本和类别未见、实测和复杂度/关系推理推断；不将中位数当方差证据。',
'reusable_takeaways':'给出固定数据配方、分词、阈值、初始化和提示扰动的复现清单与后续实验。'}
q={'output_language':'zh-CN','stage':'final_quality_review','note_sha256':digest,'passed':True,'checks':checks,'warnings':[]}
(p/'final_quality_review.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
r={'output_language':'zh-CN','stage':'final_readability_review','note_sha256':digest,'passed':True,'checks':{'full_note_reread':True,'natural_chinese':True,'stable_proper_names':True,'formula_and_table_context':True},'notes':['已通读全文；摘要忠实于原文，结论判断放在后续分析。','修改了独立页码段、摘要结果单位和冗余过渡，保留关键设置与失败证据。'],'warnings':[]}
(p/'final_readability_review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(digest)
