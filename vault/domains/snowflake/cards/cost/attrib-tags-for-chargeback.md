---
id: attrib-tags-for-chargeback
node: cost.access-history-lineage-for-cost
type: qa
tags: [grown]
---
## Q
公司要求把 Snowflake 费用按部门做内部结算（chargeback）。只靠仓库名或用户名来分摊，会有什么问题？更稳妥的做法是什么？

## A
仓库和服务账号经常被多个团队共用，仓库名、用户名并不稳定地对应部门，分摊结果会出现大块“无法归属”的成本。更稳妥的做法是给仓库、用户等对象打对象标签（object tag，如 `cost_center`），通过 `TAG_REFERENCES` 与计量视图连接汇总；对共享仓库上的查询，要求作业设置 `QUERY_TAG`，再用查询级归因视图按标签分摊。标签由治理团队集中维护，比依赖命名约定更可靠。
