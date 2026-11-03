---
id: craft-retry-backoff-dead-letter-2-transient-vs-permanent
node: craft.patterns.retry-backoff-dead-letter
type: qa
step: 2
---
## Q
**重试、退避与死信 · 什么错误值得重试**｜模式

派发线程调用渠道的 `send`，它可能抛出各种异常：超时、限流、用户地址不存在、代码里的 `KeyError`。全部重试 3 次，和区分对待，差别在哪里？渠道抛出了意料之外的异常，派发线程该怎么办？

## A
**要点。** 重试只对**暂时性**错误有意义（超时、429、503），因为下一次可能成功。永久性错误（地址不存在、参数非法、代码 bug）重试一万次结果相同，只是浪费时间并拖慢后面的消息。所以渠道用一个专门的异常类（`TransientDeliveryError`）声明「这个值得再试」；其他一切 `Exception` 直接进死信，原因写明是永久失败。无论哪种，异常都不能逃出派发循环。

```python
import heapq, itertools
from dataclasses import dataclass

class Transient(Exception): ...

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    def delay_for(self, attempt): return min(1.0 * 2 ** (attempt - 1), 8.0)

def run(send, policy, msgs):
    now, tick = 0.0, itertools.count()
    ready, delayed, sent, dead = [(m, 1) for m in msgs], [], [], []
    while ready or delayed:
        while delayed and delayed[0][0] <= now: ready.append(heapq.heappop(delayed)[2])
        if not ready: now = delayed[0][0]; continue
        msg, attempt = ready.pop(0)
        try:
            send(msg); sent.append((msg, attempt))
        except Transient as e:                     # 暂时性：退避重试，次数用尽进死信
            if attempt >= policy.max_attempts:
                dead.append((msg, attempt, f"gave up after {attempt}: {e}")); continue
            heapq.heappush(delayed, (now + policy.delay_for(attempt), next(tick), (msg, attempt + 1)))
        except Exception as e:                     # 其余一律当永久失败：重试没有意义
            dead.append((msg, attempt, f"permanent: {e!r}"))
    return sent, dead

def send(msg):
    if msg == "bad-address": raise ValueError("no such user")     # 重试一万次也一样
    if msg == "busy": raise Transient("429")

sent, dead = run(send, RetryPolicy(max_attempts=3), ["ok", "bad-address", "busy"])
print("发出:", sent)
for row in dead: print("死信:", row)
```

三条消息：正常的、地址不存在的、渠道 429 的：

```
发出: [('ok', 1)]
死信: ('bad-address', 1, "permanent: ValueError('no such user')")
死信: ('busy', 3, 'gave up after 3: 429')
```

**为什么。** 把「默认当永久失败」作为兜底有两个好处：渠道的代码有 bug 时不会触发重试风暴；永久错误立刻进死信，人可以马上看到。写 `except Exception` 而不是裸 `except` / `BaseException`：`KeyboardInterrupt`、`SystemExit` 不是业务失败，应当让进程停下来。

**代价。** 分类的责任在渠道实现者：把本该重试的错误漏标成永久，消息就被过早放弃了。所以暂时性错误要在渠道适配层（HTTP 状态码 5xx 和 429、连接超时）集中识别，不要散落在业务代码里。

**易错。** 重试之前消息必须是幂等的（同一个 `idempotency_key`），否则「超时但其实已经发出」的消息会发两遍。
