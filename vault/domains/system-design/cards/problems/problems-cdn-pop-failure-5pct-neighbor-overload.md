---
id: problems-cdn-pop-failure-5pct-neighbor-overload
node: problems.foundations.cdn
type: qa
step: 7
tags: [grown]
---
## Q
In a CDN using anycast routing with 300 edge PoPs grouped into 15 shield regions of 20 edges each, one PoP handling its peak share of about 57,870 QPS fails and withdraws its BGP route. Why does each of the 19 remaining PoPs in its shield group only absorb about 5.3% more load rather than being overwhelmed, and why does this number depend on the shield group's size?

## A
Anycast routing means the failed PoP's traffic is redistributed by BGP path selection to the topologically nearest remaining PoPs, which in this design are the other 19 members of its shield group; splitting 57,870 QPS across 19 peers adds about 57,870 / 19 = 3,046 QPS to each, which is about 3,046 / 57,870 = 5.3% of each peer's own peak load. That percentage is a direct function of group size - a smaller shield group (e.g., 5 nodes) would leave only 4 peers to absorb the same failed node's traffic, raising each peer's overload to about 25% instead of 5.3% - so shield group size is a capacity-planning parameter that trades purge/shield efficiency against single-node-failure blast radius, and each edge node must be provisioned with enough headroom (N+1) to absorb its group's worst-case single failure.

## Q zh
在一个使用 anycast 路由的 CDN 中，300 个边缘 PoP 分成 15 个屏蔽区域，每个区域 20 个边缘。一个承担其峰值份额约 57,870 QPS 的 PoP 故障并撤回 BGP 路由。为什么同组剩下的 19 个 PoP 每个只多承担约 5.3% 的额外负载而不是被压垮，且这个数字为什么取决于屏蔽组的大小？

## A zh
anycast 路由意味着故障 PoP 的流量会被 BGP 路径选择重新分配给拓扑上最近的剩余 PoP，在本设计中就是同一屏蔽组内其余 19 个成员；把 57,870 QPS 分摊到 19 个同伴上，每个大约多 57,870 / 19 ≈ 3,046 QPS，占每个同伴自身峰值负载的约 3,046 / 57,870 ≈ 5.3%。这个百分比直接取决于分组大小——更小的屏蔽组（如 5 个节点）只剩 4 个同伴分担同一个故障节点的流量，每个同伴的过载会升到约 25% 而不是 5.3%——所以屏蔽组大小是一个在「屏蔽/purge 效率」与「单节点故障的影响半径」之间权衡的容量规划参数，每个边缘节点都必须预留足够的冗余（N+1）来吸收本组最坏情况下的单节点故障。
