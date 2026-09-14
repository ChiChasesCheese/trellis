# od04 · Rate Limiter：滑窗 → 多规则排队 → 线程安全，练的是"拒绝不占名额"这条反直觉规则

> [!tldr]
> - 这题考的是：单规则滑动窗口限流打底，升级成多规则同时满足 + FIFO 排队模拟，最后包成线程安全的类
> - 三步套路：Part 1 用一个 deque 维护窗口内已接受的时间戳 → Part 2 把"单规则判定"扩展成"反复推进时间直到所有规则同时有空位" → Part 3 把 Part 2 的核心逻辑包一把锁变成可并发调用的类
> - 最值得带走的一个模式：**被拒绝/失败的请求永远不占用窗口名额**——这是本题反复强调、也是最容易被无意识做错的一条规则

## 类设计先定契约
```python
def accept_requests(request_times, limit, window_seconds) -> list[bool]: ...

class RateLimiter:
    def __init__(self, limit, window_seconds) -> None: ...
    def allow(self, t: int) -> bool: ...          # 流式版本，与 accept_requests 语义相同

def simulate_rate_limiter(requests, rules) -> list[int]: ...   # requests: (arrival, success_flag)

class MultiRuleRateLimiter:
    def __init__(self, rules: list[tuple[int,int]]) -> None: ...
    def try_acquire(self, arrival_time: int) -> int: ...        # 永远"成功"，返回实际许可时刻
```
**不变量（写代码前先想清楚）**：
1. 窗口是半开区间 `(t-window, t]`——`t-window` 本身不算在窗口内。
2. 被拒绝的请求（Part 1）/ `success_flag=0` 的请求（Part 2）**永远不占用**窗口名额。
3. 多规则必须**同时**有余量才能执行；请求按 FIFO 顺序**逐个原子地**处理，后到的请求不能插队到更早
   仍在等待的请求前面。
4. `try_acquire` 永远"成功"，只是返回值可能比 `arrival_time` 晚——check-then-act（检查有余量 + 记录
   占用）必须是原子操作。

## 1. 题目在说什么（人话版）
Part 1：一个滑动窗口限流器，过去 `window_seconds` 秒内已接受的请求数超过 `limit` 就拒绝新请求。
Part 2：升级成多条规则必须同时满足，请求按到达顺序排队，"实际开始时间"取决于什么时候所有规则都有
空位；失败的请求（`success_flag=0`）只是"经过"了这个时刻，不真正占用名额。Part 3 把这套逻辑包成一个
线程安全的类，`try_acquire` 立即执行并占用名额。

三行小例子：
```
accept_requests([1,2,3,4,7], limit=3, window=5)
t=4时窗口(-1,4]内已有3个接受(1,2,3) -> 拒绝，不占名额
t=7时窗口(2,7]内只有3,4两个接受(1,2已滑出,4虽被拒绝但从未占用) -> 接受
结果：[True,True,True,False,True]
```

## 2. 读题：把文字变成模型
- **实体**：请求（到达时间、可选的成功标志）、规则（`limit`、`window_seconds`）。
- **输入长什么样**：`main()` 三种命令流分别对应三个 part（见 problem.md）。
- **输出要什么**：Part 1 每请求一个 `True`/`False`；Part 2/3 每请求一个"实际开始时间"整数。
- **状态**：每条规则一个 deque，记录"已被真正占用的时间戳"（Part 1 是唯一规则的简化版）。
- **一句话建模**：这是一个 **滑动窗口计数器**，Part 1 只有一条规则、直接判定；Part 2/3 是"不断把
  候选时间往后推，直到所有规则的窗口同时有空位"的一个收敛过程。

> [!note] 为什么选这个数据结构
> deque 天然适合"滑动窗口"——过期的时间戳从左边弹出，新的从右边追加,均摊 O(1)。多规则场景下，每条
> 规则的 deque **永远不会超过它自己的 `limit` 长度**（因为只有确认有空位之后才会真正 append 一条
> 记录），所以即使处理了海量请求，每条规则 deque 的长度上限也是 `limit`，查询/推进都很便宜。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **接口先行**：先把四个签名（`accept_requests`/`RateLimiter`/`simulate_rate_limiter`/
   `MultiRuleRateLimiter`）过一遍,注意 Part 2/3 的"实际开始时间"和 Part 1 的布尔判定是完全不同的
   返回形状。
2. **Part 1 最小可用**：`allow(t)` 先弹出窗口外过期的时间戳（`accepted[0] <= t - window`），再判断
   `len(accepted) < limit`——够就 append 并返回 True，不够返回 False（不 append）。
3. **Part 2 叠加**：写一个共用的 `_advance(t, rules, granted_per_rule)`：对每条规则，先弹出过期记录，
   如果当前记录数已达 `limit`，算出"最早一条记录滑出窗口的时刻"作为新的候选 `t`，重复直到一轮扫描
   里所有规则都不需要再推进。`simulate_rate_limiter` 对每个请求先算 `t=max(arrival, 上一个开始时间)`
   （FIFO 约束），再调 `_advance`，`success_flag=1` 才真正往每条规则的 deque 里 append。
4. **Part 3 叠加**：把 Part 2 的状态（`granted_per_rule`、`prev_start`）搬进类的字段，`try_acquire`
   整个方法用一把锁包住（算候选时间 + `_advance` + 记录占用），保证并发调用的原子性。
5. **收尾**：用来源给的官方例子（含 `success_flag=0` 的例子）逐步手算验证；`limit=0`、空请求列表、
   某条规则永远是瓶颈这几个边界过一遍。

## 4. 代码怎么组织
```
RateLimiter.allow(t) -> bool                       # Part1: 单规则滑窗判定
accept_requests(times, limit, window) -> list[bool] # Part1 的批量包装
_advance(t, rules, granted_per_rule) -> int         # Part2/3 共用：推进到所有规则同时有空位的时刻
simulate_rate_limiter(requests, rules) -> list[int]  # Part2: FIFO 逐个原子处理
MultiRuleRateLimiter.try_acquire(arrival_time) -> int # Part3: 加锁版本，永远成功
main(stdin, stdout)                                  # 解析三种命令流，分发
```
`_advance` 是 Part 2/3 唯一共享的核心逻辑——两者的区别只是"要不要真正记录占用"（`success_flag` 控制）
和"要不要加锁"，把这部分抽出来复用，能让面试官一眼看出 Part 3 只是 Part 2 加了锁，而不是重写了一遍。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
class RateLimiter:                              # Part1
    def __init__(self, limit, window_seconds):
        self.limit, self.window = limit, window_seconds
        self._accepted = deque()
    def allow(self, t):
        while self._accepted and self._accepted[0] <= t - self.window:
            self._accepted.popleft()             # 弹出滑出窗口的记录
        if len(self._accepted) < self.limit:
            self._accepted.append(t)              # 只有真正接受才占用名额
            return True
        return False                              # 拒绝不占名额

def _advance(t, rules, granted_per_rule):        # Part2/3 共用：推到所有规则同时有空位
    while True:
        advanced = False
        for (limit, window), granted in zip(rules, granted_per_rule):
            while granted and granted[0] <= t - window:
                granted.popleft()
            if len(granted) >= limit:              # 这条规则客满，算出最早腾出空位的时刻
                new_t = granted[len(granted) - limit] + window
                if new_t > t:
                    t, advanced = new_t, True
        if not advanced:
            return t

def simulate_rate_limiter(requests, rules):      # Part2: FIFO 逐个原子处理
    granted_per_rule = [deque() for _ in rules]
    prev_start, results = None, []
    for arrival, success_flag in requests:
        t = arrival if prev_start is None else max(arrival, prev_start)  # FIFO 不早于前一个
        t = _advance(t, rules, granted_per_rule)
        prev_start = t
        if success_flag:                          # 只有成功才真正占用名额
            for g in granted_per_rule:
                g.append(t)
        results.append(t)
    return results

class MultiRuleRateLimiter:                      # Part3: 加锁，永远"成功"
    def __init__(self, rules):
        self._rules, self._granted = list(rules), [deque() for _ in rules]
        self._prev_start, self._lock = None, threading.Lock()
    def try_acquire(self, arrival_time):
        with self._lock:                          # check-then-act 全程原子
            t = arrival_time if self._prev_start is None else max(arrival_time, self._prev_start)
            t = _advance(t, self._rules, self._granted)
            self._prev_start = t
            for g in self._granted:
                g.append(t)
            return t
```

## 6. 并发追问怎么答
- **大锁性能够不够，能不能按规则分片加锁**：不行——所有规则必须同时满足才能决策，这天然是一个跨
  规则的原子操作，按规则分片加锁会破坏"同时满足"的原子性。更现实的优化方向是缩小临界区：先在锁外
  尽量算出候选时间，进锁后只做一次快速的"仍然满足吗"复核，而不是彻底去掉锁。
- **两个线程 `arrival_time` 相同，谁先被处理**：不能用 `arrival_time` 本身排序（无法区分同时到达的
  并发调用的真实顺序），应该用"先获取锁的线程先处理"——锁的获取顺序天然定义了 FIFO。
- **多区域部署下这种强一致限流器会有什么问题**：可以联系到分布式限流的通用话题——跨区域同步会有
  延迟、热点 key 问题，讨论 token bucket + 本地缓存 + 定期同步的降级方案作为开放式延伸，不要求现场
  实现。

## 7. 常见跑偏（方法层面，3 条）
- **把被拒绝/失败的请求也计入窗口名额**：这是题目反复强调的坑——`allow()` 判断不够时不能 append；
  `simulate_rate_limiter` 里 `success_flag=0` 的请求"经过"了满足条件的时刻,但不能往 `granted_per_rule`
  里记录。
- **Part 2 忘记 FIFO 约束，直接对每个请求独立算 `_advance(arrival, ...)`**：必须先取
  `max(arrival, 上一个请求的实际开始时间)`，否则后到的请求可能"抢先"排到更早到达、仍在等待的请求
  前面。
- **窗口边界算反**：半开区间 `(t-window, t]` 里 `t-window` 本身不算在窗口内，写成 `<` 还是 `<=`
  这种细节错了会导致边界样例（例如 `window=5` 时 `t'=5` 的窗口 `(0,5]` 不含 `t=0`）算错。

## 自测清单
- 空请求列表两个函数都返回空列表。
- `limit=0` 时任何请求都被拒绝/永远等不到名额（测试只验证短时间内确实一直拒绝，不构造真正死等）。
- 窗口边界严格按半开区间验证（`t-window` 本身不算在窗口内）。
- 多规则里某条规则永远是瓶颈，结果应与"只看瓶颈规则"的单规则结果一致（交叉验证没漏掉某条规则）。
- FIFO 顺序：更晚到达的请求不能插队到更早到达、仍在等待的请求前面。
- 并发 `try_acquire`：任意规则窗口内记录的许可数不超过 `limit`（多线程 + 事后扫描验证）。

## 相关题与 skills id
- skills: **S09**（类设计先定契约）· **S10**（并发正确性：跨规则原子 check-then-act）· **S06**
  （滑窗与事件流，与 Stripe ps01/cd06 同族）。
- 同族：`od01_priority_task_scheduler` 同样是"检查候选 + 标记占用必须原子"的并发模式。
- 与 SD 侧 `sd07`（分布式限流器）是编码版和系统设计版的同一主题，面试官常在两轮之间做组合追问。
- 练习命令：`python3 loop/mock.py start od04`
