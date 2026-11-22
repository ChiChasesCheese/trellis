---
id: aie-benchmark-integrity
node: t05.benchmark-integrity-contamination-saturation-gam
type: qa
step: 1
tags: [摘要]
---
## Q
**Benchmark integrity · 为什么公开榜单不能代替自家评测**｜摘要 · 必会

老板问：「既然榜单上这个模型第一，为什么还要花两个月建我们自己的评测集？」给出理由。

## A
| 问题 | 机制 | 后果 |
|---|---|---|
| **contamination** | 模型训练时见过测试题（从网上收集训练数据时混入、同源数据、有意加入） | 高分来自记忆。只在 benchmark 数据上训练的 100 万参数小模型可近乎满分（Schaeffer 2023） |
| **saturation** | 模型普遍逼近满分，题目区分不开 | 榜单要换新题；Hugging Face 的榜单在不到一年里整体更换，用 MMLU-PRO 替 MMLU、MATH lvl 5 替 GSM-8K |
| 不匹配 | 榜单测的能力不是你的任务 | 榜首模型在你的任务上未必最好 |
| 汇总任意 | 选哪些题、怎么加权 | 排名因权重而变 |

**还有一个旁证：** 同一家厂商的模型更新后，性能在不同 benchmark 上有升有降（Chen 等 2023 对 GPT-3.5 和 GPT-4 在 2023 年 3 月与 6 月的比较）。说明总排名第一不等于你的用例最好。

**benchmark 方能做的：** 保留一部分私有 hold-out 数据，并提供自动评测工具；披露训练数据中有多少比例是 benchmark，以及干净样本上的得分。

**对你：**
1. 公开榜单只用来过滤，挑 3–5 个候选；
2. 自家评测集别发布到网上，避免进入未来模型的训练数据；
3. 定期补入新的失败样本；
4. 评测集用了很久之后也会「过期」，要换新题。

**出处：** Huyen《AI Engineering》ch4 §Navigate Public Benchmarks（Data contamination、Note on saturation、Are OpenAI's Models Getting Worse）
