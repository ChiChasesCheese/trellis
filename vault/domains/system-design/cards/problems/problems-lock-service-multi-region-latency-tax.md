---
id: problems-lock-service-multi-region-latency-tax
node: problems.foundations.lock-service
type: cloze
step: 8
tags: [grown]
---
In a distributed lock/coordination service design, stretching a single 5-node consensus ensemble across three regions (2 nodes in one region, 2 in a second, 1 in a third) means every write's quorum must wait for a third acknowledgment beyond the leader and its same-region peer; at a representative same-continent RTT of about 60ms, this pushes write commit latency to roughly {{c1::60ms}}, compared to about {{c2::1ms}} for an ensemble kept within a single region — nearly two orders of magnitude slower. The better default is {{c3::one independent consensus ensemble per region for region-local coordination, with a small separate global ensemble reserved only for the rare decisions that genuinely need one answer across all regions}}.

## zh
在一个分布式锁/协调服务设计中，把单个 5 节点共识集群拉伸跨越三个区域（一个区域 2 个节点，另一个区域 2 个，第三个区域 1 个），意味着每次写的 quorum 除了 leader 和同区域的那个节点之外，还要再等第三个确认；按一个具有代表性的同大洲往返延迟约 60ms 估算，这会把写提交延迟推高到约 {{c1::60ms}}，而如果集群保持在单一区域内，这个延迟约为 {{c2::1ms}}——慢了近两个数量级。更好的默认做法是{{c3::每个区域各自部署一个独立的共识集群处理区域内协调，只用一个单独的小型全局集群服务真正需要在所有区域间给出唯一答案的少数决策}}。
