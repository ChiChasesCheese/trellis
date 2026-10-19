---
id: nr-amz-s7-full
node: amazon.full
type: qa
step: 7
---
## Q
<p class="title">schema pool<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：我们的集成测试对一个共享的 Snowflake schema 跑迁移，所以两个工程师，或者两个 AI 编码 agent 会话，在不同分支上就会撞 DDL。没有 ticket，也没有 owner，是我自己决定去解决这个摩擦。
- V1：我先从共享的 PUBLIC schema 克隆槽位。后来发现 PUBLIC 的状态取决于谁最后跑了迁移，槽位不可复现，所以必须重写。
- V2：我写了 3 篇 ADR，建一个独立的 MAIN schema，同步到生产实际部署的 commit。我查 GitHub Deployments API 而不是 release tag，因为 tag 可能打了却没部署。每个槽位是 MAIN 的零拷贝克隆，约 2 秒，因为拷的是微分区元数据，不是数据。会话借一个槽位，跑迁移和测试，用完丢弃。
- 边界：跨库 stream 会受克隆顺序影响，所以先克隆 replication DB 再克隆 app DB，并在交换之后自动扫描修复。
- 结果与学到：我可以在同一个仓库并行跑多个 Claude Code 会话而不冲突。这是个人仓库里的 23 次提交，不是团队官方工具链。我把自己看作一个 agent 团队的 tech lead，而且仍然拥有每一个 diff。

<span class="label">英文口述（60–90 秒）</span>

Nobody asked for this. Our integration tests run migrations against a shared Snowflake schema, so two engineers, or two AI coding-agent sessions, on different branches collide on DDL. I built a schema pool. Version one cloned from a shared schema whose state depended on who last ran a migration, so version two was a rewrite with three ADRs. In V2 a MAIN schema is synced to whatever commit is actually deployed to production; I query the GitHub Deployments API rather than trust the release tag, because a tag can be cut and never deployed. Each pool slot is a zero-copy clone of MAIN, about two seconds, because a clone copies micro-partition metadata, not data. A session borrows a slot, runs migrations and tests in isolation, and drops it. I also fixed real edge cases: cross-database streams break depending on clone order, so I clone the replication DB before the app DB and auto-detect the pattern after a swap. It's what lets me run several Claude Code sessions in parallel on the same repo. It lives in my own repo, not the team toolchain. I think of it as being the tech lead of a team of agents, and I still own every diff.

<div class="sources"><b>表达 · business English</b><br>• <b><i>developer velocity</i></b> — 开发效率<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The schema pool was a developer-velocity fix: tests stopped waiting on each other.”</span><br>• <b><i>unblock the team</i></b> — 帮团队解除阻塞<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The schema pool unblocked parallel work instead of everyone sharing one schema.”</span><br>• <b><i>self-serve</i></b> — 自助（不用找人审批）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Engineers could self-serve an isolated schema in seconds.”</span></div>
