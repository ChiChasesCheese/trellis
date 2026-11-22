---
id: aie-query-expansion-hyde-multi
node: t03.query-rewriting-expansion-hyde-multi-query-sub-q
type: qa
step: 2
tags: [考点]
---
## Q
**Query expansion · HyDE、multi-query、sub-question**｜考点 · 追问

用户问题很短、措辞和文档对不上（问「怎么退钱」，文档写的是「refund policy」）。三种常见改写：HyDE、multi-query、sub-question decomposition。各自做什么、各多付什么？

## A
| 做法 | 做什么 | 多付的 |
|---|---|---|
| **HyDE**（Hypothetical Document Embeddings） | 让模型先针对问题写一段**假想的答案文档**，用它的 embedding 去检索 | 一次生成调用；假想文档可能含错误细节 |
| **multi-query** | 把问题改写成几种不同说法，各检索一次，结果合并（常配 RRF） | N 次检索，可能多次模型调用 |
| **sub-question decomposition** | 把复合问题拆成几个子问题，分别检索，再汇总回答 | 多次检索加汇总调用，延迟串联 |

**HyDE 的原理：** 问题和文档在语言上不对称（问句 vs 陈述），而「文档和文档」更像。假想文档里的细节可能是编的，但 encoder 会把它压成一个向量，真正取回的是语料库里**真实**的相近文档（Gao 等 2022，零样本，不需要相关性标注）。

**什么时候用：**
- 问题和文档措辞不匹配 → HyDE、multi-query；
- 一个问题里含多个事实 → sub-question；
- 对话追问 → 先做 query rewriting（见上一张卡）。

**怎么判断值不值：** 用检索评测集比较「加改写前后」的 recall@k，再看延迟。不显著提升就别加。

<details class="pt" markdown="1"><summary>出处</summary>

HyDE：Gao 等《Precise Zero-Shot Dense Retrieval without Relevance Labels》arxiv.org/abs/2212.10496（2026-11-21 读摘要）；改写增加模型调用是 Huyen ch6 §Query rewriting 的前提

</details>
