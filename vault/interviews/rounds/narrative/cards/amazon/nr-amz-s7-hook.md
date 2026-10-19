---
id: nr-amz-s7-hook
node: amazon.outline
type: qa
step: 19
---
## Q
<p class="title">schema pool<span class="meta">02 提纲</span></p>

开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
<span class="label">开场</span>

**Nobody assigned it: two engineers, or two AI agents, collided on shared-schema DDL, so I built a pool of two-second zero-copy clones.**

<span class="label">适用 LP</span>

- 主：**Invent and Simplify**、**Bias for Action**、**Ownership**
- 副：Learn and Be Curious、Frugality、Think Big

<span class="label">数字</span>

- 克隆约 **2 秒**：拷的是微分区元数据，不是数据
- **23 次提交**，全部直推 main（个人仓库 `snowglobe-tools`，不是团队官方工具链）
- **3 篇 ADR**（V2）：0001 本地同步；0002 默认目标 = 生产部署 SHA；0003 跳过 `share` 模块 Flyway
- 难点之一 stub 表：一天约 **10 次提交**才稳定
- 相邻团队采用 on-call copilot，采用者数量无记录
- 【待补：团队/队友里有多少人用过 schema pool？无团队级采用数据】

<div class="sources"><b>表达 · business English</b><br>• <b><i>zero-copy clone</i></b> — 零拷贝克隆，只复制元数据<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Each pool slot is a zero-copy clone, so it takes about two seconds.”</span><br>• <b><i>collide on</i></b> — 在某处冲突<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Two agent sessions on different branches collide on DDL in the shared schema.”</span><br>• <b><i>personal repo</i></b> — 个人仓库，非团队官方<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“It&#x27;s 23 commits in my personal repo, not the team&#x27;s official toolchain.”</span></div>
