---
title: S7 · snowglobe-tools schema pool
aliases:
  - S7
  - schema pool
  - snowglobe-tools
tags:
  - interview/story
  - stack/snowflake
  - developer-productivity
  - ai-tooling
answers: [Q7, Q11, Q21]
stacks: [TS03, TS06]
status: verified
---

# S7 · schema pool（主动性 · 开发者效率 · AI fluency · 零拷贝克隆）

> [!abstract] 一句话
> 没人分配的活：集成测试对着共享 schema 跑迁移，两个工程师——或两个 AI 编码 agent 会话——在不同分支上就撞 DDL。我建了一个 **schema pool**：`MAIN` schema 同步到"生产实际部署的 commit"（查 GitHub Deployments API，不信 tag），每个池位是 `MAIN` 的**零拷贝克隆**（约 2 秒，拷的是微分区元数据不是数据）；会话借一个位、跑迁移和测试、归还。V2 重写带三篇 ADR，顺手修了几个真实的 Flyway 边界。

## 1. 机制

| 版本 | 做法 | 问题 / 决定 |
|---|---|---|
| V1 | 每个 `POOL_N` 直接从 `PUBLIC` 克隆 | `PUBLIC` 的状态取决于谁最后跑了什么迁移——不可预测 |
| **V2** | 先维护独立 `MAIN`，从 `repos/{owner}/{repo}/deployments?environment=production` 取当前生产 SHA 同步（tag 可能打了没部署），跑完迁移后所有池位从 `MAIN` 克隆 | ADR-0001 同步在本地跑（凭证与 checkout 一致性）· ADR-0002 默认目标 = 生产部署 SHA · ADR-0003 有意跳过 `share` 模块的 Flyway（"don't fix this"） |

Flyway 边界（Sync Failure Playbook）：
- **跨库 stream 失效顺序**：先克隆 APP_DB 再克隆 REPL_DB 会让依赖 REPL 表的 stream 失效 → 固定顺序先 REPL 后 APP，并在 `MAIN_STAGING → MAIN` 交换后自动扫描修复（Pattern A）。
- **重复的 repeatable migration**：`db/test/` 与主目录同名文件冲突 → 排除出 sync 扫描。
- **仅生产存在的依赖**：建结构空壳 stub 表满足 DDL 编译——这条最不稳，一天内十次提交才收敛。

23 次提交、全部直推 main（个人仓库）。

## 2. 为什么是好故事

- 主动性：零 ticket；看到摩擦就消除。
- database internals：零拷贝克隆为什么 2 秒（不可变微分区 + 元数据指针）；stream 对克隆顺序敏感。
- AI fluency：**"tech lead of a team of agents"**——多个 Claude Code 会话并行开发是这个工具存在的原因；rate limit 也是（每个 agent 工具有用量上限，要能同时用几个）。
- 面试里的 on-call 助手（面试时叫成了 "cheatbot"）——改名 **on-call copilot**：轮询 Slack / PagerDuty / Datadog，带上下文开对应 agent 会话，产出存为 Slack 草稿，我审后再发；相邻团队采用。

> [!warning] 证据边界
> 这是**个人**仓库，不是团队官方工具链；说 "I built it, the team adopted it" 而非 "team standard"。不用 "cheat" 这个词。

## 3. English · 首答（60 s）

> Nobody asked for this one. Our integration tests run migrations against a shared Snowflake schema, so two engineers — or two AI coding-agent sessions — on different branches collide on DDL. I built a **schema pool**: a `MAIN` schema synced to whatever commit is actually deployed to production — I query the GitHub Deployments API, not the release tag, because tags lie — and each pool slot is a **zero-copy clone** of `MAIN`. A clone takes about two seconds because it copies micro-partition metadata, not data; a session borrows a slot, runs its migrations and tests in isolation, and drops it.
>
> The second version was a rewrite with three ADRs, after the first version taught me that cloning from a shared `PUBLIC` schema is non-deterministic. I hit and fixed real Flyway edge cases — cross-database stream invalidation, which depends on clone order, so I clone the replication DB before the app DB and auto-detect the pattern after a swap; duplicate repeatable migrations; and stub tables for prod-only dependencies. It's what let me run several Claude Code sessions in parallel on the same repo — I think of it as being the tech lead of a team of agents.

**AI 工具题的完整版**（Chakra 亲历后的改写）：

> Two layers. Day to day I run Claude Code, Codex and Cursor in parallel — each has its own usage limit, so I built a schema pool of zero-copy Snowflake clones so several agent sessions can run migrations and integration tests at the same time without colliding. On top of that I built an on-call copilot: it polls Slack, PagerDuty and Datadog, opens the right agent session with that context, and drafts the reply as a Slack draft I review and send. Teams next to ours adopted it. The principle: I'm the tech lead of a team of agents, and I still own every diff.

**信任 AI 代码**：plan with the agent → TDD every phase → CI + monitoring gates；"focus on gates and thresholds, not lines of code"；in money code I read every diff myself.

## 4. 用在哪

- 回答：[[Answers#Q7]] 主动性 · [[Answers#Q11]] 定标准 · [[Answers#Q21]] ready for senior
- 亲历题：How do you use AI tools · How do you trust AI-generated code
- 技术栈：[[03-snowflake-warehouse|TS03]]（零拷贝克隆）· [[06-cicd-progressive-delivery|TS06]]（Flyway）
- 相邻：[[S6]]（同讲"主动性"的另一面）

## 5. 证据锚点

repo `snowglobe-tools`（schema-pool）：commit `42364e1`（V2）、`5d2811a`（ADR）、`0d6e94c` / `8365985`（Pattern A）、`f633677`、`c4f91bf`。
