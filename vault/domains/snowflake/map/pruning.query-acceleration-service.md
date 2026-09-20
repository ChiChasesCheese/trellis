%% trellis:begin %%
# 查询加速服务（Query Acceleration Service）
*剪枝与查询优化*

借用无服务器（serverless）计算资源，将异常耗时查询中的扫描/过滤部分并行化到超出其所属仓库自身节点数的规模。

**Requires:** [[domains/snowflake/map/query.dag-execution-model|DAG 执行模型]]

## Readings
- [[snowflak-query-acceleration|查询加速服务(QAS)加速离群查询]]

## Cards (6)
1. [[qas-bytes-scanned-inflation]]
2. [[qas-default-scale-factor]]
3. [[qas-find-candidates]]
4. [[qas-ineligible-reasons]]
5. [[qas-outlier-offload-mechanism]]
6. [[qas-scale-factor-cost-bound]]
%% trellis:end %%

## Notes
