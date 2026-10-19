---
id: nr-amz-s7-hook
node: amazon.s7
type: qa
step: 1
---
## Q
【schema pool（主动性 · 开发者效率 · AI fluency）】开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
**Nobody assigned it: two engineers, or two AI agents, collided on shared-schema DDL, so I built a pool of two-second zero-copy clones.**

**适用 LP**

- 主：**Invent and Simplify**、**Bias for Action**、**Ownership**
- 副：Learn and Be Curious、Frugality、Think Big

**数字**

- 克隆约 **2 秒**：拷的是微分区元数据，不是数据
- **23 次提交**，全部直推 main（个人仓库 `snowglobe-tools`，不是团队官方工具链）
- **3 篇 ADR**（V2）：0001 本地同步；0002 默认目标 = 生产部署 SHA；0003 跳过 `share` 模块 Flyway
- 难点之一 stub 表：一天约 **10 次提交**才稳定
- 相邻团队采用 on-call copilot，采用者数量无记录
- 【待补：团队/队友里有多少人用过 schema pool？无团队级采用数据】
