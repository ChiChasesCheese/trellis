---
id: lineage-vs-grants-difference
node: security.data-lineage-and-access-history
type: qa
tags: [grown]
---
## Q
`SHOW GRANTS` 给出的权限信息和 `ACCESS_HISTORY` 给出的访问记录，在审计上回答的是不同的问题。各自回答什么？为什么两者都需要？

## A
`SHOW GRANTS`（及 GRANTS_TO_ROLES 等视图）回答“谁有能力访问”——是授权状态的快照；`ACCESS_HISTORY` 回答“谁实际访问了、读写了哪些列”——是行为记录。权限清单无法说明过度授权是否被真正使用，访问记录也无法显示那些有权但尚未使用的潜在风险。两者结合才能做最小权限收敛：找出“有权限但长期未使用”的授权并回收。
