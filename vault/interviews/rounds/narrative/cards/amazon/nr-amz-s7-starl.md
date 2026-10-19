---
id: nr-amz-s7-starl
node: amazon.outline
type: qa
step: 20
---
## Q
<p class="title">schema pool<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- 集成测试对一个**共享 Snowflake schema** 跑迁移
- 两个工程师，或两个 **AI 编码 agent 会话**，在不同分支上**撞 DDL**

<span class="label">T</span>

- 没人要求：**无 ticket、无 owner**；我选择去解决这个摩擦

<span class="label">A</span>

- **V1**：从共享的 `PUBLIC` schema 克隆槽位
- 发现 `PUBLIC` 状态取决于**谁最后跑迁移**，槽位不可复现
- 重写 **V2**，写 **3 篇 ADR**：独立的 `MAIN` schema，同步到**生产部署的 commit**
- 查 **GitHub Deployments API** 而不是 release tag：tag 可能打了没部署
- 每个槽位是 `MAIN` 的**零拷贝克隆**，~**2 秒**；会话借用 → 测试 → 丢弃
- 修真实边界：**跨库 stream** 受克隆顺序影响 → 先克隆 **replication DB**，换新后**自动修复**

<span class="label">R</span>

- 可以在同一仓库**并行跑多个 Claude Code 会话**而不冲突
- **23 次提交**，**个人仓库**，不是团队官方工具链

<span class="label">L</span>

- 我是**一个 agent 团队的 tech lead**，而且仍然拥有**每一个 diff**

<div class="sources"><b>表达 · business English</b><br>• <b><i>scratch an itch</i></b> — 解决自己遇到的小痛点<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I built the pool to scratch an itch nobody had assigned to me.”</span><br>• <b><i>rewrite from first principles</i></b> — 回到基本原理重写<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“V1 taught me that PUBLIC was non-deterministic, so I rewrote it from first principles.”</span><br>• <b><i>deterministic</i></b> — 确定性的，同样输入同样结果<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Syncing MAIN to the deployed SHA made the slots deterministic.”</span></div>
