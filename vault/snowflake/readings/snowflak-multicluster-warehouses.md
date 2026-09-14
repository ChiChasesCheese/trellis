---
nodes:
- warehouse.multi-cluster-scaling-policy
- warehouse.query-queuing
title: 多集群仓库与扩缩容策略
corpus: snowflake-docs
section: 06-warehouses-multicluster
url: https://docs.snowflake.com/en/user-guide/warehouses-multicluster
tags:
- canonical
---

# 多集群仓库与扩缩容策略

多集群仓库(multi-cluster warehouse)让同一尺寸的仓库拥有多个并行集群,专门用来应对并发用户/查询数的波动,而不是加速单个慢查询——那是扩大尺寸(scale up)该做的事。可选最大化模式(Maximized,集群数固定不变)或自动伸缩模式(Auto-scale,按负载动态启停集群)。伸缩策略(scaling policy)决定自动伸缩的节奏:Standard 优先减少排队、更快加开集群;Economy 优先节省信用点、宁可让查询排队也要等集群装满负载再加开。读完应能根据业务对延迟与成本的取舍,判断该选哪种伸缩策略,以及集群数如何影响每小时信用点账单。
