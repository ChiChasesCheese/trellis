---
id: cc-rules-grp-empty-groups-printed
node: rules.grouping
type: qa
---
## Q
The output is one line per merchant. A merchant appears in the setup block but in no transaction. Does it get a line?

## A
**Almost always yes — with its base value — and this is a standing hidden test.**

Building the output from `groups.keys()` silently drops every entity with no rows; building it from the declared entity list keeps them. The two sources are different sets and the statement tells you which one the output is keyed on ("one line per merchant, **including those with no transactions**").

The mirror rule also exists and must be read just as carefully: "print only accounts whose final balance is non-zero" excludes an entity that had activity and netted to zero. Entity list, group list, and non-empty-result list are three different things.

## Q zh
输出是每个商户一行。某商户出现在配置块里，却没有任何交易。它有行吗？

## A zh
**几乎总是有 —— 带着它的基础值 —— 而且这是一个常驻隐藏测试。**

用 `groups.keys()` 生成输出会静默丢掉所有没有行的实体；用已声明的实体列表生成则会保留它们。这两个来源是不同的集合，而题面会告诉你输出以哪一个为准（「每个商户一行，**包括没有交易的**」）。

镜像规则同样存在，也要一样仔细地读：「只打印最终余额非零的账户」会排除掉有过活动但净额为零的实体。实体列表、分组列表、非空结果列表，是三样不同的东西。
