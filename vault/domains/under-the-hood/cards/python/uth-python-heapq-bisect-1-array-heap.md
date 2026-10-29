---
id: uth-python-heapq-bisect-1-array-heap
node: python.heapq-bisect
type: qa
step: 1
---
## Q
**heapq 的堆放在哪里**｜Python · CPython 3.14

`heapq` 只有函数、没有堆这个类，堆存在什么里？为什么 `heapify` 比逐个 `heappush` 快？

## A
**结构。** 一个普通 `list`，当作数组上的完全二叉树：下标 `i` 的子节点是 `2i+1`、`2i+2`，父节点是 `(i-1)>>1`。

**细节。**

- `heappush` 把元素放末尾再上浮，`heappop` 取走堆顶并下沉，都是 O(log n)。
- `heapify` 从 `n//2 - 1` 往回逐个下沉，总共 O(n)。
- 实测 100 万个浮点数：`heapify` 15.5 毫秒，逐个 `heappush` 26.3 毫秒。

**为什么。** 下标算术不要指针；叶子占一半，从下往上建堆时大部分节点几乎不用动。

**坑。** `(优先级, 对象)` 元组优先级相同时会比较对象，不可比较就抛 `TypeError`。

**对应 LeetCode：** LC 215 数组中的第 K 个最大元素 · LC 295 数据流的中位数
