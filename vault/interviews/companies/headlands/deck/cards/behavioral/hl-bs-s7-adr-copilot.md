---
id: hl-bs-s7-adr-copilot
node: behavioral.stories
type: qa
step: 39
---
## Q
S7 的三篇 ADR 分别记录了什么？在 schema pool 之上还做了什么？

## A
**三篇 ADR**：
1. 同步在**本地**运行。
2. 默认目标 = **已部署的 commit**。
3. 对一个模块**跳过 Flyway**——写成"**不要修这个**"。

**之上的东西**：一个 **on-call copilot**，轮询 Slack、PagerDuty 和 Datadog，带着上下文开一个 agent 会话，起草回复，**由我审阅后才发送**；**相邻团队采用了它**。
