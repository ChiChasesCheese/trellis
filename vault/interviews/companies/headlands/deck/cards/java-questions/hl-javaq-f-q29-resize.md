---
id: hl-javaq-f-q29-resize
node: java-questions.f-concurrency
type: qa
step: 15
---
## Q
用反射观察 `HashMap` 的 `table`：新建时、第 1 次、第 13 次、第 25 次 put 后容量分别是多少？为什么？

## A
- `new HashMap()`：`table = null`（**惰性分配**），第一次 put 才分配。
- 1 次 put 后：16。
- 13 次 put 后：32——阈值是 12 = 16 × 0.75，第 13 个触发翻倍。
- 25 次后 64；49 次后 128；97 次后 256。
- 读取 `HashMap.table` 的反射在 17+ 需要 `--add-opens java.base/java.util=ALL-UNNAMED`。
- 已知元素数 n 时用 `new HashMap<>(n * 4 / 3 + 1)` 避免多次扩容；`HashMap.newHashMap(n)` 是 Java 19 新增的便利方法。
