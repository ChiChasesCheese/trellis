---
id: uth-python-lru-cache-1-linked-list
node: python.lru-cache
type: qa
step: 1
---
## Q
**lru_cache 怎么 O(1) 淘汰最久没用的**｜Python · CPython 3.14

`@lru_cache(maxsize=2)` 命中时做什么？缓存满了怎么淘汰？

## A
**结构。** 一个 `dict`（key 到链表节点）加一条带哨兵节点 `root` 的环形双向链表（C 实现）。

**细节。**

- 命中：查 `dict` 找到节点，摘下来接到链表尾，O(1)。
- 满了：取 `root.next`（最久没用的）出来，从 `dict` 删掉，**复用同一个节点**装新的 key 和结果，接到链表尾。
- 实测依次调用 `f(1) f(2) f(1) f(3) f(2)`：`hits=1, misses=4, currsize=2`。

**为什么。** `dict` 负责 O(1) 查找，链表负责 O(1) 调整顺序，复用节点省掉一次分配和释放；这正是 LC 146 的标准解。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 460 LFU 缓存
