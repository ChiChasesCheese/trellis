---
id: tlc-tops-lru-cache-0-whole
node: linked-list.lru-cache
type: qa
---
## Q
**LC 146 LRU 缓存**｜Medium · 全公司热度第 4 名 · NeetCode 150、Hot 100、Top Interview 150

设计并实现满足 LRU（最近最少使用，Least Recently Used）缓存约束的数据结构 `LRUCache`：`LRUCache(capacity)` 以正整数容量初始化；`get(key)` 在关键字存在时返回其值，否则返回 `-1`；`put(key, value)` 在关键字已存在时变更其值，不存在时插入，插入后若关键字数量超过 `capacity`，就逐出**最久未使用**的关键字。`get` 和 `put` 必须以平均 `O(1)` 的时间复杂度运行。`1 <= capacity <= 3000`，`0 <= key <= 10000`，`0 <= value <= 10^5`，最多调用 `2 * 10^5` 次 `get` 和 `put`。例：容量 `2`，`put(1,1)`、`put(2,2)`、`get(1)` 得 `1`、`put(3,3)`（逐出键 `2`）、`get(2)` 得 `-1`、`put(4,4)`（逐出键 `1`）、`get(1)` 得 `-1`、`get(3)` 得 `3`、`get(4)` 得 `4`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 组合数据结构设计：哈希表 + 双向链表（hash map + doubly linked list）。

**一句话。** 哈希表存「键 → 链表节点」负责 `O(1)` 查找，双向链表按使用时间从新到旧排列，负责 `O(1)` 摘节点、放队首和逐出队尾。

**识别。** 「`O(1)` 查找」指向哈希表，「按使用顺序排、`O(1)` 删除任意位置并放到最前」指向双向链表；两个要求一个结构满足不了，所以是组合结构。调用 `2 * 10^5` 次，线性扫描会到 `10^8` 以上，必须 `O(1)`。

**推导。** 暴力：用列表按使用顺序存键值对，查找和挪动都是 `O(n)`。浪费有两处：查找可以交给字典；「挪到最前」在数组里要整体平移，而在链表里只改相邻两个节点的指针，前提是已经拿到了节点，字典恰好存着键到节点的映射。摘节点需要改前驱的指针，所以用双向链表。

**简单解法。** Python 的 `OrderedDict` 自带哈希表加双向链表，`move_to_end` 标记刚用过，`popitem(last=False)` 弹出最久未使用的键，面试官不禁用时这就是合格答案。

```python
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.od: OrderedDict[int, int] = OrderedDict()  # 队头最久未使用，队尾最近使用

    def get(self, key: int) -> int:
        if key not in self.od:
            return -1
        self.od.move_to_end(key)  # 命中：标记为刚用过
        return self.od[key]

    def put(self, key: int, value: int) -> None:
        self.od[key] = value
        self.od.move_to_end(key)  # 新键、旧键都放到队尾
        if len(self.od) > self.cap:
            self.od.popitem(last=False)  # 超容量：弹出队头
```

手写双向链表是被要求「不许用 `OrderedDict`」时的标准答案：

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0) -> None:
        self.key, self.val = key, val
        self.prev: Node | None = None
        self.next: Node | None = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.map: dict[int, Node] = {}  # key -> 链表节点，O(1) 找到节点
        # 哨兵节点消掉空链表和头尾的特判：head.next 是最近使用的，tail.prev 是最久未使用的
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node: Node) -> None:  # 摘下节点：只改相邻两个节点的指针，O(1)
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node: Node) -> None:  # 插到 head 之后 = 标记为最近使用
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._unlink(node)  # 命中也算一次使用：挪到最前
        self._push_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:  # 已存在：更新值并挪到最前，不会触发逐出
            node = self.map[key]
            node.val = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.cap:  # 满了：逐出链表尾（最久未使用）
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]  # 节点里存着 key，才能回头删字典项
        node = self.map[key] = Node(key, value)
        self._push_front(node)
```

运行：题面序列的输出是 `[None, None, None, 1, None, -1, None, -1, 3, 4]`；容量 `1` 时 `put(1,1)`、`put(2,2)` 后 `get(1)` 得 `-1`、`get(2)` 得 `2`；容量 `2` 时 `put(1,1)`、`put(2,2)`、`put(1,10)`、`put(3,3)` 后 `get(1)` 得 `10`、`get(2)` 得 `-1`、`get(3)` 得 `3`。

**复杂度。** `get`、`put` 都是 `O(1)`（一次字典操作加常数次指针修改）；空间 `O(capacity)`。

**拓展优化。**
- 要线程安全：`get` 也会改顺序，读写都要拿同一把 `threading.Lock`。
- 按访问频率逐出（LFU，LC 460）：按频次分桶，每个桶一条链表，再维护 `min_freq`。

**易错点。**
- `get` 命中也要把节点挪到队首。容量 `2`：`put(1,1)`、`put(2,2)`、`get(1)`、`put(3,3)` 后，正确逐出的是键 `2`，`get(1)` 得 `1`；漏掉 `get` 的刷新会逐出键 `1`，`get(1)` 错成 `-1`。
- `put` 更新已存在的键时不能触发逐出。容量 `2`：`put(1,1)`、`put(2,2)`、`put(2,20)` 后两个键都应保留；先判满再逐出会丢掉键 `1`，`get(1)` 错成 `-1`。
- 逐出时必须同时删链表节点和字典项，所以节点里要存 `key`，才能回头删字典。

**同模式。** LC 460 LFU 缓存、LC 432 全 O(1) 的数据结构、LC 380 O(1) 时间插入、删除和获取随机元素、LC 155 最小栈。
