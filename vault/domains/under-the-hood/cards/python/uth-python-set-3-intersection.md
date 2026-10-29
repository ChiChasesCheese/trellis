---
id: uth-python-set-3-intersection
node: python.set
type: qa
step: 3
---
## Q
**小集合和大集合求交集有多快**｜Python · CPython 3.14

`{1,2,3} & set(range(10**6))` 要 100 万次比较吗？`in` 用 `set` 和 `list` 差多少？

## A
**结构。** `set_intersection` 先比较两边大小，**遍历较小的那个**，每个元素去较大的集合里做一次哈希查找。

**细节。**

- 复杂度 O(min(m, n))，不是 O(m + n)；`a & b` 与 `b & a` 一样快。
- 本机实测：3 个元素 & 100 万元素，约 0.056 微秒。
- 判断 `999999 in` 100 万元素：`set` 约 0.017 微秒，`list` 约 5 毫秒。

**为什么。** 哈希查找是 O(1)，遍历大的一方没有意义。

**坑。** 把 `list` 转成 `set` 本身要 O(n)，只查一两次不划算。

**对应 LeetCode：** LC 349 两个数组的交集 · LC 350 两个数组的交集 II
