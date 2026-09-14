---
nodes:
- pipelines.stream-offset-bookmark
- pipelines.stream-types
- pipelines.stream-consumption-and-offset-advance
- pipelines.stream-staleness-and-retention-extension
title: 流对象(Stream)的偏移量、类型与消费语义
corpus: snowflake-docs
section: 21-streams-intro
url: https://docs.snowflake.com/en/user-guide/streams-intro
tags:
- canonical
---

# 流对象(Stream)的偏移量、类型与消费语义

Stream 本身不存数据,只是记录一个偏移量(offset)——表版本历史中的一个书签,查询它返回的是自该偏移量以来发生的变更增量。标准流(standard)追踪全部增删改并做净变化合并;仅追加流(append-only)只关心插入,性能更好;仅插入流(insert-only)用于外部表等无法追踪删除的场景。偏移量只有在一次成功提交的 DML 事务里“消费”了流的内容才会前移——单纯 SELECT 查询流不会推进偏移量,这保证了消费端崩溃重启后拿到的仍是同一批变更,不会漏掉。若流长期不被消费,其偏移量可能落到源表数据保留期之外而变得过期(stale);为避免这种情况,Snowflake 会临时延长源表的保留期,最长可达 14 天默认上限。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/streams-intro)

## Archived copy
![[snowflak-streams-clip]]
%% trellis:end %%
