---
id: hl-bq-q19-followups
node: behavioral.question-bank
type: qa
step: 40
---
## Q
"想改的设计"之后的追问：为什么用配置表？V1 哪里坏了？
Why a config table? What broke in V1?

## A
- **Why a config table?** 六个解析器**重复着同一张偏移表**。
- **What broke in V1?** 源状态是**历史相关**的（取决于最后谁迁移过），所以各 slot 不可复现。
