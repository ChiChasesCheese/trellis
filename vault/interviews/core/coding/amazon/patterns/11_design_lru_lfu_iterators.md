# 11 · 设计题：LRU / LFU / 随机集合 / 文件系统 / 迭代器（Design: caches, structures, iterators）

设计题考的是你能否为一个数据结构写出清晰的契约：有哪些操作、每个操作多快、每次操作之后哪些性质必须保持成立。LRU 和 LFU 用「哈希表 + 链表」让查找和排序同时做到 O(1)；随机集合用「数组 + 哈希表」让随机取值也是 O(1)；文件系统是一棵目录树；迭代器要实现 `__iter__` 和 `__next__`。写代码前先说出不变量，写完用断言检查它们。

> 本讲覆盖：LC 146 LRU Cache · 460 LFU Cache（Hard）· 380 Insert Delete GetRandom O(1) · 588 Design In-Memory File System（Hard）· 以及迭代器题 LC 341 Flatten Nested List Iterator（附赠，覆盖「迭代器」）
> 前置：第 01 讲（`dict`）、第 08 讲（链表指针）、Python 的 `class`。
> 读完你应该能：(1) 用「哈希表 + 双向链表」做出 O(1) 的 get / put / 淘汰；(2) 为每个操作先写出**契约和不变量**再写代码；(3) 在 LRU 上回答并发、分布式、TTL、监控的资深追问。

## 1. 这个模式是什么，为什么存在

### 1.1 设计题到底在考什么

设计题（"design a data structure"）不是在考某个算法技巧，而是考：
1. **需求澄清**：支持哪些操作？每个操作的复杂度要求？容量满了怎么办？
2. **选对数据结构的组合**：没有一个单一结构能同时满足所有要求，要把两个结构**组合**起来，让一个补另一个的短板。
3. **维护不变量**（invariant）：每次操作之后，哪些性质必须仍然成立？
4. **工程素养**：接口设计、边界、测试、线程安全。

### 1.2 从最笨的解法开始（LRU）

LRU Cache：容量为 `capacity` 的缓存，`get(key)` 返回值（没有返回 −1），`put(key, value)` 插入 / 更新，容量满了就淘汰**最近最少使用**的 key。`get` 和 `put` 都要 O(1)。

最笨的做法：用一个列表按「最近使用顺序」存 `(key, value)`。`get` 要在列表里找 key（O(n)），找到后搬到末尾（O(n)）。

### 1.3 慢在哪里 / 需要什么

你需要同时做到两件事：
- 按 key **O(1) 找到**条目 → 哈希表（`dict`）。
- 按「使用时间」**O(1) 调整顺序、O(1) 删除最老的** → 需要一个能在 O(1) 删除**任意已知节点**、并在两端 O(1) 增删的结构 → **双向链表**（doubly linked list）：每个节点有 `prev` 和 `next`，知道节点就能直接把它摘下来，不用先找它的前驱。

> 因果链：`dict` 擅长查找但没有顺序；链表擅长维护顺序但不能按 key 查找 → 让 `dict` 的值直接指向链表节点 → 两个结构互相补短板。这个**「哈希表指向链表节点」**的组合是 LRU、LFU、All O`one、Max Stack 等一整类题的骨架。

### 1.4 双向链表（从零讲）

```text
head(哨兵) <-> A <-> B <-> C <-> tail(哨兵)
最近使用                                  最久未使用
```

- **哨兵节点（sentinel）**：`head` 和 `tail` 是不存数据的假节点，保证每个真实节点都有 `prev` 和 `next`，插入 / 删除不需要判断「是不是头 / 尾」。
- **摘下节点** `node`：`node.prev.next = node.next; node.next.prev = node.prev`。O(1)。
- **插入到最前**：把 `node` 接在 `head` 和 `head.next` 之间。O(1)。
- **淘汰**：摘下 `tail.prev`，并从 `dict` 里删除它的 key——所以**节点里必须存 key**，否则不知道要从 `dict` 里删哪一项。

## 2. 模板与逐行讲解

```python
from collections import OrderedDict

# Template D1: the 10-line LRU -- OrderedDict is a hash map + doubly linked list already.
# Say it first, then (if the interviewer asks) build the list yourself, as in 4.1.
class LRUWithOrderedDict:
    def __init__(self, capacity):
        self.cap, self.d = capacity, OrderedDict()

    def get(self, key):
        if key not in self.d:
            return -1
        self.d.move_to_end(key)                 # most recent goes to the END
        return self.d[key]

    def put(self, key, value):
        self.d[key] = value
        self.d.move_to_end(key)
        if len(self.d) > self.cap:
            self.d.popitem(last=False)          # evict from the FRONT = least recent

c = LRUWithOrderedDict(2)
c.put(1, 1); c.put(2, 2); c.get(1); c.put(3, 3)
assert c.get(2) == -1 and c.get(1) == 1 and c.get(3) == 3

# Template D2: a class is a contract -- state + operations + invariants. Write the invariants as asserts.
class MinStack:                                  # LC 155: every operation O(1)
    def __init__(self):
        self.items, self.mins = [], []           # mins[i] = minimum of items[0..i]

    def push(self, x):
        self.items.append(x)
        self.mins.append(x if not self.mins else min(x, self.mins[-1]))

    def pop(self):
        self.mins.pop()
        return self.items.pop()

    def get_min(self):
        return self.mins[-1]

s = MinStack()
for v in (5, 3, 7, 3):
    s.push(v)
assert s.get_min() == 3
s.pop(); s.pop()
assert s.get_min() == 3
s.pop()
assert s.get_min() == 5

# Template D3: Python's iterator protocol -- __iter__ returns self, __next__ yields or raises StopIteration
class CountDown:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

assert list(CountDown(3)) == [3, 2, 1]
```

逐行讲解：

1. `LRUWithOrderedDict`：`OrderedDict` 本身就是「哈希表 + 双向链表」。`move_to_end(key)` 把条目移到末尾，`popitem(last=False)` 弹出最老的。**面试时先说出这个 10 行版本**，表明你知道标准库；然后说「如果不允许用，我手写」——实现见 4.1。
2. `MinStack`（LC 155）：并行维护一个 `mins` 栈，`mins[i]` 是 `items[0..i]` 的最小值，所以 `pop` 后最小值自动回退。这是「用额外状态换 O(1)」的小例子，也是写不变量的练习：`len(items) == len(mins)`，`mins[-1] == min(items)`。
3. `CountDown`：Python 迭代器协议——`__iter__` 返回迭代器自己，`__next__` 返回下一个值或抛 `StopIteration`。`for` 循环、`list()` 都依赖它。LeetCode 的 `hasNext() / next()` 是同一个概念的另一种拼写。

## 3. 完整手算（Worked trace）

LRU，容量 2。链表从左到右是「最近 → 最久」。操作序列：`put(1,1) put(2,2) get(1) put(3,3) get(2) put(4,4) get(1) get(3) get(4)`：

```python
class Node:
    def __init__(self, k=0, v=0):
        self.key, self.val, self.prev, self.next = k, v, None, None

class LRU:
    def __init__(self, cap):
        self.cap, self.map = cap, {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head
    def _unlink(self, n):
        n.prev.next, n.next.prev = n.next, n.prev
    def _front(self, n):
        n.prev, n.next = self.head, self.head.next
        self.head.next.prev = n
        self.head.next = n
    def order(self):                      # most recent first
        out, n = [], self.head.next
        while n is not self.tail:
            out.append(f"{n.key}={n.val}")
            n = n.next
        return out
    def get(self, k):
        n = self.map.get(k)
        if not n:
            return -1
        self._unlink(n)
        self._front(n)
        return n.val
    def put(self, k, v):
        n = self.map.get(k)
        if n:
            n.val = v
            self._unlink(n)
            self._front(n)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]
        n = Node(k, v)
        self.map[k] = n
        self._front(n)

c = LRU(2)
for op, args in [("put", (1, 1)), ("put", (2, 2)), ("get", (1,)), ("put", (3, 3)), ("get", (2,)), ("put", (4, 4)), ("get", (1,)), ("get", (3,)), ("get", (4,))]:
    res = getattr(c, op)(*args)
    print(f"{op}{args!s:<8} -> {res!s:<4} list (recent -> old): {c.order()}")
```

```text
put(1, 1)   -> None list (recent -> old): ['1=1']
put(2, 2)   -> None list (recent -> old): ['2=2', '1=1']
get(1,)     -> 1    list (recent -> old): ['1=1', '2=2']
put(3, 3)   -> None list (recent -> old): ['3=3', '1=1']
get(2,)     -> -1   list (recent -> old): ['3=3', '1=1']
put(4, 4)   -> None list (recent -> old): ['4=4', '3=3']
get(1,)     -> -1   list (recent -> old): ['4=4', '3=3']
get(3,)     -> 3    list (recent -> old): ['3=3', '4=4']
get(4,)     -> 4    list (recent -> old): ['4=4', '3=3']
```

读法：
- `get(1)` 之后 1 被移到最前，列表变成 `1, 2`。
- `put(3,3)` 时容量已满，淘汰最久的 **2**（不是 1，因为刚用过 1），得到 `3, 1`；所以 `get(2) = -1`。
- `put(4,4)` 淘汰最久的 1；`get(3)` 把 3 提到最前。

## 4. 题目

```python
import random
from collections import OrderedDict, defaultdict


class NestedInteger:                       # LeetCode supplies this interface for LC 341; a tiny stand-in
    def __init__(self, value):
        self._v = value

    def isInteger(self):
        return isinstance(self._v, int)

    def getInteger(self):
        return self._v

    def getList(self):
        return self._v


def make(x):
    return NestedInteger([make(i) for i in x] if isinstance(x, list) else x)
```

### 4.1 LC 146 · LRU Cache（Medium）

```python
# solutions/146_lru_cache.py
class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                              # key -> node
        self.head, self.tail = _Node(), _Node()    # sentinels: most-recent side / least-recent side
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):                   # right after head = most recently used
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.map.get(key)
        if not node:
            return -1
        self._unlink(node)
        self._push_front(node)                     # reading makes it most recent
        return node.val

    def put(self, key, value):
        node = self.map.get(key)
        if node:
            node.val = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.cap:              # evict the least recently used = node before tail
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]                  # that's why the node stores its key
        node = _Node(key, value)
        self.map[key] = node
        self._push_front(node)
```

- **一句话洞见**：`dict`：key → 链表节点；链表（带头尾哨兵）：最近使用的在 `head` 后面，淘汰 `tail.prev`。每次 `get` / `put` 都把节点摘下再插到最前面。
- **复杂度**：`get`、`put` 均 O(1)；空间 O(capacity)。
- **不变量**：`len(map) == 链表节点数 ≤ capacity`；`map[k].key == k`。

**资深追问**

- **规模 ×1000**：条目数 10⁹ 时单机放不下 → 分片：一致性哈希（consistent hashing）把 key 分配到多个缓存节点，每个节点内部一个 LRU；热点 key 要考虑本地缓存 / 副本。Python 每个对象开销大（~100 字节级，估算），真实系统用紧凑数组 / 对象池。
- **TTL 与过期**：除了 LRU 还要支持存活时间：惰性删除（访问时检查）+ 后台定期清理；**缓存雪崩**（大量 key 同时过期）可以对 TTL 加随机抖动；**缓存击穿**（热点 key 过期瞬间大量请求打到数据库）用单飞（singleflight）/ 互斥锁。
- **内存**：`__slots__` 减小节点开销；容量按条数还是按字节（按字节需要每项记录大小）？
- **并发**：单个全局锁最简单（`threading.Lock`），但 `get` 也要改链表，所以读也是写，锁竞争严重。优化：**分片 LRU**（每片一把锁）；**近似 LRU**（CLOCK 算法、随机采样）；**批量记录访问**（读路径只把访问事件写进缓冲区，由后台线程批量调整顺序，Caffeine 的做法）。
- **接口 / 契约**：`capacity <= 0`？值可以是 `None` 吗（那 `get` 返回 −1 就有歧义，更好的接口返回 `Optional` 或抛 `KeyError`）？`put` 是否返回被淘汰的条目（便于写回）？命中率等指标暴露在哪？
- **测试**：与 `OrderedDict` 参考实现做随机对拍（文件里已有，100 组 × 60 步）；容量 1、重复 `put` 同一 key 不触发淘汰、`get` 之后淘汰顺序改变；并发压力测试检查 `size <= capacity` 与无死锁。

### 4.2 LC 460 · LFU Cache（Hard）

```python
# solutions/460_lfu_cache.py
class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.vals = {}                              # key -> value
        self.freq = {}                              # key -> use count
        self.buckets = defaultdict(OrderedDict)     # count -> keys with that count, oldest first
        self.min_freq = 0

    def _touch(self, key):
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:                  # the min bucket emptied: the key moves up to f+1
                self.min_freq = f + 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key):
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) == self.cap:
            old, _ = self.buckets[self.min_freq].popitem(last=False)   # LFU, ties -> least recent
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[old], self.freq[old]
        self.vals[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1                           # a brand-new key always has the minimum count
```

- **一句话洞见**：淘汰「使用次数最少」的，次数相同时淘汰最久未用的。结构：`vals`（key→值）、`freq`（key→次数）、`buckets`（次数→一个**有序字典**，保存该次数下的 key，按最近使用排序）、`min_freq`。每次访问把 key 从 `buckets[f]` 移到 `buckets[f+1]`；淘汰时从 `buckets[min_freq]` 的最前面弹出。
- **关键细节**：新插入的 key 次数为 1，所以 `min_freq` 直接重置为 1；`_touch` 里如果最小次数的桶空了，`min_freq` 增加 1。
- **复杂度**：`get`、`put` 均 O(1)。

**资深追问**

- **规模 ×1000**：同 LRU：分片 + 紧凑内存。每个 key 要存次数，开销比 LRU 大。
- **频率衰减**：纯 LFU 的问题是**缓存污染**——曾经很热但已经不再被访问的 key 次数很高，永远淘汰不掉。工程上用**次数老化**（周期性减半）或 TinyLFU / W-TinyLFU（用 Count-Min Sketch 近似计数，Caffeine 用）。
- **并发**：同 LRU，访问会改多个结构，分片加锁；近似计数可以用无锁计数器。
- **内存**：精确计数每个 key 一个整数 + 桶结构；近似计数用 sketch，内存固定。
- **接口**：`capacity = 0` 时所有 `put` 都是空操作；`put` 已存在 key 是否算一次使用（常见约定：算）；`get` 不存在的 key 不影响任何计数。
- **测试**：与 O(n) 扫描最小 `(次数, 最近使用时间)` 的参考实现随机对拍（文件里已有）；并列次数、容量 0、容量 1、淘汰后重新插入的 key 次数从 1 开始。

### 4.3 LC 380 · Insert Delete GetRandom O(1)（Medium）

```python
# solutions/380_insert_delete_getrandom_o1.py
class RandomizedSet:
    def __init__(self):
        self.items = []
        self.pos = {}                          # value -> index in items

    def insert(self, val):
        if val in self.pos:
            return False
        self.pos[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val):
        if val not in self.pos:
            return False
        i = self.pos[val]
        last = self.items[-1]
        self.items[i] = last                   # overwrite the hole with the last element ...
        self.pos[last] = i
        self.items.pop()                       # ... then pop the tail in O(1)
        del self.pos[val]                      # delete AFTER the fix-up: val may itself be the last one
        return True

    def get_random(self):
        return random.choice(self.items)
```

- **一句话洞见**：数组支持 O(1) 随机取元素，但删除中间元素要搬动；`dict` 记录「值 → 数组下标」，删除时**把最后一个元素搬到被删位置**，然后弹出末尾，O(1)。
- **复杂度**：三个操作均 O(1)（均摊）。
- **顺序很重要**：`remove` 里先用 `last` 覆盖空位、更新 `pos[last]`，**最后**才 `del self.pos[val]`——当被删的就是最后一个元素时，才不会误删刚更新的映射。

**资深追问**

- **规模 ×1000**：线性内存；Python 列表 `append` / `pop` 均摊 O(1)（偶尔扩容）。
- **带权随机**：每个元素有权重 → 前缀和 + 二分，或树状数组（Fenwick）支持动态更新 O(log n)；或别名法（alias method）O(1) 采样、O(n) 构建（不支持动态更新）。
- **重复元素（LC 381）**：`值 → 下标集合`，删除时从集合里任取一个下标。
- **并发**：多线程下 `getRandom` 与 `remove` 并发会读到半更新的状态 → 加锁；均匀性在并发修改下需要明确定义。
- **接口 / 契约**：`insert` / `remove` 返回是否改变了集合；空集合 `getRandom` 抛异常；随机数源可注入（便于测试）。
- **测试**：不变量 `all(pos[items[i]] == i)`；删除最后一个元素和非最后元素两条路径；用固定种子做统计均匀性检验（文件里已有）。

### 4.4 LC 588 · Design In-Memory File System（Hard）

```python
# solutions/588_design_in_memory_file_system.py
class _Dir:
    def __init__(self):
        self.children = {}          # name -> _Dir
        self.content = None         # None for a directory, str for a file


class FileSystem:
    def __init__(self):
        self.root = _Dir()

    def _walk(self, path, create=False):
        node = self.root
        for part in [p for p in path.split("/") if p]:
            if part not in node.children:
                if not create:
                    return None
                node.children[part] = _Dir()
            node = node.children[part]
        return node

    def ls(self, path):
        node = self._walk(path)
        if node is None:
            return []
        if node.content is not None:                       # a file lists as itself
            return [path.rstrip("/").split("/")[-1]]
        return sorted(node.children)

    def mkdir(self, path):
        self._walk(path, create=True)

    def add_content_to_file(self, path, content):
        node = self._walk(path, create=True)
        node.content = (node.content or "") + content      # "" is a file, None is a directory

    def read_content_from_file(self, path):
        return self._walk(path).content
```

- **一句话洞见**：路径由 `/` 分隔，每一级是一个目录或文件，天然是一棵**前缀树（trie）**：每个节点有 `children`（名字 → 子节点），文件节点额外存 `content`。`ls` 对文件返回它自己的名字，对目录返回排序后的子项名。
- **复杂度**：`mkdir` / `add_content` / `read`：O(路径长度)；`ls`：O(路径长度 + k log k)（k 为子项数）。

**资深追问**

- **规模 ×1000**：目录里有百万条目时每次 `ls` 排序太慢 → 用有序字典（`SortedDict` / 平衡树）或分页；文件内容反复追加，字符串拼接是 O(n²)，改用块列表（rope / chunk list）。
- **持久化**：先写日志再改内存（WAL，write-ahead log），崩溃后重放；定期快照。
- **并发**：目录级读写锁，操作跨多个目录时按固定顺序加锁避免死锁（mkdir -p 沿路径加锁）；或不可变节点 + 原子替换根（copy-on-write）。
- **接口 / 契约**：路径规范化（`//`、结尾 `/`、`.`、`..`、符号链接）；`ls` 一个不存在的路径返回 `[]` 还是报错（LeetCode 约定返回 `[]`，真实系统应该报错）；往目录里写内容、把文件当目录用等非法操作的错误处理；权限。
- **内存**：每个节点一个 `dict`，大量小文件时开销大 → 紧凑表示。
- **测试**：根目录 `ls`、嵌套 `mkdir`、追加两次内容、`ls` 文件、不存在路径；路径规范化用例（`/a//b/`）。

### 4.5 附赠：LC 341 · Flatten Nested List Iterator（Medium）——迭代器类题的模板

```python
# solutions/341_flatten_nested_list_iterator.py
class NestedIterator:
    def __init__(self, nested_list):
        self.stack = list(reversed(nested_list))      # top of stack = next item to look at

    def has_next(self):
        while self.stack:                             # unwrap lists lazily until an integer is on top
            top = self.stack[-1]
            if top.isInteger():
                return True
            self.stack.pop()
            self.stack.extend(reversed(top.getList()))
        return False

    def next(self):
        if not self.has_next():                       # next() must be safe without a prior has_next()
            raise StopIteration
        return self.stack.pop().getInteger()
```

- **一句话洞见**：用栈**惰性**展开：栈顶是下一个要看的元素；是整数就停；是列表就弹出并把它的元素**倒序**压回栈。`has_next` 负责展开、`next` 只负责取出。
- **复杂度**：均摊 O(1) 每次 `next`；空间 O(嵌套深度 + 当前列表长度)。
- **对比急切（eager）做法**：构造时递归展开成一个平铺列表，O(n) 内存；惰性版内存小，并且支持「很大 / 无限」的嵌套结构。

**资深追问**

- **规模 ×1000**：惰性迭代器只占用与深度成正比的内存；急切展开会一次性占用 O(n)。
- **流式**：迭代器本身就是流的抽象；Python 里更惯用 `yield` 的生成器：`def flatten(x): for i in x: yield from flatten(i) if isinstance(i, list) else [i]`（递归深度受 1000 限制）。
- **并发**：迭代器**不是线程安全的**（有可变状态），文档里要写明；遍历期间底层结构被修改要么定义为未定义行为，要么像 Java 一样 fail-fast。
- **接口 / 契约**：`has_next()` 必须**幂等**（多次调用不改变语义）；`next()` 在没有调用 `has_next()` 时也必须正确；耗尽后 `next()` 抛 `StopIteration`。
- **测试**：只有空列表（`[[], [[]], []]`）、深嵌套、一开始就为空、不调用 `has_next` 直接 `next`。

## 5. 常见 bug

1. **淘汰时忘记从 `dict` 里删除**，或节点里没存 key 导致不知道删谁。
2. **`put` 已存在的 key 当作新插入**：触发多余的淘汰，或同一 key 在链表里出现两次。
3. **没有哨兵节点**：到处是 `if node.prev is None`，容易漏掉头尾的特判。
4. **LFU 里 `min_freq` 更新错**：新插入时没有重置为 1；`_touch` 后最小桶空了没有 +1。
5. **380 的 `remove` 顺序错**：当 `val` 就是最后一个元素时，先 `del pos[val]` 再 `pos[last] = i` 会把刚删的又写回来。
6. **`get` 不更新使用顺序**。
7. **迭代器的 `has_next` 有副作用却不幂等**，或 `next` 依赖调用者先调用 `has_next`。
8. **在循环里修改正在遍历的容器**（`for k in d: del d[k]`）。

## 6. 自测题

1. LRU 的节点里为什么必须存 key？
   <details><summary>答案</summary>淘汰时拿到的是链表尾部的节点，需要用它的 key 去 `dict` 里删除对应的条目；节点不存 key 就无法 O(1) 完成。</details>
2. 为什么用双向而不是单向链表？
   <details><summary>答案</summary>要 O(1) 摘下任意已知节点，必须知道它的前驱；单向链表要从头找前驱（O(n)）。</details>
3. LFU 里为什么每个频率桶要用有序字典，而不是 `set`？
   <details><summary>答案</summary>同频率下要淘汰「最久未使用」的，需要保持插入 / 使用顺序；有序字典可以 O(1) 取最老、O(1) 移走任意 key。</details>
4. 小编程：用 `OrderedDict` 写一个带 TTL 的缓存，过期的 key 在 `get` 时惰性删除。
   <details><summary>答案</summary>值存 `(value, expire_at)`；`get` 时若 `time.monotonic() >= expire_at` 就 `del` 并返回 −1；`put` 时设置 `expire_at = now + ttl`；容量满时先弹出最老的。可以再用后台线程定期扫描清理。注意使用单调时钟而不是 `time.time()`，避免系统时间调整的影响。</details>
5. 380 的随机元素为什么是均匀的？
   <details><summary>答案</summary>`random.choice(list)` 在列表下标上均匀选择，而列表里每个元素恰好出现一次，所以每个元素概率都是 1/n。</details>
6. 资深追问：你的 LRU 在 32 核机器上成了瓶颈，怎么办？
   <details><summary>答案</summary>先量（profiling）确认瓶颈是锁竞争。选项：(1) 分片，按 `hash(key) % N` 分到 N 个独立 LRU，各自一把锁；(2) 读路径不改链表，只记录访问事件到环形缓冲区，后台线程批量重排；(3) 近似 LRU（CLOCK / 采样）；(4) 缓存本身放在读多的场景里，用读写分离的快照。需要权衡命中率的损失。</details>
