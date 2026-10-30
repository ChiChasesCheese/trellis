---
id: tlc-all-oone-data-structure-5-alt
node: p4.all-oone-data-structure
type: qa
step: 5
---
## Q
**LC 432 全 O(1) 的数据结构**｜另一种解法

不手写链表，还有什么写法能通过 `AllOne`（`inc`、`dec`、`getMaxKey`、`getMinKey`，`key` 为小写字母串，最多调用 `5 * 10^4` 次）？它的复杂度是多少，什么时候该选它而不是桶链表？

## A
**两个懒删除堆。** 字典 `cnt` 记每个 key 的当前计数；最小堆存 `(计数, key)`，最大堆存 `(-计数, key)`。每次 `inc` / `dec` 把新的 `(计数, key)` 推进两个堆，旧记录不管。取最值时，如果堆顶的记录与字典里的当前计数对不上（说明它是过期记录），就弹掉，直到堆顶有效：

```python
from heapq import heappop, heappush

class AllOneHeap:
    def __init__(self) -> None:
        self.cnt: dict[str, int] = {}
        self.minh: list[tuple[int, str]] = []
        self.maxh: list[tuple[int, str]] = []

    def inc(self, key: str) -> None:
        c = self.cnt[key] = self.cnt.get(key, 0) + 1
        heappush(self.minh, (c, key))
        heappush(self.maxh, (-c, key))

    def dec(self, key: str) -> None:
        c = self.cnt[key] - 1
        if c == 0:
            del self.cnt[key]               # 堆里的旧记录以后会被当成过期丢掉
        else:
            self.cnt[key] = c
            heappush(self.minh, (c, key))
            heappush(self.maxh, (-c, key))

    def getMaxKey(self) -> str:
        while self.maxh and self.cnt.get(self.maxh[0][1]) != -self.maxh[0][0]:
            heappop(self.maxh)              # 堆顶的 (计数, key) 和字典对不上：过期记录，丢掉
        return self.maxh[0][1] if self.maxh else ""

    def getMinKey(self) -> str:
        while self.minh and self.cnt.get(self.minh[0][1]) != self.minh[0][0]:
            heappop(self.minh)
        return self.minh[0][1] if self.minh else ""
```

运行：`inc("hello")` ×2 后 `getMaxKey()` / `getMinKey()` 都是 `"hello"`；`inc("leet")` 后分别是 `"hello"` 和 `"leet"`；空结构返回 `""`；`inc("a")`、`dec("a")` 后返回 `""`。

**复杂度。** 每次 `inc` / `dec` 是 `O(log m)`，`m` 是堆里的记录数；取最值是摊还 `O(log m)`——每条过期记录最多被弹出一次。堆里的记录总数不超过操作总次数，所以空间 `O(Q)`，`Q` 是调用次数（这里 `5 * 10^4`）。

**暴力 `O(n)` 写法。** 只用字典，`getMaxKey` 取 `max(self.cnt, key=self.cnt.get)`，`getMinKey` 取 `min(...)`，空字典返回 `""`。`inc` / `dec` 是 `O(1)`，取最值是 `O(n)`；key 的种类很少（比如不超过几百）时够用，种类上万并且频繁查询时会超时。

**怎么选。**
- 面试明确要求「全 `O(1)`」→ 桶链表，这是考点；
- 现实里 `O(log n)` 足够、想写得短、少出指针错误 → 懒删除堆；
- key 种类很少或查询稀疏 → 字典加扫描最简单。

**Python 提醒**：`heapq` 是最小堆，最大堆通过取负实现；元组里放 `(计数, key)`，计数相同会继续比较 `key`（字符串可比较，没问题）。懒删除的堆会堆积过期记录，调用次数极多时要考虑定期重建。
