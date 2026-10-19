---
id: nr-amz-s3-relp
node: amazon.s3
type: qa
step: 4
---
## Q
【ACH 费用 NULL 传播事故（最难的 bug · fail loudly）】换成别的 LP 问时，强调哪一段？

## A
- **Dive Deep**：切片 → 单笔 → 回溯 → 读两个重载；强调排除时序/stream 的证据
- **Ownership**：不是 assignee，转给自己；止血之后继续 own postmortem、重载合并、DROP；别说止血 PR 是我的
- **Insist on the Highest Standards**：止血只修一例，我要让这类 bug 不可能；单函数 + versioned DROP + e2e
- **Have Backbone**：有人提议排除 ACH，我带着数字说不；只有顶住压力，没有 disagree-and-commit 后半
- **Customer Obsession**：~200 个商户被静默地错误计费；fix forward 需要更正分录；没有客户反馈数据，别编
- **Bias for Action**：转给自己，线程里几分钟给出答案；速度来自对 promote 链路的全局图景
- **Earn Trust**：postmortem 写出我们自己的测试为什么没看见（4 个缺口）
