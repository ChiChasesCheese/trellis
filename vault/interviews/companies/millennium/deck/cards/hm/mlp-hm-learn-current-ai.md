---
id: mlp-hm-learn-current-ai
node: hm.learning
type: qa
step: 3
---
## Q
**跟上新技术与用 AI 工具**｜经理面与行为面

“How do you stay current with technology trends? How do you use AI tools, and how do you trust the code they write?”

## A
这一题 Millennium 会认真听，岗位本身强调 AI 基础设施和智能体工具。答法是做出来的东西，不是读了什么。

- **学新领域的办法：** 为了弄懂金融，你做了 Quant-Stroller，用做的方式学：point-in-time 数据（只用当时已知的信息，避免前视偏差）、净化交叉验证（purged cross-validation）、成本模型。
- **日常用法：** 同时跑 Claude Code、Codex 和 Cursor，每个工具有自己的用量上限，所以做了 schema pool，让多个智能体会话并行跑迁移和集成测试而不互相冲突。
- **on-call 助手：** 轮询 Slack、PagerDuty、Datadog，带上下文打开对应的智能体会话，把回复存成 Slack 草稿，由你审过再发；相邻团队采用了。
- **怎么信任 AI 代码：** 和智能体先做计划，每个阶段测试先行，CI 和监控设闸门和阈值；钱相关的代码每个 diff 自己读。

**英文答法。**
- Day to day I run **Claude Code, Codex and Cursor in parallel**, and I built a **schema pool** so several agent sessions can run migrations and tests without colliding.
- On top of that, an **on-call copilot** polls Slack, PagerDuty and Datadog, opens the right agent session, and drafts the reply for me to **review and send**.
- I'm the **tech lead of a team of agents**, and I still **own every diff**.
- To trust the code: **plan with the agent, test-first each phase, CI and monitoring gates** — and in money code I read every diff myself.

**追问。**
- **How do you learn a new domain?** By building in it: Quant-Stroller taught me what survives costs and out-of-sample tests.
- **Did AI change your work on the resume?** I moved legacy Ruby and Kotlin logic to Snowflake and Java with Claude Code for review, test generation and refactoring, keeping behavioural parity through tests.
- **Where do you not trust it blindly?** In money code I read every diff myself; gates and thresholds, not lines of code, are my trust mechanism.
