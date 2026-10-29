---
id: uth-python-asyncio-2-lazy-cancel
node: python.asyncio
type: qa
step: 2
---
## Q
**取消的定时器怎么从堆里删掉**｜Python · CPython 3.14

`call_later` 返回的句柄调用 `cancel()` 后，它会马上从最小堆里移除吗？

## A
**结构。** 不会。这是堆上的**惰性删除**（lazy deletion）：只给句柄打上已取消标记，仍留在堆里。

**细节。**

- 每轮循环，堆顶如果是已取消的，就 `heappop` 丢掉。
- 堆里超过 100 项且已取消的占一半以上时，过滤掉它们再 `heapify` 整个重建。
- 实测 1000 个定时器取消尾部 400 个，堆仍是 1000；累计取消 600 个后降到 400。

**为什么。** 从堆中间删一个元素要先找到它，O(n)；惰性删除让 `cancel` 是 O(1)，批量清理摊到各轮里。

**对应 LeetCode：** LC 480 滑动窗口中位数 · LC 218 天际线问题
