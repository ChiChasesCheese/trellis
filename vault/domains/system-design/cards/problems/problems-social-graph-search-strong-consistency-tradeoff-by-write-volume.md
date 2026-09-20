---
id: problems-social-graph-search-strong-consistency-tradeoff-by-write-volume
node: problems.social.social-graph-search
type: qa
step: 7
tags: [grown]
---
## Q
A social graph design stores a friendship as two directed rows (A→B and B→A) and writes both synchronously inside a cross-shard transaction so they always succeed or fail together, at an estimated peak write rate of about 29 edge writes/sec. Why would this same choice stop making sense if this store also had to carry a much higher-frequency edge type, such as a 'like' modeled as an edge at tens of thousands of writes/sec?

## A
A cross-shard transaction's coordination overhead is a fixed per-write cost that a design can afford when write volume is low relative to what the coordination mechanism can sustain — at ~29 writes/sec, that overhead is negligible. At a vote/like-scale write rate, the same per-write coordination cost would become the dominant bottleneck, the way a high-write-rate voting system instead accepts asynchronous propagation of the second row plus a reconciliation pass that repairs any temporarily one-sided edges, trading brief inconsistency for throughput headroom the strongly consistent approach can't provide at that scale.

## Q zh
一个社交图设计把一条好友关系存成两行有向记录（A→B 和 B→A），并把两者包进一个跨分片事务同步写入，使其要么同时成功要么同时失败，估算的边写入峰值约为每秒 29 条。如果这份存储还要承载一种频率高得多的边类型（比如把「点赞」也建模成一条边，写入量级到每秒几万条），为什么这个选择就不再成立了？

## A zh
跨分片事务的协调开销是每次写入固定要付的成本，当写入量级相对协调机制能承受的上限很低时（约每秒 29 条写入下，这点开销可以忽略），这个成本负担得起。到了投票/点赞级别的写入速率，同样的每次写协调成本会变成主导瓶颈，这时候需要转向像高写入速率投票系统那样，异步传播第二行、再配合一个修复临时单向边的对账流程，用短暂的不一致换取强一致方案在那个量级下给不了的吞吐余量。
