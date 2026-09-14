---
nodes:
- pruning.query-acceleration-service
- cost.serverless-feature-billing
title: 查询加速服务(QAS)加速离群查询
corpus: snowflake-docs
section: 11-query-acceleration-service
url: https://docs.snowflake.com/en/user-guide/query-acceleration-service
tags:
- canonical
---

# 查询加速服务(QAS)加速离群查询

查询加速服务(Query Acceleration Service,QAS)把一个仓库里跑得特别慢的“离群查询”——通常是大扫描配合选择性过滤,或大批量插入/复制——的扫描过滤部分,借用 Snowflake 提供的共享 serverless 计算资源并行处理,从而不必为偶发的重查询把整个仓库开得很大。是否加速、加速到什么程度由系统自动判断,用户只能通过扩展因子(scale factor)设置资源上限来控制成本;该服务与其他 serverless 特性一样,按使用秒数单独计费,与仓库信用点分开出现在账单里。读完应理解:QAS 解决的是单条查询的尾延迟问题,而非整体并发问题。
