---
id: tlc-all-oone-data-structure-0-whole
node: a.all-oone-data-structure
type: qa
---
## Q
**LC 432 全 O(1) 的数据结构**｜Hard · TikTok 高频

设计一个存储字符串计数的数据结构，并能返回计数最小和最大的字符串。实现类 `AllOne`：`inc(key)` 让 `key` 的计数加 `1`，不存在则插入计数为 `1` 的 `key`；`dec(key)` 让 `key` 的计数减 `1`，减到 `0` 就把它删除（保证调用 `dec` 时 `key` 存在）；`getMaxKey()` 返回任意一个计数最大的字符串，没有元素则返回 `""`；`getMinKey()` 返回任意一个计数最小的字符串，没有元素则返回 `""`。每个函数都要求**平均 `O(1)`** 时间。`1 <= key.length <= 10`，`key` 由小写英文字母组成，最多调用 `5 * 10^4` 次。例：`inc("hello")` 两次，`getMaxKey()` 与 `getMinKey()` 都得 `"hello"`；再 `inc("leet")`，`getMaxKey()` 得 `"hello"`，`getMinKey()` 得 `"leet"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 哈希表加双向链表：链表按计数从小到大串起若干「桶」（bucket），每个桶装着计数相同的所有 key；哈希表 `where` 记每个 key 当前在哪个桶。`inc` / `dec` 只让计数变化 `±1`，所以 key 只会移到相邻的桶（没有就在旁边新建一个），空桶立即摘掉；最小在链表头，最大在链表尾。全部 `O(1)`。

**识别。** 「改计数 + 取最大最小」第一反应是堆或平衡树，但它们是 `O(log n)`。「全 `O(1)`」的关键在于：计数每次只变 `±1`，所以排序结构里 key 的位置只会挪到**紧邻**的位置，不需要重新比较。这是 LFU 缓存（LC 460）的同一个结构：按频率分桶，桶之间用链表相连。

**推导。** 暴力：字典 `key → 计数`，`getMax` / `getMin` 用 `max(d, key=d.get)` 扫描，`O(n)`，`5 * 10^4` 次调用时超时。想要 `O(1)`：必须能立刻拿到最大和最小，就要维护一个按计数有序的结构；用数组按计数下标会太稀疏，用堆每次 `±1` 要 `O(log n)`。观察：计数相同的 key 可以放进同一个桶，桶按计数排序成链表；`inc` 把 key 从计数 `c` 的桶挪到计数 `c + 1` 的桶——这个桶要么就是链表里紧邻的下一个，要么不存在、新建并插在旁边，`dec` 对称。桶清空后立刻摘掉，这样链表头一定是非空桶。头尾各用一个哨兵（sentinel）节点，省掉空链表的特判。

```python
class Bucket:
    __slots__ = ("cnt", "keys", "prev", "next")

    def __init__(self, cnt: int = 0) -> None:
        self.cnt = cnt
        self.keys: set[str] = set()
        self.prev: Bucket | None = None
        self.next: Bucket | None = None


class AllOne:
    def __init__(self) -> None:
        self.head, self.tail = Bucket(0), Bucket(-1)   # 哨兵：head.next 是最小计数桶，tail.prev 是最大
        self.head.next, self.tail.prev = self.tail, self.head
        self.where: dict[str, Bucket] = {}              # key -> 它当前所在的桶

    def _insert_after(self, node: Bucket, cnt: int) -> Bucket:
        new = Bucket(cnt)
        new.prev, new.next = node, node.next
        node.next.prev = new
        node.next = new
        return new

    def _remove(self, node: Bucket) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def inc(self, key: str) -> None:
        cur = self.where.get(key)
        anchor = self.head if cur is None else cur      # 新桶（计数 +1）该插在 anchor 后面
        target = anchor.next
        new_cnt = anchor.cnt + 1
        if target.cnt != new_cnt:                       # 相邻桶不是 cnt + 1 就新建一个
            target = self._insert_after(anchor, new_cnt)
        target.keys.add(key)
        self.where[key] = target
        if cur is not None:
            cur.keys.discard(key)
            if not cur.keys:
                self._remove(cur)                       # 空桶要摘掉，否则 getMinKey 会读到空集合

    def dec(self, key: str) -> None:
        cur = self.where[key]
        if cur.cnt == 1:
            del self.where[key]                         # 计数归零：key 彻底删除
        else:
            target = cur.prev
            if target.cnt != cur.cnt - 1:
                target = self._insert_after(cur.prev, cur.cnt - 1)
            target.keys.add(key)
            self.where[key] = target
        cur.keys.discard(key)
        if not cur.keys:
            self._remove(cur)

    def getMaxKey(self) -> str:
        if self.tail.prev is self.head:
            return ""
        return next(iter(self.tail.prev.keys))          # 任取一个即可

    def getMinKey(self) -> str:
        if self.head.next is self.tail:
            return ""
        return next(iter(self.head.next.keys))
```

运行：`inc("hello")` 两次后 `getMaxKey()` → `"hello"`，`getMinKey()` → `"hello"`；再 `inc("leet")`，`getMaxKey()` → `"hello"`，`getMinKey()` → `"leet"`。空结构 `getMaxKey()` / `getMinKey()` → `""`；`inc("a")` 再 `dec("a")` 后两者都是 `""`。

**复杂度。** 五个操作都是 `O(1)`（一次字典操作加常数次指针修改）；空间 `O(n)`：每个 key 在一个桶里，桶数不超过 key 数。

**易错点。**
- 空桶没摘掉：`inc("a")`、`inc("a")` 之后计数 `1` 的桶空了却留在链表里，`getMinKey()` 对空集合取元素，抛 `StopIteration`。
- `inc` 里先摘掉空的 `cur`、再在 `cur` 后面插入新桶：新桶被插到了已经摘下的节点后面，丢失。`inc("a")`、`inc("a")` 后 `getMinKey()` 得到 `""`（正确是 `"a"`）。必须先把 key 放进目标桶（必要时新建），再摘空桶。
- `dec` 到 `0` 时只从桶里删、没从 `where` 里删：之后再 `inc` 同一个 key 会拿到过期的桶引用。
- 哨兵计数要选不会与真实计数相等的值（`0` 和 `-1`），这样 `target.cnt != new_cnt` 对哨兵永远成立，会触发新建桶。

**追问。**
- LFU 缓存（LC 460）：同样的“频率分桶 + 链表”，每个桶内用 `OrderedDict` 保持最近使用顺序，逐出时取最小频率桶里最久未用的 key。
- 要求 `getMaxKey` 返回字典序最小的那个：桶内集合换成有序结构（或堆），代价上升到 `O(log n)`。
- 允许 `O(log n)` 时：两个带懒删除的堆更短（见另一种解法）。

**同模式。** LC 460 LFU 缓存、LC 146 LRU 缓存、LC 380 `O(1)` 时间插入删除和获取随机元素、LC 895 最大频率栈。
