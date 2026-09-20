---
nodes: [problems.foundations.lock-service]
url: https://research.google/pubs/the-chubby-lock-service-for-loosely-coupled-distributed-systems/
tags: [reference]
---
# Burrows — The Chubby Lock Service for Loosely-Coupled Distributed Systems (OSDI 2006)

值得读：一手论文，本题解的会话/KeepAlive 参数（12 秒默认续约量、45 秒宽限期）、真实部署
规模（单元经常同时服务几万个客户端）、真实故障构成（700 单元-天里 61 次中断的具体原因
分布、6 次数据丢失的原因分布）全部引自这篇论文，用来给本题的设计参数提供真实量级参照。
和本题解的分歧在于：Chubby 把锁和小文件存储绑在一个类文件系统接口里，本题解按
ZooKeeper/etcd 更晚近的做法选择了更精简的路径式键值原语接口。

%% trellis:begin %%
## Source
[Open the original ↗](https://research.google/pubs/the-chubby-lock-service-for-loosely-coupled-distributed-systems/)
%% trellis:end %%
