---
id: tag-classification-false-negative
node: security.data-classification-and-tagging
type: qa
tags: [grown]
---
## Q
依赖“自动分类 + 基于标签的脱敏”后，治理团队最需要防范的失败模式是什么？

## A
漏标（false negative）：自动分类基于采样和模式匹配，列名含义不清、格式不标准（如把手机号存在自由文本 JSON 字段里）时可能识别不出来，而基于标签的脱敏只保护打了标签的列，于是没被识别的敏感列完全裸露且不易被发现。缓解方式是把分类作为持续任务重复运行、人工复核结果，并对高风险库在模式或数据库层级设置默认标签作为兜底。
