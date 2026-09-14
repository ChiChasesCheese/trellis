%% trellis:begin %%
# 多集群共享数据模型
*核心架构*

该模型与无共享架构（shared-nothing，每个节点拥有自己的数据）以及共享磁盘架构（shared-disk，所有节点共享一块磁盘）的区别——每个仓库都在同一份共享的、带版本的数据存储之上拥有自己独立的计算资源。

## Readings
- [[snowflak-key-concepts-architecture|Snowflake 关键概念与整体架构]]

## Cards (5)
- [[multi-cluster-shared-consistent-view]]
- [[multi-cluster-shared-data-hybrid-benefit]]
- [[multi-cluster-shared-independent-compute-one-store]]
- [[multi-cluster-shared-vs-shared-disk-bottleneck]]
- [[multi-cluster-shared-vs-shared-nothing]]
%% trellis:end %%

## Notes
