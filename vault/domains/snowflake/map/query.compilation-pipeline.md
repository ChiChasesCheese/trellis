%% trellis:begin %%
# 编译流水线
*查询编译与执行*

解析（parse）→ 绑定（bind）→ 优化（optimize）→ 代码生成（codegen）的顺序，以及每个阶段运行在哪里。

**Requires:** [[domains/snowflake/map/metadata.query-compiler-pipeline|查询编译流水线]]

**Unlocks:** [[domains/snowflake/map/query.dag-execution-model|DAG 执行模型]], [[domains/snowflake/map/query.explain-plan-interpretation|EXPLAIN 执行计划解读]]

## Cards (4)
- [[compile-error-stage-diagnosis]]
- [[compile-plan-carries-file-list]]
- [[compile-predicate-pushdown-enables-pruning]]
- [[compile-stage-order-and-location]]
%% trellis:end %%

## Notes
