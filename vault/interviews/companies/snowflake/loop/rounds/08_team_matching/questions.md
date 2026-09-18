# Team Matching 轮 —— 题库（10 题）+ 反问

> 来源：`catalog/raw/bq_hm_recruiter.md` §4（GenSWE 官方；Blind z4cg3oq0 2025-06 一手：全过后 headcount 被占、新 HM 重面、10+ 天无回音；Blind bkgoqjdw 实习 team matching "losing hope"）。形式：HM 30–45 min。练习：`python3 loop/mock.py bq team -n 3 -m 3`。
> **一句话**：这是"团队要不要你 + headcount 还在不在"的真实门槛。目标：让 HM 在会后能一句话向 recruiter 说清你为什么适合这个组。

## 三个方向偏好（先说，带理由）

| 方向 | 对应 org（公开可查） | 我的理由（一句） |
|---|---|---|
| Tasks / Dynamic Tables / 调度 | Cloud Services（serverless tasks、Dynamic Tables） | 两年重度使用 Streams/Tasks，知道 stream staleness 与 DAG 部分失败的痛 |
| Metering / Billing | Billing Platform（Menlo Park） | 结算级对账迁移到计量级对账；AI token 计量的归因问题 |
| FDB / Unistore / Postgres | Database Engineering（Menlo Park / Bellevue / Berlin） | 结算 OLTP 该放 Hybrid Table 还是 Postgres，我有真实负载可比 |

## 题目

| 问题原文 | 考什么 | 踩雷点 |
|---|---|---|
| "What problems do you want to work on?" | 偏好是否具体、是否与团队重合 | "都行" |
| "Where would you contribute in six months?" | 把团队的 scope 映射到自己做过的事 | 没听懂团队 scope 就答 |
| "How do you ramp up on a big codebase?" | 方法：入口 → 测试 → 一个小改动上线 | "读文档" |
| "What did you like least about your team?" | 诚实但不抱怨 | 吐槽 manager |
| "On-call?" | 真实经验（[[S3]]/S9）+ 对 pager 频率的提问 | 说"不喜欢" |
| "3 days in office?" | 直接回答；问执行口径 | 含糊 |
| "How do you use AI tools?" | 简历 bullet 4 + snowglobe-tools；"tech lead of agents" | 说"不用" |
| "Learn a new tech quickly?" | [[S1]] 定宽解析 / Terraform grant | 无 |
| "Questions about the team?" | pager 频率、RTO 执行、headcount、第一个项目 | 没问题 |
| "Anything that would make you say no?" | 诚实边界（on-call 强度、RTO） | "没有" |

## 反问（每次挑 3 个，见 `../../../06-questions-to-ask.md` §C/§D）

- "What's the one system on this team you wish someone would own end to end?"
- "What does on-call look like — pager frequency, rotation size?"
- "Is the headcount for this role already approved, and what's the timeline after this conversation?"（一手风险，必问）
- "How is the 3-day RTO applied on this team in practice?"
- "How are CoCo / Claude Code used in the team's own workflow?"
