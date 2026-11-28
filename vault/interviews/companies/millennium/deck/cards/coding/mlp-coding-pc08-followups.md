---
id: mlp-coding-pc08-followups
node: coding.pc08
step: 2
type: qa
---
## Q
**LRU 缓存与中位数：追问与变体**｜编程轮

LRU 缓存和数据流中位数写完后，面试官会怎么追问？

## A
- **不用 `OrderedDict` 怎么写：** 手写双向链表加字典 `key -> 节点`。最近使用的放尾部，最久未用的放头部；头尾各放一个哨兵节点（sentinel，不存数据的占位节点），这样删除和插入不用判断空链表。命中就先摘下再挂到尾部；超容量就摘掉头部后面的第一个节点，并把它的 key 从字典里删掉，所以节点里必须存 key。

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val, self.prev, self.next = key, val, None, None

class LRU:
    def __init__(self, cap):
        self.cap, self.map = cap, {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head
    def _unlink(self, n):
        n.prev.next, n.next.prev = n.next, n.prev
    def _push(self, n):                       # 挂到尾部（最近使用）
        last = self.tail.prev
        last.next, n.prev, n.next, self.tail.prev = n, last, self.tail, n
    def get(self, key):
        n = self.map.get(key)
        if not n:
            return -1
        self._unlink(n)
        self._push(n)
        return n.val
    def put(self, key, val):
        if key in self.map:
            n = self.map[key]
            n.val = val
            self._unlink(n)
            self._push(n)
            return
        n = Node(key, val)
        self.map[key] = n
        self._push(n)
        if len(self.map) > self.cap:
            lru = self.head.next              # 头部后面的第一个就是最久未用
            self._unlink(lru)
            del self.map[lru.key]
```

- **过期为什么用惰性清理：** 不需要后台线程和定时器，代价是过期条目在被读到之前一直占着容量；容量淘汰和过期是两个独立机制，满了照样按 LRU 顺序淘汰，不管它有没有 ttl。
- **绝对截止还是滑动过期：** 绝对截止是 `写入时刻 + ttl`；滑动过期要在每次 `get` 时刷新截止时间，两者语义不同，写之前要问清楚。
- **要主动清理过期条目：** 可以另外维护一个按截止时间排序的最小堆，定期弹出已过期的；代价是多一份结构，更新条目时旧堆项要忽略。
- **为什么中位数用两个堆：** 每次插入后全量排序是 O(n log n)，有序插入是 O(n)；两个堆让插入 O(log n)、取中位数 O(1)。
- **中位数的变体：** 只要第 k 大元素，用一个大小为 k 的小顶堆；还要支持删除，则需要延迟删除或平衡树。
- **多线程使用缓存：** 每个操作都改共享结构，要加锁；`OrderedDict` 的单个操作在 CPython 里是原子的，但"先查再改"的组合不是。
- **会多花一个测试用例的边界：** 容量为 1；对已有 key 再 `put` 要更新值并算作最近使用；`get` 命中后该 key 变成最近使用，会改变淘汰顺序；过期条目被读到时返回 -1 并释放位置；中位数在偶数个元素时是中间两个数的平均值；空流取中位数抛 `ValueError`；重复数字。

**英文答法。**
- "I keep a **sentinel** at each end of the list so I never special-case an empty list."
- "Expiry is **lazy**: I check the deadline on read, so there's no background thread."
- "I'd confirm whether TTL is an **absolute deadline** or sliding, since they behave differently."
