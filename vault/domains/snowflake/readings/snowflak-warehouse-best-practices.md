---
nodes:
- warehouse.sizing-t-shirt
- warehouse.auto-suspend-resume
- warehouse.scaling-up-vs-out
- cache.warehouse-local-disk-cache
title: 仓库调优:扩容(up)还是扩出(out)、本地磁盘缓存
corpus: snowflake-docs
section: 07-warehouses-considerations
url: https://docs.snowflake.com/en/user-guide/warehouses-considerations
tags:
- canonical
---

# 仓库调优:扩容(up)还是扩出(out)、本地磁盘缓存

本节把选尺寸、配自动挂起/恢复的实践经验系统化:按秒计费意味着完全可以先选大尺寸再逐步收缩,而不必过早优化。扩容(scale up,调大仓库尺寸)适合让单个慢查询变快;扩出(scale out,增加多集群仓库的集群数)适合缓解并发排队,二者解决的是不同症状,选错了收益有限。运行中的仓库会维护一份最近扫描过的微分区本地磁盘缓存(warehouse-local disk cache),挂起时整份缓存被丢弃,恢复后要重新预热,这是权衡是否挂起仓库时必须考虑的隐性成本。读完能在“查询慢”与“查询排队”两种症状间对症选择对策。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/warehouses-considerations)

## Archived copy
![[snowflak-warehouse-best-practices-clip]]
%% trellis:end %%
