---
id: hl-ld03-backoff
node: problems.ld03-async-tcp-channel
type: qa
step: 10
---
## Q
指数退避（exponential backoff）和全抖动（full jitter）是什么？`Backoff.next()` 怎么避免溢出？

## A
对端宕机时每 1 毫秒重试，浪费 CPU，且对端恢复瞬间「惊群」——大量客户端同时重连把刚恢复的服务打死。

**指数退避**：第 1 次等 `initial`，之后每次翻倍（乘 `multiplier`，封顶 `max`）；**抖动（jitter）**：在 `[0, 当前延迟]` 随机取值（全抖动，full jitter），分散重试时刻；成功后**重置**。

```java
public Backoff(long initialMs, long maxMs, int multiplier)  // 初始 > 0；max >= initial；multiplier >= 1
public long next() {
    long d = current;
    current = current > maxMs / multiplier ? maxMs : Math.min(maxMs, current * multiplier);
    return d;
}
public long next(RandomGenerator rng)  // 全抖动：rng.nextLong(next() + 1)，[0, 上限] 均匀
public void reset()
```
- 序列：`100, 200, 400, 800, 1000, 1000…`（initial=100，max=1000，multiplier=2）；`multiplier = 1` 则恒定；
- 用 `current > maxMs / multiplier ? maxMs : min(maxMs, current * multiplier)` 先用除法判断会不会超上限，**避免乘法溢出**（`maxMs` 可以是 `Long.MAX_VALUE`）；
- 非法参数抛 `IllegalArgumentException`；
- `RandomGenerator`（Java 17）：统一 `Random/SplittableRandom/ThreadLocalRandom` 的接口，有 `long` 范围方法 `rng.nextLong(cap + 1)`，旧的 `Random` 没有 long 范围版本常写成有偏差的 `(long)(rnd.nextDouble()*bound)`；测试里传带种子的 `Random` 结果就是确定的。

加强：「稳定连接 N 秒后才重置」（避免抖动连接一连上就重置造成重连风暴）：`run` 里连接成功时不立刻 `reset()`，记 `connectedAt`；`pump` 返回（断开）后若 `now − connectedAt >= stableAfter` 才 `reset()`，否则保留退避继续增长；`Backoff` 不变，需要可注入的时钟（`LongSupplier nanoTime`）才能确定性测试。

测试：`reset`；全抖动在 `[0, 当前上限]`；失败几次后成功，再被踢，重连应当从最短退避开始（连接成功时 `backoff.reset()`）。
