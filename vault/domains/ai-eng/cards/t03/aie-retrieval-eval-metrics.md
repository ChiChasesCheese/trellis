---
id: aie-retrieval-eval-metrics
node: t03.retrieval-evaluation-recall-k-precision-mrr-ndcg
type: qa
step: 1
tags: [摘要]
---
## Q
**Retrieval evaluation · 四个指标**｜摘要 · 必会

怎么给 retriever 打分，而不看最终回答？context precision、context recall 分别是什么？排名重要时用什么？

## A
**先准备评测集：** 一批测试 query，加上每个 query 对应的哪些文档相关、哪些不相关的标注（可以由人标，也可以由 AI judge 标；AI judge 指用另一个模型按标准给输出打分，t05 详讲）。

| 指标 | 问的是 |
|---|---|
| **Context precision**（precision） | 取回的文档里，有多少比例是相关的 |
| **Context recall**（recall） | 所有相关的文档里，有多少比例被取回了 |
| **MRR**（mean reciprocal rank） | 第一个相关文档的名次的倒数，对多个 query 取平均 |
| **nDCG、MAP** | 关心整体排序：越相关的越靠前，得分越高 |

**注意：**
- recall 需要标出库里**所有**相关文档，很贵；很多 RAG 框架只支持 precision，因为只要判断已取回的文档是否相关，AI judge 就能做。
- 对 embedding 检索，还要单独评 embedding 质量（如 MTEB）。
- 评一个检索器，最终要看它是否帮助系统生成高质量回答，所以**检索指标和最终答案质量要分开看**。

**出处：** Huyen《AI Engineering》ch6 §Comparing retrieval algorithms（context precision / recall、NDCG、MAP、MRR）
