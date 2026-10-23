---
id: hl-cx-benchmark-numbers
node: foundations.complexity
type: qa
step: 31
---
## Q
在 Apple Silicon、JDK 21 上实测：纯算术紧循环、`HashMap`、`TreeMap`、O(n²) 数对循环的速度各是多少？这说明「10⁸ 次/秒」法则是偏保守还是偏乐观？

## A
- 纯算术依赖乘加循环：10⁹ 次 0.64 秒，约 1.6 × 10⁹ 次/秒；二重循环约 2 × 10⁹ 对/秒，比 10⁸ 快 10–20 倍。
- `HashMap<Integer,Integer>`（100 万随机键）：`put` 60 ns，`get` 10 ns。
- `TreeMap`：`put` 239 ns，`get` 215 ns，约 4 × 10⁶ 次/秒，比 HashMap 慢约 4 倍（20 层树 × 每层可能一次缓存未命中）。
- O(n²) 数对：n = 2 万约 0.1 秒，n = 10 万（5 × 10⁹ 对）约 **2.4 秒**，限时 1 秒就超时。

结论：纯算术下 10⁸ 偏保守，但只要每步碰数据结构就远低于 10⁸，方向是对的。
