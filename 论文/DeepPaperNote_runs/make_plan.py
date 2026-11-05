import json
from pathlib import Path
p=Path(__file__).parent/'deeppapernote'
d=json.loads((p/'grounding_dino_figure_table_decisions.json').read_text(encoding='utf-8'))
for x in d['decisions']:
 if x['decision']=='insert': x['visual_review']['notes']='已检查原候选及修复后的图表；主体完整、编号匹配、无正文或图注混入。'
d['decision_freeze']='complete'; d['output_language']='zh-CN'
(p/'grounding_dino_figure_table_decisions.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
plan={'output_language':'zh-CN','paper_id':'arxiv:2303.05499','paper_type':'AI_method','paper_type_rationale':'提出三阶段跨模态融合检测架构，并以跨数据集检测和消融验证。','dominant_domain':'论文2',
'must_cover':['三阶段融合与混合查询初始化','子句注意力掩码与区域词元分类','零样本协议与数据重叠','长尾及REC失败证据'],
'key_numbers':['52.5','26.1','900','256','48.1','16.1','13.1'],
'real_comparisons':['GLIP-T与同数据Grounding DINO T','DINO与Grounding DINO','LVIS上的DetCLIPv2'],
'central_claims':[{'claim':'三阶段语言融合对跨域检测有效','supporting_evidence':[{'pages':[7,8,9,14]}],'what_it_actually_proves':'同O365训练下移除融合或文本注意力降低LVIS和COCO表现。','what_it_does_not_prove':'不能证明每种分布均优于其他架构，也没有多种子显著性。'},{'claim':'预训练数据分布决定泛化边界','supporting_evidence':[{'pages':[10,12,13,24]}],'what_it_actually_proves':'RefC训练改善指代任务却降低LVIS及ODinW；增大BERT未稳定改善。','what_it_does_not_prove':'不能将其归因于唯一的架构瓶颈或宣称语言模型规模无效。'}],
'claim_boundaries':['COCO零样本是未用其图像而非类别未见','COCO与RefC存在图像泄漏风险'],
'negative_or_limiting_results':['LVIS稀有类落后GLIP','闭集12轮训练48.1低于DINO49.0','REC未训练时准确率偏低'],
'mechanism_result_map':['编码器融合对应LVIS16.1降至13.1','静态查询对应LVIS13.6，逐行差为2.5而正文写3.0，记录差异'],
'comparative_positioning':['比GLIP的单阶段融合更深入；同时DINO本体已很强，不能全归功于文本'],
'reuse_takeaways':['锁定检查点数据组成后再复现','分别记录罕见类别、跨域中位数和属性指代'],
'followup_questions':['固定预训练预算后子句掩码是否改善类别顺序鲁棒性？','同数据条件下加入拒识阈值是否降低不存在对象误检？'],
'section_plan':[]}
focus={
'研究问题':('将封闭类别检测推广到语言指定的对象，解释三处融合相比固定分类头的必要性。',[2,3,4]),
'数据与任务定义':('区分COCO跨数据集迁移、LVIS长尾、ODinW跨域及REC单框准确率，注明预训练数据。',[8,9,10,12,20]),
'方法主线':('重建六层特征增强、文本引导900查询选择、六层解码及区域词元匹配损失的张量流程。',[5,6,7,8,9,20]),
'关键结果':('用表格对比同数据基线、逐项移除消融，呈现REC及数据配方改变后的泛化代价。',[8,10,11,12,13,14]),
'深度分析':('把区域级对齐与查询路由对应实验收益，讨论稀有类、计算成本和冻结DINO的复现路径。',[14,20,21,22,23,24,26]),
'局限':('区分未见图像和未见类别，说明COCO与RefC图像重叠、误检、无分割以及评测统计不足。',[9,12,14,24])}
for s,(t,pg) in focus.items(): plan['section_plan'].append({'section':s,'focus':t,'evidence_sources':[{'pages':pg}]})
(p/'note.plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
