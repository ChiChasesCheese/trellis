# pc08 · LRU Cache + TTL + Median From Stream：两道经典设计题打包成一题

> 45 分钟第一轮编码题；Part 1、Part 3 是一手报道的独立经典题（合并成一题的三个 part），Part 2 **(reconstructed)**。

## 背景

QuantVault 的 Millennium 面试题单里，LRU Cache 与 Median from a Data Stream 各自单独列出（未标具体轮次），和这套题库里其它 45 min 编码题同族——都是"经典设计题，面试官边看边追问"。本题把两道题接成一份三 part 的题：Part 1 是 LRU Cache 本身（LC 146），Part 2 是它最常见的追问"如果条目要过期呢"，Part 3 是另一道独立经典题 Median from a Data Stream（LC 295）。

## API 契约（英文签名）

```python
class LRUCache:
    def __init__(self, capacity: int) -> None: ...
    def get(self, key: int) -> int: ...
    def put(self, key: int, value: int) -> None: ...

class LRUCacheLinked:            # 同样的行为，手写双链表实现
    def __init__(self, capacity: int) -> None: ...
    def get(self, key: int) -> int: ...
    def put(self, key: int, value: int) -> None: ...

class LRUCacheTTL:
    def __init__(self, capacity: int, clock=time.monotonic) -> None: ...
    def get(self, key: int) -> int: ...
    def put(self, key: int, value: int, ttl: float | None = None) -> None: ...

class MedianStream:
    def __init__(self) -> None: ...
    def add(self, num: int | float) -> None: ...
    def median(self) -> float: ...
```

- `capacity` 必须是正 `int`；否则 `ValueError`。
- `key`、`value` 必须是 `int`（不含 `bool`）；否则 `ValueError`。
- `ttl` 必须是正数或 `None`；否则 `ValueError`。
- `num` 必须是 `int` 或 `float`（不含 `bool`）；否则 `ValueError`。
- `median()` 在空流上调用 → `ValueError`。

## 规则

### Part 1 — LRU Cache（LC 146），两种实现对照

`LRUCache(capacity)`：`get(key)` 命中返回值并把该 key 标记为最近使用，未命中返回 `-1`（不抛异常——缓存未命中是正常状态）；`put(key, value)` 写入或更新，写入后若条目数超过 `capacity`，淘汰**最久未使用**的那个。两种实现必须行为完全一致：

- `LRUCache`：用 `collections.OrderedDict`（`move_to_end` + `popitem(last=False)`）。
- `LRUCacheLinked`：手写双向链表（MRU 在尾部、LRU 在头部）+ `dict[key -> node]`，面试官常追问"不用 `OrderedDict` 你怎么写"就是要这个版本。

### Part 2 — 加 TTL **(reconstructed)**

`LRUCacheTTL(capacity, clock=time.monotonic)`：`clock` 是可注入的无参可调用对象，返回当前时间（默认真实时钟，测试里注入假时钟）。`put(key, value, ttl=None)` 的 `ttl` 是**从写入时刻起的绝对到期时长**（到期时刻 = `clock() + ttl`），不是"每次 `get` 都刷新"的滑动窗口——`get` 会把条目标记为最近使用（影响 LRU 淘汰顺序），但**不会延后它的过期时间**。过期是惰性检查：`get` 时若 `clock() >= 到期时刻`，视为未命中（返回 `-1`）并顺带把这条过期的记录从缓存里清掉；查询一个已经在别处被淘汰或过期的 key 不是错误。容量淘汰（真正的 LRU 逻辑）和 TTL 过期是**两套独立机制**：只要 `put` 后条目数超过 `capacity`，就淘汰最久未使用的那个，跟它是否设了 TTL、TTL 是否还早无关（和 Part 1 完全一样的淘汰规则）。

### Part 3 — Median From a Data Stream（LC 295）

`MedianStream`：`add(num)` 把一个数加入流；`median()` 返回目前为止所有数的中位数（元素个数为偶数时是中间两个数的平均值）。用一个大顶堆存较小的一半、一个小顶堆存较大的一半，每次 `add` 后调整两堆大小差不超过 1；中位数就是较大那堆的堆顶，或者两堆堆顶的平均值。

## Worked examples（全部由 `solution.py` 实际运行得出）

**Part 1**（`LRUCache(2)` 与 `LRUCacheLinked(2)` 在同一操作序列上行为完全一致）
```python
c = LRUCache(2)
c.put(1, 1); c.put(2, 2)
c.get(1)      # -> 1（1 变成最近使用）
c.put(3, 3)   # 容量满，淘汰最久未使用的 2
c.get(2)      # -> -1（已被淘汰）
c.put(4, 4)   # 淘汰最久未使用的 1
c.get(1)      # -> -1
c.get(3)      # -> 3
c.get(4)      # -> 4
```

**Part 2**（`LRUCacheTTL(2, clock=lambda: now)`，测试里用可控的假时钟）
```python
now = 0
tc.put(1, 100, ttl=5)   # 到期时刻 = 0 + 5 = 5
tc.put(2, 200)          # 无 ttl，永不过期
tc.get(1)                # -> 100（还没到期）
now = 6
tc.get(1)                 # -> -1（6 >= 5，已过期，惰性清除）
tc.get(2)                  # -> 200（没设 ttl，不受影响）
```
```python
# 容量淘汰不看 ttl：
tc2 = LRUCacheTTL(2, clock=...)   # ttl 都设成很远的将来
tc2.put(1, 1, ttl=1000); tc2.put(2, 2, ttl=1000)
tc2.get(1)                          # 1 变成最近使用
tc2.put(3, 3)                        # 容量满，淘汰最久未使用的 2（即使它 ttl 还早）
tc2.get(2)                            # -> -1
tc2.get(1)                             # -> 1
tc2.get(3)                              # -> 3
```

**Part 3**
```python
m = MedianStream()
m.add(5);  m.median()   # 5
m.add(15); m.median()   # (5+15)/2 = 10
m.add(1);  m.median()   # 排序后 [1,5,15]，中位数 5
m.add(3);  m.median()   # 排序后 [1,3,5,15]，(3+5)/2 = 4
```

## `main()` 命令流

**Part 1**：首行 `CAPACITY <n>`，然后 `PUT <k> <v>`（无输出）/ `GET <k>` → 整数（用 `LRUCache`）。
**Part 2**：首行 `CAPACITY <n>`，然后 `PUT <k> <v> <ttl或->`（`-` 表示不设 TTL）/ `GET <k>` → 整数 / `TICK <n>`（把包装器内置的假时钟前进 `n` 秒，无输出；这个假时钟只在批处理接口里用，与 `clock` 参数默认的真实时钟无关，保证 io 测试完全确定）。
**Part 3**：`ADD <num>`（无输出）/ `MEDIAN` → 格式化后的数（整数值不带小数点，如 `5` 而不是 `5.0`；否则原样输出，如 `4.5`）。

```
PART 1
CAPACITY 2
PUT 1 1
PUT 2 2
GET 1
PUT 3 3
GET 2
PUT 4 4
GET 1
GET 3
GET 4
→ 1
  -1
  -1
  3
  4
```

## 边界清单

- `capacity <= 0` 或非 `int` → `ValueError`（Part 1/2 均适用）
- `get` 未命中的 key（从未 `put` 过，或已被淘汰/过期）→ `-1`，不抛异常
- 对已存在的 key 再次 `put`：更新值 + 标记为最近使用，**不**额外占用容量
- `capacity=1`：每次 `put` 一个新 key 都会淘汰刚存在的那一个（除非是同一个 key）
- `LRUCache` 与 `LRUCacheLinked` 在同一组随机操作序列上必须给出完全相同的 `get` 返回值序列
- Part 2：`ttl=0` 或负数 → `ValueError`（`ttl` 必须是正数或 `None`）；`get` 命中后不会推迟过期时间（"不刷新"是本题的关键设计点，需要专门用例验证）
- Part 2：容量淘汰与 TTL 过期互相独立——一个 TTL 还早的条目仍可能被容量淘汰挤掉；一个未过期但容量内的条目会一直保留直到过期或被挤出
- Part 3：只有一个元素时中位数就是它本身；元素个数为偶数时是中间两个的平均值（可能不是整数）；负数、重复值、大量相同值都要正确
- Part 3：在空流上调用 `median()` → `ValueError`
- Part 3：`add` 的输入含 `bool`（`True`/`False` 是 `int` 子类）→ `ValueError`（不当成 1/0 悄悄接受）

## 追问

1. **`LRUCache` 与 `LRUCacheLinked` 为什么行为必须完全一致？两者复杂度一样吗？** 都是均摊 O(1) get/put；`OrderedDict` 内部也是双向链表 + 哈希表，`LRUCacheLinked` 只是把这套机制显式手写出来——面试官要看你是否理解"O(1) LRU"背后到底在维护什么结构，而不是只会调库。
2. **Part 2 的并发场景：多个线程同时 `get`/`put` 需要加锁吗？** 需要——`get` 的"检查过期 + 删除 + 标记最近使用"和 `put` 的"写入 + 判断容量 + 淘汰"都是多步操作，必须整体加锁（不能只保护 dict 本身的读写），否则会有"两个线程都判断容量超限，各自淘汰一个，实际淘汰了两个"这类竞态。
3. **为什么用两个堆求中位数，而不是维护一个有序列表？** 有序列表插入是 O(n)（要移动元素定位插入点），两个堆插入是 O(log n)；两个堆牺牲的是"看某个非中位数的排名"这种查询能力，但本题只要中位数，O(log n) 插入 + O(1) 查询是最优权衡。
4. **LRU 和 LFU（最不常用淘汰）有什么区别？什么场景选哪个？** LRU 淘汰"最久没被访问的"，假设"最近用过的还会再用"（时间局部性）；LFU 淘汰"访问次数最少的"，适合访问频率长期稳定、不随时间剧烈变化的场景，但要处理"新条目还没来得及攒够访问次数就被误淘汰"的问题（通常需要额外的衰减机制）。

## 来源与置信度

- **MED**：QuantVault Millennium 面试题单（LRU Cache、Median from a Data Stream，各自独立列出，未标注具体轮次）；两题都是 Stripe/Snowflake 同族题库里的高频经典设计题，形态与本题库其它"经典题 + 追问"的第一轮编码题一致。
- Part 2（TTL 扩展）未见一手报道，标 **(reconstructed)**：是 LRU Cache 面试里最常见的标准追问方向之一。

## 考什么

O(1) 缓存设计的两种实现路径（库 vs 手写双链表）及其等价性 · 惰性过期与主动淘汰两套独立机制的边界（"过期"不等于"被淘汰"）· 依赖注入的时钟让"时间相关"逻辑变得可测试 · 双堆求中位数的复杂度权衡（插入 O(log n) vs 有序结构插入 O(n)）。
