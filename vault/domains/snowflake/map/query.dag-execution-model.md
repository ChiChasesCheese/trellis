%% trellis:begin %%
# DAG 执行模型
*查询编译与执行*

编译后的查询会变成一个由算子（operator）组成的有向无环图（DAG），并被分发给仓库各节点上的工作进程执行。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/query.compilation-pipeline|编译流水线]]

**Unlocks:** [[domains/snowflake/map/query.join-strategies-broadcast-shuffle|连接（join）策略]], [[domains/snowflake/map/query.spilling-to-remote-disk|溢出（spilling）到本地与远程磁盘]], [[domains/snowflake/map/query.reading-query-profile|解读查询画像（query profile）]], [[domains/snowflake/map/pruning.query-acceleration-service|查询加速服务（Query Acceleration Service）]]

## Cards (5)
1. [[dag-failure-whole-query-retry]]
2. [[dag-multi-step-queries]]
3. [[dag-no-buffer-pool-no-txn-during-exec]]
4. [[dag-push-vs-volcano-pull]]
5. [[dag-shared-intermediate-results]]
%% trellis:end %%

## Notes
