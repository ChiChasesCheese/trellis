---
id: uth-python-heapq-bisect-2-max-heap
node: python.heapq-bisect
type: qa
step: 2
---
## Q
**heappop 为什么先下沉到底**｜Python · CPython 3.14

`heappop` 把末尾元素放到堆顶后，为什么不是比较到合适位置就停，而是先一路下沉到叶子？最大堆呢？

## A
**结构。** `_siftup`：每层把较小的孩子上移一格，直到叶子，再把原来的末尾元素从那里上浮回去。

**细节。**

- 末尾元素通常很大，从根往下比，大多数时候走不到提前退出，所以先到底再上浮。
- 源码注释的实测：1000 次 `heappop` 的比较次数从约 14996 降到约 8680。
- 3.14 起有了 `heappush_max`、`heappop_max`、`heapify_max`；以前只能存负数。

**为什么。** 比较可能是自定义的 `__lt__`，很贵，省比较比省赋值重要。

**对应 LeetCode：** LC 23 合并 K 个升序链表 · LC 347 前 K 个高频元素
