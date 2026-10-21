# S7 · 没人要的工具：schema pool，以及为什么克隆只要 2 秒（自主性 · 好奇心 · 确定性）

用于：something you built unasked / curiosity about internals / a design you rewrote / how you use AI。

**Hook：「Nobody assigned it: two engineers, or two AI agents, collided on shared-schema DDL, so I built a pool of two-second zero-copy clones.」**

## 数字

- 一次克隆约 2 秒；23 次提交，全部直推 main（个人仓库）；3 篇 ADR。
- 最不稳的一块（仅生产存在的依赖用结构空壳 stub）一天内约 10 次提交才收敛。

## 60 秒

> 先说：**it's my personal repo, not the team toolchain.**

**S**
- Integration tests ran migrations against **one shared schema**; two engineers, or two **AI coding sessions**, **collided on DDL**.

**T**
- **No ticket, no owner**; I chose to remove the friction.

**A**
1. **V1**: pool slots **cloned** from the shared schema.
2. Its state depended on **who migrated last**: slots weren't **reproducible**.
3. **V2**: a separate `MAIN` synced to the **production-deployed commit** via the **Deployments API**, not the release tag (a tag can be cut and never deployed).
4. Each slot is a **zero-copy clone** of `MAIN`: ~**2 seconds**, because a clone copies **metadata**, not data.
5. **Edge case**: clone order breaks **cross-database streams**; clone the **replication DB first** and **auto-repair** after a swap.
6. Three **ADRs**, one of them records what I **deliberately did not fix**.

**R**
- Several agent sessions run **migrations and tests concurrently** without colliding.

**L**
- Make test state **deterministic**: derive it from **what's deployed**, never from **who ran last**.

## 2 分钟（在 60 秒上加）

- **Why clones are cheap**: data lives in **immutable micro-partitions**; a clone **points** at the same files; storage cost appears only as data **diverges**.
- Also fixed **duplicate repeatable migrations** and added **stub tables** for prod-only dependencies.
- **ADRs**: sync runs **locally**; default target = **deployed commit**; **skip Flyway for one module**, written down as "don't fix this".
- On top: an **on-call copilot** that polls Slack, PagerDuty and Datadog, opens an agent session with context, and drafts replies **I review** before sending; **adjacent teams adopted it**.
- **Different next time**: start from the **deployed commit**, not a shared schema.

## 追问

- **Why is a clone 2 seconds?** **Immutable micro-partitions + metadata pointers**; no data copied.
- **What broke in V1?** Source state **history-dependent**.
- **Cross-database streams?** Cloning the **app DB first** invalidates streams that depend on **replication** tables; fixed order, **replication first**.
- **Two sessions grab the same slot?** 【待 Chi 补：真实的借用/归还机制】
- **Session crashes holding a slot?** 【待 Chi 补：泄漏回收】
- **How do you trust AI-written code?** **Plan with the agent, TDD every phase, CI and monitoring gates**; watch **gates and thresholds**, not lines; in money code I **read every diff**.
- **Why direct-push to main?** Personal repo; it doesn't touch team code.

## 别说

- "team standard"；schema pool 的团队使用者数（无记录）；"cheat" 这个词。
- "For this interview I'm working without AI" 仅当你真的关掉 AI 练过。

## 待 Chi 补

- V1 用了多久；除你外有几个人用；DDL 冲突前后对比。
