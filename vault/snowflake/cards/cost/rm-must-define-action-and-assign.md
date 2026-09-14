---
id: rm-must-define-action-and-assign
node: cost.resource-monitors-and-budgets
type: qa
source: snowflake-docs
---
## Q
管理员用 SQL 执行了 `CREATE RESOURCE MONITOR` 并设置了配额，但一个月后发现仓库花超了、监控器却毫无反应。可能漏了哪些步骤？

## A
(1) 没有分配对象：SQL 创建监控器后，还要单独执行 `ALTER WAREHOUSE … SET RESOURCE_MONITOR` 或 `ALTER ACCOUNT` 把它挂到仓库或账户上，未设置监控类型的监控器处于休眠状态，不跟踪任何用量。(2) 没有定义动作：监控器至少要有一个动作（最多 1 个 Suspend、1 个 Suspend Immediate、5 个 Notify），否则达到阈值什么也不会发生。(3) 通知默认关闭：需要用户在 Snowsight 中验证邮箱并开启资源监控器通知才能收到提醒。
