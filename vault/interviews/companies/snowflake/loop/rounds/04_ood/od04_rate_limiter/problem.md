# od04 · Rate Limiter — sliding window, multi-rule FIFO queueing, thread-safe try_acquire

**类型：** onsite 单规则滑窗（VO）+ 电面多规则排队（PS）· 45–60 min · 3 part + 追问
**最近：** 2026-08 · **置信度：** MED（见文末）

## 背景
限流器在 Snowflake 的面试池里出现两个变体：onsite 版是"单规则滑动窗口"，函数/类形状都行；电面版
明确要求"排队 + 多规则同时满足 + 线程安全"，是更贴近"分布式限流"这条 D05 系统设计主题的编码版
投影。本题把两个变体合并成一道 3-part 的递进题：先写最简单的单规则滑窗，再升级成多规则排队
FIFO 模拟，最后把排队版本包成一个线程安全的类。

## API 契约（英文签名）
```python
def accept_requests(request_times: list[int], limit: int, window_seconds: int) -> list[bool]: ...

class RateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None: ...
    def allow(self, t: int) -> bool: ...          # same semantics as accept_requests, streaming

def simulate_rate_limiter(
    requests: list[tuple[int, int]],   # (arrival_time, success_flag)
    rules: list[tuple[int, int]],      # (limit, window_seconds) per rule, ALL must hold
) -> list[int]: ...                    # actual start time each request was handled at

class MultiRuleRateLimiter:
    def __init__(self, rules: list[tuple[int, int]]) -> None: ...
    def try_acquire(self, arrival_time: int) -> int: ...  # returns actual start time
```

## 规则

### Part 1 — 单规则滑动窗口
半开区间 `(t - window_seconds, t]`：`accept_requests` 按输入顺序（时间戳非递减）依次处理每个
请求，若过去窗口内已被接受的请求数 `< limit` 就接受（记入窗口），否则拒绝（**被拒绝的请求不占
用窗口名额**——这是本题反复强调的一条，很多候选人会误把拒绝的请求也计入窗口计数）。`RateLimiter`
类是同一逻辑的流式封装：`allow(t)` 等价于把 `t` 追加到 `accept_requests` 的输入流并只看这一个
的结果，内部用一个 `deque` 维护"当前窗口内已接受的时间戳"，均摊 O(1)。

### Part 2 — 多规则排队 FIFO 模拟
`simulate_rate_limiter(requests, rules)` 处理一个**有限的 FIFO 请求流**，每个请求是
`(arrival_time, success_flag)`。所有 `rules` 必须**同时**有余量才能"执行"一个请求：某条规则
`(limit, window)` 允许在 `(t - window, t]` 内至多 `limit` 次**成功**执行。请求按 FIFO 顺序**逐个
原子地**处理（不能乱序、不能并行处理同一个流）：
- 每个请求的"实际开始时间"是**不早于它的 `arrival_time`、也不早于前一个请求的实际开始时间**
  （FIFO——后到的请求不能抢在先到的请求前面处理）、且**所有规则同时有余量**的最早整数时刻。
- 若 `success_flag == 1`："执行"这个请求会真正占用每条规则的一个名额（计入各自的滑动窗口）。
- 若 `success_flag == 0`："失败的处理器等待名额，但不消耗名额"——它仍然要按 FIFO 顺序找到一个
  "此刻所有规则都满足"的时刻才算"轮到它"，但**不占用**任何规则的窗口名额（不影响后续请求的
  限流判断）。
- 返回值是每个请求的实际开始时间列表，顺序与输入 `requests` 一致。

来源原文例子（全部 `success_flag=1`）：`requests=[(0,1),(1,1),(2,1),(3,1),(4,1)]`，
`rules=[(2,5)]` → `[0, 1, 5, 6, 10]`（单规则 `limit=2, window=5`：前两个请求 t=0,1 直接通过；
第三个请求 arrival=2 时窗口 `(−3,2]` 内已有 2 个成功记录，客满，要等到 t=5 时窗口 `(0,5]`
内只剩 1 个成功记录（t=1 那次的窗口边界 `t-5<=1` 已经滑出）才有名额；以此类推）。

### Part 3 — 线程安全的 `try_acquire`
```python
class MultiRuleRateLimiter:
    def __init__(self, rules: list[tuple[int, int]]) -> None: ...
    def try_acquire(self, arrival_time: int) -> int: ...
```
把 Part2 的"多规则同时满足"逻辑包成一个可以被多线程并发调用的类：`try_acquire(arrival_time)`
永远"成功"（不像 `simulate_rate_limiter` 有 `success_flag`），返回它被实际许可执行的时间，并
立即在所有规则里记下这次占用。多个线程可能同时调用 `try_acquire`；要求：
- 任意时刻，回看任何一条规则在其滑动窗口内被 `try_acquire` 记录的许可次数，永远不超过该规则的
  `limit`（不会有两个线程同时"确认有名额"并都占用了同一个名额——check-then-act 必须原子）。
- 不丢许可：所有线程提交的 `try_acquire` 调用最终都必须拿到一个返回时刻（不会永久阻塞/丢失）。

## Worked examples

**例 1（Part1，`accept_requests`）**
```
accept_requests([1, 2, 3, 4, 7], limit=3, window_seconds=5)
```
→ `[True, True, True, False, True]`
（t=4 时窗口 `(-1,4]` 内已有 3 个接受(1,2,3)，客满 → 拒绝，且这次拒绝不占名额；t=7 时窗口
`(2,7]` 内只有 t=3,4 两个接受（t=1,2 已滑出窗口，t=4 那次虽然被拒绝但从未占用名额，不计入）→
未满 → 接受。）

**例 2（Part2，来源原文例子）**
```
simulate_rate_limiter(
    requests=[(0,1), (1,1), (2,1), (3,1), (4,1)],
    rules=[(2, 5)],
)
```
→ `[0, 1, 5, 6, 10]`

**例 3（Part2，`success_flag=0` 要等名额但不占名额）**
```
simulate_rate_limiter(
    requests=[(0,1), (1,0), (2,1)],
    rules=[(1, 5)],
)
```
→ `[0, 5, 5]`
（规则 `limit=1, window=5` 只有一个"名额"。第一个请求 `(0,1)` 立刻在 t=0 拿到名额并占用它（窗口
`(-5,0]` 记满）。第二个请求 `(1,0)`：FIFO 最早不早于 `max(arrival=1, 前一个开始时间=0)=1`；但
t=1 时名额仍被 t=0 那次占用（`0 > 1-5`），必须等到 t=5（`0 > 5-5=0` 为假，名额才滑出窗口）才算
"轮到它"——但因为 `success_flag=0`，它只是**等到了**名额空出的那一刻，并不真的占用，窗口状态
不变。第三个请求 `(2,1)`：FIFO 最早不早于 `max(arrival=2, 前一个开始时间=5)=5`；t=5 时名额仍是
空的（第二个请求没占用它）→ 立刻在 t=5 拿到并占用。三个请求的开始时间分别是 0、5、5——第二、第三
个请求开始时间相同，这是允许的：`success_flag=0` 的请求"经过"了 t=5 但没有留下占用记录。）

## `main()` 命令流

**Part1** 首行之后：
```
LIMIT <limit>
WINDOW <window_seconds>
<t1>
<t2>
...
```
每个 `<t>` 行驱动一次 `RateLimiter.allow(t)`（同一个实例，流式），输出对应一行 `True`/`False`。

**Part2** 首行之后：
```
RULES <limit1>:<window1>[,<limit2>:<window2>...]
<t1>:<f1>
<t2>:<f2>
...
```
一次性调用 `simulate_rate_limiter`，按输入顺序逐行输出每个请求的实际开始时间（整数）。

**Part3** 首行之后：
```
RULES <limit1>:<window1>[,<limit2>:<window2>...]
<t1>
<t2>
...
```
每个 `<t>` 行驱动一次 `MultiRuleRateLimiter.try_acquire(t)`（同一个实例，单线程顺序调用——并发
保证由 `test_od04.py` 直接用多线程对类本身验证，不通过这个行驱动接口），输出对应一行开始时间
（整数）。

## 边界清单
- 空请求列表 → 空输出列表（两个函数都要处理）
- `limit=0`：任何请求都被拒绝（Part1）/ 永远等不到名额，测试只验证很短的时间范围内确实一直拒绝
  /未被处理，不构造真正的死等
- 窗口边界严格按半开区间：`t - window_seconds` 本身**不算**在窗口内（例：`window=5`，t=0 的记录
  在 `t'=5` 时的窗口 `(0,5]` 里**不算**，因为 `0 <= t'-window`）
- 被拒绝的请求（Part1）/ `success_flag=0` 的请求（Part2）永远不占用窗口名额
- 多规则里某一条规则永远是瓶颈（另一条 `limit` 很大/`window` 很小），结果应该和"只看瓶颈规则"
  的单规则结果一致——用于交叉验证 Part2 实现没有漏掉某条规则
- FIFO 顺序：即使某个更晚到达的请求本可以更早满足所有规则，也不能插队到更早到达、仍在等待的
  请求前面
- 并发 `try_acquire`：任意规则的滑动窗口内被记录的许可数不超过其 `limit`，用多线程 + 事后扫描
  每条规则的许可时间戳验证

## 并发追问
1. "`try_acquire` 用一把大锁包住'检查所有规则 + 记录许可'这一整段，性能够吗？如果规则很多、
   调用很频繁怎么优化？" —— 期望候选人讨论按规则分片加锁很难（因为需要所有规则同时满足才能
   决策，天然是一个跨规则的原子操作），更现实的优化方向是缩小临界区（先在锁外算出候选时间，
   进锁后只做一次快速的"仍然满足吗"复核）而不是彻底去掉锁。
2. "如果两个线程的 `arrival_time` 相同，谁先被处理？" —— 期望候选人指出"先调用先处理"（用锁的
   获取顺序天然定义 FIFO），而不是试图用 `arrival_time` 本身排序两个并发调用（无法区分同时到达
   的调用之间的真实顺序）。
3. "生产环境里这种全局强一致限流器在多区域部署下会有什么问题？" —— 期望候选人联系到
   `catalog/CATALOG.md` sd07 分布式限流器的追问：跨区域同步的延迟/热点 key，讨论 token bucket +
   本地缓存 + 定期同步的降级方案，是一个开放式的延伸讨论,不要求现场实现。

## 变体
- onsite 版本（`accept_requests`）是纯函数/流式类，电面版本（`simulate_rate_limiter`）明确要求
  排队与线程安全——同一个"限流器"主题在不同轮次里被问出不同侧重，练习时两个都要覆盖。
- 一个变体用 token bucket 而非滑动窗口日志实现，语义上对"突发流量"更宽松；本题不要求实现，只
  在并发追问 1 里提及作为优化方向的类比。

## 来源与置信度
- https://www.fastprep.io/problems/snowflake-sliding-window-rate-limiter （Medium, Fulltime
  Onsite；`acceptRequests(requestTimes, limit, windowSeconds)`，例子
  `[1,2,3,4,7], limit=3, window=5 -> [T,T,T,F,T]`）
- https://www.fastprep.io/problems/snowflake-queued-multi-rule-rate-limiter （Medium, Phone
  Screen；"serialized, thread-safe... Handlers execute atomically in FIFO order. Failed handlers
  wait for capacity but consume no slots."，例子
  `requests=[[0,1],[1,1],[2,1],[3,1],[4,1]], rules=[[2,5]] -> [0,1,5,6,10]`）
- 主题级印证（LOW-MED，不单独计分）：tryexponent.com、algo.monster 的 Snowflake 面试指南提到
  "distributed rate limiter"是常见设计话题
- `catalog/raw/ood.md` #4、`catalog/CATALOG.md` Table B od04 行；置信度 **MED**：两个 fastprep
  页面各自独立、给出精确例子，但均为单一聚合站来源，无一手候选人挂经交叉。

## 考什么
S09 类设计先定 API 契约（`RateLimiter`/`MultiRuleRateLimiter` 的状态边界）· S10 并发正确性
（跨规则原子 check-then-act）· S06（滑窗与事件流，与 Stripe ps01/cd06 同族）· S20 自测试
