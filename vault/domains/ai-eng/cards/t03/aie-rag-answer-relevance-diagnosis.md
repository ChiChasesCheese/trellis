---
id: aie-rag-answer-relevance-diagnosis
node: t03.rag-faithfulness-answer-relevance
type: qa
step: 2
tags: [考点]
---
## Q
**RAG 生成端评测 · 把检索和生成的指标分开看**｜考点 · 必会

一次评测里得到这样的数字：context precision 很高，faithfulness 却很低。另一次是 precision 很低，但 faithfulness 很高、用户仍不满意。分别说明什么？下一步改哪里？

## A
**faithfulness** 问：回答是否被资料支持。**answer relevance** 问：回答是否切题、回答了用户问的事。两者和检索指标共同构成一张诊断表：

| 检索指标 | faithfulness | 结论 | 改哪里 |
|---|---|---|---|
| 高 | **低** | 资料对，模型没老实用，或编了东西 | prompt（要求只依据资料、拒答）、模型、context 的顺序和长度 |
| **低** | 高 | 模型忠实地复述了**错误**或不相关的资料，所以用户不满意 | 检索：chunking、embedding、hybrid、reranking |
| 高 | 高 | 通常没问题；若仍不满意，看是否切题 | answer relevance、用户问题改写 |
| 低 | 低 | 两头都有问题 | 先修检索，再修生成 |

**要点：** "忠实"不等于"正确"。模型忠实地依据一份**错误的资料**，faithfulness 仍然是高分。所以必须同时有检索指标和最终回答质量的评测。

**回到题目：**
- 第一次：检索没问题，改生成端。
- 第二次：改检索端，faithfulness 高并不代表答对。

**做法：** 书里的建议是限制模型只使用给出的 context，并用 AI judge 检查回答是否被 context 支持。

**出处：** Huyen《AI Engineering》ch4 §Factual consistency（local factual consistency）；ch6 §Comparing retrieval algorithms（逐组件评测）；ch5 §How to Restrict a Model's Knowledge to Only Its Context
