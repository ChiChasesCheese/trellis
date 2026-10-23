---
id: hl-cx-pitfall-small-n
node: foundations.complexity
type: qa
step: 40
---
## Q
O(n log n) 一定比 O(n²) 快吗？JDK 的 `TimSort` 怎么利用这一点？

## A
不一定，只对足够大的 n 成立。n = 20 时插入排序（O(n²)）常比归并排序（O(n log n)）快，因为 O(n²) 算法常数小、没有递归和额外内存开销。

所以 JDK 的 `TimSort` 对短片段用**二分插入排序**，长数据才用归并。这和「小数据下排好序的 `ArrayList` + 二分常比 `TreeMap` 快」是同一个道理：渐近复杂度只描述 n 很大时的趋势。
