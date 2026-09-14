# pc03 Recent Event Stream — report

## Summary
把 Snowflake 电面池的"最近 m 条事件"滑窗题（两个独立聚合站描述同一机制）做成 2-part：Part1
还原原文的按条数保留策略（`record`/`count`/`top`），Part2（重建）把保留策略换成 od04 限流器同款
的半开时间窗口，练的是同一套 deque+计数哈希骨架在两种窗口语义下如何分别维护淘汰逻辑。

## Sources & confidence
MED（Part1）——fastprep 与 prachub 两个独立结构化来源在"按条数保留 + record/count/top 三种操作 +
count 是distinct key 数、strictly before + top 按频率、字典序 tie-break"这组规则上完全一致；
原文只给出输出片段 `m=3, ops -> ["2","a","2","a"]`，完整操作序列由本题按语义重建后用
`solution.py` 验证，重建的序列产出与原文输出片段逐字符匹配。Part2 的时间窗口变体无来源，标注为
重建，不并入评级。

## Approach by part
1. `RecentEventStream` 用一个 `deque` 保存窗口内的 `(ts, key)`，一个 `Counter` 同步维护窗口内
   `key -> 出现次数`；`record` 超过容量 `m` 时弹出队首并同步递减计数（计数归零就整个删掉这个
   key，保证 `top()` 不会把已经出局的 key 当成候选）。`count(ts)` 对窗口做一次线性扫描（窗口
   容量被 `m` 卡死，与历史事件总数无关，这是这题预期的电面级答案，不需要更复杂的索引）。
2. `RecentEventStreamByTime` 的淘汰条件从"队列长度超过 m"换成"队首时间戳落出
   `(最新ts − window_seconds, 最新ts]`"，和 od04 `RateLimiter.allow` 用完全一样的半开区间写法
   （`<=` 判定），且**先淘汰、再追加新事件**——这个顺序在 `window_seconds=0` 时是关键：如果反过来
   先追加再淘汰，新加入的事件会立刻拿自己的时间戳判定"过期"，把自己刚插入就淘汰掉，这是实现里
   最容易踩的一个顺序陷阱。
3. 两个变体的 `count`/`top` 逻辑完全共享（都是对当前窗口内容的查询），差异只在 `record` 里
   "什么时候淘汰"这一处，体现"同一套骨架、换一处淘汰条件就分岔"的练习点。

## Pitfalls hidden tests target
- `top()` 的并列 tie-break 是字典序最小，不是"最近插入"或"最早插入"（`test_top_tie_break_is_
  lexicographic_not_recency` 用两种插入顺序交叉验证）
- `count(ts)` 是严格早于，窗口内恰好有一条事件时间戳等于查询 `ts` 时不计入
- `record` 必须先淘汰再追加：`window_seconds=0` 时如果顺序反了，新事件会淘汰自己
  （`test_window_zero_purges_even_same_timestamp_predecessors` 专门测这个边界）
- Part1 按条数、Part2 按时间——同一组记录喂给两个变体可能保留不同的事件集合
  （`test_count_vs_time_based_divergence_from_count_based`）
- 空窗口查询不抛异常：`top()` 返回 `""`，`count()` 返回 `0`

## Complexity & measured cost
`record` 均摊 `O(1)`（每个事件最多入队出队各一次）；`count`/`top` 均为 `O(窗口容量)`，与历史
事件总数无关。10 万条混合操作（`m=500`，约 70% record / 15% count / 15% top）纯函数耗时约
0.16s，通过 `run_script` 端到端实测 well under 2s / 256MB。

## Test inventory
17 tests — part1: 8（含 1 io、1 fmt）· part2: 6（含 1 io）；edge 10 · fmt 1 · io 2 · perf 1。

## Skills exercised
S06 滑窗与事件流（deque + 计数哈希 + 最频 key）· S08 复杂度权衡（O(m) 线性扫描 vs 辅助索引）
