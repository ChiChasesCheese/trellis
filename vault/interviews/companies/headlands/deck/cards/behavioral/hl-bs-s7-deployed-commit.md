---
id: hl-bs-s7-deployed-commit
node: behavioral.stories
type: qa
step: 37
---
## Q
S7 的 V2 为什么用"生产已部署的 commit"作为同步目标，而不是 release tag？V1 的问题在哪？

## A
- **V1 的问题**：slot 从共享 schema 克隆，那个 schema 的状态取决于**最后谁迁移过**——**历史相关**，所以不可复现。
- **V2 的做法**：一个独立的 `MAIN`，同步到**生产已部署的 commit**，通过 **Deployments API** 获取。
- **为什么不是 release tag**：tag 可能**被打出来却从没部署**，而测试要对着真正在生产里的 schema 跑。

教训：把系统的输入变成**一个确定的东西**。下次一开始就从**已部署的 commit** 出发，而不是共享 schema。
