---
id: hl-hc11-binary-search-cpp
node: problems.hc11-order-interval-overlap
type: qa
step: 15
---
## Q
坐标压缩里的 `floorIndex` / `lowerBound` 怎么用 `Arrays.binarySearch` 写？C++ 版线段树实现要注意什么？

## A
二分辅助：`Arrays.binarySearch` 没找到返回 `-(插入点) - 1`（插入点 = 第一个大于 x 的下标），所以
```java
private int floorIndex(long x)  { int i = Arrays.binarySearch(coords, x); return i >= 0 ? i : -i - 2; }  // ≤ x 的最大下标
private int lowerBound(long x)  { int i = Arrays.binarySearch(coords, x); return i >= 0 ? i : -i - 1; }  // ≥ x 的最小下标
```
线段树下标是压缩后的小 `int`，不会溢出，但坐标（`long`）只比较不做减法。

C++ 要点：「查询时下推标记」让查询变非 `const`、并发读也不安全，所以用永久化标记；`IntervalIndex::update` 要先对两个端点都做 `exact_index` 再改树，否则第二个端点未知时树已被改成半更新；`enum class Side` 可以装 `static_cast<Side>(7)`，要在入口检查。
