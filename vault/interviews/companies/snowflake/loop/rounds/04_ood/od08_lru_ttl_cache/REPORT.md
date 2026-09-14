# od08 LRU/TTL/Two-Tier Cache — report

## Summary
经典 LC 146 LRU Cache 打底 → 加 TTL 过期（半开区间，过期腾出的空间优先于 LRU 淘汰）→ 一个
本仓库重建的双层 hot/cold 缓存（命中冷层就自动升级，热层溢出就降级到冷层，冷层溢出才真正丢弃）。
对应 Snowflake warehouse cache 框架里"SSD 热层 + 更大冷层"的产品形状。

## Sources & confidence
Part1 **HIGH**（LC 146 原题，多处独立确认曾用于电面）；"Snowflake 反复问 LRU"这个论断本身
**LOW-MED**（staffengprep/interviewchamp/techprep 三个 prep 站用几乎相同措辞描述"warehouse
micro-partition cache"框架，但均无一手候选人日期）；TTL 扩展是通用 LeetCode Discuss 帖子里的
常见追问，未标注 Snowflake；Part3 双层设计**明确标注重建**——来源没有给出 promotion/demotion
的具体规则，本题选择"任意一次命中冷层就立即升级"这个最简单策略并在 problem.md 的变体一节写明
这是本仓库的设计选择，不是面试官原话。

## Approach by part
1. 内部 `_LRUStore`（`OrderedDict` 包一层）同时给三个类复用：`get`/`set_mru` 做 O(1)
   MRU-touch，`pop_lru` 做 O(1) 淘汰，`remove` 做 O(1) 删除——LRUCache 本身只是一层薄封装。
2. `TTLCache` 存 `(value, expire_at)`；`get` 先查是否过期（`now >= expire_at`），过期则惰性
   删除并返回 -1。容量淘汰时**先扫一遍找已过期的条目**优先删除，找不到才退回标准 LRU 淘汰——
   这个顺序是 problem.md 明确要求的："过期是免费腾出来的空间，不应该逼着系统提前淘汰一个仍然
   有效的条目"。
3. `TwoTierCache` 是两个独立的 `_LRUStore`：`get` 命中冷层触发"升级"（从冷层移除、插入热层
   MRU，若热层因此溢出则把热层 LRU 端降级到冷层，若冷层又因此溢出则彻底丢弃冷层 LRU 端）；
   `put` 对已在冷层的 key 走同样的升级链路，全新 key 直接进热层——升级/降级/丢弃三种结果共享
   同一段 `_insert_hot`/`_insert_cold` 代码，不是三份重复逻辑。

## Pitfalls hidden tests target
- `get`/`put` 命中都要标记 MRU，不只是"读"或"改值"不算访问
- TTL 半开区间：`now == expire_at` 算过期，`now == expire_at - 1` 仍有效
- 容量淘汰要区分"淘汰未过期条目（纯 LRU）"与"过期条目本来就该被清理"两种不同原因——即使两个
  worked example（2a/2b）的最终输出形式相同，测试文件用独立的构造分别验证淘汰的真正原因
  （problem.md 里也明确写出这条区分，不靠输出反推）
- 同一个 key 重复 `put`：完全覆盖旧的值和过期时间，不是取更晚的那个
- 双层缓存里一个 key 永远不会同时出现在热层和冷层——升级/降级都是"先移除再插入"
- `hot_capacity=0`：新写入立即被降级到冷层（等价于所有条目从一开始就只能活在冷层）；
  `cold_capacity` 也是 0 时彻底不保留任何条目

## Complexity & measured cost
三个类的核心操作都是 O(1) 均摊（`OrderedDict` 的 `move_to_end`/`popitem` 均为 O(1)）；
`TTLCache` 的"找任意一个过期条目"是 O(容量)，但只在每次 `put` 导致溢出时触发最多一次，容量本身
在 perf 测试里选得较小（100），10 万次操作 well under 2s / 256MB（LRU 与 TTL 两个 part 各自
独立测过）。

## Test inventory
22 tests — part1: 8（含 1 io、1 fmt、1 perf）· part2: 7（含 1 io、1 perf）· part3: 7（含 1 io）；
edge 12 · fmt 1 · io 3 · perf 2。

## Skills exercised
S12 缓存与淘汰（LRU/TTL/多级）· S09 类设计先定 API 契约（半开区间、升级/降级规则要主动写清楚，
不留给面试官猜）· S10（间接，并发追问层面讨论锁粒度与分片）
