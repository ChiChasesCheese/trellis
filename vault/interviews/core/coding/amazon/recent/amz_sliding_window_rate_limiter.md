# 多粒度滑动窗口限流（Sliding-window rate limiter）

限流器（rate limiter）决定一个请求现在能不能放行：在任意长度为 W 的时间窗口内，同一个对象最多放行 limit 个请求。对象可以是 IP 地址、用户、或某个业务场景（experience），这就是「多粒度」。这是一道编码题，不是类的设计题：要写出能运行的限流逻辑，说清楚精确算法（滑动窗口日志）和近似算法（滑动窗口计数）的取舍，以及内存怎样不无限增长。

## 开场先问的澄清问题
1. 接口长什么样：`allow(request, now)` 返回 True/False？时间由调用者传入还是读系统时钟？
2. 「窗口」是 N 秒的滑动窗口，还是整点的固定窗口？边界是 `(now−W, now]` 还是闭区间？
3. 多个粒度（IP、用户、experience）是**同时**限制吗？一个请求被拒绝时是否要占用其他粒度的额度？（不应占用。）
4. 要精确，还是允许近似来换内存？
5. 单机内存里还是分布式（Redis）？（先写单机，再答分布式。）

## 先补一点基础：为什么要「滑动」
- **固定窗口计数（fixed window）**：每个整点窗口计一个数，实现最简单。缺点是**边界突发**：限制 10 次/分钟，在 0:59 来 10 次、1:00 又来 10 次，一秒内放行了 20 次。
- **滑动窗口日志（sliding window log）**：记录每个被接受请求的时间戳，只数最近 W 秒内的。**精确**，内存 O(limit)。
- **滑动窗口计数（sliding window counter）**：只存当前桶与上一桶两个计数，估计 `prev × (1 − 已走比例) + cur`。内存 O(1)，但是近似（假设上一桶内的请求均匀分布）。

## 最笨解
每个 key 存全部历史时间戳，每次请求数一遍窗口内的个数。内存无界，时间 O(历史长度)（`_exact` 即此）。

## 逐步改进
1. **问题**：历史无限增长。
2. **日志版**：只存被接受的请求，且被接受的请求在窗口内至多 `limit` 个，所以每个 key 的队列长度 ≤ limit。每次请求先从队首弹出过期时间戳（均摊 O(1)），再看队列长度是否 < limit。
3. **计数版**：当内存要降到 O(1)/key：两个桶 + 线性插值。可能放行的请求数略大于或小于精确值，但不会让每个桶超过上限。
4. **多粒度**：每个粒度一个独立的限流器，请求带 `{"ip":…, "user":…, "experience":…}`，key 函数就是「取出该粒度的字段」。
5. **关键细节（原子性）**：先对所有粒度只检查（peek），**全部通过**才统一记录（record）。否则 IP 限额通过、用户限额失败时，IP 的额度被白白消耗。
6. **内存上界**：key 数量可能随用户数无限增长，定期（或惰性）淘汰窗口已空的 key；日志版每 key 最多 limit 条，总内存 ≤ 活跃 key 数 × limit。

```python
class SlidingWindowLog:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.logs = {}                                    # key -> deque of accepted timestamps (at most `limit` of them)

    def peek(self, key, now):
        log = self.logs.get(key)
        while log and log[0] <= now - self.window:        # window is (now - window, now]
            log.popleft()
        return len(log or ()) < self.limit

    def record(self, key, now):
        self.logs.setdefault(key, deque()).append(now)

class SlidingWindowCounter:
    """Two fixed buckets blended: count = prev * (1 - elapsed/window) + cur. Memory: two integers per key."""
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.state = {}                                   # key -> [bucket_start, cur, prev]

    def _roll(self, key, now):
        start = now - now % self.window
        s = self.state.setdefault(key, [start, 0, 0])
        if start != s[0]:
            s[2] = s[1] if start - s[0] == self.window else 0     # skipped a whole bucket => prev is empty
            s[1], s[0] = 0, start
        return s, (now - start) / self.window

    def peek(self, key, now):
        s, frac = self._roll(key, now)
        return s[2] * (1 - frac) + s[1] < self.limit

    def record(self, key, now):
        self._roll(key, now)[0][1] += 1

class RateLimiter:
    def __init__(self, rules, make=SlidingWindowLog):
        self.rules = {name: make(limit, window) for name, (limit, window) in rules.items()}

    def allow(self, request, now):
        keys = [(name, request[name]) for name in self.rules if name in request]   # one key per granularity
        if not all(self.rules[name].peek(k, now) for name, k in keys):
            return False                                  # check ALL first: a rejected request must not use up any quota
        for name, k in keys:
            self.rules[name].record(k, now)
        return True

    def evict_idle(self, now):                            # memory bound: forget keys whose window is empty
        for rule in self.rules.values():
            if isinstance(rule, SlidingWindowLog):
                for k in [k for k, log in rule.logs.items() if not log or log[-1] <= now - rule.window]:
                    del rule.logs[k]
            else:
                for k in [k for k, s in rule.state.items() if s[0] + 2 * rule.window <= now]:
                    del rule.state[k]
```

示例：IP 限额 2 次/10 秒，时间点 0、1、2、9、10、11 的结果是 通过、通过、拒绝、拒绝、通过、通过（时间 10 时 0 已过期，窗口是 `(0, 10]`）。IP 5 次/10 秒、用户 2 次/10 秒时，用户 `u` 的第 3 次请求被拒绝，且 IP 日志里只有 2 条（被拒绝的请求没有占额度）。计数版 4 次/10 秒：时间 0..3 各通过；时间 10 时上一桶=4、已走比例=0，估计 4 ≥ 4 拒绝；时间 15 时估计 4×0.5=2 < 4 通过。

## 复杂度
日志版：每次请求均摊 O(粒度数)，内存 O(活跃 key × limit)。计数版：O(粒度数) 时间，O(活跃 key) 内存。

## senior 追问
1. **分布式**：每个 key 的状态放 Redis；日志版用 sorted set（`ZREMRANGEBYSCORE` 清过期 + `ZCARD` + `ZADD`），把这几步放进 Lua 脚本保证原子；计数版用两个计数器 + `INCR` 与 TTL。
2. **热点 key（一个 IP 压垮单个 Redis 分片）**：本地令牌预取（每个实例先领一批配额），牺牲精度换吞吐。
3. **时钟不一致**：用 Redis 的 `TIME` 或单调时钟，不要用各机器本地时间。
4. **突发允许（令牌桶 token bucket）**：窗口限流是「窗口内总量」，令牌桶是「平均速率 + 突发上限」，两者的区别是常见追问。
5. **返回 `Retry-After`**：日志版 = 队首时间戳 + W − now；计数版需要解方程估算。
6. **限额按付费等级不同**：`rules` 里 limit 变成函数 `limit(key)`，key 函数不变。
7. **统计被拒绝的请求**：另开计数，不要和限流状态混在一起。

## 自测题
1. 窗口为什么是 `(now−W, now]` 而不是闭区间？
<details><summary>答案</summary>闭区间会让恰好相隔 W 的两个请求同时落入窗口，实际放行量比限额少一个；半开区间使 `[t, t+W)` 恰好容纳 limit 个。</details>
2. 为什么要先 peek 全部粒度、再 record？
<details><summary>答案</summary>被拒绝的请求不应消耗任何粒度的额度。</details>
3. 日志版内存为什么有上界？
<details><summary>答案</summary>只记录被接受的请求，窗口内被接受的不会超过 limit，而过期的会被弹出。</details>
4. 计数版相对日志版丢了什么？
<details><summary>答案</summary>精确性：它假设上一桶请求均匀分布，估计会偏高或偏低；换来每 key 常数内存。</details>
