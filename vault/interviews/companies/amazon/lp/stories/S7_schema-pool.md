# S7 · schema pool（主动性 · 开发者效率 · AI fluency）

> 来源：`core/stories/S7 Schema pool.md`（status: verified）。**个人仓库 `snowglobe-tools`，不是团队官方工具链。**
> 主 LP：**Invent and Simplify · Bias for Action · Ownership**；副：Learn and Be Curious · Frugality · Think Big。
> 一句话：*"Nobody assigned it: two engineers, or two AI agents, collided on shared-schema DDL, so I built a pool of zero-copy clones."*

## 1. 数字

| 数字 | 口径 |
|---|---|
| 克隆约 2 秒 | 拷的是微分区元数据不是数据 |
| 23 次提交，全部直推 main | 个人仓库 |
| 3 篇 ADR（V2） | ADR-0001 本地同步 · 0002 默认目标 = 生产部署 SHA · 0003 跳过 `share` 模块 Flyway |
| 相邻团队采用 on-call copilot | 来自 S7 笔记；采用者数量无记录 |
| 其余 | 无团队级采用数据 【待 Chi 补：团队/队友里有多少人用过 schema pool？】 |

## 2. 60–90 秒口播版（≈ 190 词）

> Nobody asked for this. Our integration tests run migrations against a shared Snowflake schema, so two engineers — or two AI coding-agent sessions — on different branches collide on DDL. I built a schema pool. A `MAIN` schema is synced to whatever commit is actually deployed to production — I query the GitHub Deployments API rather than trust the release tag, because a tag can be cut and never deployed. Each pool slot is a zero-copy clone of `MAIN`, about two seconds, because a clone copies micro-partition metadata, not data. A session borrows a slot, runs migrations and tests in isolation, and drops it.
>
> Version one cloned from a shared schema whose state depended on who last ran a migration, so version two was a rewrite with three ADRs. I fixed real edge cases: cross-database streams break depending on clone order, so I clone the replication DB before the app DB and auto-detect the pattern after a swap. It's what lets me run several Claude Code sessions in parallel on the same repo. I think of it as being the tech lead of a team of agents — and I still own every diff.

## 3. 2 分钟版（≈ 300 词）

> **The friction.** Integration tests ran migrations against a shared schema. Two people, or increasingly two AI agent sessions, would collide on DDL and break each other's runs. No ticket, no owner.
>
> **V1.** Pool slots cloned from `PUBLIC`. The problem: `PUBLIC`'s state depends on whoever ran a migration last, so a slot wasn't reproducible.
>
> **V2 design.** A separate `MAIN` schema, synced from the production-deployed commit. I read the GitHub Deployments API for the production environment, since tags can be cut without being deployed. After migrations, all slots clone from `MAIN`. Three ADRs: sync runs locally for credentials and checkout consistency; the default target is the production-deployed SHA; and deliberately skip Flyway for the `share` module — "don't fix this" documented.
>
> **Hard parts.** Cross-database stream invalidation: cloning the app DB before the replication DB breaks streams that depend on replication tables, so the order is fixed — replication first — with an automatic repair after a swap. Duplicate repeatable migrations from a test directory: excluded from the scan. Prod-only dependencies: structure-only stub tables so DDL compiles — the least stable, it took about ten commits in a day to settle.
>
> **Why it matters.** I run Claude Code, Codex and Cursor in parallel — each has its own usage limits — and several agent sessions can run migrations and integration tests concurrently. On top I built an on-call copilot that polls Slack, PagerDuty and Datadog, opens the right agent session with context, and drafts replies I review before sending; adjacent teams adopted it. **Boundary:** it's my personal repo; I built it and the team used it, it isn't the team's official toolchain. In money code I read every diff.

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Invent and Simplify** (P) | "A two-second clone replaced the whole 'wait for your turn on the shared schema' problem." | 零拷贝克隆；MAIN 同步到部署 SHA | 说成团队标准 |
| **Bias for Action** (P) | "Nobody assigned it; I started with V1 in an afternoon and rewrote after it taught me why `PUBLIC` is non-deterministic." | V1 快速上、V2 改；23 次直推 | — |
| **Ownership** (P) | "It's outside my job description, and I maintain it." | 无 ticket；ADR；Sync Failure Playbook | — |
| **Learn and Be Curious** (S) | "I had to learn how zero-copy clones and cross-database streams actually behave." | 微分区元数据；stream 对克隆顺序敏感 | — |
| **Frugality** (S) | "Clones cost metadata, not storage." | 2 秒；不复制数据 | 无具体费用数字，别编 |
| **Think Big** (S) | "The same tool made a 'team of agents' workflow possible." | tech lead of a team of agents；on-call copilot | 夸大成「改变了团队」 |

## 5. 追问（≥5）

1. **Why GitHub Deployments API, not tags?** → 打了 tag 没部署；Deployments API 记录生产环境实际部署的 SHA。
2. **Why is a clone 2 seconds?** → 不可变微分区 + 元数据指针，不拷数据。
3. **What broke in V1?** → `PUBLIC` 的状态取决于谁最后跑了什么迁移，不可预测。
4. **Cross-database streams?** → 先克隆 APP_DB 再 REPL_DB 会让依赖 REPL 表的 stream 失效；固定顺序先 REPL 后 APP + `MAIN_STAGING → MAIN` 交换后自动扫描修复（Pattern A）。
5. **How do you trust AI-generated code?** → plan with the agent → TDD every phase → CI + monitoring gates；关注 gates 和 thresholds 而非行数；money code 里我读每一个 diff。
6. **Who uses it?** → 【待 Chi 补：团队里其他工程师是否用了 schema pool？人数/频率】；on-call copilot 相邻团队采用（人数无记录）。
7. **Why direct-push to main?** → 个人仓库，不影响团队代码；诚实说明。

## 6. Senior 升级点（bar = senior）

当前档位：**initiative + mechanism 是 senior 级，但 scope 停在个人工具**。要升到 senior 需要「别人因你而更强」的证据。
- 【待 Chi 补：除你以外有几位工程师/agent 工作流依赖 schema pool？有没有人因为它省了可量化的时间（例如 CI 排队、DDL 冲突次数从 X 降到 Y）？】
- 【待 Chi 补：on-call copilot 的相邻团队是谁（角色/团队，不点名）、采用后你收到什么反馈？】
- 【待 Chi 补：有没有尝试推动团队把它升级为官方工具链，对方怎么说？（Ownership beyond your task + 现实感）】
- 升级句：「I built the guardrails that let several agents work in parallel — and the part I'm proudest of is the ADR that says what we deliberately did not fix.」
