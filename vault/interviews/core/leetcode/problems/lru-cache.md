---
slug: lru-cache
---
## Q
**LC 146 LRU 缓存**｜Medium

设计容量为 `capacity` 的 LRU（最近最少使用）缓存：`get(key)` 不存在返回 `-1`，`put(key, value)` 超容量时逐出最久未使用的键；两个操作都要 `O(1)`。

## A
**一句话。** 哈希表存「键→节点」负责查找，双向链表按新旧排列负责挪动和逐出，访问就摘下放链表头，满了删链表尾。

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap, self.map = capacity, {}
        self.head, self.tail = Node(), Node()   # 哨兵省去边界判断
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, n):
        n.prev.next, n.next.prev = n.next, n.prev

    def _push_front(self, n):
        n.prev, n.next = self.head, self.head.next
        self.head.next.prev = n
        self.head.next = n

    def get(self, key):
        if key not in self.map:
            return -1
        n = self.map[key]
        self._unlink(n)           # 摘下再放最前 = 刚用过
        self._push_front(n)
        return n.val

    def put(self, key, value):
        if key in self.map:
            n = self.map[key]
            n.val = value
            self._unlink(n)
            self._push_front(n)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev          # 最久未使用
            self._unlink(lru)
            del self.map[lru.key]         # 节点要存 key 才能删表项
        n = self.map[key] = Node(key, value)
        self._push_front(n)
```

**复杂度。** `get`、`put` 均 `O(1)`，空间 `O(capacity)`。

**易错点。**
- `get` 命中不刷新：容量 2，`put(1)`、`put(2)`、`get(1)`、`put(3)` 会误逐出 `1`。
- `put` 更新已有键时还去逐出：容量 2，`put(1)`、`put(2)`、`put(2,20)` 会丢掉键 `1`。
- 逐出只删链表不删字典：节点里没存 `key` 就没法回头删。

**追问。**
- 为什么必须双向链表？：摘任意节点要改前驱的 `next`，单链表找前驱要 `O(n)`。
- 要线程安全？：`get` 也会改顺序，读写都要拿同一把锁。
- 按访问频率逐出（LFU）？：按频次分桶，每桶一条链表，再维护 `min_freq`。

**同模式。** LC 460 LFU 缓存、LC 432 全 O(1) 的数据结构、LC 380 O(1) 时间插入删除和获取随机元素、LC 707 设计链表
