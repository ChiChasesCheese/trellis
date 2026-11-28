---
id: hi-c-lld-rate-limiter-b04-http-semantics
node: lld.problem-breakdowns.rate-limiter.beyond
type: qa
step: 1
---
## Q
**限流器 · 拓展：把结果映射成 HTTP，以及限流器自己坏了怎么办**｜拓展 · 追问

网关拿到 `RateLimitResult` 后怎么回给客户端？限流器本身出故障时放行还是拒绝？

## A
**模式。** 结果对象与传输层分离：限流器只给出决策，翻译成 HTTP 的是网关。

```python
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    allowed: bool
    remaining: int
    retry_after_ms: int | None = None


def to_http(r: Result, limit: int) -> tuple[int, dict[str, str]]:
    headers = {"X-RateLimit-Limit": str(limit), "X-RateLimit-Remaining": str(r.remaining)}
    if r.allowed:
        return 200, headers
    # Retry-After 的标准形式是整数秒；毫秒向上取整，不能让客户端早到
    headers["Retry-After"] = str(math.ceil((r.retry_after_ms or 0) / 1000))
    return 429, headers


def guarded(limiter_allow, client: str, endpoint: str) -> Result:
    try:
        return limiter_allow(client, endpoint)
    except Exception:                            # 限流器自己坏了：放行还是拒绝是业务决定
        return Result(True, 0)                   # 这里选 fail-open；支付、登录等敏感接口可选 fail-closed


assert to_http(Result(False, 0, 1200), 10) == (429, {"X-RateLimit-Limit": "10", "X-RateLimit-Remaining": "0", "Retry-After": "2"})
assert to_http(Result(True, 7), 10)[0] == 200
```
- **状态码：** 被限流返回 429（Too Many Requests）。`Retry-After` 头的标准形式是整数秒（也可以是日期），所以毫秒要向上取整成秒，不能让客户端早到。
- **额度头：** `X-RateLimit-Limit`、`X-RateLimit-Remaining` 是业界通行的非标准写法；标准化的 `RateLimit` 头字段还在 IETF 草案里讨论，面试里说"通行做法"即可。
- **限流器自己出错：** fail-open（放行）保证可用性，代价是失去保护；fail-closed（拒绝）保证保护，代价是误伤全部流量。普通读接口多用 fail-open，登录、支付、成本高的接口可以 fail-closed。要把选择写出来并告警。
- **客户端行为：** 好的客户端读 `Retry-After` 并加抖动（jitter）重试，否则大量客户端在同一毫秒重试，形成重试风暴。
- **何时不用：** 内部库调用不走 HTTP，直接用结果对象即可。
