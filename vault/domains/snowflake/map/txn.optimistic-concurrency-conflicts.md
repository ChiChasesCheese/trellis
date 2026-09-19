%% trellis:begin %%
# 写并发：表级锁与写冲突
*事务与并发控制*

普通表上 UPDATE、DELETE、MERGE 会加锁，通常阻塞同表上其他 UPDATE/DELETE/MERGE，而 INSERT 与 COPY 一般可以并行；锁等待超时与死锁如何表现。

**Requires:** [[domains/snowflake/map/txn.mvcc-immutable-partitions|基于不可变微分区的 MVCC]]

## Cards (5)
1. [[concurrency-deadlock-victim-rule]]
2. [[concurrency-insert-vs-update-parallelism]]
3. [[concurrency-lock-timeout-failure]]
4. [[concurrency-many-small-updates-antipattern]]
5. [[concurrency-standard-vs-hybrid-lock-granularity]]
%% trellis:end %%

## Notes
