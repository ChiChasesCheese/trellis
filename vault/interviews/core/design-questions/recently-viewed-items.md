---
slug: recently-viewed-items
kind: low-level-design
---
## Q
**设计"最近浏览"记录（类似 LRU 缓存，上限在构造时给定）**｜低层设计

设计一个跟踪每位客户最近浏览过哪些商品的组件：类初始化时传入一个整数上限 `limit`，每位客户最多保留最近浏览的 `limit` 个商品，超过后丢弃最久未浏览的；重复浏览同一商品只是把它提到最前面，不会占两个位置。题目的变体是：客户多次访问门户，要随时回答"到目前为止第一个只访问过一次的客户是谁"（与"第一个唯一数字"的算法题相同）。面试官会追问线程安全、客户数量巨大时的内存、以及真实系统里把它放在哪里。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** "最近浏览"就是每个客户一个定长的 LRU：用"按插入顺序排列且能 O(1) 摘除任意元素"的结构（哈希表加双向链表，语言里的有序字典），重复浏览是"摘下来放到队尾"，超限是"丢掉队头"；"第一个唯一值"是同一个思路——有序字典当队列，出现第二次就摘掉。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求，定接口：`view`、`recent`，`limit` 的校验 |
| 8–12 分 | 讲数据结构：每客户一个有序字典，重复浏览提前，超限丢队头 |
| 12–40 分 | 写核心实现：`RecentlyViewed` 一个类，一把锁 |
| 40–45 分 | 跑例子：`limit=3` 浏览 a、b、c、b、d |
| 45–60 分 | 追问：分段锁和外层 LRU、「第一个唯一值」、Redis |

**需求。**
- 功能：
  - 构造时给定 `limit`（正整数）；
  - `view(customer, item)`：记录一次浏览；
  - `recent(customer)`：返回该客户最近浏览的商品，最新的在前，最多 `limit` 个；
  - 重复浏览同一商品：移到最前面，不增加数量；
  - （变体）`visit(customer)` 与 `first()`：返回到目前为止只出现一次的第一个客户。
- 非功能：
  - 记录和查询都是 O(1)（`recent` 是 O(返回个数)）；
  - 线程安全；
  - 客户很多时内存有上界；
  - 不合法的 `limit`（0 或负数）要在构造时拒绝。

**核心实体与接口。**
- `RecentlyViewed(limit)`：`view(customer, item)`、`recent(customer) -> list`。
- 内部结构：外层 `customer -> 有序字典(item)`；有序字典的顺序就是"最近使用顺序"，队尾最新。
- `FirstUnique`：`visit(customer)`、`first()`；内部是"只出现一次的候选"（有序字典，按首次出现顺序）加"见过的集合"。
- 模式：组合（LRU 套 LRU：每位客户一个，外层再限制客户数）；分段锁用于降低并发争用。

**整体设计。** 外层 `customer → 有序字典`，字典的顺序就是最近使用顺序，队尾最新。`view` 先查重：已看过就 `move_to_end`，否则追加，超限 `popitem(last=False)` 丢最老的；`recent` 反向遍历，最新的在前。

**核心实现。** 27 行。用一把全局锁先保证线程安全。

```python
import threading
from collections import OrderedDict
from typing import Hashable


class RecentlyViewed:
    """每个客户一个定长、按最近访问排序的字典：重复浏览只"提前"，不重复占位；超过 limit 丢最老的。"""
    def __init__(self, limit: int) -> None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        self._limit = limit
        self._by_customer: dict[str, OrderedDict[Hashable, None]] = {}  # 字典的顺序就是最近使用顺序，队尾最新
        self._lock = threading.Lock()  # 先用一把全局锁，保证正确；争用问题见逐步扩展 1

    def view(self, customer: str, item: Hashable) -> None:
        with self._lock:
            items = self._by_customer.setdefault(customer, OrderedDict())
            if item in items:
                items.move_to_end(item)  # 已看过：移到最新，O(1)
            else:
                items[item] = None
                if len(items) > self._limit:
                    items.popitem(last=False)  # 淘汰最久未看的，O(1)

    def recent(self, customer: str) -> list[Hashable]:
        with self._lock:
            return list(reversed(self._by_customer.get(customer, ())))  # 最新的在前
```

**运行。**

```python
rv = RecentlyViewed(3)
for x in "abcbd":
    rv.view("u1", x)
```

- `rv.recent("u1")` → `['d', 'b', 'c']`：浏览 b 时 b 提前成 a、c、b；浏览 d 超限，丢掉最老的 a。
- `rv.recent("nobody")` → `[]`。
- `limit=1` 时依次浏览 a、b、b → `['b']`；`RecentlyViewed(0)` → `ValueError`。
- **并发浏览测试：** 8 个线程对同一客户浏览 2000 次、`limit=5` → 最后恰好 5 条。

**复杂度。** `view` 是 `O(1)`，`recent` 是 `O(返回个数)`，每客户内存 `O(limit)`。

**逐步扩展。**
1. 【追问再讲】分段锁和外层 LRU：一把全局锁让所有客户互相阻塞；客户有上亿时内存也放不下。外层也做成 LRU 限制活跃客户数，内层用按客户哈希的分段锁。把 `__init__`、`view`、`recent` 换成下面的版本。

```python
def __init__(self, limit: int, max_customers: int = 1_000_000, stripes: int = 64) -> None:
    if limit <= 0:
        raise ValueError("limit must be positive")
    self._limit, self._max_customers = limit, max_customers
    # 外层也是 LRU：不活跃的客户整体被挤出，内存有上界（冷客户的最近浏览回源到存储）
    self._by_customer: OrderedDict[str, OrderedDict[Hashable, None]] = OrderedDict()
    self._locks = [threading.Lock() for _ in range(stripes)]  # 分段锁：不同客户互不阻塞
    self._outer = threading.Lock()

def _lock_for(self, customer: str) -> threading.Lock:
    return self._locks[hash(customer) % len(self._locks)]

def view(self, customer: str, item: Hashable) -> None:
    with self._outer:  # 只保护外层 map 的结构变化，持锁极短
        items = self._by_customer.get(customer)
        if items is None:
            items = self._by_customer[customer] = OrderedDict()
            if len(self._by_customer) > self._max_customers:
                self._by_customer.popitem(last=False)
        else:
            self._by_customer.move_to_end(customer)
    with self._lock_for(customer):
        if item in items:
            items.move_to_end(item)
        else:
            items[item] = None
            if len(items) > self._limit:
                items.popitem(last=False)

def recent(self, customer: str) -> list[Hashable]:
    with self._lock_for(customer):
        return list(reversed(self._by_customer.get(customer, ())))
```

`max_customers=2`：浏览完 u1 的 a、b、c、b、d，再浏览 u2、u3 → u1 被挤出，`recent("u1")` 是 `[]`，`recent("u3")` 是 `['y']`。4 个客户、8 个线程各浏览 1000 次、`limit=5` → 每人恰好 5 条。

2. **【追问再讲】首个只访问一次的变体：** 变体「到目前为止第一个只访问过一次的客户」：有序字典当候选队列，`seen` 集合记录见过的，全部操作 `O(1)`。

```python
class FirstUnique:
    def __init__(self) -> None:
        self._unique: dict[Hashable, None] = {}
        self._seen: set[Hashable] = set()
        self._lock = threading.Lock()

    def visit(self, customer: Hashable) -> None:
        with self._lock:
            if customer not in self._seen:
                self._seen.add(customer)
                self._unique[customer] = None  # 第一次出现：进候选队尾
            else:
                self._unique.pop(customer, None)  # 第二次及以后：永久出局

    def first(self) -> Hashable | None:
        with self._lock:
            return next(iter(self._unique), None)
```

依次访问 a、b、a、c、b：`first()` 依次是 a、a、b、b、c；再访问 c → `None`。

**深入。**
1. 【必讲】数据结构选择。
   - 数组：查重和移动是 `O(limit)`，`limit` 小时可用，但不是 `O(1)`。
   - 哈希表加双向链表（有序字典）：查找、摘除、追加、丢队头全是 `O(1)`，这是 LRU 的标准结构。
   - 选有序字典。面试官要求自己实现时，手写哈希表加双向链表，用哨兵头尾节点简化边界。
2. 【必讲】线程安全与并发。
   - 一把全局锁：简单，但所有客户互相阻塞。
   - 每客户一把锁：锁数量等于客户数，内存代价大。
   - 分段锁：固定 N 段（例如 64），按客户哈希选锁，争用低、内存小；外层字典的结构变化用另一把短锁保护。
3. 【追问再讲】客户数量巨大时的内存：每客户至多 `limit` 条，但客户有上亿时仍放不下，所以外层再套一层 LRU（LRU 套 LRU）限制活跃客户数，被挤出的客户回源到持久层。真实系统更常见的是直接放 Redis。
4. 【追问再讲】可接受的竞态：客户刚被外层淘汰，另一线程还拿着旧的有序字典写入，这次写入丢失。对「最近浏览」这种尽力而为的数据可以接受；不能容忍时外层和内层用同一把锁，代价是争用变高。
5. 【追问再讲】「第一个唯一值」的另一种做法：队列加计数表，`first()` 时从队头跳过计数大于 1 的元素，摊还 `O(1)`。有序字典在第二次出现时就摘掉，`first()` 严格 `O(1)`，代码也更短。内存是 `O(不同客户数)`；要限制内存只能放弃精确性（布隆过滤器会有误判）。
6. 【加分】真实系统放在哪里。
   - Redis 有序集合：键 `recent:{customer}`，成员是商品，分数是浏览时间戳；浏览时 `ZADD`（已存在则更新分数，等于提前）加 `ZREMRANGEBYRANK key 0 -(limit+1)` 裁掉多余，读取用 `ZREVRANGE key 0 limit-1`，键设过期（如 30 天）。
   - 事件量大时，先合并同一商品的重复上报，再批量写。
   - 登录前后：匿名设备的记录在登录时与账号的记录按时间合并后再裁剪。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- `limit` 改成运行时可调：缩小时要裁剪所有客户的列表，可以惰性处理，下次访问该客户时裁剪。
- 要不要时间戳：需要「最近 7 天」时，字典的值存时间戳，读取时过滤过期的。
- 浏览同一商品要不要计频次：值改为（次数，最后时间），顺序仍按最后时间；这会演变成带频次的缓存。
- 多实例：同一客户请求粘性路由到同一实例，或统一放 Redis，避免各实例视图不一致。
- 测试点：重复浏览提前、恰好达到上限、超限丢最老、不存在的客户返回空列表、`limit=1`、并发浏览同一客户。

**级别期望。**
- 中级：用有序字典或列表实现 `view` 与 `recent`，处理重复和上限，指出时间复杂度；核心实现能跑通例子。
- 高级：`O(1)` 结构的原理（哈希表加双向链表）、分段锁、客户级内存上界、讲出 Redis 有序集合的真实方案。
- 资深/专家：竞态的取舍、事件合并与批量写、登录合并、容量与过期策略，以及「第一个唯一值」的摊还分析与内存精确性的权衡。

**先修概念。**
- **答题框架：** [[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]
- [[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]
- [[hi-low-level-design-concurrency-intro|并发入门]]
- [[hi-system-design-core-concepts-caching|缓存]]

**同类题。**
- [[solution-lru-cache|设计题解：LRU 缓存]]
- [[solution-ttl-cache|设计题解：带过期时间的缓存]]
- [[solution-amz-configurable-cache|设计题解：可配置缓存]]
- [[hi-system-design-deep-dives-redis|Redis]]：有序集合与过期
