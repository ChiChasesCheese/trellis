---
id: uth-storage-query-exec-3-merge-join
node: storage.query-exec
type: qa
step: 3
---
## Q
**排序归并连接：双指针**｜PostgreSQL · 18

两张表都已按连接键有序时，怎么连接最省？键有重复怎么办？

## A
**结构。** 归并连接（merge join）：两侧各一个游标，较小的一侧前进，相等就输出，像合并两个有序数组。

**细节。**

- 代价 O(n + m)，不建哈希表；输入没排序就先排序，所以执行计划里常见 `Sort` → `Merge Join`。
- 重复键：外侧遇到每一条重复键，内侧游标都要回到该键的第一条；执行器对内侧做标记（mark），之后恢复（restore）。
- 连接条件只能是等值，形如 `outerKey = innerKey`。

**为什么。** 输入本来就有序（走了索引，或下游要 `ORDER BY`）时，比哈希连接更省，输出还自带顺序。

**对应 LeetCode：** LC 88 合并两个有序数组 · LC 986 区间列表的交集
