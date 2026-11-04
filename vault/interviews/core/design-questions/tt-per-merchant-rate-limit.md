---
slug: tt-per-merchant-rate-limit
kind: low-level-design
---
## Q
**按商户限流**｜低层设计

支付接口要按商户限流：每个商户有自己的速率和突发上限（大商户更高），没有单独配置的用默认值。实现 `allow(merchant, cost)`，返回是否放行（被拒时还要告诉调用方多久后再试）。商户数量可能有几十万，绝大多数长期不活跃，内存不能无限增长。调用来自多个线程。面试官会追问：为什么选令牌桶、不用定时器怎么补充令牌、被淘汰的商户会怎样、单个锁成为瓶颈怎么办、多实例部署怎么办、配置实时修改怎么办。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 令牌桶管"速率与突发"，惰性补充让每次判定 O(1) 且不需要定时器，按访问顺序排序的哈希表（LRU）管"几十万商户的内存上限"，分段加锁管"并发"，时钟注入管"可测试"。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求（速率、突发、默认值、内存上限、多线程）；定 `allow(merchant, cost) -> Decision`；口述令牌桶、惰性补充、LRU、分段锁 |
| 8–40 分 | 写 `Limit`、`Decision`、`Bucket`、`_Shard.take`、`MerchantRateLimiter.allow` |
| 40–45 分 | 用假时钟跑：突发、等待时间、补充、超额 `cost`、淘汰 |
| 45–58 分 | 追问：单锁瓶颈与分段锁、配置热更新、多实例 |
| 58–60 分 | 口述限流器故障时放行还是拒绝 |

**需求。**
功能：
1. `allow(merchant, cost=1)`：判断该商户此刻能否放行，放行就扣减 `cost` 个令牌。
2. 每个商户可以有自己的（速率，突发上限）；没配置的用默认值。
3. 被拒时返回需要等待的时间，用于 `Retry-After`。
4. 配置可以随时修改，下一次判定生效。
5. 内存有上限：桶的数量不超过 `max_buckets`。

非功能：
- 每次判定 O(1)。
- 线程安全，不同商户尽量不互相阻塞。
- 时间从外部注入，测试时可以手动拨时钟，不用 `sleep`。
- 不变量：任意时刻 0 ≤ 令牌数 ≤ 突发上限；任意长度为 T 的时间窗口内放行的总量不超过 突发上限 + 速率 × T。

**核心实体与接口。**
- `Limit(rate, burst)`：速率（令牌/秒）和桶容量，不可变。
- **Decision 不可变判定：** `Decision(allowed, remaining, retry_after)`：不可变的判定结果。
- `Bucket(tokens, updated)`：一个商户的状态，只有两个字段。
- `_Shard`：一个分段，一把锁加一个 `OrderedDict`（哈希表 + 双向链表，队头是最久没用的商户）。
- `MerchantRateLimiter`：入口，持有配置表、默认值、时钟和若干分段；`allow` 按商户哈希选分段。
- 模式：令牌桶算法；LRU 缓存（哈希表 + 链表）；分段锁（lock striping）；依赖注入（时钟）。

**整体设计。**
`allow` 的流程：从配置表取该商户的 `Limit`（没有就用默认）→ 对商户名取哈希选一个分段 → 在该分段的锁内：取出商户的桶，没有就创建一个满桶并在超过容量时淘汰队头；把该商户移到队尾（标记为最近使用）；按"当前时间减去上次更新时间"乘以速率补充令牌，不超过容量；令牌够就扣减并放行，不够就返回拒绝和需要等待的时间。

整个过程没有任何后台线程：令牌是在请求到来时才折算补充的（惰性补充），一个长期不活跃的商户不消耗任何 CPU，只占一个桶的内存。

**核心实现。** 约 70 行，一次写完。

```python
from __future__ import annotations

import threading
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable

Clock = Callable[[], float]


@dataclass(frozen=True)
class Limit:
    rate: float                  # 每秒补充的令牌数
    burst: int                   # 桶容量，也是允许的最大突发


@dataclass(frozen=True)
class Decision:
    allowed: bool
    remaining: int
    retry_after: float           # 秒；放行时为 0


@dataclass
class Bucket:
    tokens: float
    updated: float


class _Shard:
    """一个分段：一把锁 + 一个按最近使用排序的 OrderedDict（哈希表 + 链表）。"""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.lock = threading.Lock()
        self.buckets: OrderedDict[str, Bucket] = OrderedDict()   # 队头最久没用

    def take(self, merchant: str, lim: Limit, cost: int, now: float) -> Decision:
        with self.lock:
            b = self.buckets.get(merchant)
            if b is None:
                b = self.buckets[merchant] = Bucket(float(lim.burst), now)   # 新桶是满的
                if len(self.buckets) > self.capacity:
                    self.buckets.popitem(last=False)                       # 淘汰最久没用的商户
            self.buckets.move_to_end(merchant)
            # 惰性补充：按"距上次的时间 × 速率"一次补齐；时钟回拨时补 0
            b.tokens = min(float(lim.burst), b.tokens + max(0.0, now - b.updated) * lim.rate)
            b.updated = now
            if cost > lim.burst:
                return Decision(False, int(b.tokens), float("inf"))        # 永远凑不够，别让客户端空等
            if b.tokens >= cost:
                b.tokens -= cost
                return Decision(True, int(b.tokens), 0.0)
            return Decision(False, int(b.tokens), (cost - b.tokens) / lim.rate)


class MerchantRateLimiter:
    def __init__(self, limits: dict[str, Limit], default: Limit, clock: Clock,
                 max_buckets: int = 100_000, shards: int = 16) -> None:
        self._limits, self._default, self._clock = limits, default, clock
        per = max(1, max_buckets // shards)
        self._shards = [_Shard(per) for _ in range(shards)]

    def allow(self, merchant: str, cost: int = 1) -> Decision:
        lim = self._limits.get(merchant, self._default)             # 配置在锁外读取，改配置下次生效
        shard = self._shards[hash(merchant) % len(self._shards)]
        return shard.take(merchant, lim, cost, self._clock())
```

**运行。** 默认限额为速率 5/秒、突发 10，桶数量上限 4：

```python
now = [0.0]
rl = MerchantRateLimiter({}, Limit(5, 10), lambda: now[0], max_buckets=4, shards=1)
print([rl.allow("m1").allowed for _ in range(11)].count(True), rl.allow("m1").retry_after)   # 10  0.2
now[0] = 1.0
print([rl.allow("m1").allowed for _ in range(6)])    # 5 次 True 然后 False
print(rl.allow("m1", cost=11).retry_after)           # inf
for m in ("a", "b", "c", "d", "e"):
    rl.allow(m)
print(sum(len(s.buckets) for s in rl._shards))       # 4，最久没用的被淘汰
```

- 时间 0 连续请求 11 次：前 10 次放行，第 11 次被拒，`retry_after` = 1 个令牌 ÷ 5 个/秒 = 0.2 秒。
- 时钟拨到 1.0 秒，补回 5 个令牌：接下来 5 次放行，第 6 次被拒。
- `cost=11` 超过突发上限 10，永远凑不够，返回无穷大的等待时间，而不是让客户端空等。
- 第 5 个商户出现时，最久没用的那个被淘汰，桶数量保持 4。

**复杂度。** 每次判定 `O(1)`；内存最多 `max_buckets` 个桶。

**逐步扩展。**
1. 【追问再讲】配置热更新：改配置用「复制后整体替换」，`allow` 在锁外读取配置，看到的永远是完整的旧表或新表。容量变小时，补充时的 `min(burst, …)` 会自然把现有令牌截断到新容量；速率变化从下一次补充起生效。

```python
# MerchantRateLimiter 新增：
    def set_limit(self, merchant: str, lim: Limit) -> None:
        self._limits = {**self._limits, merchant: lim}               # 复制后整体替换
```

2. 【加分】多实例按商户路由：同一商户的请求固定落到同一个实例，桶留在本地内存。进程内的 `hash` 对字符串在不同进程里取值不同，路由要换成稳定的哈希；分段选择也一样。

```python
# 顶部 import zlib；allow 里选分段改成：
        shard = self._shards[zlib.crc32(merchant.encode()) % len(self._shards)]
```

**深入。**
1. 【必讲】为什么选令牌桶。
- 问题：支付流量有尖峰（促销开始、批量调用），限流既不能把正常的短时突发全部拒掉，又要保护后端。
- 选项：固定窗口计数最简单，但窗口交界处能放过两倍流量；滑动窗口日志精确，但每个放行请求都要存一条时间戳，内存随请求数线性增长，大商户代价大；滑动窗口计数是折中；令牌桶只存两个字段，允许不超过突发上限的短时突发，长期速率又严格受限。
- 选择：令牌桶。商户的突发上限和速率可以分别配置，也容易表达"大商户更高"。
2. 【必讲】惰性补充与时间。
- 问题：给几十万个桶各挂一个定时器去加令牌，成本高且没必要。
- 做法：每次访问时补充 `max(0, now − updated) × rate`，上限为突发容量，再把 `updated` 设为 `now`。补充量取 `max(0, …)`，所以时钟回拨不会产生负数。
- 时间源：生产里用单调时钟（`time.monotonic`），不用墙钟，NTP 校时或手工改时间不会打乱令牌。时钟作为构造参数注入，测试用可手动拨动的假时钟。
- 被拒时的等待时间：缺少的令牌数除以速率，就是下一次可以放行的时间，直接放进 `Retry-After`。
3. 【必讲】内存上限与淘汰。
- 问题：商户数量几十万，桶会一直增长。
- 做法：每个分段是 LRU，超过容量就淘汰最久没用的商户。被淘汰的商户下次出现会得到一个满桶。
- 淘汰的代价：如果被淘汰时桶还没有补满（刚用过大量令牌），它再次出现就多得到一次突发。对长期不活跃的商户，桶早已补满，淘汰与重建完全等价，所以按"最久没用"淘汰几乎无损。需要更严格时，可以只淘汰已经补满的桶，或为淘汰的桶保留一个"欠账到期时间"。
- 选择：LRU 淘汰；容量按活跃商户数的数倍估算，监控淘汰率，淘汰率高说明容量偏小。
4. 【追问再讲】并发：从单锁到分段锁。
- 问题：一把全局锁让所有商户的判定串行，吞吐受最慢临界区限制；每个商户一把锁会让锁对象数量和桶一样多。
- 做法：按商户名哈希分成若干个分段，每个分段自己的锁和自己的 LRU。临界区只有几个算术运算，持有时间极短。不同分段互不阻塞，同一个商户的请求仍然串行，保证它的令牌记账正确。
- 注意：配置表在锁外读取，更新配置见逐步扩展 1；分布式路由要换成稳定的哈希，见逐步扩展 2。
- 选择：分段数取 16 到 64，足以消除绝大多数争用，又不浪费内存。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 多实例部署？一种做法是把桶放进 Redis，用一个 Lua 脚本原子地完成"读状态、补充、扣减、写回"；另一种是按商户 ID 一致性哈希，把同一商户的请求路由到固定的实例，桶留在本地内存，延迟最低，代价是实例变动时桶要迁移或重置。
- **严格上限选滑动窗口：** 滑动窗口和令牌桶怎么选？要求"任意 T 秒内严格不超过 N"时用滑动窗口日志；要求"平均速率受限但允许突发"时用令牌桶。
- 配置实时修改？下一次 `allow` 读到新配置，见逐步扩展 1。
- **限流返回 429：** 被限流的请求怎么办？返回 429 和 `Retry-After`。支付请求本身带幂等键，客户端重试是安全的；客户端应使用带抖动的指数退避，避免同时重试。
- 请求有权重？`cost` 参数：批量接口一次消耗多个令牌；`cost` 大于容量要直接拒绝，避免客户端无限等待。
- **故障时失败即拒绝：** 限流器自己出故障？对支付这类宁可拒绝也不能放大风险的场景，倾向失败即拒绝；对普通读接口倾向失败即放行并告警。需要明确说出选择和理由。
- 如何测试？假时钟验证：满桶消耗、等待时间的数值、补充后恢复、容量封顶、时钟回拨不产生负令牌；商户之间互不影响；淘汰后桶数量不超过上限；多线程对同一商户并发调用 N+M 次，放行数恰好不超过突发上限加期间补充量。

**级别期望。**
- 中级：令牌桶加按商户的字典，能放行与拒绝，说出惰性补充。
- 高级：LRU 控制内存，线程安全，时钟注入，返回等待时间，说明不同算法的取舍。
- 资深/Staff：分段锁的粒度，淘汰对公平性的影响，分布式部署的两种做法，配置热更新，故障时放行还是拒绝，指标与容量规划。

**先修概念。** [[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-concurrency-intro|并发入门]]、[[hi-low-level-design-concurrency-correctness|并发正确性]]、[[hi-system-design-deep-dives-redis|Redis]]、[[hi-system-design-core-concepts-caching|缓存]]

**同类题。** [[tt-rate-limiter-implementation|手写限流器]]、[[tt-lru-cache-ttl|带 TTL 的 LRU]]、[[rate-limiter-system|限流器（单机类设计）]]、[[distributed-rate-limiter|分布式限流器（系统设计）]]、[[tiktok-service-protection|服务保护八股]]
