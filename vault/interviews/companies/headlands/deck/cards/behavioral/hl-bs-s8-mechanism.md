---
id: hl-bs-s8-mechanism
node: behavioral.stories
type: qa
step: 44
---
## Q
S8 的机制是什么：为什么所有权转移会失败，`outbound_privileges` 解决什么？Terraform 没有事务意味着什么？

## A
- **机制**：转移所有权前必须先撤销**依赖授权**；资源用 `outbound_privileges`（**REVOKE** 或 **COPY**）来表达这一点，不设置时 apply 会**失败**。
- **Terraform 没有事务**：失败的 apply 会留下**部分状态**，所以危险的改动要保持**小而可重跑**。
- **最危险的"无害"操作**：**重命名**资源——默认是**删除再重建**；要用 `moved` block 或 `state mv`。
