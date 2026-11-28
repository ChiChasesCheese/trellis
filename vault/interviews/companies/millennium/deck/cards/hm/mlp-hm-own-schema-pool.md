---
id: mlp-hm-own-schema-pool
node: hm.ownership
type: qa
step: 1
---
## Q
**没人分配的事：schema pool**｜经理面与行为面

“Tell me about a time you took ownership of something that wasn't assigned to you.”

## A
用 schema pool。它没有工单、没人要求，是你自己看到摩擦后建的，而且你说得出里面的数据库原理。

- **问题：** 集成测试对着同一个共享的 Snowflake schema 跑数据库迁移，两个工程师（或两个 AI 编码智能体会话）在不同分支上就会撞上 DDL（建表改表语句）。
- **做法：** 一个 `MAIN` schema 同步到“生产实际部署的 commit”，查 GitHub Deployments API 而不是看 tag；每个池位是 `MAIN` 的零拷贝克隆（zero-copy clone，只拷元数据不拷数据，约 2 秒）；会话借一个，跑完归还。
- **第二版：** 第一版从共享的 `PUBLIC` 克隆，状态不可预测，所以重写，写了三篇架构决策记录（ADR）。
- **边界：** 这是你个人的仓库，说“我建的，团队采用了”，不说成团队标准。

**英文答法。**
- Nobody asked for this. Two engineers, or two **AI coding-agent sessions**, on different branches collided on **DDL** in a shared schema.
- I built a **schema pool**: `MAIN` synced to the commit **actually deployed** to production — I query the Deployments API, not the tag, because tags lie.
- Each slot is a **zero-copy clone** of `MAIN`, about **two seconds**: it copies metadata, not data.
- Version two was a rewrite with **three ADRs**; it let me run several Claude Code sessions in parallel — I'm the tech lead of a team of agents.

**追问。**
- **Why not clone from `PUBLIC`?** Its state depends on whoever ran migrations last; that was version one's flaw.
- **What broke?** Cross-database streams get invalidated by clone order, so I clone the replication DB before the app DB; also duplicate repeatable migrations and stub tables for prod-only dependencies.
- **Did the team adopt it?** I built it in my own repo and the team adopted it; I wouldn't call it a team standard.
