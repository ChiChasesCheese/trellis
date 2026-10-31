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
- LC 981 基于时间的键值存储（高频）

**堆 / 窗口维护的汇总量**
- LC 295 数据流的中位数（双堆）
- LC 1352 最后 K 个数的乘积（前缀积，遇零重置）

**树 / 路径结构**
- LC 588 设计内存文件系统（路径树）
- LC 211 添加与搜索单词（字典树）
- LC 208 实现 Trie (前缀树)（高频）

**模拟**
- LC 2502 设计内存分配器
- LC 348 设计井字棋（高频）

**栈 / 队列**
- LC 155 最小栈（高频）
- LC 232 用栈实现队列（高频）
- LC 622 设计循环队列（高频）

**TikTok 变体**
- 带 TTL 的 LRU 缓存（哈希表 + 双向链表管使用顺序，最小堆按到期时刻清过期）
- 手写限流器（每个 key 一个时间戳队列，或一对 (令牌数, 上次补充时刻)）
- 限制并发数的异步任务执行器（信号量限流，结果按下标写回）
- 定长数组实现双端队列（环形缓冲区：数组 + 队首下标 + 元素个数）
- 内存 KV 存储：快照与恢复（哈希表 + 长度前缀序列化）
- 幂等、带版本号的数据更新（哈希表存 (值, 版本)，再加一张请求结果表）
- 连续内存分配器（按地址排序的空闲块列表，二分定位后与相邻块合并）

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

**例题：** LC 981 基于时间的键值存储

设计一个 `TimeMap` 类：同一个键在不同时间戳可以存多个值，并能按时间戳取值。`set(key, value, timestamp)` 在时间戳 `timestamp` 存入键 `key` 对应的值 `value`；`get(key, timestamp)` 返回此前某次 `set` 中满足 `timestamp_prev <= timestamp` 的值，若有多个，返回 `timestamp_prev` 最大的那个；没有则返回空串 `""`。`1 <= key.length, value.length <= 100`，由小写字母和数字组成，`1 <= timestamp <= 10^7`，所有 `set` 的时间戳**严格递增**，`set` 与 `get` 合计最多 `2 * 10^5` 次调用。

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

**例题：** LC 208 实现 Trie (前缀树)

实现前缀树（Trie）类：`Trie()` 初始化；`insert(word)` 插入单词；`search(word)` 若 `word` 已被插入返回 `true`，否则 `false`；`startsWith(prefix)` 若某个已插入单词以 `prefix` 为前缀返回 `true`。约束：`1 <= word.length, prefix.length <= 2000`，仅小写英文字母；三种操作总共调用不超过 `3 * 10^4` 次。

```python
class TrieNode:
    __slots__ = ("children", "end")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}   # 字符 -> 子结点
        self.end = False                          # 是否有单词恰好在这里结束


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:           # 不用 setdefault：它每次都会白造一个结点
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end = True

    def _walk(self, s: str) -> TrieNode | None:
        node = self.root
        for ch in s:
            if (node := node.children.get(ch)) is None:
                return None                       # 路走不通：没有以 s 为前缀的单词
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.end      # 路径存在还不够，必须是单词结尾

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
```

**例题：** LC 348 设计井字棋

在 `n x n` 的棋盘上实现井字棋的胜负判定器：两名玩家（编号 `1` 和 `2`）轮流落子，`move(row, col, player)` 在 `(row, col)` 放下 `player` 的棋子，返回落子后获胜的玩家编号，还没有人获胜返回 `0`。同一行、同一列或同一条对角线上全是自己的棋子就获胜。保证每次落子都在棋盘内、落在空格里，有人获胜后游戏不再继续。`2 <= n <= 100`，最多调用 `move` `n^2` 次。进阶：每次 `move` 能否比 `O(n^2)` 更快？

```python
class TicTacToe:
    def __init__(self, n: int) -> None:
        self.n = n
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag = self.anti = 0

    def move(self, row: int, col: int, player: int) -> int:
        d = 1 if player == 1 else -1            # 玩家 1 记 +1，玩家 2 记 -1
        self.rows[row] += d
        self.cols[col] += d
        if row == col:
            self.diag += d
        if row + col == self.n - 1:
            self.anti += d
        if self.n in (abs(self.rows[row]), abs(self.cols[col]), abs(self.diag), abs(self.anti)):
            return player
        return 0
```

**例题：** LC 155 最小栈

设计一个支持 `push`、`pop`、`top`，并能在**常数时间**内取到栈中最小元素的栈。实现 `MinStack` 类：`MinStack()` 初始化；`push(val)` 压入元素；`pop()` 删除栈顶；`top()` 返回栈顶；`getMin()` 返回栈中最小元素。`-2^31 <= val <= 2^31 - 1`；`pop`、`top`、`getMin` 总是在非空栈上调用；各操作合计最多调用 `3 * 10^4` 次。

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

**例题：** LC 232 用栈实现队列

只用两个栈实现先入先出（FIFO）队列，支持 `push(x)` 把 `x` 放到队尾、`pop()` 移除并返回队首、`peek()` 返回队首、`empty()` 判断队列是否为空。只能使用标准的栈操作（压栈、弹栈、看栈顶、取大小、判空），Python 里可以用 `list` 或 `deque` 模拟栈。`1 <= x <= 9`，最多调用 `100` 次，调用都合法（空队列不会 `pop` / `peek`）。进阶：每个操作**均摊** `O(1)`。

```python
class MyQueue:
    def __init__(self) -> None:
        self.inbox: list[int] = []        # 只负责 push：新元素压在栈顶
        self.outbox: list[int] = []       # 只负责 pop / peek：栈顶就是队首

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def _move(self) -> None:
        if not self.outbox:               # 只有 outbox 空了才倒，倒的时候整个 inbox 一次倒完
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self) -> int:
        self._move()
        return self.outbox.pop()

    def peek(self) -> int:
        self._move()
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox
```

**例题：** LC 622 设计循环队列

设计循环队列（环形缓冲器）：先进先出，队尾连接到队首形成环，可以重复利用出队腾出的空间。实现类 `MyCircularQueue(k)`，容量为 `k`，支持：`enQueue(value)` 入队，成功返回 `True`，队满返回 `False`；`deQueue()` 出队，成功返回 `True`，队空返回 `False`；`Front()` 取队首，空则返回 `-1`；`Rear()` 取队尾，空则返回 `-1`；`isEmpty()`、`isFull()`。值在 `0` 到 `1000`，操作数在 `1` 到 `1000`，不要使用内置的队列库。

```python
class MyCircularQueue:
    def __init__(self, k: int) -> None:
        self.buf = [0] * k
        self.cap = k
        self.head = 0                           # 队首下标
        self.size = 0                           # 元素个数：用 size 区分空和满，不浪费一格

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self.buf[(self.head + self.size) % self.cap] = value
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.buf[self.head]

    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.buf[(self.head + self.size - 1) % self.cap]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.cap
```

**例题：** 带 TTL 的 LRU 缓存（含 LFU / 加权 / 线程安全追问）

设计固定容量 `capacity` 的 LRU 缓存，`put(key, value, ttl)` 为每条设置存活时间，`get(key)` 读到过期条目时当作不存在并删除；新 key 写入时容量已满，先清掉所有已过期的条目，仍满再淘汰最久未使用的；`get` 与 `put` 均摊 `O(1)`（堆清理为 `O(log n)`），时间来自可注入的 `clock()`。

```python
import heapq
import time
from collections import OrderedDict
from collections.abc import Callable
class LRUCacheTTL:
    def __init__(self, capacity: int, clock: Callable[[], float] = time.monotonic) -> None:
        self.cap = capacity
        self.clock = clock
        self.data: OrderedDict[int, tuple[int, float]] = OrderedDict()
        self.expiry: list[tuple[float, int, int]] = []
        self.version: dict[int, int] = {}
        self.counter = 0
    def get(self, key: int) -> int:
        item = self.data.get(key)
        if item is None:
            return -1
        value, expire_at = item
        if self.clock() >= expire_at:
            self._drop(key)
            return -1
        self.data.move_to_end(key)
        return value
    def put(self, key: int, value: int, ttl: float) -> None:
        now = self.clock()
        if key not in self.data and len(self.data) >= self.cap:
            self._purge_expired(now)
            if len(self.data) >= self.cap:
                oldest = next(iter(self.data))
                self._drop(oldest)
        self.counter += 1
        self.data[key] = (value, now + ttl)
        self.data.move_to_end(key)
        self.version[key] = self.counter
        heapq.heappush(self.expiry, (now + ttl, self.counter, key))
        if len(self.expiry) > 4 * self.cap + 16:
            self.expiry = [(e, self.version[k], k) for k, (_, e) in self.data.items()]
            heapq.heapify(self.expiry)
    def _drop(self, key: int) -> None:
        del self.data[key]
        del self.version[key]
    def _purge_expired(self, now: float) -> None:
        while self.expiry and self.expiry[0][0] <= now:
            _, ver, key = heapq.heappop(self.expiry)
            if self.version.get(key) == ver:
                self._drop(key)
```

**例题：** 手写限流器（滑动窗口 / 令牌桶）

实现 `allow(key, now) -> bool`：每个 `key` 每秒最多放行 `r` 次请求，突发上限为 `b`；先用滑动窗口，再用令牌桶重写；key 的数量可达 `10^6`。

```python
from collections import defaultdict, deque
class SlidingWindowLimiter:
    """滑动窗口日志：每个 key 最多保留窗口内被放行的时间戳。"""
    def __init__(self, rate: int, window: float = 1.0) -> None:
        self.rate, self.window = rate, window
        self.logs: defaultdict[str, deque[float]] = defaultdict(deque)
    def allow(self, key: str, now: float) -> bool:
        log = self.logs[key]
        while log and log[0] <= now - self.window:
            log.popleft()
        if len(log) >= self.rate:
            return False
        log.append(now)
        return True
class TokenBucketLimiter:
    """令牌桶：桶容量 burst，每秒补 rate 个令牌，一次请求消耗 1 个。"""
    def __init__(self, rate: float, burst: int) -> None:
        self.rate, self.burst = rate, burst
        self.state: dict[str, tuple[float, float]] = {}
    def allow(self, key: str, now: float) -> bool:
        tokens, last = self.state.get(key, (float(self.burst), now))
        tokens = min(self.burst, tokens + max(0.0, now - last) * self.rate)
        ok = tokens >= 1.0
        self.state[key] = (tokens - 1.0 if ok else tokens, max(now, last))
        return ok
```

**例题：** 限制并发数的异步任务执行器

实现 `async def run_limited(tasks, limit)`：同一时刻最多执行 `limit` 个异步任务，一个结束立刻补上下一个，每个任务恰好调用一次；返回与输入顺序一致的 `("fulfilled", 值)` 或 `("rejected", 异常)` 列表，`limit` 不是正整数时抛 `ValueError`。

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
        async with sem:
            try:
                results[i] = ("fulfilled", await task())
            except Exception as exc:
                results[i] = ("rejected", exc)
    async with asyncio.TaskGroup() as tg:
        for i, task in enumerate(tasks):
            tg.create_task(run_one(i, task))
    return results
```

**例题：** 定长数组实现双端队列 / 列表（全部操作 O(1)）

用一个定长数组实现 `FixedDeque(capacity)`：`push_head`、`push_tail`（已满返回 `False`）、`pop_head`、`pop_tail`（空时返回 `None`）、`index(i)`（从队首数第 `i` 个，越界返回 `None`），全部操作 `O(1)`。

```python
class FixedDeque:
    """定长数组实现的双端队列：五个操作全部 O(1)。"""
    def __init__(self, capacity: int) -> None:
        self.buf: list[int | None] = [None] * capacity
        self.cap = capacity
        self.head = 0
        self.size = 0
    def push_head(self, x: int) -> bool:
        if self.size == self.cap:
            return False
        self.head = (self.head - 1) % self.cap
        self.buf[self.head] = x
        self.size += 1
        return True
    def push_tail(self, x: int) -> bool:
        if self.size == self.cap:
            return False
        self.buf[(self.head + self.size) % self.cap] = x
        self.size += 1
        return True
    def pop_head(self) -> int | None:
        if self.size == 0:
            return None
        x = self.buf[self.head]
        self.buf[self.head] = None
        self.head = (self.head + 1) % self.cap
        self.size -= 1
        return x
    def pop_tail(self) -> int | None:
        if self.size == 0:
            return None
        tail = (self.head + self.size - 1) % self.cap
        x = self.buf[tail]
        self.buf[tail] = None
        self.size -= 1
        return x
    def index(self, i: int) -> int | None:
        """第 i 个元素（从队首数，0 起）；越界返回 None。"""
        if not 0 <= i < self.size:
            return None
        return self.buf[(self.head + i) % self.cap]
```

**例题：** 内存 KV 存储：快照与恢复（序列化）

实现 `KVStore` 的 `put`、`get`、`delete`，再加 `snapshot()`（把全部数据序列化成字符串）和 `restore(data)`（恢复到快照时刻）；不能用现成的 `json` / `pickle`，key 和 value 可以含任意字符，数据损坏时 `restore` 抛 `ValueError` 且原存储不变。

```python
def _encode_str(s: str) -> str:
    return f"{len(s)}:{s}"
def _read_str(data: str, pos: int) -> tuple[str, int]:
    colon = data.find(":", pos)
    if colon == -1 or not data[pos:colon].isdecimal():
        raise ValueError(f"bad length at {pos}")
    end = colon + 1 + int(data[pos:colon])
    if end > len(data):
        raise ValueError("truncated data")
    return data[colon + 1:end], end
class KVStore:
    def __init__(self) -> None:
        self.data: dict[str, str] = {}
    def put(self, key: str, value: str) -> None:
        self.data[key] = value
    def get(self, key: str) -> str | None:
        return self.data.get(key)
    def delete(self, key: str) -> bool:
        return self.data.pop(key, None) is not None
    def snapshot(self) -> str:
        """格式：先写条目数，再依次写 key、value，每个字符串都是 长度:内容。"""
        parts = [_encode_str(str(len(self.data)))]
        for key, value in self.data.items():
            parts.append(_encode_str(key))
            parts.append(_encode_str(value))
        return "".join(parts)
    def restore(self, snap: str) -> None:
        """先解析到临时字典，全部成功才替换：数据损坏时原存储不变。"""
        count_text, pos = _read_str(snap, 0)
        if not count_text.isdecimal():
            raise ValueError("bad count")
        loaded: dict[str, str] = {}
        for _ in range(int(count_text)):
            key, pos = _read_str(snap, pos)
            value, pos = _read_str(snap, pos)
            loaded[key] = value
        if pos != len(snap):
            raise ValueError("trailing data")
        self.data = loaded
```

**例题：** 幂等、带版本号的数据更新

实现 `VersionedStore.update(request_id, key, value, expected_version)`：当前版本等于 `expected_version` 才写入并版本加 `1`，返回 `(True, 新版本)`，否则返回 `(False, 当前版本)`；同一个 `request_id` 重试时原样返回第一次的结果、不重复写；`get(key)` 对不存在的 key 返回 `(None, 0)`。

```python
class VersionedStore:
    def __init__(self) -> None:
        self.data: dict[str, tuple[str, int]] = {}
        self.done: dict[str, tuple[bool, int]] = {}
    def get(self, key: str) -> tuple[str | None, int]:
        return self.data.get(key, (None, 0))
    def update(self, request_id: str, key: str, value: str, expected_version: int) -> tuple[bool, int]:
        """返回 (是否写入, 版本)：成功时是新版本，冲突时是当前版本。"""
        if (prev := self.done.get(request_id)) is not None:
            return prev
        _, version = self.get(key)
        if version == expected_version:
            self.data[key] = (value, version + 1)
            result = (True, version + 1)
        else:
            result = (False, version)
        self.done[request_id] = result
        return result
```

**例题：** 连续内存分配器（first-fit、拆分与合并）

管理地址空间 `[0, capacity)`：`alloc(size)` 用 first-fit 返回起始地址（放不下返回 `-1`，`size` 非法抛 `ValueError`），`free(addr)` 释放后与相邻空闲块合并（重复释放抛 `ValueError`），支持可选的对齐 `alignment`；`capacity <= 10^9`，最多 `10^5` 次操作。

```python
from bisect import bisect_left
class Allocator:
    def __init__(self, capacity: int, alignment: int = 1) -> None:
        self.capacity, self.align = capacity, alignment
        self.free_list: list[tuple[int, int]] = [(0, capacity)]
        self.used: dict[int, int] = {}
    def alloc(self, size: int) -> int:
        if size <= 0 or size > self.capacity:
            raise ValueError(f"illegal size {size}")
        for idx, (start, length) in enumerate(self.free_list):
            addr = -(-start // self.align) * self.align
            pad = addr - start
            if length >= pad + size:
                tail = length - pad - size
                pieces = ([(start, pad)] if pad else []) + ([(addr + size, tail)] if tail else [])
                self.free_list[idx:idx + 1] = pieces
                self.used[addr] = size
                return addr
        return -1
    def free(self, addr: int) -> None:
        if addr not in self.used:
            raise ValueError(f"invalid or double free at {addr}")
        size = self.used.pop(addr)
        free_list = self.free_list
        idx = bisect_left(free_list, (addr, 0))
        start, length = addr, size
        if idx < len(free_list) and free_list[idx][0] == addr + size:
            length += free_list.pop(idx)[1]
        if idx:
            left_start, left_len = free_list[idx - 1]
            if left_start + left_len == addr:
                free_list.pop(idx - 1)
                start, length, idx = left_start, length + left_len, idx - 1
        free_list.insert(idx, (start, length))
```
