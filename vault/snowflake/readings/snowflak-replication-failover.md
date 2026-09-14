---
nodes:
- continuity.replication-and-failover
title: 跨账户复制与故障切换(Replication & Failover)
corpus: snowflake-docs
section: 35-account-replication-intro
url: https://docs.snowflake.com/en/user-guide/account-replication-intro
tags:
- canonical
---

# 跨账户复制与故障切换(Replication & Failover)

复制组(replication group)把源账户里选定的一批对象持续复制到一个或多个目标账户,目标端得到的是只读副本;故障切换组(failover group)是能够被提升(promote)为可读写主副本的复制组,一旦提升,原来的只读副本立刻获得读写权限,这就是跨区域、跨云容灾的核心机制。复制支持数据库、共享、角色、仓库、网络策略等一长串对象类型,但角色对象必须一并复制,权限授予关系才能在目标账户里正确落地;某些高级对象类型(账户级参数、用户、故障切换组本身)仅限 Business Critical 版本及以上。复制按预设周期自动刷新,任一时刻只允许一次刷新在执行,故障切换前需要先暂停调度中的复制以避免切换过程中数据不一致。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/account-replication-intro)

## Archived copy
![[snowflak-replication-failover-clip]]
%% trellis:end %%
