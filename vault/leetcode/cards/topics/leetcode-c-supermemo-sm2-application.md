---
id: leetcode-c-supermemo-sm2-application
node: topics.uncategorised
type: qa
anki: 1787361362747
tags: [algorithm::heuristic-update, algorithm::spaced-repetition, algorithm::state-machine, application, case, case::supermemo-sm2, category::developer-infrastructure, chapter::18, leetcode, system::supermemo-sm-2]
---
## Q
SM-2 的 repetitions、interval、easiness factor 分别如何响应一次失败？为什么它只是 heuristic？

## A
失败会重置 repetition 并把 interval 拉回较短值；quality 同时影响 easiness，后续成功增长速度随之改变。更新公式来自经验规则，不是从个人历史拟合出的概率模型。

**Evidence**

SuperMemo 官方 SM-2 页面给出 quality grades、interval recurrence、easiness update 与 failure reset。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FSuperMemo%20SM-2%EF%BC%9A%E8%AF%84%E5%88%86%E9%A9%B1%E5%8A%A8%E7%9A%84%E9%97%B4%E9%9A%94%E7%8A%B6%E6%80%81%E6%9C%BA)
