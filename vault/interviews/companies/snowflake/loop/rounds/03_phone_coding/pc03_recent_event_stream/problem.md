# pc03 · Recent Event Stream — sliding window over the most recent m events, count/top queries

**类型：** phone screen（40 min）· 2 part 递进 · 滑窗与事件流（deque + 计数哈希 + 最频 key）
**最近：** 2026-08 · **置信度：** MED（Part1）/ 重建（Part2，见文末）

## 背景
Snowflake 电面池里两个独立聚合站（fastprep、prachub）描述了同一道题："只保留最近 m 条事件"的
滑窗，支持记录、按时间过滤计数、查最频 key 三种操作——这和 Stripe 题库里 ps01/cd06 是同一族
（S06：滑窗与事件流），只是保留策略不是"按时间窗口"而是"按事件条数"。本题 Part1 还原这个计数式
滑窗，Part2（重建）把保留策略换成更常见的"按时间窗口"（类似 od04 的限流器），练的是同一套
deque+计数哈希骨架在两种窗口语义下如何分别维护。

## API 契约（英文签名）
```python
class RecentEventStream:
    def __init__(self, m: int) -> None: ...
    def record(self, ts: int, key: str) -> None: ...
    def count(self, ts: int) -> int: ...   # distinct keys in the retained window with timestamp < ts
    def top(self) -> str: ...              # most frequent key in the retained window, lex tie-break

def process_recent_event_stream(operations: list[tuple], m: int) -> list[str]: ...

class RecentEventStreamByTime:
    def __init__(self, window_seconds: int) -> None: ...
    def record(self, ts: int, key: str) -> None: ...
    def count(self, ts: int) -> int: ...
    def top(self) -> str: ...

def process_recent_event_stream_by_time(operations: list[tuple], window_seconds: int) -> list[str]: ...
```
`operations` 是一个按到达顺序排列的操作列表，每项是 `("record", ts, key)` / `("count", ts)` /
`("top",)`；输入流假定 `ts` 非递减（和本题库其它流式题——比如 od04 限流器——同样的假设）。

## 规则

### Part 1 — 按条数保留的滑窗（来源原文机制）
`RecentEventStream(m)` 只保留**最近记录的 m 条事件**，不管它们的时间戳跨度有多大——第 `m+1`
次 `record` 会把最老的那条事件挤出窗口（不管挤出的那条时间戳是多久以前）。
- `record(ts, key)`：记录一条事件，若当前窗口已满则先淘汰最老的一条。
- `count(ts)`：返回**当前保留窗口内**、时间戳**严格早于** `ts` 的事件里有多少个**不同的 key**
  （不是"多少条事件"，是"多少个不同的 key"）。
- `top()`：返回当前保留窗口内出现次数最多的 key；并列时取**字典序最小**的那个。窗口为空时返回
  空字符串 `""`（不抛异常——查询一个还没记录过任何事件的流是正常状态，不是错误）。

`process_recent_event_stream(operations, m)` 是同一逻辑的批处理封装：按顺序执行
`operations`，`record` 不产生输出，`count`/`top` 各产生一行字符串输出。

### Part 2 — 按时间窗口保留（重建）
`RecentEventStreamByTime(window_seconds)` 换一种保留策略：保留**时间戳落在
`(最近一次 record 的 ts − window_seconds, 最近一次 record 的 ts]` 半开区间内**的所有事件（和
od04 限流器 `RateLimiter` 完全一样的边界写法），**不限制条数**——窗口内可能有任意多条事件，只要
它们的时间戳够新。`count`/`top` 的语义与 Part1 完全一样，只是"当前保留窗口"的定义换了。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1（Part1，还原自来源原文例子结构，`m=3`）**
```python
ops = [
    ("record", 1, "a"),
    ("record", 2, "b"),
    ("record", 3, "a"),
    ("count", 10),
    ("top",),
    ("record", 4, "a"),
    ("count", 10),
    ("top",),
]
process_recent_event_stream(ops, m=3)
```
→ `["2", "a", "2", "a"]`（与来源原文摘录的输出序列 `m=3, ops -> ["2","a","2","a"]` 完全一致：
第一次 `count(10)` 时窗口是 `(1,a),(2,b),(3,a)`，不同 key 有 `{a,b}` = 2 个；`top()` 时 `a`
出现 2 次胜出；`record(4,a)` 挤掉最老的 `(1,a)`，窗口变成 `(2,b),(3,a),(4,a)`，不同 key 仍是
`{a,b}` = 2 个，`top()` 里 `a` 出现 2 次仍然胜出）。

**例 2（Part1，按条数淘汰会挤掉"还很新"的事件——这是和 Part2 分岔的关键）**
```python
stream = RecentEventStream(m=2)
stream.record(1, "a"); stream.record(2, "b"); stream.record(3, "c")
stream.top()
```
→ `"b"`（窗口容量 2，第三次 `record` 把最老的 `(1,a)` 挤出，剩下 `(2,b),(3,c)`，两者各出现 1
次，`top()` 按字典序取 `"b"`）。

**例 3（Part2，时间窗口保留，同一组时间戳给出不同的淘汰结果）**
```python
ops = [
    ("record", 0, "a"),
    ("record", 1, "b"),
    ("record", 5, "c"),
    ("count", 10),
    ("top",),
]
process_recent_event_stream_by_time(ops, window_seconds=5)
```
→ `["2", "b"]`（`record(5,c)` 时窗口边界是 `(5-5, 5] = (0, 5]`，`ts=0` 的事件 `a` 因为
`0 <= 0` 被淘汰出窗口——即使按条数算它只是"三条里最老的一条"，和 Part1 的行为可能不同；保留窗口
变成 `(1,b),(5,c)`，`count(10)` 内不同 key `{b,c}` = 2 个，`top()` 里 `b`、`c` 各出现 1 次，
按字典序取 `"b"`）。

## `main()` 命令流
**Part1** 首行之后：`M <m>`，然后每行一条操作：`RECORD <ts> <key>` / `COUNT <ts>` / `TOP`。
**Part2** 首行之后：`WINDOW <window_seconds>`，操作行格式与 Part1 相同。
两个 part 的输出都是每条 `COUNT`/`TOP` 操作各一行；`RECORD` 不产生输出行。

## 边界清单
- 空操作序列（只有 `M`/`WINDOW` 行，没有任何操作）→ 空输出
- 窗口为空时调用 `top()` → 返回 `""`，不抛异常；`count(ts)` → 返回 `0`
- `count(ts)` 是"严格早于"：窗口内恰好有一条事件 `ts` 与查询的 `ts` 相等，不计入结果（例3 的
  `count(10)` 场景可以改造成边界测试：把 `10` 换成窗口内某条事件的确切时间戳，验证不计入）
- `top()` 的并列 tie-break 是字典序最小，不是"最早/最晚出现的那个 key"（例2 专门验证这一点）
- Part1 按**条数**淘汰、Part2 按**时间**淘汰——同一组 `(ts, key)` 记录序列在两种策略下可能保留
  不同的事件集合（例3 展示这种分岔：如果 Part2 的窗口足够宽，`m=3` 的条数窗口反而会更早淘汰掉
  仍然"没那么老"的事件）
- `window_seconds=0`（Part2）：只保留和最近一次 `record` 时间戳完全相同的事件；`m=1`（Part1）：
  窗口永远只有最后一条记录的事件
- 一次 `record` 之后立刻查询 `count`/`top`，不需要等待任何"下一个事件到达"才刷新窗口（和 od04
  限流器的"惰性淘汰、在下一次操作时才清理过期记录"是同一种实现哲学）

## 追问
1. "如果 `count(ts)` 被非常频繁地调用、且窗口容量 `m` 很大，你的实现复杂度会不会退化？"——期望
   候选人指出当前实现是每次 `count` 都线性扫描窗口（`O(m)`），如果 `m` 很大且 `count` 调用频率
   远高于 `record`，可以考虑按时间戳排序的辅助结构（比如按 key 维护有序时间戳列表 + 二分）换
   查询延迟，但要讨论这个优化在"窗口本身就有淘汰"的场景下维护成本是否划算。
2. "Part2 的时间窗口如果要支持''重放乱序到达的事件''（`ts` 不再保证非递减）呢？"——期望候选人
   意识到当前"惰性淘汰只看队首"的实现依赖非递减假设，乱序输入下需要换成更重的结构（比如按 key
   分别维护、或者干脆不淘汰只在查询时过滤），属于开放式讨论，不要求现场实现。
3. "生产环境里这种''最近事件流''通常还需要支持多个并发写入者，你的 `record` 需要加锁吗？"——
   联系 od04 限流器的并发追问，期望候选人讨论"check-then-act"式的窗口淘汰 + 计数更新需要整体
   原子，不是简单地给 deque 套一把锁就完事（还要保护 Counter 的同步更新）。

## 变体
- 来源原文用的是 `processRecentEvents(operations, m) -> String[]` 单一批处理签名；本题额外
  拆出一个显式的 `RecentEventStream` 类，方便 Part2 复用同一套接口只换保留策略，同时保留
  批处理封装函数以兼容原始题面形状。
- Part2 的时间窗口变体没有独立的一手或聚合站来源，是本题按"滑窗题最常见的另一种保留策略"
  重建的延伸，练习目的是让候选人对比两种窗口语义在实现上的差异（条数淘汰 vs 时间淘汰）。

## 来源与置信度
- https://www.fastprep.io/problems/snowflake-recent-event-stream-queries （Phone Screen,
  Medium, Hash-Table/Queue，最近 2026-08）："sliding window of `m` most-recent events; ops
  `record ts key`, `count ts` (distinct keys strictly before ts), `top` (most frequent key, lex
  tie-break)."`processRecentEvents(operations, m) -> String[]`；例子 `m=3, ops ->
  ["2","a","2","a"]`（原文只给出输出片段，完整操作序列由本题按语义重建，问题描述本身逐字取自
  原文）。
- https://prachub.com/coding-questions/query-unique-and-most-frequent-keys-in-a-recent-event-window
  （Medium, Technical Screen，"Last Updated" 2026-08-29）："Process a timestamp-ordered event
  stream while retaining only its most recent m arrivals... most frequent qualifying key,
  lexicographic tie-breaking."——与 fastprep 描述的规则完全一致，独立确认"按条数保留"这条核心
  机制。
- `catalog/raw/coding_phone_onsite.md` #13、`catalog/CATALOG.md` Table A pc03 行；置信度
  **MED**（Part1）：两个独立结构化来源在核心规则上高度吻合，但均未给出完整的操作序列，worked
  example 的具体输入是重建的（输出片段是原文的）。Part2 的时间窗口变体**无来源**，标注为重建，
  不并入上述评级。

## 考什么
S06 滑窗与事件流（deque + 计数哈希 + 最频 key）· S08 复杂度权衡（O(m) 线性扫描 vs 辅助索引）
