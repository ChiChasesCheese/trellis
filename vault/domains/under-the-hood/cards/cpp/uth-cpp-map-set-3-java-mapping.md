---
id: uth-cpp-map-set-3-java-mapping
node: cpp.map-set
type: qa
step: 3
---
## Q
**C++ 的 lower_bound 对应 Java 的哪个方法**｜C++ · map / set 与 Java TreeMap

刷题时要找“不小于 x 的最小元素”或“小于 x 的最大元素”，C++ 与 Java 各怎么写？

## A
**结构。** 同一棵红黑树，两种语言只是给“向下找最近邻居”起了不同的名字。

**细节。**

| 需求 | C++ | Java `TreeMap` |
|---|---|---|
| 第一个 ≥ x | `lower_bound(x)` | `ceilingKey(x)` |
| 第一个 > x | `upper_bound(x)` | `higherKey(x)` |
| 最后一个 ≤ x | `prev(upper_bound(x))` | `floorKey(x)` |
| 最后一个 < x | `prev(lower_bound(x))` | `lowerKey(x)` |

**坑。** C++ 找不到时返回 `end()`，往前挪之前要先判断是不是 `begin()`；Java 找不到返回 `null`。

**对应 LeetCode：** LC 220 存在重复元素 III · LC 855 考场就座
