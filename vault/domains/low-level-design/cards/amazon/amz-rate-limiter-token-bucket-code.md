---
id: amz-rate-limiter-token-bucket-code
node: amazon.amz-rate-limiter
type: qa
step: 3
tags: [grown]
---
## Q
在限流器设计里，令牌桶（Token Bucket）的 `allow` 怎么写？为什么不用后台线程定时补令牌？

## A
令牌桶：桶里最多存 `burst` 个令牌，每秒补 `rate` 个，一次请求拿走 `cost` 个。不开线程，而是在每次请求时按「距上次的时间差」一次性补齐——零后台线程、每个 key 只存两个数。
```python
class TokenBucket:
    def __init__(self, rate, burst, now):
        self.rate, self.burst = rate, burst
        self.tokens, self.last = burst, now

    def allow(self, now, cost=1):
        self.tokens = min(self.burst, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens < cost:
            return False
        self.tokens -= cost
        return True
```
