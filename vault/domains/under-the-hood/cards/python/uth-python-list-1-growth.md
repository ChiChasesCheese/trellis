---
id: uth-python-list-1-growth
node: python.list
type: qa
step: 1
---
## Q
**append 为什么是均摊 O(1)**｜Python · CPython 3.14

`list.append` 连续调用时，容量是怎样一步步增长的？

## A
**结构。** 一块连续的指针数组（pointer array），对象里记着当前长度 `size` 和已分配容量 `allocated`。

**细节。**

- 容量用完才 `realloc`，新容量 ≈ `n + n/8 + 6`，再向下取整到 4 的倍数。
- 实测逐个 append 时，容量依次是：

```
0 → 4 → 8 → 16 → 24 → 32 → 40 → 52 → 64 → 76 ...
```

**为什么。** 只多留约 12.5%（Java `ArrayList` 是 1.5 倍），省内存；仍是按比例的几何增长，所以均摊 O(1)。

**对应 LeetCode：** LC 380 O(1) 时间插入、删除和获取随机元素 · LC 1472 设计浏览器历史记录
