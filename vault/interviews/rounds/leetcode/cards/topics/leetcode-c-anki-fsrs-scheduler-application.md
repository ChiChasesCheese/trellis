---
id: leetcode-c-anki-fsrs-scheduler-application
node: topics.uncategorised
type: qa
anki: 1787361361593
tags: [algorithm::optimization, algorithm::spaced-repetition, algorithm::state-model, application, case, case::anki-fsrs-scheduler, category::developer-infrastructure, chapter::07, chapter::18, leetcode, system::anki, system::fsrs]
---
## Q
Anki FSRS 的 stability、retrievability 和 desired retention 分别控制什么？

## A
stability 表示记忆衰减速度，retrievability 是当前回忆概率估计，desired retention 是允许它下降到的目标。scheduler 据此计算下一 interval；目标越高，复习量越大。

**Evidence**

Anki 官方手册定义 FSRS 状态、desired retention 与参数优化；开源 FSRS 仓库提供模型实现。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FAnki%20FSRS%EF%BC%9A%E9%81%97%E5%BF%98%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%A4%8D%E4%B9%A0%E8%B0%83%E5%BA%A6%E4%BC%98%E5%8C%96)
