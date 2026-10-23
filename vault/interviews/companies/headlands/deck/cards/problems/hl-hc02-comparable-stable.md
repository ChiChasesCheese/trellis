---
id: hl-hc02-comparable-stable
node: problems.hc02-merge-k-streams
type: qa
step: 2
---
## Q
合并有序序列时为什么不能用 `a - b` 比较？「稳定」(stable) 是什么意思，签名里的 `<T extends Comparable<? super T>>` 表示什么？

## A
- **不能用 `a - b < 0`**：`Long.MIN_VALUE - 1` 之类会溢出成大正数，判断反了。永远用 `compareTo` 或 `Long.compare`。C++ 里 `a - b` 是有符号溢出（UB），而且元素可能只有 `operator<`。
- **稳定**：两个元素相等（`compareTo == 0`）但不是同一个东西时，稳定的合并让它们**保持原来的相对顺序**。这里规定相等时**序列编号小的在前**，同序列内保持原顺序，输出才确定、期望才能写。只有元素的 `compareTo` 只比较部分字段时，稳定性才看得出。
- **`<T extends Comparable<? super T>>`**：`T` 必须能和「T 或其父类」比较。`Dog extends Animal`、`Animal implements Comparable<Animal>` 时，`Dog` 不是 `Comparable<Dog>` 却能和 `Animal` 比，`? super T` 让它也能用（`Collections.sort` 同写法）。

实现稳定的方法：堆的比较键是 `(值, 序列编号)`，先比值再比编号。
