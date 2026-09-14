# od08 · LRU/TTL/双层 Cache：练的是"淘汰规则一层层叠加，底层存储不用换"

> [!tldr]
> - **Part 3（双层 hot/cold + 自动升级）是 (reconstructed)**：来源只用"warehouse SSD 热层 + 更大冷层"这个产品形状做主题级印证，没有给出具体的 promotion/demotion 规则，本题选择"命中 cold 立即升级"这个最简单的策略
> - 这题考的是：经典 LRU（LC 146）打底，叠加 TTL 半开区间过期，再叠加"热层/冷层，访问自动升级、淘汰自动降级"
> - 三步套路：先写一个内部 `_LRUStore` helper（O(1) 触达 MRU、O(1) 弹 LRU）→ Part 1/2 都基于它扩展（TTL 只是多存一个过期时间）→ Part 3 用两个独立的 `_LRUStore` 实例组合出双层结构
> - 最值得带走的一个模式：**过期腾出的空间不该逼着系统淘汰一个仍然有效的条目**——容量超出时优先清理过期记录，清理后仍超容量才走标准 LRU 淘汰

## 类设计先定契约
```python
class LRUCache:
    def __init__(self, capacity: int) -> None: ...
    def get(self, key) -> int: ...             # -1 缺失
    def put(self, key, value: int) -> None: ...

class TTLCache:
    def __init__(self, capacity: int) -> None: ...
    def get(self, key, now: int) -> int: ...              # -1 缺失或已过期
    def put(self, key, value: int, now: int, ttl: int) -> None: ...

class TwoTierCache:  # (reconstructed)
    def __init__(self, hot_capacity: int, cold_capacity: int) -> None: ...
    def get(self, key) -> int: ...             # -1 两层都没有
    def put(self, key, value: int) -> None: ...
```
**不变量（写代码前先想清楚）**：
1. `get`/`put` 命中已存在的 key 都要更新 MRU 位置，不是"只读不算访问"。
2. TTL 是半开区间 `[now, now+ttl)`——`now+ttl` 这一刻本身已经过期。
3. 容量超出时**先清理过期记录**腾出空间，清理后仍超容量才淘汰未过期记录里最久未使用的那个。
4. 双层缓存里一个 key 不会同时出现在 hot 和 cold 两层——升级/降级都先从原层移除再插入另一层。

## 1. 题目在说什么（人话版）
Part 1 是标准 LRU：容量满了淘汰最久未使用的。Part 2 加 TTL：每条记录有个过期时间，过期的记录
`get` 不到，且容量不够时优先靠"清理过期记录"腾地方而不是冤枉淘汰一个还有效的条目。Part 3 模拟
"SSD 热层 + 更大冷层"：新写入总进热层，热层满了把最旧的降级到冷层；冷层命中会被"升级"回热层。

三行小例子（Part 2）：
```
put("p", 1, now=0, ttl=2)     # p 在 [0,2) 有效
put("q", 2, now=5, ttl=100)   # now=5 时 p 已过期(5>=2)，插入q不需要淘汰任何仍有效的条目
get("p", now=5) -> -1；get("q", now=5) -> 2
```

## 2. 读题：把文字变成模型
- **实体**：缓存条目（key、value，可能带过期时间）、访问顺序（LRU 端到 MRU 端）。
- **输入长什么样**：`main()` 命令流 `GET/PUT`，Part 2 额外带 `now`/`ttl`。
- **输出要什么**：`GET` 输出值或 `-1`。
- **状态**：一个按访问顺序排列的有序字典（`OrderedDict` 或等价的哈希表+双向链表）。
- **一句话建模**：这是一个 **围绕"O(1) 触达 MRU + O(1) 弹出 LRU"这一份底层能力，逐层叠加淘汰规则**
  的问题——TTL 是"多一个过期检查"，双层是"两份底层能力组合出降级/升级流程"。

> [!note] 为什么选这个数据结构
> Python 的 `OrderedDict` 天然支持 `move_to_end`（O(1) 标记 MRU）和 `popitem(last=False)`（O(1)
> 弹出 LRU 端），正是 LRU 需要的两个操作。把这层封装成一个内部 `_LRUStore` helper，三个 part 都基于
> 它构建——`LRUCache` 直接用；`TTLCache` 往值里塞一个 `(value, expire_at)` 元组；`TwoTierCache`
> 用两个独立的 `_LRUStore` 实例分别代表热层和冷层。这样"访问顺序"这个核心机制只写一次。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **接口先行**：先写 `_LRUStore` 这个内部 helper 的方法（`get`/`set_mru`/`remove`/`pop_lru`/
   `peek`/`__contains__`），再把三个公开类的签名过一遍——讲清楚它们各自往 `_LRUStore` 里存什么值。
2. **Part 1 最小可用**：`LRUCache` 直接包一层 `_LRUStore`：`put` 调 `set_mru`，超容量就 `pop_lru`；
   `get` 不存在返回 -1，存在就调 `get`（触达 MRU）。用官方 LC 146 样例验证。
3. **Part 2 叠加**：`TTLCache` 往 `_LRUStore` 里存 `(value, now+ttl)`；`get` 先查过期（`now >= 过期
   时间`就移除返回 -1），未过期才触达 MRU 返回值；`put` 超容量时先扫一遍找任意一个已过期的记录
   移除，找不到才退回标准 LRU 淘汰。
4. **Part 3 叠加**：`TwoTierCache` 内部两个 `_LRUStore`（hot/cold）。`_insert_hot` 写入热层后检查
   超容量，超了就 `pop_lru` 降级到冷层（调用 `_insert_cold`）；`_insert_cold` 同理，超了直接丢弃。
   `get` 先查热层，命中直接返回；查冷层命中就移除后调 `_insert_hot`（升级，可能连锁触发降级）。
5. **收尾**：用官方例子（尤其例 2a/2b 区分"LRU 淘汰"和"过期腾空间"两种不同原因）和例 3（升级/降级
   /彻底丢弃全链路）逐步验证。

## 4. 代码怎么组织
```
_LRUStore                                  # 内部 helper：OrderedDict 封装,O(1) 触达/弹出/移除
LRUCache.get/put(...)                       # 直接包一层 _LRUStore
TTLCache.get/put(...)                       # 存 (value, expire_at)，容量超出优先清过期
TwoTierCache._insert_hot/_insert_cold(...)  # 两个 _LRUStore 组合出升级/降级链路
main(stdin, stdout)                         # 解析三种命令流，分发
```
`_LRUStore` 是唯一知道"用什么数据结构实现 O(1) LRU"的地方，三个公开类都不直接操作 `OrderedDict`，
这样如果要把底层换成手写双向链表+哈希表，只需要改 `_LRUStore` 一个类。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
class _LRUStore:                            # 内部 helper：O(1) 触达 MRU / 弹出 LRU
    def __init__(self):
        self._data = OrderedDict()
    def get(self, key):
        v = self._data[key]
        self._data.move_to_end(key)          # 触达 -> 移到 MRU 端
        return v
    def set_mru(self, key, value):
        self._data[key] = value
        self._data.move_to_end(key)
    def pop_lru(self):
        return self._data.popitem(last=False)  # 弹出 LRU 端

class TTLCache:
    def __init__(self, capacity):
        self._capacity, self._store = capacity, _LRUStore()

    def get(self, key, now):
        if key not in self._store:
            return -1
        value, expire_at = self._store.peek(key)
        if now >= expire_at:                  # 半开区间：now==expire_at 已过期
            self._store.remove(key)
            return -1
        return self._store.get(key)[0]        # 触达 MRU

    def put(self, key, value, now, ttl):
        self._store.set_mru(key, (value, now + ttl))
        while len(self._store) > self._capacity:
            expired = self._find_any_expired(now)
            self._store.remove(expired if expired is not None else next(iter(self._store)))
            if expired is None:               # 没有过期记录才真正走 LRU 淘汰
                break

class TwoTierCache:
    def __init__(self, hot_capacity, cold_capacity):
        self._hot_cap, self._cold_cap = hot_capacity, cold_capacity
        self._hot, self._cold = _LRUStore(), _LRUStore()

    def get(self, key):
        if key in self._hot:
            return self._hot.get(key)
        if key in self._cold:                 # 命中冷层 -> 升级
            value = self._cold.peek(key)
            self._cold.remove(key)
            self._insert_hot(key, value)
            return value
        return -1

    def _insert_hot(self, key, value):
        self._hot.set_mru(key, value)
        if len(self._hot) > self._hot_cap:     # 热层满了，降级最旧的一个
            k, v = self._hot.pop_lru()
            self._insert_cold(k, v)

    def _insert_cold(self, key, value):
        self._cold.set_mru(key, value)
        if len(self._cold) > self._cold_cap:    # 冷层也满了，彻底丢弃
            self._cold.pop_lru()
```

## 6. 并发追问怎么答
- **多线程 `get`/`put` 最简单的线程安全做法**：一把全局锁包住整个方法——代价是把 O(1) 操作序列化
  成互斥访问，高并发下吞吐明显下降；更细粒度的方向是按 key 哈希分片成多个子 LRU，各自独立加锁。
- **TTL 惰性清除依赖 `get` 触发，永远不会被访问的过期 key 会一直占容量吗**：会——惰性清除只在访问
  时生效，是本题 Part 2 的设计选择；生产系统通常配一个后台定时清扫线程（active expiration）作为
  补充，覆盖"读多写少"和"写多读少"两种模式。

## 7. 常见跑偏（方法层面，3 条）
- **TTL 容量淘汰时直接走标准 LRU，不优先清过期记录**：会把一个仍然有效的条目冤枉淘汰掉，而这一刻
  其实存在一个已经过期、本该免费腾出空间的记录——例 2a/2b 就是专门测这个区分的。
- **双层缓存的"升级"没有先从冷层移除**：如果只是"复制"到热层而不从冷层删除，会导致同一个 key 同时
  存在于两层，破坏"一个 key 只在一层"的不变量。
- **降级/丢弃链路没有递归处理**：热层降级一个条目到冷层后，冷层可能因此也超容量，需要接着触发冷层
  的丢弃逻辑——这是一个连锁反应，不能只处理"降级到冷层"这一步就结束。

## 自测清单
- `capacity=0` 时任何 `put` 都不会真正保留条目，`get` 永远 -1。
- `get`/`put` 命中已存在 key 都要更新 MRU 位置。
- TTL 边界：`now==过期时间` 算已过期,`now==过期时间-1` 仍有效。
- 同一 key 被 `put` 两次、ttl 不同，第二次完全覆盖第一次。
- 双层缓存：`hot_capacity=0` 时新写入立即降级到冷层；一个 key 不会同时出现在两层。
- 1e5 次操作在 2s 内完成（三个 part 各自独立测）。

## 相关题与 skills id
- skills: **S12**（缓存与淘汰：LRU/TTL/多级）· **S09**（类设计先定契约，TTL 半开区间/升级降级
  规则要主动讲清楚）· S10（并发追问层面的锁粒度讨论）。
- 同族：Stripe 的 `cd03_account_scheduler_lru` 也是"接口先行 + LRU tie-break"的类设计题。
- 练习命令：`python3 loop/mock.py start od08`
