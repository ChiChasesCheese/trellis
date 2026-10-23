---
id: hl-j18-comparator-contract
node: java21.j18-comparators-interfaces
type: qa
step: 1
---
## Q
`Comparator<T>` 的 `compare(a, b)` 返回值代表什么？它和 `Comparable` 有什么区别？比较器必须满足哪三条契约，违反会怎样？

## A
`int compare(Order a, Order b)`：负数 = a 排在 b 前；0 = 相等；正数 = a 排在 b 后。`Comparator<T>` 是**外部比较器**；类自己实现 `Comparable<T>` 的 `compareTo` 是**自然顺序**。

三条契约：
1. **反对称**：`compare(a, b)` 与 `compare(b, a)` 符号相反；
2. **传递**：`a<b` 且 `b<c` 则 `a<c`；
3. **一致**：同样的输入永远得到同样的结果。

违反契约，轻则排序结果乱，重则 `TimSort` 抛 `IllegalArgumentException: Comparison method violates its general contract!`（不保证每次都检测到）。
