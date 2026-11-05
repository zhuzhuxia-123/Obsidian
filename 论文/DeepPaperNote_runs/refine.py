from pathlib import Path
import json
p=Path(__file__).parent/'deeppapernote'; f=p/'note.md'; t=f.read_text(encoding='utf-8')
lint=json.loads((p/'note_lint.json').read_text(encoding='utf-8'))
for x in lint['mixed_language_issues']:
 s=x['line']
 if s.startswith('| T 模型'): t=t.replace(s,'| 训练配方 | COCO直接评估 | LVIS评估 | ODinW评估 |'); continue
 if s.startswith('令视觉特征'):
  t=t.replace(s,'视觉与文本特征分别记为：\n\n$$\nX_I\\in\\mathbb{R}^{N_I\\times d},\\qquad X_T\\in\\mathbb{R}^{N_T\\times d}.\n$$\n\n论文设置特征维度为256；视觉词元通常超过一万个，文本长度上限为256。查询位置索引为：'); continue
 # 按完整句子重组段落，避免长段内堆叠模型缩写。
 t=t.replace(s,s.replace('。','。\n\n').strip())
t=t.replace('建议位置：局限中的细粒度语言问题。','建议位置：我的笔记，作为语言编码器实验的补充。').replace('建议位置：局限中的评测口径。','建议位置：我的笔记，作为伪标注实验的补充。')
f.write_text(t,encoding='utf-8')
