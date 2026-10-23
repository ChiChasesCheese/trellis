---
id: hl-j18-real-sites
node: java21.j18-comparators-interfaces
type: qa
step: 22
---
## Q
真实代码里比较器和卫语句的典型用法有哪些？

## A
- 作业链排序：`out.sort(Comparator.comparingLong(Chain::totalSeconds).reversed().thenComparingInt(Chain::startJob))`，总时长降序、同时长按起点升序（`reversed()` 位置正确，基本类型版避免装箱）。
- k 路合并堆：`Comparator.<Head<T>, T>comparing(h -> h.value).thenComparingInt(h -> h.stream)`，值相同按流编号 tie-break；显式类型参数解决类型推导盲区。
- 买盘价位表：`new TreeMap<>(Comparator.reverseOrder())`，价格降序，`firstEntry()` 就是最优买价。
- 卫语句：`Order`/`Limit`/`Market` 紧凑构造器里 `Objects.requireNonNull(side, "side")`；`TickerMap` 每个公共方法第一行 `Objects.requireNonNull(key, "key")`；`Objects.requireNonNull(h.source.next(), "null element in stream " + h.stream)`。

接口 default 冲突规则作为概念被问到，实现里最接近的是 `sealed interface` 层级，成员都是 record。
