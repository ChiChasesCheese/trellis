---
id: udf-scalar-vs-udtf
node: openplatform.snowpark-udf-udtf
type: qa
tags: [grown]
---
## Q
Snowflake 中的标量 UDF（scalar user-defined function）和表函数 UDTF（user-defined table function）在输入输出形态上有什么区别？分别适合什么需求？

## A
标量 UDF 对每一行输入返回恰好一个值，适合逐行的转换或打分（如解析一个字符串、计算一个特征）。UDTF 对输入返回一张表：每行输入可以产出零行、一行或多行，并可在同一分区（`PARTITION BY`）内保持状态，Python UDTF 通过 `process` 方法逐行处理、`end_partition` 在分区结束时输出汇总行。适合一行拆多行（如展开 JSON 数组）或按分区做跨行计算。
