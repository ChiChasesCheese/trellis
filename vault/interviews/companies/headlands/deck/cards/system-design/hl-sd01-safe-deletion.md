---
id: hl-sd01-safe-deletion
node: system-design.sd01-unused-code
type: qa
step: 21
---
## Q
从候选到安全删除的流程怎么设计？软删除怎么做，什么时候允许直接删除？

## A
流程：候选 → 分簇 → 按 CODEOWNERS 分配 owner → 机器人开 PR（每个簇一个，≤ 500 LOC）→ CI 全量构建 + 测试 + 再跑一遍可达性（删后图不应出现新的未解析引用）→ 软删除或直接删除 → 真删。

- **软删除**（默认，对 L2 / L3）：`@Deprecated(forRemoval=true)` + 被调用时打一条日志 / 指标，观察 N 个发布周期，无调用则真删；
- **直接删除**：仅 L0 / L1 HIGH；
- 回滚路径：一个 revert，PR 里附「如何恢复」。
