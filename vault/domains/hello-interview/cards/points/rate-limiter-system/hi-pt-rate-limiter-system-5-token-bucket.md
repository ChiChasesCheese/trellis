---
id: hi-pt-rate-limiter-system-5-token-bucket
node: qb.lld.rate-limiter-system.points
type: qa
step: 5
---
## Q
**限流器（单机类设计） · 令牌桶的惰性补充**｜必会 · 出自：限流器（单机类设计） › 整体设计

令牌桶需要后台线程补充令牌吗？状态和公式是什么？

## A
**不需要。** 惰性补充：保存当前令牌数和上次时间，请求到来时按「流逝时间 × 速率」折算，上限为桶容量。
```python
self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
```
**特点。** 允许容量范围内突发，长期速率等于补充速率，是 API 限流默认选择。
