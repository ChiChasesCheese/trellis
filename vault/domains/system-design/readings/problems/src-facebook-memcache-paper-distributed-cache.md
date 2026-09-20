---
nodes: [problems.foundations.distributed-cache]
url: https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf
tags: [paper]
---
# Scaling Memcache at Facebook
值得读：这是本题解的核心一手来源——NSDI 2013 论文原文，披露了 Facebook 生产环境里
memcache 集群的真实读写比（读比写高两个数量级）、单次热门页面加载平均触发约 521 次
不同的 memcache 查询、用于防止 stale set 和 thundering herd 的 lease 机制、约占集群
1% 节点规模的 gutter pool 故障降级池,以及 mcsqueal daemon 解析数据库提交日志做批量
失效广播的设计。本题解与论文的不同：论文描述的是单一真实部署的具体数字，本题解把
论文披露的这些机制套进一个假设的 2 亿日活场景重新做了一遍容量估算，并补充了论文未
展开的"同一工作负载下 Redis 风格与 Memcached 风格谁是 QPS 瓶颈、谁是内存瓶颈"这个
技术选型对比。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.usenix.org/system/files/conference/nsdi13/nsdi13-final170_update.pdf)

## Archived copy
![[src-facebook-memcache-paper-distributed-cache-clip]]
%% trellis:end %%
