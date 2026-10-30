---
id: tlc-tt-rate-limiter-implementation-4-followup
node: p2.tt-rate-limiter-implementation
type: qa
step: 4
---
## Q
**手写限流器**｜追问

每个 key 每秒最多放行 `r` 次、突发上限 `b` 的限流器，已经有滑动窗口和令牌桶两种单机实现。面试官接着问：（1）多个服务实例、状态放 Redis，怎么保证不超限？（2）固定窗口计数为什么不够，有没有省内存的近似？（3）key 太多时内存怎么控制？（4）时钟不准怎么办？

## A
1. **Redis 版**：状态是 `(tokens, last)`，不能「先 `GET` 再 `SET`」，多个实例会各自读到旧值而超发。把整段「读、补充、判断、扣减、写回」写成一个 Lua 脚本，Redis 单线程执行，天然原子；时间取脚本里的 `redis.call('TIME')`，不用各实例自己的时钟；key 形如 `rl:{业务}:{用户}`，写回时 `PEXPIRE`，空闲的 key 自动消失。
2. **固定窗口计数**：每个整秒一个计数器，`O(1)` 内存，但窗口交界处可以突发 `2r`（上一秒末 `r` 个加下一秒初 `r` 个）。近似方案「滑动窗口计数」：保留上一窗口和当前窗口两个计数，估算 `prev * (1 - 当前窗口已过去的比例) + cur`，内存 `O(1)`，误差有界。
3. **内存**：令牌桶里令牌已回满的 key 可以删除，下次来按满桶处理，结果相同：

```python
def sweep(self, now: float) -> None:
    for key, (tokens, last) in list(self.state.items()):
        if tokens + max(0.0, now - last) * self.rate >= self.burst:
            del self.state[key]          # 已回满：等价于从未出现过
```

   定时批量清理，不要在每次 `allow` 里清。
4. **时钟**：用单调时钟（`time.monotonic`）；多机版统一用 Redis 服务端时间；回拨时 `elapsed` 取 `max(0, …)`。

**Python 提醒**：浮点时间做差会丢精度，`0.7 - 0.6` 是 `0.09999999999999998`，`rate = 10`、`burst = 1` 时 `t = 0.6, 0.7` 的第二个请求会被误拒；生产实现里时间用整数毫秒、令牌按「毫令牌」整数记。
