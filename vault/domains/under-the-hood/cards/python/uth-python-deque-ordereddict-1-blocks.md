---
id: uth-python-deque-ordereddict-1-blocks
node: python.deque-ordereddict
type: qa
step: 1
---
## Q
**deque 为什么两端都是 O(1)**｜Python · CPython 3.14

`collections.deque` 的内部是链表还是数组？为什么不直接一个元素一个链表节点？

## A
**结构。** 双向链表，但每个节点是一个**固定 64 槽的数据块**（`BLOCKLEN = 64`），两端各记一个块内下标。

**细节。**

- 在头尾增删只改端点块里的一个槽，满了才挂一个新块，不搬动其他元素，也不用 `realloc`。
- 实测 `appendleft` 加 `popleft` 约 22 纳秒。

**为什么。** 一元素一节点要带两个指针，额外开销 200%，每个元素还要一次 `malloc`；分块后链接开销约 3%，相邻元素也靠在一起。

**对应 LeetCode：** LC 239 滑动窗口最大值 · LC 641 设计循环双端队列
