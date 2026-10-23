---
id: hl-j18-comparator-api
node: java21.j18-comparators-interfaces
type: qa
step: 5
---
## Q
`Comparator` 的静态和默认方法有哪些（`comparing`、`comparingInt/Long/Double`、`naturalOrder/reverseOrder`、`reversed`、`thenComparing`、`nullsFirst/nullsLast`）？各自作用是什么？

## A
- `Comparator.comparing(keyExtractor)`：按「从元素里抽出的键」比较，键需 `Comparable`；`comparing(keyExtractor, keyComparator)` 键用你给的比较器；
- `comparingInt` / `comparingLong` / `comparingDouble`：键是基本类型，**避免装箱**；
- `naturalOrder()` / `reverseOrder()`：自然顺序 / 反过来；
- `c.reversed()`：把比较器 `c` 反过来；
- `c.thenComparing(...)` / `thenComparingInt/Long/Double`：`c` 比不出来（返回 0）时再用第二个键；
- `Comparator.nullsFirst(c)` / `nullsLast(c)`：包一层，`null` 排前/排后，非 null 用 `c`。

每个调用返回新的 `Comparator`，所以能链式，**从左到右**读（Java 8）。
