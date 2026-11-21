---
id: aie-judge-prompt-and-scoring
node: t05.llm-as-judge
type: qa
step: 4
tags: [实践]
---
## Q
**LLM-as-judge · 怎么写 judge 的 prompt、选打分方式**｜实践 · 必会

团队写了 judge prompt："给这个回答打 1 到 10 分"，结果同一个回答多次打出 6、8、7 分。应该怎么改这个 prompt 和打分方式？

## A
**judge prompt 要写清三件事：**
1. **任务：** 要评什么（例：判断回答与问题的相关性）；
2. **标准：** 具体怎么判（越详细越好）；
3. **打分方式：** 可选类别、离散数字、连续数字。

**打分方式的选择（书里的 Tip）：**

| 方式 | 评价 |
|---|---|
| **分类**（好 / 坏，相关 / 不相关 / 中性） | judge 在**分类上比数字更稳** |
| **离散数字**（1–5） | 其次；范围越宽，效果越差，典型是 1–5 |
| 连续数字（0–1） | 最差 |

模型更擅长文字而不是数字。

**回到题目：** 去掉 1–10 的宽范围，改成**二元好 / 坏**，并为"好"和"坏"各写清标准和例子；要求先给理由再给结论，便于审计。

```
你要判断回答是否忠实于给定资料。
标准：回答中每一条陈述都能从资料中得到支持，才算"忠实"。
- 忠实：<例子 + 为什么>
- 不忠实：<例子 + 为什么>
先写理由，再输出 PASS 或 FAIL。
资料：{context}
回答：{answer}
```

**其他要点：**
- 流行的工具对同一个词（如 faithfulness）的提示和打分各不相同：MLflow 是 1–5，Ragas 是 0/1，LlamaIndex 是 YES/NO，**分数不可互相比较**；
- judge 的 temperature 设为 0 减少波动（但不保证一致）；
- 判断对象不同，用法不同：单独打分、对照 reference、pairwise 比较。

**出处：** Huyen《AI Engineering》ch3 §How to Use AI as a Judge（judge prompt 三要素、Tip、Table 3-4）；ch4 §Evaluate your evaluation pipeline（temperature 0）
