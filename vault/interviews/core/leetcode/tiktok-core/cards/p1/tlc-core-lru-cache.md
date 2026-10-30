---
id: tlc-core-lru-cache
node: p1.lru-cache
type: qa
---
## Q
**LC 146 LRU 缓存**｜Medium · LC TikTok 热度 100/100（近 30 天） · 近一年被问：美国 14 次、国内 27 次 · CodeTop 国内累计 367 次 · 最近 2026-10（面试记录） · 也在：Amazon、LeetCode Hot 100、NeetCode 150、Top Interview 150

设计一个 LRU（最近最少使用，Least Recently Used）缓存类 `LRUCache(capacity)`：`get(key)` 在缓存里就返回值，否则返回 `-1`；`put(key, value)` 在 `key` 已存在时更新值，不存在时插入，插入后键的数量超过 `capacity` 就逐出**最久未使用**的键。`get` 和 `put` 都要平均 `O(1)`。`1 <= capacity <= 3000`，`0 <= key <= 10000`，`0 <= value <= 10^5`，最多调用 `2 * 10^5` 次。例：容量 2，`put(1,1)`、`put(2,2)`、`get(1)` 得 `1`、`put(3,3)` 逐出键 `2`、`get(2)` 得 `-1`、`put(4,4)` 逐出键 `1`、`get(1)` 得 `-1`、`get(3)` 得 `3`、`get(4)` 得 `4`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 哈希表（hash map）存「键 → 链表节点」负责 `O(1)` 查找，双向链表（doubly linked list）按使用时间从新到旧排列负责 `O(1)` 挪动和逐出；每次访问把节点摘下放到链表头，满了就删链表尾。

**识别。** 「`O(1)` 查找」指向哈希表，「按使用顺序排、`O(1)` 删除任意位置再放到最前」指向双向链表；两个要求一个结构满足不了，所以是**组合数据结构**的设计题。调用 `2 * 10^5` 次、容量 3000，列表线性扫描会到 `6 * 10^8` 量级，必须 `O(1)`。

**推导。** 暴力：用列表按使用顺序存键值对，查找和挪动都是 `O(n)`。浪费有两处：查找可以交给字典；「把某个元素挪到最前」在数组里要整体平移。链表摘掉一个节点只要改相邻两个指针，前提是**已经拿到节点**，而字典恰好存着键到节点的映射；摘节点要改前驱的指针，所以用双向；头尾各放一个哨兵节点（sentinel）消掉空链表和头尾的特判。逐出时尾部节点自己带着 `key`，用它回头删字典。

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
        self.map: dict[int, Node] = {}
        self.head, self.tail = Node(), Node()      # 哨兵：head.next 是最近使用，tail.prev 是最久未使用
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node: Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node: Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._unlink(node)                         # 摘下来再放到最前面 = 标记为刚用过
        self._push_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.cap:              # 满了：逐出链表尾部（最久未使用）
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]
        node = self.map[key] = Node(key, value)
        self._push_front(node)
```

运行：题面序列的输出是 `[None, None, 1, None, -1, None, -1, 3, 4]`；容量 1 时 `put(1,1)`、`put(2,2)` 后 `get(1)` 得 `-1`、`get(2)` 得 `2`；容量 2 时 `put(1,1)`、`put(2,2)`、`put(1,10)`、`put(3,3)` 后 `get(1)` 得 `10`、`get(2)` 得 `-1`、`get(3)` 得 `3`。

**复杂度。** `get`、`put` 都是 `O(1)`（一次字典操作加常数次指针修改）；空间 `O(capacity)`。

**易错点。**
- `get` 命中也要把节点挪到链表头。容量 2 时 `put(1,1)`、`put(2,2)`、`get(1)`、`put(3,3)`：正确逐出键 `2`，之后 `get(1)` 得 `1`；漏掉 `get` 的刷新会逐出键 `1`，`get(1)` 错成 `-1`。
- `put` 更新已存在的键时不能触发逐出。容量 2 时 `put(1,1)`、`put(2,2)`、`put(2,20)`：正确做法两个键都保留；先判满再逐出会丢掉键 `1`，`get(1)` 错成 `-1`。
- 逐出时必须同时删链表节点和字典项，节点里要存 `key` 才能回头删字典。

**追问。**
- 不想手写链表：`OrderedDict` 的 `move_to_end(key)` 和 `popitem(last=False)` 各是 `O(1)`，十行内写完，面试里先写链表版再说这个。
- 要线程安全：`get` 也会改顺序，所以读写都要拿同一把 `threading.Lock`。
- 按访问频率逐出（LFU）：按频次分桶，每个桶一条链表，再维护 `min_freq`。

**同模式。** LC 460 LFU 缓存、LC 432 全 O(1) 的数据结构、LC 380 O(1) 时间插入删除和获取随机元素（字典加数组）、LC 707 设计链表。
