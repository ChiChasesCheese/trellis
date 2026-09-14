---
nodes:
- continuity.retention-vs-failsafe
- continuity.at-before-statement-syntax
- continuity.undrop-recovery
- txn.mvcc-immutable-partitions
- storage.table-types
title: 时间旅行(Time Travel):可查询窗口、AT/BEFORE 与 UNDROP
corpus: snowflake-docs
section: 13-data-time-travel
url: https://docs.snowflake.com/en/user-guide/data-time-travel
tags:
- canonical
---

# 时间旅行(Time Travel):可查询窗口、AT/BEFORE 与 UNDROP

任何 DML 修改或对象删除发生前,Snowflake 都会先保留旧版本数据——这正是多版本并发控制(MVCC)在不可变微分区上的体现:写入永远不原地修改,而是生成新版本、旧数据继续保留一段时间。默认保留窗口 1 天,企业版及以上可配置到最长 90 天,永久表、瞬态表(transient)、临时表在这份保留期和后续 Fail-safe 窗口上的待遇并不相同。窗口内可以用 AT/BEFORE 子句按时间戳、相对偏移或语句 ID 查询历史数据、克隆对象,或用 UNDROP 把被删除的表/schema/数据库原地恢复——这是纯元数据操作,不是从备份还原。一旦超出保留期,数据进入 Fail-safe,这些操作全部失效。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/data-time-travel)

## Archived copy
![[snowflak-time-travel-clip]]
%% trellis:end %%
