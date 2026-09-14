---
id: udf-snowpark-optimized-warehouse
node: openplatform.snowpark-udf-udtf
type: qa
tags: [grown]
---
## Q
在标准仓库上运行一个加载大型机器学习模型的 Python UDTF 时频繁报内存不足。除了把仓库调大，还有什么针对性的选择？

## A
改用 Snowpark 优化型仓库（Snowpark-optimized warehouse）：在相同尺寸下，它的每个节点提供比标准仓库多得多的内存，面向内存密集的 UDF/UDTF 和存储过程（如在单节点上加载大模型或训练）。代价是同尺寸下信用点费率更高。单纯调大标准仓库增加的是节点数和总算力，未必能解决单个 Python 进程在单节点上内存不够的问题。
