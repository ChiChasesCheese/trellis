---
id: leetcode-c-duolingo-half-life-regression-application
node: topics.uncategorised
type: qa
anki: 1787361361696
tags: [algorithm::half-life-regression, algorithm::predictive-model, algorithm::spaced-repetition, application, case, case::duolingo-half-life-regression, category::developer-infrastructure, chapter::09, chapter::18, leetcode, system::duolingo]
---
## Q
Half-Life Regression 如何把复习历史变成当前 recall probability？它和固定 Leitner box 有什么本质区别？

## A
模型先用 learner/item/history features 预测 half-life，再结合 elapsed time 计算记忆概率。固定 box 只有离散统一间隔，HLR 能对不同人和知识点个体化。

**Evidence**

Duolingo HLR 论文公开了 half-life prediction、forgetting curve 与大规模语言练习数据评估。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FDuolingo%20Half-Life%20Regression%EF%BC%9A%E9%A2%84%E6%B5%8B%E9%81%97%E5%BF%98%E5%86%8D%E6%8E%92%E7%BB%83%E4%B9%A0)
