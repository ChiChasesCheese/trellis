---
id: craft-retry-backoff-dead-letter-1-backoff-as-pure-function
node: craft.patterns.retry-backoff-dead-letter
type: qa
step: 1
---
## Q
**重试、退避与死信 · 发送失败以后，什么时候再试、试几次、最后怎么办**｜模式

通知服务调用短信渠道失败了（对方返回 503）。最直接的做法是 `for _ in range(3): try: send(); break; except: time.sleep(1)`。它有哪些问题？一个可测试、不会把对方打得更惨的重试应该由哪几块组成？

## A
**要点。** 三块：一个纯函数 `delay_for(attempt)`，给出第 n 次失败之后要等多久（指数退避：每次翻倍，封顶）；一个按「到期时刻」排序的延迟堆，重试的消息放进去，到点才回到可处理队列，派发线程在此期间继续处理别的消息；一个出口，次数用完就进死信（dead letter），而不是无限试或悄悄丢。

```python
import heapq, itertools
from dataclasses import dataclass

class Transient(Exception): ...                       # 值得重试：超时、限流、503

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 5
    base: float = 1.0
    multiplier: float = 2.0
    max_delay: float = 8.0
    def delay_for(self, attempt: int) -> float:       # 第 attempt 次失败之后等多久（从 1 起）
        return min(self.base * self.multiplier ** (attempt - 1), self.max_delay)

def run(send, policy, msgs):
    """假时钟：没有可跑的消息时，直接把时钟拨到下一个重试到期的时刻，不 sleep。"""
    now, tick = 0.0, itertools.count()
    ready, delayed, log, dead = [(m, 1) for m in msgs], [], [], []
    while ready or delayed:
        while delayed and delayed[0][0] <= now:                   # 到点的重试回到就绪队列
            ready.append(heapq.heappop(delayed)[2])
        if not ready:
            now = delayed[0][0]; continue
        msg, attempt = ready.pop(0)
        try:
            send(msg)
        except Transient as e:
            if attempt >= policy.max_attempts:
                dead.append((msg, attempt, f"gave up: {e}")); continue
            d = policy.delay_for(attempt)
            log.append((now, msg, attempt, f"retry in {d:g}s"))
            heapq.heappush(delayed, (now + d, next(tick), (msg, attempt + 1)))   # 不 sleep，放进延迟堆
    return log, dead

p = RetryPolicy()
print("退避序列:", [p.delay_for(a) for a in range(1, 6)], "<- 到 8 封顶")

def flaky(msg): raise Transient("503")                            # 渠道总是 503
log, dead = run(flaky, RetryPolicy(max_attempts=4), ["hello"])
for row in log: print(row)
print("死信:", dead)
```

用注入的假时钟推进（总是失败的渠道，最多 4 次）：

```
退避序列: [1.0, 2.0, 4.0, 8.0, 8.0] <- 到 8 封顶
(0.0, 'hello', 1, 'retry in 1s')
(1.0, 'hello', 2, 'retry in 2s')
(3.0, 'hello', 3, 'retry in 4s')
死信: [('hello', 4, 'gave up: 503')]
```

**为什么。** `sleep` 版有三个毛病：睡眠期间占着线程，其他消息都被它挡住；固定间隔对一个正在恢复的服务是持续的压力，指数增长给它喘息；测试要真等好几秒。延迟堆让线程不睡觉，`delay_for` 是纯函数所以一个断言就能验证整个序列，封顶避免等待时间无限增长。

**代价。** 堆里的消息在进程退出时丢失，要持久化就得换成数据库或消息队列的延迟投递。堆元素带一个自增序号（`next(self.tick)`）打破时刻相同的平局，否则比较会落到消息对象上。
