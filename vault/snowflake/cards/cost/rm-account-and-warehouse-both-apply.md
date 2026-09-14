---
id: rm-account-and-warehouse-both-apply
node: cost.resource-monitors-and-budgets
type: qa
source: snowflake-docs
---
## Q
账户级资源监控器配额 5000 credit，仓库 W3 另有一个 1000 credit 的仓库级监控器。W3 在本月最多能用多少？账户监控器会覆盖仓库监控器吗？

## A
两者同时生效，不存在覆盖：账户监控器或仓库监控器任一方达到带挂起动作的阈值，W3 都会被挂起。所以 W3 本月最多用 1000 credit，但如果全账户先用满 5000，W3 即使没到 1000 也会被挂起。一个账户只能有一个账户监控器；一个仓库在账户级以下只能分配给一个监控器，一个监控器可以管多个仓库（最多 500 个）。
