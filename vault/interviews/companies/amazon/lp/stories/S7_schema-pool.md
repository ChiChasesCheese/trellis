# schema pool（主动性 · 开发者效率 · AI fluency）

**Nobody assigned it: two engineers, or two AI agents, collided on shared-schema DDL, so I built a pool of two-second zero-copy clones.**

## 适用 LP

- 主：**Invent and Simplify**、**Bias for Action**、**Ownership**
- 副：Learn and Be Curious、Frugality、Think Big

## 数字

- 克隆约 **2 秒**：拷的是微分区元数据，不是数据
- **23 次提交**，全部直推 main（个人仓库 `snowglobe-tools`，不是团队官方工具链）
- **3 篇 ADR**（V2）：0001 本地同步；0002 默认目标 = 生产部署 SHA；0003 跳过 `share` 模块 Flyway
- 难点之一 stub 表：一天约 **10 次提交**才稳定
- 相邻团队采用 on-call copilot，采用者数量无记录
- 【待补：团队/队友里有多少人用过 schema pool？无团队级采用数据】

## S / T / A / R / L

### S
- 集成测试对一个**共享 Snowflake schema** 跑迁移
- 两个工程师，或两个 **AI 编码 agent 会话**，在不同分支上**撞 DDL**

### T
- 没人要求：**无 ticket、无 owner**；我选择去解决这个摩擦

### A
- **V1**：从共享的 `PUBLIC` schema 克隆槽位
- 发现 `PUBLIC` 状态取决于**谁最后跑迁移**，槽位不可复现
- 重写 **V2**，写 **3 篇 ADR**：独立的 `MAIN` schema，同步到**生产部署的 commit**
- 查 **GitHub Deployments API** 而不是 release tag：tag 可能打了没部署
- 每个槽位是 `MAIN` 的**零拷贝克隆**，~**2 秒**；会话借用 → 测试 → 丢弃
- 修真实边界：**跨库 stream** 受克隆顺序影响 → 先克隆 **replication DB**，换新后**自动修复**

### R
- 可以在同一仓库**并行跑多个 Claude Code 会话**而不冲突
- **23 次提交**，**个人仓库**，不是团队官方工具链

### L
- 我是**一个 agent 团队的 tech lead**，而且仍然拥有**每一个 diff**

## 追问与回答

- **Why GitHub Deployments API, not tags?**
  - 打了 **tag 没部署**；Deployments API 记录**生产环境实际部署**的 SHA
- **Why is a clone 2 seconds?**
  - **不可变微分区** + **元数据指针**，不拷数据
- **What broke in V1?**
  - `PUBLIC` 的状态取决于**谁最后跑了什么迁移**，不可预测
- **How do cross-database streams break?**
  - 先克隆 APP_DB 再 REPL_DB 会让依赖 REPL 表的 **stream 失效**
  - 固定顺序**先 REPL 后 APP**；`MAIN_STAGING → MAIN` 交换后**自动扫描修复**
- **How do you trust AI-generated code?**
  - **plan with the agent → TDD every phase → CI + monitoring gates**；看 **gates 和 thresholds**，不看行数
  - money code 里我读**每一个 diff**
- **Why direct-push to main?**
  - **个人仓库**，不影响团队代码；诚实说明
- **Who uses it?**
  - 见待补；on-call copilot 是相邻团队采用（人数无记录）

## 换个 LP 讲

- **Invent and Simplify**：两秒克隆取代「等共享 schema 轮到你」；MAIN 同步到部署 SHA；别说成团队标准
- **Bias for Action**：没人派，一个下午上 V1，学到 `PUBLIC` 为什么不确定后重写；23 次直推
- **Ownership**：不在我岗位描述里，我维护它；无 ticket、有 ADR、有 Sync Failure Playbook
- **Learn and Be Curious**：学 zero-copy clone 与跨库 stream 的真实行为；微分区元数据、stream 对克隆顺序敏感
- **Frugality**：克隆花的是元数据不是存储；2 秒、不复制数据；无费用数字，别编
- **Think Big**：同一个工具让「agent 团队」工作流成为可能；on-call copilot；别夸大成「改变了团队」

## 待补

- 【待补：团队里其他工程师是否用了 schema pool，人数/频率】
- 【待补：除你以外有几位工程师/agent 工作流依赖它；有无可量化的节省（CI 排队、DDL 冲突次数 X → Y）】
- 【待补：on-call copilot 的相邻团队是谁（角色/团队，不点名）、采用后收到什么反馈】
- 【待补：有没有尝试推动团队把它升级为官方工具链、对方怎么说】

<details><summary>逐字稿</summary>

> Nobody asked for this. Our integration tests run migrations against a shared Snowflake schema, so two engineers — or two AI coding-agent sessions — on different branches collide on DDL. I built a schema pool. Version one cloned from a shared schema whose state depended on who last ran a migration, so version two was a rewrite with three ADRs. In V2 a `MAIN` schema is synced to whatever commit is actually deployed to production — I query the GitHub Deployments API rather than trust the release tag, because a tag can be cut and never deployed. Each pool slot is a zero-copy clone of `MAIN`, about two seconds, because a clone copies micro-partition metadata, not data. A session borrows a slot, runs migrations and tests in isolation, and drops it.
>
> I fixed real edge cases: cross-database streams break depending on clone order, so I clone the replication DB before the app DB and auto-detect the pattern after a swap. It's what lets me run several Claude Code sessions in parallel on the same repo. I think of it as being the tech lead of a team of agents — and I still own every diff.

</details>
