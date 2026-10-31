---
id: tlc-patterns-design-1-signals
node: patterns.design
type: qa
step: 1
---
## Q
**数据结构设计题（Design）｜信号**

"设计一个支持若干操作的类"这类题怎么入手？怎样从复杂度要求反推数据结构？

## A
设计题考的不是新算法，而是把**几种基础结构组合起来**，让每个操作达到题目要求的复杂度。入手顺序：

1. **列出接口**：有哪些方法、参数、返回值，边界（空、重复、不存在）怎么处理。
2. **写下复杂度目标**：题面常写"每个操作平均 `O(1)`"。
3. **逐个操作问"需要什么能力"**，再选结构：

| 需要的能力 | 结构 |
|---|---|
| 按键 `O(1)` 查找 / 更新 / 删除 | 哈希表 `dict`（例：幂等、带版本号的数据更新） |
| 按位置 `O(1)` 随机取 | 数组 `list`（例：LC 1472 设计浏览器历史记录） |
| `O(1)` 删除中间节点 + 保持顺序 | 双向链表（`dict` 指向节点）（例：LC 146 LRU 缓存） |
| 取最大 / 最小 | 堆，或维护一个有序的计数桶链（例：LC 155 最小栈） |
| 按版本 / 时间回查 | 每个键存 `(时间, 值)` 升序列表 + `bisect`（例：LC 981 基于时间的键值存储） |
| 滑动窗口内求和 / 平均 | `deque` + 维护的和（例：LC 1352 最后 K 个数的乘积） |

**常见组合：**
- LRU（LC 146）：哈希 + 双向链表（例：LC 146 LRU 缓存）。
- 随机集合（LC 380）：哈希 + 数组（交换删除）（例：LC 380 O(1) 时间插入、删除和获取随机元素）。
- 全 O(1)（LC 432）：哈希 + 按计数分桶的双向链表（例：LC 460 LFU缓存；高频：LC 432 全 O(1) 的数据结构）。
- 快照数组（LC 1146）：每个下标一个变更历史 + 二分（例：LC 1146 快照数组）。
- 数据流中位数（LC 295）：双堆（例：LC 295 数据流的中位数）。
- 内存分配器（LC 2502）：数组 / 区间表模拟（例：LC 2502 设计内存分配器）。

**近似信号：**
- 数据范围很小（`<= 1000` 次调用）⇒ 朴素 `O(n)` 的扫描就能过，别过度设计（例：LC 1381 设计一个支持增量操作的栈；高频：LC 2502 设计内存分配器）。
- 需要持久化 / 并发 ⇒ 先问面试官是否要考虑（例：限制并发数的异步任务执行器）。
- 只是一次性计算 ⇒ 普通算法题，不是设计题（例：LC 53 最大子数组和）。

**例题：** 幂等、带版本号的数据更新

实现内存键值存储 `VersionedStore`：`update(request_id, key, value, expected_version)` 仅当 `key` 当前版本等于 `expected_version` 时写入并升版本，否则返回冲突；同一个 `request_id` 重试时原样返回第一次的结果；`get(key)` 返回 `(value, version)`，不存在为 `(None, 0)`。调用总数 `<= 10^5`。

```python
class VersionedStore:
    def __init__(self) -> None:
        self.data: dict[str, tuple[str, int]] = {}           # key -> (value, version)
        self.done: dict[str, tuple[bool, int]] = {}          # request_id -> 第一次的结果
    def get(self, key: str) -> tuple[str | None, int]:
        return self.data.get(key, (None, 0))                 # 不存在的 key 版本为 0
    def update(self, request_id: str, key: str, value: str, expected_version: int) -> tuple[bool, int]:
        """返回 (是否写入, 版本)：成功时是新版本，冲突时是当前版本。"""
        if (prev := self.done.get(request_id)) is not None:
            return prev                                      # 重试：原样返回，不再写
        _, version = self.get(key)
        if version == expected_version:                      # 比较并更新（compare-and-set）
            self.data[key] = (value, version + 1)
            result = (True, version + 1)
        else:
            result = (False, version)
        self.done[request_id] = result                       # 冲突结果也要记住
        return result
```

**例题：** LC 1472 设计浏览器历史记录

实现 `BrowserHistory`：`visit(url)` 访问新页面并清空可前进的记录，`back(steps)` / `forward(steps)` 后退 / 前进最多 `steps` 步（越界就停在最前 / 最后一页）并返回当前 URL。`1 <= steps <= 100`，总调用不超过 5000 次。

```python
class BrowserHistory:
    def __init__(self, homepage: str) -> None:
        self.history: list[str] = [homepage]
        self.cursor = 0
    def visit(self, url: str) -> None:
        del self.history[self.cursor + 1:]
        self.history.append(url)
        self.cursor += 1
    def back(self, steps: int) -> str:
        self.cursor = max(0, self.cursor - steps)
        return self.history[self.cursor]
    def forward(self, steps: int) -> str:
        self.cursor = min(len(self.history) - 1, self.cursor + steps)
        return self.history[self.cursor]
```

**例题：** LC 146 LRU 缓存

设计容量为 `capacity` 的 LRU 缓存（`1 <= capacity <= 3000`）：`get(key)` 命中返回值、否则 `-1`；`put(key, value)` 写入，超出容量时淘汰最久未使用的键；两个操作都要 `O(1)`。

```python
from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.store: OrderedDict[int, int] = OrderedDict()  # 队首最旧，队尾最新
    def get(self, key: int) -> int:
        if key not in self.store:
            return -1
        self.store.move_to_end(key)
        return self.store[key]
    def put(self, key: int, value: int) -> None:
        self.store.pop(key, None)
        self.store[key] = value
        if len(self.store) > self.capacity:
            self.store.popitem(last=False)
```

**例题：** LC 155 最小栈

设计支持 `push`、`pop`、`top` 和 `O(1)` 取最小元素 `getMin` 的栈，`pop`/`top`/`getMin` 总在非空栈上调用，总调用不超过 `3 * 10^4` 次。

```python
class MinStack:
    def __init__(self) -> None:
        self.stack: list[tuple[int, int]] = []    # 每项 (值, 压入它时栈内的最小值)
    def push(self, val: int) -> None:
        low = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, low))             # 最小值跟着元素一起入栈，随它一起出栈
    def pop(self) -> None:
        self.stack.pop()
    def top(self) -> int:
        return self.stack[-1][0]
    def getMin(self) -> int:
        return self.stack[-1][1]
```

**例题：** LC 981 基于时间的键值存储

设计 `TimeMap`：`set(key, value, timestamp)` 存入带时间戳的值（时间戳严格递增），`get(key, timestamp)` 返回该键在 `<= timestamp` 的最近一次值，没有则返回 `""`。调用总数不超过 `2 * 10^5`。

```python
from bisect import bisect_right
from collections import defaultdict
class TimeMap:
    def __init__(self) -> None:
        self.times: defaultdict[str, list[int]] = defaultdict(list)    # key -> 递增的时间戳
        self.values: defaultdict[str, list[str]] = defaultdict(list)   # key -> 与 times 同下标的值
    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)       # 时间戳严格递增：直接 append 就是有序的
        self.values[key].append(value)
    def get(self, key: str, timestamp: int) -> str:
        times = self.times.get(key)             # 用 .get：defaultdict 的 [] 会凭空造出空列表
        if not times:
            return ""
        i = bisect_right(times, timestamp)      # 第一个 > timestamp 的位置，i-1 就是最后一个 <= timestamp 的
        return self.values[key][i - 1] if i else ""
```

**例题：** LC 1352 最后 K 个数的乘积

设计 `ProductOfNumbers`：`add(num)` 追加一个数（`0 <= num <= 100`），`getProduct(k)` 返回最后 `k` 个数的乘积（`1 <= k <= 4 * 10^4`，保证不超过 32 位整数），两个操作都希望 `O(1)`。

```python
class ProductOfNumbers:
    def __init__(self) -> None:
        self.prefix: list[int] = [1]        # prefix[i]：最近一个 0 之后前 i 个数的乘积，prefix[0] = 1
    def add(self, num: int) -> None:
        if num == 0:
            self.prefix = [1]               # 遇到 0：之前的前缀全部作废，重新开始
        else:
            self.prefix.append(self.prefix[-1] * num)
    def getProduct(self, k: int) -> int:
        if k >= len(self.prefix):           # 最后 k 个数跨过了最近的 0
            return 0
        return self.prefix[-1] // self.prefix[-1 - k]   # 前缀积相除，整除是精确的
```

**例题：** LC 380 O(1) 时间插入、删除和获取随机元素

设计 `RandomizedSet`：`insert(val)` / `remove(val)` 插入 / 删除元素（返回是否成功），`getRandom()` 等概率返回现有元素之一；三个操作平均时间都是 `O(1)`，总调用不超过 `2 * 10^5` 次。

```python
import random
class RandomizedSet:
    def __init__(self) -> None:
        self.items: list[int] = []         # 紧凑数组：getRandom 按下标 O(1) 取
        self.pos: dict[int, int] = {}      # 值 -> 它在 items 里的下标
    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.items)
        self.items.append(val)
        return True
    def remove(self, val: int) -> bool:
        if (i := self.pos.pop(val, None)) is None:
            return False
        last = self.items.pop()            # 先弹出末尾，数组保持紧凑
        if i < len(self.items):            # val 不在末尾：把 last 填进空出的 i
            self.items[i] = last
            self.pos[last] = i
        return True
    def getRandom(self) -> int:
        return random.choice(self.items)
```

**例题：** LC 460 LFU缓存

设计 `LFUCache(capacity)`（`1 <= capacity <= 10^4`）：`get` / `put` 都要 `O(1)`，容量满时先淘汰使用次数最少的键，次数相同则淘汰最久未使用的；与 LC 432 同样是按「计数」分桶的结构。

```python
from collections import OrderedDict, defaultdict
class LFUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.key_to_val: dict[int, int] = {}
        self.key_to_freq: dict[int, int] = {}
        self.freq_to_keys: dict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)
        self.min_freq = 0
    def _touch(self, key: int) -> None:
        freq = self.key_to_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq] and freq == self.min_freq:
            self.min_freq += 1
        self.key_to_freq[key] = freq + 1
        self.freq_to_keys[freq + 1][key] = None
    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        self._touch(key)
        return self.key_to_val[key]
    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._touch(key)
            return
        if len(self.key_to_val) >= self.capacity:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1
```

**例题：** LC 1146 快照数组

设计 `SnapshotArray(length)`（`1 <= length <= 50000`）：`set(index, val)` 修改元素，`snap()` 拍快照并返回快照编号，`get(index, snap_id)` 读取拍快照时该下标的值；总调用不超过 50000 次。

```python
class SnapshotArray:
    def __init__(self, length: int) -> None:
        self.snap_id = 0
        self.history: list[list[tuple[int, int]]] = [[(0, 0)] for _ in range(length)]
    def set(self, index: int, val: int) -> None:
        hist = self.history[index]
        if hist[-1][0] == self.snap_id:        # 同一个快照期内多次写：覆盖即可
            hist[-1] = (self.snap_id, val)
        else:
            hist.append((self.snap_id, val))
    def snap(self) -> int:
        self.snap_id += 1                      # 不复制数组，只推进快照号
        return self.snap_id - 1
    def get(self, index: int, snap_id: int) -> int:
        hist = self.history[index]
        pos = bisect_right(hist, snap_id, key=lambda rec: rec[0]) - 1
        return hist[pos][1]
```

**例题：** LC 295 数据流的中位数

设计 `MedianFinder`：`addNum(num)` 向数据流加入一个整数（`-10^5 <= num <= 10^5`），`findMedian()` 返回当前所有数的中位数；总调用不超过 `5 * 10^4` 次。

```python
from heapq import heappop, heappush, heappushpop
class MedianFinder:
    def __init__(self) -> None:
        self.low: list[int] = []              # 大根堆（存相反数）：较小的一半，堆顶 = 这一半的最大值
        self.high: list[int] = []             # 小根堆：较大的一半，堆顶 = 这一半的最小值
    def addNum(self, num: int) -> None:
        heappush(self.high, -heappushpop(self.low, -num))   # 先过 low 再交给 high，保证 low 的每个数 <= high 的每个数
        if len(self.high) > len(self.low):                  # 保持 len(low) 等于 len(high) 或多 1
            heappush(self.low, -heappop(self.high))
    def findMedian(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
```

**例题：** LC 2502 设计内存分配器

设计 `Allocator(n)`（`1 <= n, size, mID <= 1000`，总调用不超过 1000 次）管理 `n` 个内存单元：`allocate(size, mID)` 分配最左侧连续 `size` 个空闲单元并标记为 `mID`，返回起始下标，不存在返回 `-1`；`freeMemory(mID)` 释放所有标记为 `mID` 的单元，返回释放数量。

```python
class Allocator:
    def __init__(self, n: int) -> None:
        self.mem = [0] * n             # mem[i] 是占用该单元的 mID；mID >= 1，所以 0 表示空闲
    def allocate(self, size: int, mID: int) -> int:
        run = 0                        # 当前连续空闲单元的个数
        for i, owner in enumerate(self.mem):
            run = run + 1 if owner == 0 else 0
            if run == size:            # 第一次凑够 size 个，就是最左侧的块
                start = i - size + 1
                self.mem[start:i + 1] = [mID] * size   # 切片赋值，一次写入整块
                return start
        return -1
    def freeMemory(self, mID: int) -> int:
        freed = 0
        for i, owner in enumerate(self.mem):
            if owner == mID:           # 同一个 mID 可能分散在多个块里，全部释放
                self.mem[i] = 0
                freed += 1
        return freed
```

**例题：** LC 1381 设计一个支持增量操作的栈

设计 `CustomStack(maxSize)`：`push(x)`（栈满则忽略）、`pop()`（空栈返回 `-1`）、`increment(k, val)` 把栈底的前 `k` 个元素都加 `val`。`1 <= maxSize, x, k <= 1000`，每个方法至多调用 1000 次。

```python
class CustomStack:
    def __init__(self, maxSize: int) -> None:
        self.cap = maxSize
        self.stack: list[int] = []
        self.add: list[int] = [0] * maxSize   # add[i]：下标 0..i 的元素都还欠着这笔增量
    def push(self, x: int) -> None:
        if len(self.stack) < self.cap:
            self.stack.append(x)
    def pop(self) -> int:
        if not self.stack:
            return -1
        i = len(self.stack) - 1
        inc, self.add[i] = self.add[i], 0     # 取走栈顶的欠账，并把这一格清零
        if i:
            self.add[i - 1] += inc            # 欠账往下传给新的栈顶
        return self.stack.pop() + inc
    def increment(self, k: int, val: int) -> None:
        if self.stack:
            self.add[min(k, len(self.stack)) - 1] += val   # 只记在第 k 个（或栈顶）上
```

**例题：** 限制并发数的异步任务执行器

实现 `async def run_limited(tasks, limit)`：`tasks` 是 `n` 个无参异步函数（`0 <= n <= 10^5`），同一时刻最多并发执行 `limit` 个，一个结束立刻补上下一个；按输入顺序返回每项的 `("fulfilled", 值)` 或 `("rejected", 异常)`，任务抛出的异常（含调用时同步抛出）都要记录，`limit` 不是正整数时抛 `ValueError`。

```python
import asyncio
from collections.abc import Awaitable, Callable
from typing import Any
type Outcome = tuple[str, Any]
async def run_limited[T](tasks: list[Callable[[], Awaitable[T]]], limit: int) -> list[Outcome]:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
        raise ValueError(f"limit 必须是正整数，收到 {limit!r}")
    results: list[Outcome] = [("rejected", None)] * len(tasks)
    sem = asyncio.Semaphore(limit)
    async def run_one(i: int, task: Callable[[], Awaitable[T]]) -> None:
        async with sem:                              # 名额在 async with 退出时自动归还
            try:
                results[i] = ("fulfilled", await task())   # 调用本身也在 try 里：同步抛出的异常同样被记录
            except Exception as exc:                 # 不捕获 BaseException，CancelledError 必须继续往外传
                results[i] = ("rejected", exc)
    async with asyncio.TaskGroup() as tg:
        for i, task in enumerate(tasks):
            tg.create_task(run_one(i, task))
    return results
```

**例题：** LC 53 最大子数组和

整数数组 `nums`（`1 <= nums.length <= 10^5`，`-10^4 <= v <= 10^4`），求和最大的非空连续子数组的和。

```python
from itertools import islice
def max_sub_array(nums: list[int]) -> int:
    best = cur = nums[0]                # cur：以当前元素结尾的最大子数组和
    for x in islice(nums, 1, None):     # 跳过首元素，又不拷贝切片
        cur = max(x, cur + x)           # 接在前面后面，或者从 x 重新开始
        best = max(best, cur)
    return best
```

**例题：** LC 432 全 O(1) 的数据结构

设计一个存储字符串计数的数据结构，并能返回计数最小和最大的字符串。实现类 `AllOne`：`inc(key)` 让 `key` 的计数加 `1`，不存在则插入计数为 `1` 的 `key`；`dec(key)` 让 `key` 的计数减 `1`，减到 `0` 就把它删除（保证调用 `dec` 时 `key` 存在）；`getMaxKey()` 返回任意一个计数最大的字符串，没有元素则返回 `""`；`getMinKey()` 返回任意一个计数最小的字符串，没有元素则返回 `""`。每个函数都要求**平均 `O(1)`** 时间。`1 <= key.length <= 10`，`key` 由小写英文字母组成，最多调用 `5 * 10^4` 次。

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
        self.head, self.tail = Bucket(0), Bucket(-1)
        self.head.next, self.tail.prev = self.tail, self.head
        self.where: dict[str, Bucket] = {}
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
        anchor = self.head if cur is None else cur
        target = anchor.next
        new_cnt = anchor.cnt + 1
        if target.cnt != new_cnt:
            target = self._insert_after(anchor, new_cnt)
        target.keys.add(key)
        self.where[key] = target
        if cur is not None:
            cur.keys.discard(key)
            if not cur.keys:
                self._remove(cur)
    def dec(self, key: str) -> None:
        cur = self.where[key]
        if cur.cnt == 1:
            del self.where[key]
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
        return next(iter(self.tail.prev.keys))
    def getMinKey(self) -> str:
        if self.head.next is self.tail:
            return ""
        return next(iter(self.head.next.keys))
```
