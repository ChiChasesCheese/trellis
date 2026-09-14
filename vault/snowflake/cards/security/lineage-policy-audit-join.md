---
id: lineage-policy-audit-join
node: security.data-lineage-and-access-history
type: qa
tags: [grown]
---
## Q
如何证明“过去 90 天里只有 HR 角色读取过 `employees.salary` 列”？需要组合哪些信息？

## A
在 `ACCESS_HISTORY` 中展开 `BASE_OBJECTS_ACCESSED` 的列数组，筛出 `employees.salary` 被读的记录，得到 query_id 和用户；再用 query_id 连接 `QUERY_HISTORY` 拿到执行时的角色、仓库和时间。按角色分组即可列出所有实际读过该列的主体。之所以要看底层对象而非直接对象，是因为通过视图间接读取也必须算在内。
