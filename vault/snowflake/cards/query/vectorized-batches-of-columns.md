---
id: vectorized-batches-of-columns
node: query.vectorized-columnar-execution
type: qa
tags: [grown]
---
## Q
Snowflake 的向量化执行（vectorized execution）具体是怎样处理数据的？这种做法源自哪个系统？

## A
算子不逐行处理，而是以列式格式、按每批几千行的批次（batch）在算子之间流水线式传递和处理：每批数据由若干列的值数组组成，算子在一个紧密循环里对整列数组做同一种运算。这种执行方式由 VectorWise（最初是 MonetDB/X100 项目）开创。
