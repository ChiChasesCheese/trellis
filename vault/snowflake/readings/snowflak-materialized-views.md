---
nodes:
- pruning.materialized-views-maintenance
title: 物化视图(Materialized View)的预计算与维护成本
corpus: snowflake-docs
section: 12-views-materialized
url: https://docs.snowflake.com/en/user-guide/views-materialized
tags:
- canonical
---

# 物化视图(Materialized View)的预计算与维护成本

物化视图把查询结果预先算好并存储,之后查询直接读取物化视图,常用于加速频繁运行且开销大的聚合、投影类查询。与结果缓存不同,物化视图由后台服务在基表变更后自动增量刷新(insert 触发追加、delete 触发压缩),始终对用户呈现最新数据;优化器甚至能在用户没有显式引用物化视图的情况下,自动改写查询去命中它。收益的另一面是持续的存储成本和维护计算成本——基表每次 DML 都可能触发物化视图的重写,尤其当物化视图的聚簇键与基表不同时,一次小改动可能波及大量微分区。读完应能判断什么场景该用物化视图而非普通视图或结果缓存。
