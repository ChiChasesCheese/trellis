---
id: cbr-ask-triage-loop
node: ask.engineers
type: qa
step: 1
---
## Q
反问技术面的工程师：问哪两个关于失败分诊和反馈回路的问题？想听出什么？

## A
- **问法 1**："When the nightly regression has twenty failures, how do you sort real regressions from flaky tests and infrastructure noise today?"
  - 好答案：有标签、历史数据、自动重跑、隔离队列。
  - 坏答案：每个都人工看。你能马上带来价值，但会很累。
- **问法 2**："If a commit breaks something only visible on a real system, how long until someone notices, and how do you find which commit it was?"
  - 好答案：每晚或每次合入有真机回归，能自动二分查找。
  - 坏答案：发布前才发现，靠人猜是哪次提交。
- **第三个备选**："What do you like most here, and what slows you down the most?"
