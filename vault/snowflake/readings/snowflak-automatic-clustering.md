---
nodes:
- storage.automatic-reclustering
title: 自动重新聚簇服务(Automatic Clustering)
corpus: snowflake-docs
section: 04-tables-auto-reclustering
url: https://docs.snowflake.com/en/user-guide/tables-auto-reclustering
tags:
- canonical
---

# 自动重新聚簇服务(Automatic Clustering)

一旦表定义了聚簇键,后续的 DML 会让数据逐渐偏离理想的聚簇状态;Automatic Clustering 是 Snowflake 在后台无感运行的托管服务,持续监控并按需重写微分区,使其重新贴合聚簇键,期间不阻塞用户的 DML。新一代 Optima Clustering 按摄入的数据量而非计算时长计费,旧版 Clustering Classic 按 serverless 计算小时计费,二者都归入同一账单科目。可以随时挂起/恢复该服务,但挂起不等于省钱——恢复时往往要补上挂起期间积压的重新聚簇工作。读完应理解:聚簇键定义之后,维护成本是持续、自动、且与信用点(credit)直接挂钩的。
