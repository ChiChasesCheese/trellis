---
id: foundations-when-estimates-change-design
node: foundations.estimation
type: qa
---
## Q
Give three estimate outcomes that each flip a design decision (the whole point of doing the math).

## A
- **Working set fits in RAM** (≲ a few hundred GB) → cache or serve it all from memory; no need to optimize disk paths.
- **Write QPS exceeds a single node** (~tens of thousands for a tuned DB) → partitioning is mandatory, choose a shard key now.
- **Read/write ratio is 100:1+** → invest in caching and read replicas, not write throughput.

If an estimate doesn't change any decision, say so and move on.


## Q zh
给出三个会各自翻转一个设计决策的估算结果（这正是做这些数学的意义所在）。

## A zh
- **工作集能放进内存**（≲ 几百 GB）→ 全部缓存或直接从内存提供服务；不需要优化磁盘路径。
- **写 QPS 超过单节点能力**（调优过的数据库约几万 QPS）→ 分区是必须的，现在就要选分片键。
- **读写比在 100:1 以上** → 应该投资于缓存和读副本，而不是写吞吐量。

如果一个估算不会改变任何决策，就直说，然后继续往下走。
