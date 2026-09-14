---
id: compile-stage-order-and-location
node: query.compilation-pipeline
type: cloze
tags: [grown]
---
Snowflake 一条 SQL 的处理顺序：{{c1::解析（parse）}}，把文本变成语法树 → {{c2::绑定（bind）}}，依据元数据解析对象名并检查权限 → {{c3::优化（optimize）}}，做逻辑改写、基于代价选择物理计划并完成分区剪枝 → 生成物理执行计划。前三步运行在 {{c4::云服务（Cloud Services）层}}，最后计划被派发到 {{c5::虚拟仓库（virtual warehouse）}} 的工作节点上执行。
