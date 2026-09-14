---
id: udf-per-row-overhead-vectorized
node: openplatform.snowpark-udf-udtf
type: qa
tags: [grown]
---
## Q
一个 Python 标量 UDF 在十亿行表上运行得很慢，而同样逻辑用内置 SQL 函数很快。慢在哪里？向量化 UDF（vectorized UDF）怎么缓解？

## A
内置 SQL 函数在 Snowflake 的原生执行引擎内按列批量运行；Python UDF 则在仓库节点上的独立沙箱进程里执行，数据要在引擎和 Python 解释器之间序列化传递，并且逐行调用 Python 函数，每行都有解释器调用开销。向量化 UDF 以批（pandas DataFrame/Series）为单位接收输入、返回结果，把逐行调用变为批量调用，并能利用 NumPy/pandas 的向量化运算，大幅降低每行的开销。能用内置 SQL 表达的逻辑仍应优先使用 SQL。
