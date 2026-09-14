# od08 · LRU Cache — O(1) LRU, TTL expiry, two-tier hot/cold with promotion

**类型：** onsite（VO，60 min，3 part）· **最近：** 2026（主题级反复出现，无单一一手日期）
**置信度：** LOW-MED for "Snowflake 反复问"，但 Part1（经典 LRU）本身是 HIGH（LC 146 原题）

## 背景
三个独立的准备站（staffengprep、interviewchamp、techprep）用几乎相同的措辞把 LRU Cache 描述成
"Snowflake warehouse cache 的基础"："frequently-accessed micro-partitions stay hot in SSD;
cold ones get evicted by exactly this policy"。这是一个**主题级**、没有单一一手候选人日期的说法
（LOW-MED），但 LRU 本身（LC 146）是被反复独立确认的经典题，本题把它当作载体，逐步加 TTL 过期
（多处 LeetCode Discuss 帖子讨论过"LRU + TTL"的组合，但没有标注 Snowflake），最后加一个**本仓库
重建**的"双层 hot/cold + 访问自动升级"扩展——对应 warehouse cache 框架里"SSD 热层 + 更大的冷层"
这个真实存在但没有面试报道细节的产品形状。

## API 契约（英文签名）
```python
Key = Hashable  # int or str, doesn't matter -- the cache never inspects key contents

class LRUCache:
    def __init__(self, capacity: int) -> None: ...
    def get(self, key: Key) -> int: ...          # -1 if missing (LC 146 sentinel convention)
    def put(self, key: Key, value: int) -> None: ...

class TTLCache:
    def __init__(self, capacity: int) -> None: ...
    def get(self, key: Key, now: int) -> int: ...              # -1 if missing OR expired
    def put(self, key: Key, value: int, now: int, ttl: int) -> None: ...

class TwoTierCache:  # (reconstructed)
    def __init__(self, hot_capacity: int, cold_capacity: int) -> None: ...
    def get(self, key: Key) -> int: ...   # -1 if missing from both tiers
    def put(self, key: Key, value: int) -> None: ...
```
(`main()`'s line format always carries keys as plain tokens/strings -- see below; the direct
Python API is exercised with whatever key type a test finds convenient, ints included, since the
class never inspects key contents.)

## 规则

### Part 1 — 经典 LRU，O(1)
标准 LC 146：`capacity` 个槽位；`get`/`put` 都要把命中的 key 标记为"最近使用"（移到 MRU 端）；
`put` 一个已存在的 key 更新其值并同样标记为 MRU；容量超出时淘汰**最久未使用**（LRU 端）的
条目。全部操作 O(1)（哈希表 + 双向链表，或等价结构——`OrderedDict.move_to_end` 是可接受的
实现手段，但候选人应该能讲清楚它底层就是双向链表）。

### Part 2 — TTL 过期
`TTLCache` 在 LRU 基础上给每条记录加一个过期时间：`put(key, value, now, ttl)` 让这条记录在
`[now, now + ttl)` 区间内有效（**半开区间**，与 od04 限流器的窗口约定一致：`now + ttl` 这一刻
本身已经过期）。`get(key, now)`：
- key 不存在，或存在但 `now >= 过期时间`（已过期）→ 返回 `-1`；已过期的记录在这次 `get` 里被
  **惰性清除**（不占用容量、也不再参与后续的 LRU 排序）。
- 未过期 → 正常 LRU 语义（标记为 MRU，返回值）。

容量淘汰规则：插入新 key 导致超出 `capacity` 时，**先尝试清理已经过期的记录**腾出空间（无论它们
是不是最久未使用的那个）；清理后仍然超出容量，才按标准 LRU 顺序淘汰未过期记录中最久未使用的
那个。换句话说：**过期是免费腾出来的空间，不应该逼着系统提前淘汰一个仍然有效的条目**。

### Part 3 — 双层 hot/cold + 访问自动升级（**重建**）
`TwoTierCache` 用两个独立容量的 LRU 层模拟"SSD 热层 + 更大冷层"：
- 新写入的 key 总是先进入 **hot** 层（作为 hot 的 MRU）。如果 hot 层因此超出 `hot_capacity`，
  把 hot 层最久未使用的那个条目**降级**（demote）到 cold 层（作为 cold 的 MRU，不是直接丢弃）；
  如果 cold 层因此也超出 `cold_capacity`，才真正**丢弃** cold 层最久未使用的那个条目。
- `get(key)`：先查 hot 层，命中则按 Part1 语义标记 MRU 并返回。查不到再查 cold 层，命中则
  **升级**（promote）：把这个条目从 cold 层移除、插入 hot 层（作为 hot 的 MRU），如果因此
  hot 层超容量，重复上面"降级一个到 cold，cold 满则丢弃"的流程。两层都查不到返回 `-1`。
- `put(key, value)` 对已存在于 hot 或 cold 的 key：更新值，并当作一次"访问"处理（如果原来在
  cold 层，同样触发升级到 hot；如果原来在 hot 层，标记为 hot 的 MRU）。对全新 key：按上面"新写入
  总是进 hot"处理。

## Worked examples

**例 1（Part1，LC 146 经典序列，capacity=2）**
```
put(1, 1)
put(2, 2)
get(1)        -- 1 变为 MRU；此时 LRU 顺序（旧->新）是 [2, 1]
put(3, 3)     -- 超容量，淘汰 LRU 端的 2；顺序变为 [1, 3]
get(2)
put(4, 4)     -- 超容量，淘汰 LRU 端的 1；顺序变为 [3, 4]
get(1)
get(3)
get(4)
```
→ `[1, -1, -1, 3, 4]`

**例 2a（Part2，容量淘汰优先清理过期记录）**
```
cache = TTLCache(capacity=1)
put("x", 1, now=0, ttl=5)     -- x 在 [0,5) 有效
put("y", 2, now=3, ttl=100)   -- now=3 时 x 仍未过期(3<5)；容量=1，只能靠标准 LRU 淘汰 x
get("x", now=4)
get("y", now=4)
```
→ `[-1, 2]`（x 是被 LRU 淘汰的，不是过期——`now=3 < 5`，x 此刻仍有效，但容量不够只能让位）

**例 2b（Part2，过期腾出的空间不需要走 LRU 淘汰）**
```
cache = TTLCache(capacity=1)
put("p", 1, now=0, ttl=2)     -- p 在 [0,2) 有效
put("q", 2, now=5, ttl=100)   -- now=5 时 p 已经过期（5>=2），插入 q 不需要淘汰任何"仍然有效"的条目
get("p", now=5)
get("q", now=5)
```
→ `[-1, 2]`
（例 2a 与例 2b 最终输出形式相同，但淘汰原因不同——测试文件分别用两个独立断言覆盖，不靠输出
反推原因。）

**例 3（Part3，升级/降级/彻底丢弃全链路，hot_capacity=1, cold_capacity=1）**
```
put(a, 1)     -- hot=[a] cold=[]
put(b, 2)     -- hot 超容量：a 降级到 cold；hot=[b] cold=[a]
get(a)        -- 命中 cold，升级 a 到 hot；hot 超容量：b 降级到 cold；hot=[a] cold=[b]
get(b)        -- 命中 cold，升级 b 到 hot；hot 超容量：a 降级到 cold；hot=[b] cold=[a]
put(c, 3)     -- 新写入 c 进 hot；hot 超容量：b 降级到 cold；cold 超容量：丢弃 cold 的 LRU 端 a
get(a)        -- a 已被彻底丢弃
```
→ `[1, 2, -1]`（`get(a)` 返回 1，`get(b)` 返回 2，最后 `get(a)` 返回 -1）

## `main()` 命令流
**Part1**：`GET <key>` / `PUT <key> <value>`，一行一操作，`GET` 输出一行整数。
**Part2**：`GET <key> <now>` / `PUT <key> <value> <now> <ttl>`。
**Part3**：`GET <key>` / `PUT <key> <value>`（与 Part1 同形，但驱动的是 `TwoTierCache`）。
首行仍是 `PART n`；`capacity`（Part1/Part2）或 `hot_capacity,cold_capacity`（Part3）由紧随
`PART n` 之后的一行 `CAPACITY <n>` / `CAPACITY <hot>,<cold>` 给出。

## 边界清单
- `capacity=0`（Part1/Part2）：任何 `put` 都不会真正保留任何条目，`get` 永远 `-1`
- `get`/`put` 命中已存在的 key 都要更新 MRU 位置，不只是"值更新"或"只读不算访问"
- TTL 边界：`now == 过期时间`（`put` 时的 `now+ttl`）算已过期（半开区间，`get` 返回 -1）；
  `now == 过期时间 - 1` 仍然有效
- 同一个 key 被 `put` 两次、ttl 不同：第二次 `put` 完全覆盖第一次的过期时间和值，不是取更晚/
  更早的那个
- Part3：`hot_capacity=0` 时任何新写入都会立即触发"降级"，相当于所有条目从一开始就只能活在
  cold 层（除非 `cold_capacity` 也是 0，那就彻底不保留任何条目）
- Part3：一个 key 不会同时出现在 hot 和 cold 两层（升级/降级都先从原来那一层**移除**再插入
  另一层）
- 10^5 次操作在 2s 预算内完成（三个 part 各自独立测）

## 并发追问
（Cross-cutting 并发笔记没有把 LRU 题单独列入"5/10 有明确并发追问"，但通用 prep 指南把"concurrent
LRU cache"列为一个常见考法，作为合理延伸追问）
1. "多线程 `get`/`put`，最简单的线程安全做法是什么，代价是什么？" —— 期望候选人先说"一把全局锁
   包住整个方法"，再讨论代价（把 O(1) 的操作序列化成互斥访问，高并发下退化明显），以及更细粒度
   方案（分片成多个子 LRU、按 key 哈希路由）的取舍。
2. "TTL 的惰性清除依赖 `get` 被调用到才会触发，如果一个 key 永远不会再被 `get`，它会一直占着
   容量吗？" —— 期望候选人指出"惰性清除只在访问时生效"是本题 Part2 的设计选择，生产系统通常会
   配一个后台定时清扫线程（active expiration）作为补充，两者结合覆盖"读大于写"和"写多读少"两种
   访问模式。

## 变体
- 一些来源提到"TTL 扩展"是通用 LeetCode Discuss 帖子的常见追问（未标注 Snowflake），本题按
  "reasonable extension"处理，不算作 Snowflake 专属证据。
- Part3 的双层设计是本仓库对"warehouse SSD 热层 + 冷层"这个产品框架的**重建**，来源没有给出
  具体的 promotion/demotion 规则；本题选择"任何一次访问命中 cold 就立即升级"这个最简单的策略，
  面试现场如果被问"这样会不会让偶发的一次性扫描污染 hot 层"，是一个合理的追问方向（生产系统常用
  "访问 N 次才升级"或"频率计数"来避免这个问题），不要求实现。

## 来源与置信度
- https://staffengprep.com/companies/snowflake/、https://interviewchamp.ai/company-coding/snowflake/lru-cache、
  https://www.techprep.app/companies/snowflake ——三个 prep 站用几乎相同措辞描述"LRU 是
  Snowflake warehouse cache 的基础，SDE-II onsite 反复出现"，但均未给出具体日期/候选人一手记录
- LC 146（LRU Cache）本身是被 2019 电面逐字确认过的独立经典题（`catalog/raw/coding_oa.md` 等
  处的通用 LC 复用模式）
- `catalog/raw/ood.md` #9、`catalog/CATALOG.md` Table B od08 行；置信度 **LOW-MED**（"在
  Snowflake 反复问"这个论断本身）；Part1 单独看是 **HIGH**（LC 原题）；Part3 明确标注**重建**。

## 考什么
S12 缓存与淘汰（LRU/TTL/多级）· S09 类设计先定 API 契约（TTL 的半开区间、升级/降级规则要主动
讲清楚）· S10（间接，并发追问层面的锁粒度讨论）
