---
id: uth-java-linkedhashmap-treemap-3-treemap
node: java.linkedhashmap-treemap
type: qa
step: 3
---
## Q
**TreeMap 怎么 O(log n) 找到最近的 key**｜Java · OpenJDK 25

`TreeMap` 的 `floorKey`、`ceilingKey` 是怎么实现的？它判断 key 相等用 `equals` 吗？

## A
**结构。** 红黑树（red-black tree）：每个节点有 `left`、`right`、`parent` 和颜色，中序遍历就是升序。

**细节。**

- `ceilingKey(k)` 从根往下走：小于当前节点往左，大于往右，等于直接返回；树高 O(log n)。
- 实测 `{10,20,30}` 上：`floorKey(25)=20`，`ceilingKey(25)=30`，`floorKey(5)=null`。
- 相等只看 `compareTo`（或比较器）：`BigDecimal` 的 `1.0` 和 `1.00` 在 `TreeMap` 里是同一个 key（大小 1），在 `HashMap` 里是两个（大小 2）。

**为什么。** 哈希表只能精确匹配；找前驱、后继、区间要有序结构，代价是 O(log n)。

**对应 LeetCode：** LC 729 我的日程安排表 I · LC 220 存在重复元素 III
