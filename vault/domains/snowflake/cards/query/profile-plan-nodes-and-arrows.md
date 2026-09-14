---
id: profile-plan-nodes-and-arrows
node: query.reading-query-profile
type: qa
source: snowflake-docs
---
## Q
Snowflake 查询画像（Query Profile）中央的执行计划图，节点和箭头分别代表什么？排查慢查询时应先看哪个窗格定位瓶颈？

## A
节点是算子节点（operator node），代表行集算子（rowset operator），如 TableScan、Filter、Join、Aggregate；箭头表示从一个算子流出、流入下一个算子的行集（rowset）。先看 Most Expensive Nodes（最昂贵节点）窗格：它按执行时间降序列出所有耗时占查询总执行时间（多步查询则为当前步骤）1% 及以上的节点，能直接定位最耗时的算子。
