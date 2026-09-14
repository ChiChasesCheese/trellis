---
nodes:
- storage.micro-partition-format
- storage.micro-partition-metadata
- storage.columnar-compression-encoding
- storage.clustering-keys
- pruning.min-max-zone-maps
- pruning.partition-elimination
- pruning.clustering-depth-metric
- metadata.optimizer-statistics
title: 微分区与数据聚簇的物理基础
corpus: snowflake-docs
section: 02-tables-clustering-micropartitions
url: https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions
tags:
- canonical
---

# 微分区与数据聚簇的物理基础

全书讲存储引擎绕不开的一篇:表数据被自动切成 50–500MB(压缩前)的微分区(micro-partition),按列存储、按列压缩,每个微分区的表头记录每列的最小/最大值、去重计数等统计信息——这些统计正是优化器做基数估计、选择执行计划所依据的元数据,全程无需扫描数据本身。查询裁剪(pruning)就是靠比较谓词与这些最小/最大值(min/max zone map),在编译期排除不可能命中的微分区,把全表扫描降级为部分扫描。文中还定义了聚簇深度(clustering depth)——衡量微分区在某些列上重叠程度的指标,深度越大说明裁剪效果越差,是判断是否需要显式聚簇键的信号。读完能解释裁剪、压缩、聚簇三者如何共享同一份微分区元数据。
