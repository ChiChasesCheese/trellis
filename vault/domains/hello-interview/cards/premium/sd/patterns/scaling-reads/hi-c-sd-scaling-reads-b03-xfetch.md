---
id: hi-c-sd-scaling-reads-b03-xfetch
node: sd.patterns.scaling-reads.beyond
type: qa
step: 3
---
## Q
**读扩展 · 概率性提前刷新的公式**｜拓展 · 加分

"越老越可能刷新"具体怎么算才不会拍脑袋定概率？

## A
```python
import math
import random


def should_refresh(now: float, expiry: float, recompute_cost: float, beta: float = 1.0) -> bool:
    # XFetch：recompute_cost 是上次重建耗时。-ln(U) 是非负随机数，
    # 重建越贵，越早开始以较大概率刷新；beta>1 更激进
    return now - recompute_cost * beta * math.log(random.random()) >= expiry
```
- **效果：** 重建耗时 5 秒、离过期还有 10 秒时，约 14% 的请求会触发刷新；还剩 2 秒约 67%；快过期时接近 100%。刷新被分散到临近过期的一段时间，并且大概率只有一两个请求先触发。
- **优于固定阈值：** 不需要协调者，每个请求独立抛骰子；重建越贵越早刷新。
- **配合：** 发现要刷新的请求在后台重建，其余请求继续返回旧值（等价于 HTTP 的 stale-while-revalidate 思路）。
- **不够时：** 对绝对不能击穿的数据，仍用后台定时刷新。
