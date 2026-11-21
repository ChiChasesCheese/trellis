---
id: aie-chunking-strategies
node: t03.chunking-semantic-chunking
type: qa
step: 1
tags: [摘要]
---
## Q
**Chunking · 几种切法**｜摘要 · 必会

一份 50 页的手册要放进 RAG。固定每 2,048 个字符切一刀，有什么问题？还有哪些切法？

## A
**问题：** 固定长度会在句子、段落中间切断。例如 "I left my wife a note" 被切成 "I left my wife" 和 "a note"，两块都不能单独表达原意。

| 切法 | 做法 | 适合 |
|---|---|---|
| 固定长度 | 按字符、单词、句子或段落数切成等长 | 最简单，作 baseline |
| **Recursive** | 先按章节切；太长的再按段落切；还太长再按句子 | 尽量不拆开相关文字 |
| 按结构 | 按文档本身的结构：代码用专门的 splitter，问答文档一问一答为一块 | 有明确结构的文档 |
| 按 token | 用生成模型 tokenizer 的 token 作单位切 | 方便匹配下游模型；换了 tokenizer 的模型要重建索引 |
| **加 overlap** | 相邻 chunk 重叠一小段，例如 chunk 2,048 字符、重叠 20 字符 | 保证边界处的信息至少完整出现在一个 chunk 里 |

**限制：** chunk 不能超过生成模型的最大 context length；做 embedding 检索时，也不能超过 embedding 模型的输入上限。中文等语言可能需要与英文不同的切法。

**semantic chunking（按语义切）：** 目标是让每块是一个"意思完整的单位"，而不是一刀切；上面的 recursive 和按结构都是朝这个方向走。没有放之四海皆准的最佳 chunk 大小或 overlap，要在你的数据上实验。

**出处：** Huyen《AI Engineering》ch6 §Retrieval Optimization → Chunking strategy
