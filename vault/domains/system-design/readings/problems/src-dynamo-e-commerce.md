---
nodes: [problems.commerce.e-commerce]
url: https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
tags: [paper]
---
# Dynamo: Amazon's Highly Available Key-value Store

值得读：Amazon 官方发表的经典论文，把购物车服务明确列为"必须在网络分区、磁盘故障
下依然可写"的动机案例（"customers should be able to view and add items to their
shopping cart even if disks are failing, network routes are flapping, or data centers
are being destroyed by tornados"），并用向量时钟做多版本合并、把冲突推迟到读时解
决。本题解购物车一节采用同样的"始终可写"动机，但方案更轻——匿名购物车走 TTL 缓存、
登录购物车走一次性显式合并，而不是论文里持续存在的多版本向量时钟，因为本设计假设的
购物车丢失代价远低于论文描述的场景。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

## Archived copy
![[dynamo-paper-clip]]
%% trellis:end %%
