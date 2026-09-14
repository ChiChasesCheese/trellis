---
id: distributed-lag-anomalies
node: distributed.replication.leader
type: qa
---
## Q
Name the two classic read anomalies replication lag causes besides missing your own writes, and the guarantee that fixes each.

## A
- **Going backwards in time**: successive reads hit differently-lagged replicas, so data you already saw disappears. Fix: **monotonic reads** — pin a session to one replica (or track a min-version the serving replica must have).
- **Seeing effects before causes**: an answer replicates faster than the question it references. Fix: **consistent prefix / causal reads** — expose writes only in an order that preserves causality (per-partition ordering, causal tokens).

Both are session/ordering guarantees — far cheaper than making all reads linearizable, which is the sledgehammer answer.

## Q zh
除了看不到自己刚写的数据之外，说出复制延迟导致的两种经典读异常，以及各自对应的能修复它的保证。

## A zh
- **时间倒流**：连续的读命中了延迟程度不同的副本，于是你已经看到过的数据又消失了。修复：**单调读（monotonic reads）**——把一个会话固定到一个副本上（或者跟踪一个提供服务的副本必须满足的最小版本号）。
- **先看到结果后看到原因**：一个答案复制得比它所引用的问题还快。修复：**一致前缀 / 因果读（consistent prefix / causal reads）**——只按保持因果关系的顺序暴露写入（按分区排序、因果 token）。

这两者都是会话/排序层面的保证——比让所有读都线性一致（那种大力出奇迹的做法）要便宜得多。
