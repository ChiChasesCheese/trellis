---
slug: all-oone-data-structure
---
## Q
**LC 432 全 O(1) 的数据结构**｜Hard

实现 `AllOne`：`inc(key)`、`dec(key)`（计数减到 `0` 就删除）、`getMaxKey()`、`getMinKey()`（任取一个计数最大 / 最小的 key，没有返回 `""`），每个操作平均 `O(1)`。

## A
**一句话。** 按计数从小到大的双向链表，每个桶装计数相同的 key，哈希表记 key 所在的桶；计数只变 `±1`，所以只挪到相邻桶。

```python
class Bucket:
    def __init__(self, cnt=0):
        self.cnt = cnt
        self.keys = set()
        self.prev = self.next = None


class AllOne:
    def __init__(self):
        # 哨兵：head.next 是最小桶，tail.prev 是最大桶
        self.head, self.tail = Bucket(0), Bucket(-1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.where = {}          # key -> 所在的桶

    def _add(self, node, cnt):
        new = Bucket(cnt)
        new.prev, new.next = node, node.next
        node.next.prev = new
        node.next = new
        return new

    def _drop(self, node):
        p, q = node.prev, node.next
        p.next, q.prev = q, p

    def inc(self, key):
        cur = self.where.get(key)
        anchor = self.head if cur is None else cur
        target = anchor.next
        if target.cnt != anchor.cnt + 1:   # 相邻桶不对就新建
            target = self._add(anchor, anchor.cnt + 1)
        target.keys.add(key)
        self.where[key] = target
        if cur is not None:
            cur.keys.discard(key)
            if not cur.keys:               # 空桶必须摘掉
                self._drop(cur)

    def dec(self, key):
        cur = self.where[key]
        if cur.cnt == 1:
            del self.where[key]
        else:
            target = cur.prev
            if target.cnt != cur.cnt - 1:
                target = self._add(target, cur.cnt - 1)
            target.keys.add(key)
            self.where[key] = target
        cur.keys.discard(key)
        if not cur.keys:
            self._drop(cur)

    def getMaxKey(self):
        if self.tail.prev is self.head:
            return ""
        return next(iter(self.tail.prev.keys))

    def getMinKey(self):
        if self.head.next is self.tail:
            return ""
        return next(iter(self.head.next.keys))
```

**复杂度。** 时间 每个操作 `O(1)`，空间 `O(n)`。

**易错点。**
- 空桶没摘掉：`inc("a")` 两次后计数 `1` 的桶已空，`getMinKey()` 对空集合取元素抛 `StopIteration`。
- 先摘空桶再插新桶：新桶插到已摘下的节点后面而丢失，`getMinKey()` 得 `""`。要先放进目标桶再摘。
- `dec` 到 `0` 没从 `where` 里删：再 `inc` 同一个 key 会拿到过期的桶。

**追问。**
- LFU 缓存（LC 460）怎么做？：同样按频率分桶，桶内用 `OrderedDict`，逐出最小频率桶里最久未用的 key。

**同模式。** LC 460 LFU 缓存、LC 146 LRU 缓存、LC 380 O(1) 时间插入、删除和获取随机元素、LC 895 最大频率栈
