# od12 Top K Book Sales — report

## Summary
累计销量榜：Part 1 正确性（累加 + 按总量降序/书名升序取前 k）→ Part 2 懒失效堆
（lazy-invalidation max-heap，reconstructed 的效率要求）→ Part 3 退货（负数增量，批量
all-or-nothing 校验）+ `rank()`（reconstructed）。唯一来源是 TrueInterview 同步清单的标题级
预览（"累加销量并即时返回前 k"），效率/退货/排名细节全部重建。

## Sources & confidence
MED：kevin-2023-code/Tech-Interview-Questions（TrueInterview 同步）第 47 题 "Top K Book
Sales"，LLD，2026-02 报告，正文付费。机制上与 LeetCode 1244 "Design A Leaderboard" 同构（未见
来源明确引用该题号，仅作背景说明）。

## Approach by part
1. `best_sellers` 先把同一次调用里对同一本书的多次增量合并成一个净变化量，再一次性应用，避免
   对同一本书重复 push 堆记录、也避免"批量校验"（Part3）出现漏判。
2. 懒失效堆：`(-total, name)` 记录只 push 不删；查询时不断 pop，用 `self._totals` 校验记录是
   否仍然有效，无效的记录永久丢弃，有效的记录（凑够 k 个）弹出后原样塞回堆里。均摊下来每条记
   录一生只被"验证"一次，N 次更新 + Q 次查询总代价 O((N + Q·k)·log N)，不随书籍规模退化为对全
   量排序。
3. Part3 的退货校验做在应用之前：先按书名合并本次调用的净变化量，检查是否会导致任何一本书总
   量为负，任何一本触发就整批拒绝（`ValueError`，不留副作用）；`rank()` 走独立的简单全量排序
   路径，因为效率要求（Part2）明确只落在 `best_sellers` 这条被标记为高频的路径上。

## Pitfalls hidden tests target
- `k<=0` 返回空；`k` 超过书籍数返回全部
- 同一调用内同一本书出现多次：先合并增量再应用一次
- 总销量并列按书名升序打平，`rank()` 与 `best_sellers()` 用同一套排序键
- 懒失效堆里的过期记录不能污染查询结果——随机操作序列与朴素全量排序模型交叉验证
- Part3 批量退货必须整批拒绝且不产生任何副作用（哪怕批次里其他书的净变化本身合法）
- 退货减到恰好 0 允许，减到负数才拒绝
- `rank()` 对未知书名抛 `KeyError`

## Complexity & measured cost
`best_sellers` 更新 O(log n)（堆 push）；查询 O((验证到的过期记录数 + k)·log n)，均摊
O((N+Qk) log N)。`rank()` O(n log n)（全量排序，明确不是本题优化目标）。10 万次更新 + 1 万次
查询的端到端脚本实测远低于 2s 预算（独立压测约 0.18s，脚本预算含解释器与 IO 开销）。

## Test inventory
20 tests — part1 7 · part2 3（含 1 perf、1 随机交叉验证）· part3 6；edge 10 · perf 1 · io 2 ·
fmt 1。

## Skills exercised
S09 类设计先定契约（批量退货的原子性、`k<=0`/超量的边界）· 懒失效堆是"高效 TopK 但不支持高效
任意删除"这类问题的标准解法（与 LC 1244/2349 同族）· 先测哪条路径热、再决定优化哪条的工程判断
（`rank()` vs `best_sellers()`）。
