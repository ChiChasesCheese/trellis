---
id: hi-pt-top-k-counts-4-merge-correct
node: qb.sd.top-k-counts.points
type: qa
step: 4
---
## Q
**Top-K 热门榜 · 分片前 K 归并的正确性**｜必会 · 出自：Top-K 热门榜 › 整体设计

各分片各取前 K 再归并，为什么得到的是精确的全局前 K？

## A
**为什么。** 对象按 ID 分区，每个对象只属于一个分片，所以全局前 K 一定包含在各分片前 K 的并集里。
**易错。** 若按时间或随机分区，同一对象的计数散在多个分片，结论不成立。
