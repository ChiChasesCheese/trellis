---
id: errors-retry-backoff-jitter
node: errors.retry
type: qa
step: 2
---
## Q
重试之间为什么要等待，而且要“指数增长再加随机抖动”？固定间隔 1 秒重试有什么问题？

## A
**等待时间指数增长，再乘一个随机数**

- **固定间隔会惊群**：下游刚恢复，所有失败过的客户端在同一秒一起回来，把它再次压垮（thundering herd）；
- **指数退避**：第 n 次失败后等 `base × 2ⁿ`，给下游越来越长的恢复时间；
- **必须封顶**：`min(cap, …)`，否则第 10 次要等十几分钟，调用方早就超时了；
- **抖动（jitter）**：在 `[0, 上限]` 里随机取一个值（full jitter），把客户端错开；
- **服务给了等待时间就听它的**：`Retry-After` 比自己算的更准。

```python
import random

def backoff(attempt: int, base: float = 0.1, cap: float = 5.0) -> float:
    return random.uniform(0, min(cap, base * 2 ** attempt))   # attempt 从 0 开始

ceilings = [min(5.0, 0.1 * 2 ** n) for n in range(8)]
print(ceilings)                                               # 上限：翻倍到 5.0 封顶
print(all(0 <= backoff(n) <= c for n, c in enumerate(ceilings)))   # True
```

<details class="pt"><summary>延伸</summary>

测试里不要真睡：把 `sleep` 和随机源当参数传进来，测试传一个记录调用的假函数，既快又能断言“第 3 次等待不超过 0.4 秒”。

</details>

**知识点：**重试与退避（Retry & Backoff）
