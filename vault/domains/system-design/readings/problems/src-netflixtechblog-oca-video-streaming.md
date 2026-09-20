---
nodes: [problems.media.video-streaming]
url: https://netflixtechblog.com/serving-100-gbps-from-an-open-connect-appliance-cdb51dda3b99
tags: []
---
# Serving 100 Gbps from an Open Connect Appliance

值得读：Netflix 官方工程博客（2017）披露了把一台基于 NVMe 闪存、100GbE 网卡的 Open
Connect Appliance（OCA）单机吞吐优化到稳定跑满 100 Gbps 的真实工程细节，包括此前的
闪存机型受 CPU 限制只能到约 40 Gbps、以及排查 FreeBSD 锁竞争瓶颈的过程。本题解「容量
估算」边缘命中率一段用这篇文章的 100 Gbps 真实数字做 10% 保守折扣（90 Gbps）计算所
需边缘设备数，并同时给出不打折扣、直接用 100 Gbps 计算的对照结果，不把之前未经验证
的"90 Gbps 官方数字"说法继续保留。
