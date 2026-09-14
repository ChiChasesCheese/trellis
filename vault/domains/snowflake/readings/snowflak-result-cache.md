---
nodes:
- cache.result-cache
- cache.result-cache-invalidation
title: 结果缓存(Result Cache)命中与失效条件
corpus: snowflake-docs
section: 08-querying-persisted-results
url: https://docs.snowflake.com/en/user-guide/querying-persisted-results
tags:
- canonical
---

# 结果缓存(Result Cache)命中与失效条件

查询结果会被持久化缓存最长 24 小时(每次命中都会重置计时,最长可达 31 天),命中时 Snowflake 直接跳过重新计算,零计算成本返回上次的结果。命中条件相当苛刻:SQL 文本必须逐字一致(大小写、别名都算数)、不含 UUID_STRING/RANDOM 等不确定函数、所涉及表的微分区自上次执行后未发生任何变化、且执行角色对所有表仍具备权限。正因为判断依据是“表数据是否变了”而非“查询是谁发起的”,不同会话、不同用户执行完全相同的语句也能命中同一份缓存。读完应能诊断为什么两条看起来一样的查询,其中一条没有走缓存。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/querying-persisted-results)

## Archived copy
![[snowflak-result-cache-clip]]
%% trellis:end %%
