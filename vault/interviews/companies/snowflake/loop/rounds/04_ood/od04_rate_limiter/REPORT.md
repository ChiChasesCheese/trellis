# od04 Rate Limiter — report

## Summary
把 Snowflake 面试池里两个独立的限流器变体合并成一道 3-part 递进题：onsite 的单规则滑动窗口
（`accept_requests`/`RateLimiter.allow`）→ 电面的多规则 FIFO 排队模拟（`simulate_rate_limiter`，
显式区分"成功执行"与"失败但仍占 FIFO 顺序"的请求）→ 把多规则逻辑包成线程安全的
`MultiRuleRateLimiter.try_acquire`。三部分共享同一个核心算法（`_advance`：把候选时间推进到
"所有规则同时有余量"的最早时刻）。

## Sources & confidence
MED——两个独立 fastprep 页面，各自给出精确的 worked example：onsite 版
`[1,2,3,4,7], limit=3, window=5 -> [T,T,T,F,T]`；电面版
`requests=[[0,1],[1,1],[2,1],[3,1],[4,1]], rules=[[2,5]] -> [0,1,5,6,10]`（problem.md 例2 逐步
手算验证，`_advance` 算法与其完全吻合）。两个来源均为单一聚合站（无一手候选人挂经交叉），主题级
印证（"distributed rate limiter"是常见 Snowflake 设计话题）来自 tryexponent/algo.monster 的
通用指南，LOW-MED，不单独计分。

## Approach by part
1. `RateLimiter` 用一个 `deque` 维护当前窗口内被接受的时间戳；每次 `allow(t)` 先从队首弹出
   `ts <= t - window` 的过期记录（半开区间 `(t-window, t]` 的精确边界），再判断 `len(队列) <
   limit`。被拒绝的请求完全不触碰队列，天然满足"拒绝不占名额"。
2. `_advance(t, rules, granted_per_rule)` 是 Part2/Part3 共享的核心：对每条规则先购物式地弹出
   过期记录，若剩余数量 `>= limit` 就算出"最老的那条超额记录何时过期"（`granted[len-limit] +
   window`）并把候选时间推到那一刻，重复整个循环直到一轮下来没有任何规则再推进时间为止（因为
   推进某条规则可能让另一条规则的过期计算发生变化，必须整体收敛）。这个不变量成立：只有确认
   "有余量"才会真正 `append`，所以每条规则的 `granted` deque 长度永远不超过它自己的 `limit`，
   索引开销与总请求数无关。
3. `simulate_rate_limiter` 在此基础上加 FIFO 约束（`t = max(arrival, 上一个请求的实际开始
   时间)`）和 `success_flag`：只有 `flag=1` 才真正 `append` 占用名额，`flag=0` 只是"等到了"那个
   时刻但不留下占用记录（例3 逐步手算验证）。
4. `MultiRuleRateLimiter.try_acquire` 是同一套逻辑的有状态、线程安全封装：把"读取 `prev_start` →
   `_advance` → 写回 `prev_start` → 记录占用"整段包在一把锁里，保证并发调用下"检查有余量"和
   "占用名额"是一个原子操作。

## Pitfalls hidden tests target
- 半开区间的精确边界：`t - window` 本身不算在窗口内（`allow(0)` 后 `allow(window)` 必须重新
  接受）
- 被拒绝/`success_flag=0` 的请求永远不占用名额，即使它们仍然要"等到"规则满足的那一刻
- FIFO：即使某个更晚到达的请求自身规则立刻满足，也不能早于前一个仍在等待的请求的开始时间
- 多规则里瓶颈规则应该独立决定结果——加一条极宽松的规则不改变输出（交叉验证没有漏掉某条规则）
- 并发 `try_acquire`：任意一个"以某次许可结束时刻为右端点、宽度为 window"的窗口内，许可数不超
  过 `limit`（用排序后的许可时间戳逐一验证，而不是抽样断言）
- `limit=0` 永远拒绝；空请求列表返回空列表

## Complexity & measured cost
`allow`/`try_acquire` 均摊 O(limit)（deque 长度上限即为 `limit`，与历史请求总数无关）。10 万条
混合请求（单规则）通过 `run_script` 实测 well under 2s / 256MB。

## Test inventory
18 tests — part1: 8（含 1 io、1 fmt）· part2: 7（含 1 io、1 perf）· part3: 3；edge 8 · fmt 1 ·
io 2 · perf 1。

## Skills exercised
S09 类设计先定 API 契约（`success_flag` 语义、`try_acquire` 无 flag 恒成功的差异要讲清楚）· S10
并发正确性（跨规则原子 check-then-act）· S06 滑窗与事件流（与 Stripe ps01/cd06 同族）· S20
自测试
