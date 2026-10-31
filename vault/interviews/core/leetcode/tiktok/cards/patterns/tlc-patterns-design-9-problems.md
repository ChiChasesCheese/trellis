---
id: tlc-patterns-design-9-problems
node: patterns.design
type: qa
step: 9
---
## Q
**数据结构设计题｜本组的设计题**

按组合方式分类，这个题组里哪些题属于数据结构设计？

## A
**哈希 + 链表 / 数组**
- LC 146 LRU 缓存（哈希 + 双向链表）
- LC 380 O(1) 时间插入、删除和获取随机元素（哈希 + 数组）
- LC 432 全 O(1) 的数据结构（哈希 + 计数桶双向链表）
- LC 706 设计哈希映射（桶数组 + 链地址法）

**按版本 / 时间存储 + 二分**
- LC 1146 快照数组

**堆 / 窗口维护的汇总量**
- LC 295 数据流的中位数（双堆）
- LC 1352 最后 K 个数的乘积（前缀积，遇零重置）

**树 / 路径结构**
- LC 588 设计内存文件系统（路径树）
- LC 211 添加与搜索单词（字典树）

**模拟**
- LC 2502 设计内存分配器
- LC 1860 增长的内存泄露（按规则模拟）

提示：先列接口和复杂度目标，再逐个操作问需要什么能力，最后写出不变量并在每个方法结束时核对。

**例题：** LC 146 LRU 缓存

设计 `LRUCache(capacity)`：`get(key)` 命中返回值、否则返回 `-1`；`put(key, value)` 写入或更新，写入后键数超过 `capacity` 就逐出最久未使用的键。两个操作平均 `O(1)`。`1 <= capacity <= 3000`，最多调用 `2 * 10^5` 次。

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

**例题：** LC 380 O(1) 时间插入、删除和获取随机元素

实现 `RandomizedSet`：`insert(val)` 不存在时插入并返回 `true`；`remove(val)` 存在时删除并返回 `true`；`getRandom()` 等概率返回现有元素之一。每个操作平均 `O(1)`，调用 `getRandom` 时集合非空，最多 `2 * 10^5` 次调用。

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

**例题：** LC 432 全 O(1) 的数据结构

实现 `AllOne`：`inc(key)` 计数加 `1`（不存在则以 `1` 插入），`dec(key)` 计数减 `1`（减到 `0` 就删除），`getMaxKey()` / `getMinKey()` 返回计数最大 / 最小的任意一个键（没有则返回 `""`）。每个操作平均 `O(1)`，键长 `1..10`，最多调用 `5 * 10^4` 次。

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

**例题：** LC 706 设计哈希映射

不用内建哈希表，实现 `MyHashMap`：`put(key, value)` 插入或更新，`get(key)` 不存在时返回 `-1`，`remove(key)` 删除映射。`0 <= key, value <= 10^6`，最多调用 `10^4` 次。

```python
class MyHashMap:
    SIZE = 1009                               # 质数个桶：key 有规律时也分得开
    def __init__(self) -> None:
        self.buckets: list[list[list[int]]] = [[] for _ in range(self.SIZE)]   # 每个桶是一条链：[[key, value], ...]
    def _bucket(self, key: int) -> list[list[int]]:
        return self.buckets[hash(key) % self.SIZE]
    def put(self, key: int, value: int) -> None:
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:                # 已存在：原地更新，不能再追加一条
                pair[1] = value
                return
        bucket.append([key, value])
    def get(self, key: int) -> int:
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1
    def remove(self, key: int) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = bucket[-1]        # 链内顺序无所谓：和最后一个交换再弹出，O(1) 删除
                bucket.pop()
                return
```

**例题：** LC 1146 快照数组

实现 `SnapshotArray(length)`，元素初值为 `0`：`set(index, val)` 修改，`snap()` 拍快照并返回快照号（从 `0` 递增），`get(index, snap_id)` 返回该次快照时下标 `index` 的值。`length <= 50000`，总共最多 `50000` 次调用。

```python
class SnapshotArray:
    def __init__(self, length: int) -> None:
        self.snap_id = 0
        # 每个下标一条历史：(写入时的快照号, 值)，快照号递增；初始值 0 记在快照 0
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
        # 找最后一个 “快照号 <= snap_id” 的记录
        pos = bisect_right(hist, snap_id, key=lambda rec: rec[0]) - 1
        return hist[pos][1]
```

**例题：** LC 295 数据流的中位数

实现 `MedianFinder`：`addNum(num)` 加入数据流中的整数，`findMedian()` 返回当前所有数的中位数（偶数个时取中间两数的平均）。`-10^5 <= num <= 10^5`，最多 `5 * 10^4` 次调用。

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

**例题：** LC 1352 最后 K 个数的乘积

实现 `ProductOfNumbers`：`add(num)` 在末尾追加一个数，`getProduct(k)` 返回最后 `k` 个数的乘积。`0 <= num <= 100`，`1 <= k <= 4 * 10^4`，任何连续段的乘积都在 32 位整数内，总共最多 `4 * 10^4` 次调用。

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

**例题：** LC 588 设计内存文件系统

实现内存文件系统 `FileSystem`：`ls(path)` 列出文件名或目录内容（按字典序），`mkdir(path)` 逐级创建目录，`addContentToFile(filePath, content)` 创建文件或追加内容，`readContentFromFile(filePath)` 读文件。路径为绝对路径，长度 `<= 100`，四个方法合计最多 `300` 次调用，参数都有效。

```python
class _Entry:
    def __init__(self) -> None:
        self.children: dict[str, "_Entry"] = {}
        self.content: str | None = None    # None 表示目录，字符串表示文件
class FileSystem:
    def __init__(self) -> None:
        self.root = _Entry()
    def _walk(self, path: str, create: bool = False) -> _Entry:
        node = self.root
        for name in filter(None, path.split("/")):     # "/" 拆出来是 ["", ""]，filter 去掉空串
            if create:
                node = node.children.setdefault(name, _Entry())
            else:
                node = node.children[name]
        return node
    def ls(self, path: str) -> list[str]:
        node = self._walk(path)
        if node.content is not None:                   # 文件：只返回它自己的名字
            return [path.rsplit("/", 1)[-1]]
        return sorted(node.children)
    def mkdir(self, path: str) -> None:
        self._walk(path, create=True)
    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self._walk(filePath, create=True)
        node.content = (node.content or "") + content  # 追加，不是覆盖
    def readContentFromFile(self, filePath: str) -> str:
        return self._walk(filePath).content or ""
```

**例题：** LC 211 添加与搜索单词

实现 `WordDictionary`：`addWord(word)` 添加单词，`search(word)` 判断是否有已添加的单词匹配，其中 `'.'` 可匹配任意一个字母。`1 <= word.length <= 25`，总共最多 `10^4` 次调用。

```python
class WordDictionary:
    def __init__(self) -> None:
        self.root: dict[str, dict] = {}           # 字典树：键是字母，值是子结点；键 "$" 标记单词在此结束
    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})        # 有就取、没有就建，一步完成
        node["$"] = {}
    def search(self, word: str) -> bool:
        def dfs(node: dict[str, dict], i: int) -> bool:
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":                         # 通配符：除结束标记外，每个孩子都试一遍
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return ch in node and dfs(node[ch], i + 1)
        return dfs(self.root, 0)
```

**例题：** LC 2502 设计内存分配器

实现 `Allocator(n)`（`n` 个初始空闲的内存单元）：`allocate(size, mID)` 找最左侧的连续 `size` 个空闲单元，标记为 `mID` 并返回起始下标，找不到返回 `-1`；`freeMemory(mID)` 释放所有 id 为 `mID` 的单元并返回释放数量。`1 <= n, size, mID <= 1000`，最多调用 `1000` 次。

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

**例题：** LC 1860 增长的内存泄露

两个内存条分别剩 `memory1`、`memory2` 位。第 `i` 秒（从 `1` 开始）把 `i` 位分给剩余较多的那个（相等分给第一个）；两个都不足 `i` 位时程序退出。返回 `[退出时刻, 内存条1剩余, 内存条2剩余]`。`0 <= memory1, memory2 <= 2^31 - 1`。

```python
def mem_leak(memory1: int, memory2: int) -> list[int]:
    second = 1                                 # 当前要分配的位数，也是秒数
    while max(memory1, memory2) >= second:     # 至少有一条放得下，程序才没崩
        if memory1 >= memory2:                 # 相等时给第一条，所以用 >=
            memory1 -= second
        else:
            memory2 -= second
        second += 1
    return [second, memory1, memory2]
```
