---
id: analytics-skew-stragglers
node: analytics.batch
type: qa
---
## Q
A 1000-task stage finishes in 5 minutes except one task still running after an hour. Give the two distinct causes and the fix for each.

## A
- **Data skew (hot key)**: hash partitioning sent one giant key (the null key, the whale customer) to one reducer. Fixes: **salt the key** (split it into `key#0..N` subkeys, aggregate twice), map-side pre-aggregation, or the engine's skew-join handling (e.g. Spark AQE splits oversized partitions).
- **Slow node (straggler)**: same data volume, sick machine (failing disk, noisy neighbor). Fix: **speculative execution** — run a duplicate of the slow task elsewhere, take the first finisher.

Diagnose by task input size: huge input = skew; normal input, slow progress = straggler. Speculation does nothing for skew — the duplicate gets the same giant key.

## Q zh
1000 个 task 的阶段在 5 分钟内完成，除了一个 task 在一小时后仍在运行。给出两个不同的原因和每个的修复。

## A zh
- **数据倾斜（hot key）**：hash partition 发送一个巨大 key（null key、whale customer）到一个 reducer。修复：**salt key**（把它分成`key#0..N` subkey，聚合两次）、map-side pre-aggregation、或引擎的 skew-join 处理（例如 Spark AQE 分裂超大 partition）。
- **慢节点（straggler）**：相同数据量，生病机器（失败磁盘、嘈杂邻居）。修复：**推测执行** — 在其他地方运行慢 task 的副本，取第一个完成者。

通过 task 输入大小诊断：巨大输入 = 倾斜；正常输入、慢进度 = straggler。推测对倾斜无效 — 副本得到相同巨大 key。
