# q23 · 限流器（滑动窗口：全局 → 按客户 → 带权重；令牌桶 + 空闲清理）

> `problems/q23_rate_limiter/` · 4 个 part
> **主题：窗口边界的开闭 + "被拒的请求不记账" + 惰性补充令牌。**

## 一句话题意

请求按时间序到达 `(timestamp_ms, client_id)`，判定 `ALLOW` / `DENY`。
P1 全局滑动窗口，P2 按客户分窗，P3 请求带权重，P4 换成令牌桶并支持清理空闲客户。

## 输入 / 输出

```
PART n
LIMIT <limit> <window_ms>            P1–3，缺省 "LIMIT 5 2000"
BUCKET <capacity> <refill_per_sec>   P4，缺省 "BUCKET 5 2"
<ts_ms> [<client>] [<weight>]        每行一个请求，最多 10^6 行
CLEANUP <now_ms> <idle_ms>           P4
```
输出：每个请求一行 `ALLOW` / `DENY`；时间戳乱序打印 `ERROR`；`CLEANUP` 打印 `EVICTED <n>`。

## 核心考点

`S03` 每客户状态 · **`S05` 严格 vs 非严格边界** · `S12` 时间窗口 · **`S16` 滑动窗口 / 令牌桶** ·
`S18` 校验 · `S21` `collections.deque` · **`A07` 按时间排序的滑动窗口** · **`performance`：10^6 行**

## 解题思路

### Part 1 — 滑动窗口

**窗口是左开右闭 `(t − window_ms, t]`。**

```python
class SlidingWindow:
    def __init__(self, limit, window): self.limit, self.window, self.dq = limit, window, deque()
    def allow(self, ts, weight=1) -> bool:
        while self.dq and self.dq[0][0] <= ts - self.window:   # ★ <= 而不是 <，因为左端开
            self.total -= self.dq.popleft()[1]
        if self.total + weight > self.limit:
            return False                                        # ★ 被拒的**不记账**
        self.dq.append((ts, weight)); self.total += weight
        return True
```

`5 per 2000 ms` 的验证序列（题面给的，用来自测）：
`0,1,2,3,4 → ALLOW`；`5 → DENY`；**`1999 → DENY`**（0 还在 `(−1, 1999]` 里）；
**`2000 → ALLOW`**（0 离开了 `(0, 2000]`）。

**被拒的请求不记录、不消耗容量** —— 否则一串拒绝会把封锁期无限延长。

### Part 2 — 按客户

每个 client 一个独立的 `deque`（首次见到时创建）。客户之间互不影响。

### Part 3 — 带权重

`sum(窗口内权重) + weight <= limit` 才允许。
`weight > limit` **永远拒绝**（且仍不记账）；`weight <= 0` → `ValueError`。

### 乱序时间戳（所有 part）

时间戳必须**按客户非递减**。小于该客户上次**见到**（不论允许还是拒绝）的时间戳 →
`ValueError("out-of-order timestamp")`，`main()` 打印 `ERROR` 并继续。

### Part 4 — 令牌桶

**桶起始是满的**（`capacity` 个令牌）。**惰性补充**，用**毫令牌的整数运算**（不用 float）：

```python
def allow(self, client, ts, cost=1) -> bool:
    b = self.buckets.setdefault(client, Bucket(self.cap * 1000, ts))
    b.milli = min(self.cap * 1000, b.milli + (ts - b.last) * self.refill)   # refill 是 per-sec → per-ms 的千分之
    b.last = ts
    if b.milli < cost * 1000:
        return False                    # 被拒不改令牌数（但补充保留）
    b.milli -= cost * 1000
    return True
```

`capacity 5, refill 2/s` 的验证序列：
`t=0` 五次 `ALLOW`；`t=0` 第六次 `DENY`；`t=500 → ALLOW`（补了 1 个）；
**`t=600 → DENY`**（只有 0.2 个）；`t=5000 → ALLOW`。

**`cleanup(now_ms, idle_ms)`**：删除最后一次请求在 `now_ms − idle_ms` **或更早**的客户
（空闲**至少** `idle_ms`），返回删除数量。被删的客户回来时是满桶 ——
当 `idle_ms >= capacity / refill * 1000` 时这与不删完全等价。

## 坑

1. **窗口左端开右端闭**：`t − window` **排除**，`t` **包含**（`2000` 允许，`1999` 拒绝）。
2. **被拒的请求不记账。**
3. 同一时间戳的多个请求全在窗口内，按输入序处理。
4. 单客户猛打 vs 多客户各自不超限（公平性 follow-up）。
5. 权重**恰好填满**（`sum + w == limit`）→ ALLOW，多 1 → DENY。
6. 令牌桶的**小数补充不能被舍掉**：600 ms × 2/s = 1.2 个令牌要累计，但 0.2 个不够一次请求。
   → 用毫令牌整数。
7. 桶有**上限**：空闲一天也不会超过 `capacity`。
8. `cleanup` 的边界是 `==` 也驱逐。
9. **10^6 个请求要在 2 s 内**：每个请求 O(1) 摊还（deque 弹出），**不能每次扫全表**。

## 变体

- "3 requests per 10 seconds"、"100 requests per 15 minutes per user" —— 只改构造参数。
- **固定窗口计数器**（`(user, window_start) → count`）作为更简单的 P1 —— 有的面试官接受，
  但候选人报告描述的是滑动版。
- Stripe 博客的另外三种限流器（并发请求、负载降级、worker 利用率）通常作为讨论题而非编码题。

## Code Core 节点

**`chrono.windows`** · **`toolbox.deque`** · **`algorithms.sliding-window`** ·
`performance.amortized` · `performance.memory`（空闲清理） · `rules.thresholds`

## 自测清单

- [ ] `0,1,2,3,4 / 5 / 1999 / 2000` 的完整序列
- [ ] 一串 DENY 之后窗口没有被延长
- [ ] 同一时间戳的多个请求
- [ ] `sum + w == limit` / `+1`
- [ ] `weight > limit` / `weight <= 0`
- [ ] 令牌桶 `t=0×6 / 500 / 600 / 5000`
- [ ] 空闲一天不超上限
- [ ] `cleanup` 的 `==` 边界
- [ ] 乱序时间戳 → `ERROR` 且继续
- [ ] 10^6 行的耗时
