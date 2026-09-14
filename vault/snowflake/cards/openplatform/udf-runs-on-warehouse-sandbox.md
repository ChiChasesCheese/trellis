---
id: udf-runs-on-warehouse-sandbox
node: openplatform.snowpark-udf-udtf
type: qa
tags: [grown]
---
## Q
Snowpark 的 Python/Java/Scala UDF 代码实际在哪里执行？为什么说这样“代码向数据移动”而不是“数据向代码移动”？

## A
UDF 代码在执行查询的虚拟仓库节点上、在安全沙箱（sandbox）中运行，与查询算子一起并行处理数据，费用计入该仓库的信用点消耗。数据无需导出到外部应用服务器再处理，也就避免了大规模数据传输以及数据离开 Snowflake 治理边界的安全风险。Python 依赖包从 Snowflake 提供的 Anaconda 渠道或上传到 stage 的文件中加载。
