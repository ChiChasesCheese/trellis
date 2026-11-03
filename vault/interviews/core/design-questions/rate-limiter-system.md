---
slug: rate-limiter-system
kind: low-level-design
---
## Q
**限流器（单机类设计）**｜低层设计

设计一个限流器：在 T 秒内最多允许某个调用方发起 N 个请求，超出的请求被拒绝。要求支持多种限流算法（固定窗口、滑动窗口、令牌桶等），可以按用户或 API Key 分别限流，线程安全，算法可以替换而不改调用方。这是类与接口层面的设计题，和"分布式限流器"那道系统设计题不同——这里关心的是类怎么划分、状态怎么放、并发怎么处理、怎样写出能测试的代码。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 这是策略模式的典型题：把"算法"做成可替换的、只管单个 key 的状态机，把"按 key 管理与并发"放在外层，并让时间可以注入，代码才好测。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求（算法种类、按什么 key、要不要剩余额度），定 `Decision` 和 `allow(key)` |
| 8–13 分 | 类结构：`Limiter` 策略、`RateLimiter` 入口、per-key 锁 |
| 13–43 分 | 写核心实现：三种算法和 `RateLimiter` |
| 43–48 分 | 跑例子：窗口边界、令牌桶、key 隔离、多线程 |
| 48–60 分 | 追问：内存回收、多规则、权重、分布式 |

**需求。**
功能：
1. `allow(key)`：判断该 key 此刻是否可以放行，同时消耗一次配额。
2. 返回的不只是布尔值：还有剩余额度和被拒后应该多久再试（用于 `Retry-After`）。
3. 支持固定窗口、滑动窗口（日志式）、令牌桶三种算法，并可扩展。
4. 每个 key 独立计数；多线程并发调用时结果正确。
5. 时间可注入（测试里用假时钟）。

非功能：单次判断 O(1) 或摊还 O(1)；不同 key 之间不互相阻塞；内存随活跃 key 数增长，需要有清理手段。

**核心实体与接口。**
- `Decision`：不可变值对象，`allowed`、`remaining`、`retry_after`。
- `Limiter`（抽象类）：单个 key 的状态和判定，`try_acquire(now) -> Decision`。算法差异全在子类里。
- `FixedWindow`、`SlidingWindowLog`、`TokenBucket`：三种策略实现。
- `RateLimiter`：入口，持有"key 到（锁，Limiter）"的映射和时钟；`allow(key)` 取出对应 Limiter，加该 key 的锁后调用。
- 模式：策略（Strategy）——算法可替换；简单工厂/工厂函数——`RateLimiter` 通过 `factory` 为新 key 创建 Limiter；依赖注入——时钟可替换。

**整体设计。**
调用路径：`RateLimiter.allow(key)` → 全局锁下取得或创建该 key 的（锁，Limiter）→ 释放全局锁 → 只持有该 key 的锁调用 `try_acquire(clock())`。全局锁只保护字典的"创建条目"这一瞬间，真正的判定在 per-key 锁里，所以热点 key 之间互不影响，只有同一个 key 的并发调用会串行。

三种算法的状态：
- 固定窗口：窗口起点和计数。窗口按绝对时间对齐（`now - now % window`），进入新窗口就清零。状态最小，但窗口边界处允许最多 2N 的突发（上一窗口末尾 N 个加下一窗口开头 N 个）。
- 滑动窗口日志：保存窗口内每个放行请求的时间戳（双端队列），每次先弹出已过期的，再比较个数。最精确，内存为 O(N)。被拒时，最早那条过期的时刻就是可以重试的时刻。
- 令牌桶：保存当前令牌数和上次时间。不需要后台线程补充令牌，而是惰性补充：请求到来时按"流逝时间乘以速率"折算，上限是桶容量。允许容量范围内的突发，长期速率等于补充速率。被拒时，`(1 - 令牌数) / 速率` 就是下一个令牌到来的等待时间。

**核心实现。** 约 30 分钟，下面是全部要写的代码：三种算法和按 key 加锁的入口。

```python
import threading
import time
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Decision:
    allowed: bool
    remaining: int
    retry_after: float  # 秒；放行时为 0


class Limiter(ABC):
    """单个 key 的限流状态机；算法差异全部封装在这里（策略模式）。"""

    @abstractmethod
    def try_acquire(self, now: float) -> Decision: ...


class FixedWindow(Limiter):
    def __init__(self, limit: int, window: float) -> None:
        self.limit, self.window = limit, window
        self.start, self.count = 0.0, 0

    def try_acquire(self, now: float) -> Decision:
        # 窗口按绝对时间对齐；进入新窗口就清零
        start = now - (now % self.window)
        if start != self.start:
            self.start, self.count = start, 0
        if self.count < self.limit:
            self.count += 1
            return Decision(True, self.limit - self.count, 0.0)
        return Decision(False, 0, self.start + self.window - now)


class SlidingWindowLog(Limiter):
    def __init__(self, limit: int, window: float) -> None:
        self.limit, self.window = limit, window
        self.log: deque[float] = deque()

    def try_acquire(self, now: float) -> Decision:
        while self.log and self.log[0] <= now - self.window:   # 弹出窗口外的旧请求
            self.log.popleft()
        if len(self.log) < self.limit:
            self.log.append(now)
            return Decision(True, self.limit - len(self.log), 0.0)
        return Decision(False, 0, self.log[0] + self.window - now)


class TokenBucket(Limiter):
    def __init__(self, capacity: int, refill_per_sec: float) -> None:
        self.capacity, self.rate = capacity, refill_per_sec
        self.tokens, self.last = float(capacity), None

    def try_acquire(self, now: float) -> Decision:
        if self.last is not None:                    # 惰性补充：请求到来时按流逝时间折算
            self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return Decision(True, int(self.tokens), 0.0)
        return Decision(False, 0, (1 - self.tokens) / self.rate)


class RateLimiter:
    """入口：按 key 找到各自的 Limiter；per-key 加锁，不同 key 互不阻塞。"""

    def __init__(self, factory: Callable[[], Limiter],
                 clock: Callable[[], float] = time.monotonic) -> None:
        self._factory, self._clock = factory, clock
        self._entries: dict[str, tuple[threading.Lock, Limiter]] = {}
        self._guard = threading.Lock()

    def allow(self, key: str) -> Decision:
        with self._guard:                            # 只在创建 key 条目时短暂持有全局锁
            if key not in self._entries:
                self._entries[key] = (threading.Lock(), self._factory())
            lock, limiter = self._entries[key]
        with lock:                                   # 先释放全局锁再取 key 锁，不会死锁
            return limiter.try_acquire(self._clock())
```

**运行。** 用可拨动的假时钟：
- `FixedWindow(3, 10)`：0、1、2 秒放行，剩余额度 2、1、0；3 秒被拒，`retry_after` 是 7.0；10 秒进入新窗口，放行。
- 窗口边界突发：8、8.1、8.2 秒和 10、10.1、10.2 秒共 6 个请求全部放行。同样的请求给 `SlidingWindowLog(3, 10)`，后三个被拒，到 18.05 秒才放行。
- `TokenBucket(2, 1)`：0 秒放行两次，第三次被拒，`retry_after` 是 1.0；1 秒后放行一次。
- 额度为 1 的 key `a` 第二次被拒，key `b` 不受影响。
- 额度 100 的 key 被 130 个线程同时调用：恰好 100 个放行。

**深入。**
1. 【必讲】并发正确性：
- 问题：多个线程同时对同一个 key 调用，若先读计数再写回，会各读到旧值，双双放行，超出限额。
- 方案：per-key 锁，让"读状态、判定、写状态"成为一个临界区。这是最简单且正确的做法。
- 选项：全局一把锁，简单但所有 key 串行化，吞吐被最慢的临界区限制；per-key 锁，并发度高，代价是每个 key 多一把锁；无锁（CAS 循环）更快，但状态含多个字段（令牌数加时间）时，需要把它们打包成一个不可变对象再整体 CAS，复杂度高。选择：per-key 锁。
- 死锁风险：代码里从不同时持有全局锁和 key 锁——先释放全局锁再取 key 锁，避免锁顺序问题。

2. 【必讲】算法的取舍：
- 固定窗口最便宜，但有边界突发；滑动窗口日志最准但内存随额度线性增长（N 很大时不适合）；滑动窗口计数（保留当前与上一窗口两个计数，按重叠比例加权估算）是折中，内存 O(1)、误差小；令牌桶最灵活，允许突发，是 API 限流的默认选择。
- 选择依据：要的是"严格每 T 秒不超过 N"（用滑动窗口日志），还是"平均速率受限但允许一定突发"（令牌桶）。面试里先实现一种，说出其他几种的差别，再按要求补一个。

3. 【必讲】时间源：
- 使用单调时钟（`time.monotonic`），不使用墙钟（`time.time`）：系统时间被调整（NTP 校时、手工修改）时，墙钟会回退，导致令牌为负或窗口错乱。
- 时钟作为构造参数注入，测试里用一个可手动拨动的假时钟，避免 `sleep`，测试既快又确定。

4. 【追问再讲】内存增长：
- 问题：`_entries` 对每个出现过的 key 都留一份状态，key 来自用户输入时会无限增长。
- 方案：给每个 Limiter 记录最后访问时间，用后台线程或惰性清理删除长时间不活跃的 key（删除时要在全局锁里，且要确认没有线程正拿着该条目的锁，或者允许"删除后重建"的重复，因为不活跃的 key 状态本来就应是满额）；或使用带容量上限的 LRU 字典。令牌桶和滑动窗口的状态在不活跃一个窗口之后等价于初始状态，所以删除不影响正确性。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 单机还是分布式：这个设计只在单个进程里有效。多实例时状态要放进共享存储（如 Redis 加 Lua 脚本保证原子性），`Limiter` 接口基本不变，只是实现换成远端调用——这也是接口只依赖 `try_acquire` 的好处。
- 多规则组合（每秒 10 次且每分钟 100 次）：组合模式——一个 `CompositeLimiter` 持有多个 Limiter，全部通过才放行；注意其中一个拒绝时，之前已通过的那些不应被扣减（先检查、后统一扣，或提供回滚）。
- 带权重的请求：把 `try_acquire(now)` 扩展为 `try_acquire(now, cost=1)`，令牌桶直接扣 `cost`；窗口类算法按 `cost` 累加。
- 是否阻塞等待：这里是非阻塞的"立即判定"。若需要"等到有配额再执行"（平滑整形），在 `retry_after` 之上封装一个睡眠加重试，或使用条件变量。
- 测试：用假时钟验证三类场景——窗口边界、突发后的恢复、不同 key 隔离；并发测试用多线程对同一 key 调用 N+M 次，断言放行数恰好是 N。

**级别期望。**
- 中级：写出一种算法（如固定窗口或滑动窗口）加按 key 的字典，逻辑正确。
- 高级：用策略模式支持多种算法，per-key 锁保证并发正确，单调时钟与时钟注入，说清各算法的取舍。
- 资深/Staff：内存回收、带权重与多规则组合、从单机扩展到分布式时接口如何保持不变、并发测试方案、性能分析。

**先修概念。** [[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-in-a-hurry-design-principles|设计原则]]、[[hi-low-level-design-concurrency-intro|并发入门]]、[[hi-low-level-design-concurrency-correctness|并发正确性]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]

**同类题。** [[hi-low-level-design-problem-breakdowns-rate-limiter|限流器（拆解）]]、[[distributed-rate-limiter|分布式限流器（系统设计）]]、[[api-circuit-breaker|熔断器]]、[[solution-ttl-cache|带过期的缓存]]
