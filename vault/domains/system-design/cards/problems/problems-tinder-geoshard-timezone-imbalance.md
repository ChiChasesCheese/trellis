---
id: problems-tinder-geoshard-timezone-imbalance
node: problems.social.tinder
type: qa
step: 7
tags: [grown]
---
## Q
Tinder's own engineering blog reports that geoshards covering different regions can see peak request rates differing by more than 10x at any given moment, because users within the same geoshard tend to sit in adjacent time zones and peak/off-peak hours differ by time zone. Why did they reject manually assigning complementary-timezone geoshard replicas to the same physical hosts, and what did they use instead?

## A
Manually pairing geoshards with offsetting peak times onto the same hosts is an NP-hard combinatorial problem that would need to be re-solved every time the cluster is resharded as the user base grows. Instead, they randomly distribute each geoshard's replicas across physical hosts — statistically, random distribution alone averages out the time-zone-driven peak/off-peak mismatch across hosts without needing a custom scheduling algorithm, trading a small amount of theoretical optimality for avoiding an NP-hard problem that has to be re-solved on every resharding.

## Q zh
Tinder 自己的工程博客披露，覆盖不同地区的 geoshard 在同一时刻的峰值请求率可以相差超过 10 倍，因为同一个 geoshard 内的用户通常处在相邻时区，峰值/低谷时段因时区而不同。为什么他们放弃了「把互补时区的 geoshard 副本手动分配到同一台物理机」这个方案？他们改用了什么？

## A zh
把峰值时段互补的 geoshard 手动配对到同一台物理机是一个 NP 难的组合优化问题，而且每次因用户增长而重新分片时都要重新求解一次。他们改为把每个 geoshard 的副本随机分布到物理主机上——统计学上，仅靠随机分布本身就能把时区导致的峰值/低谷错位在各台主机上摊平，不需要定制调度算法，用放弃一部分理论最优性换来不必每次重新分片都重新求解一个 NP 难问题。
