---
id: aid-agent-friendly
node: t08.readability-testability-agent-friendly
type: qa
step: 1
tags: [摘要]
---
## Q
**Agent-friendly 设计**｜摘要 · 追问

怎样的代码库，agent 做起来既快又对？这些特点对人也有好处吗？

## A
| 特点 | 对 agent 的好处 | 对人的好处 |
|---|---|---|
| **清晰的模块边界** | 一个任务只需读一个模块，context 小 | 理解和改动的范围小 |
| **快速的测试** | 反馈回路短，能多次自检 | 本地开发更快 |
| **类型** | 挡住 hallucinated API 和参数错误 | IDE 提示、重构更安全 |
| **命名清楚、函数短** | 读代码能推出意图 | 同上 |
| **一条命令就能验证**（测试、type check、lint） | 能写进 CLAUDE.md，形成闭环 | 新人上手快 |

**核心：** agent 的能力来自环境反馈（t01）。让反馈更快、更明确，就是让环境对 agent 友好；这些也恰是对人好的工程实践。

**DORA 的相关发现：** 没有强自动化测试、成熟版本控制和快速反馈，AI 带来的变更量会变成不稳定。

**做：** 把"一条命令验证"当第一优先级。
**别做：** 为了 agent 去重写整个代码库。

**出处：** DORA《2025 State of AI-assisted Software Development》；Claude Code docs《Best practices》（Give Claude a check to run）
