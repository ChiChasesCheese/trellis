---
id: hl-javaq-f-q30-atomic-ops
node: java-questions.f-concurrency
type: qa
step: 19
---
## Q
8 线程各 20 万次对 16 个 key 做 `merge(i&15, 1, Integer::sum)`，`HashMap` 与 `ConcurrentHashMap` 各得到多少？CHM 里哪些操作是原子的，哪些组合不是？

## A
- 预期 1,600,000：`HashMap` 得到 **1,231,627**，丢了 368,373（约 23%）；`ConcurrentHashMap` 得到 **1,600,000**，丢 0。
- `HashMap` 并发更新同一个 key：读-改-写交错 → 丢更新。
- **CHM 单个方法是原子的**：`putIfAbsent`、`computeIfAbsent`、`merge`、`compute`。
- **组合不是原子的**：`if (!m.containsKey(k)) m.put(k, v)` 有竞态（check-then-act），要用 `putIfAbsent`。
- 每 key 一个原子计数器：`map.computeIfAbsent(k, x -> new LongAdder()).increment()` 或 `merge`。
