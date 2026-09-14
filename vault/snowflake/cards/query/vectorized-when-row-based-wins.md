---
id: vectorized-when-row-based-wins
node: query.vectorized-columnar-execution
type: qa
tags: [grown]
---
## Q
列式向量化执行在分析型负载上占优，为什么 Snowflake 的 hybrid table（混合表）扫描还会出现 ROW_BASED（按行）扫描模式？什么负载更适合按行？

## A
列式执行的优势来自“对少数列做大批量运算”；但事务型负载多是按主键或索引取少量完整的行，要把分散在各列中的值重新拼成整行，这对列式布局反而是额外开销。混合表面向低延迟、高吞吐的单行随机读写，因此其查询画像中的 TableScan/IndexScan 会标出扫描模式是 ROW_BASED 还是 COLUMN_BASED：点查和少量整行读取适合按行，大范围聚合分析适合按列。
