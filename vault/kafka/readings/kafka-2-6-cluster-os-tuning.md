---
nodes:
- practice.sizing-tuning
title: 配置Kafka集群：broker数量与操作系统调优
corpus: kafka-2e
section: 025-2-6-kafka
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 配置Kafka集群：broker数量与操作系统调优

本节讨论一个集群需要多少个broker、如何设置broker级别的配置，以及操作系统层面(如文件描述符限制、虚拟内存、磁盘调度器)的调优要点。这些调优细节直接影响集群在高负载下的稳定性，是从单机验证过渡到多节点生产集群时必须补的一课。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
