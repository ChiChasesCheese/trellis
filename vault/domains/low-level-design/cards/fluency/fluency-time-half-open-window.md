---
id: fluency-time-half-open-window
node: fluency.time-numbers
type: qa
step: 3
---
## Q
重置令牌有效期 30 秒，代码写成 `age <= timedelta(seconds=30)`；另一处活动“未来 7 天内”写成 `abs(start - now) <= 7 天`。边界上各出什么错？时间窗口默认该用哪种区间？

## A
**时间窗口默认半开：含起点，不含终点**

- **半开 `[start, end)`**：`start <= t < end`；令牌有效期是 `[0, 30)` 秒，恰好 30 秒已过期；相邻窗口（每小时一桶、周六 0 点到周一 0 点）首尾相接，每个时刻恰好落进一个窗口，不重叠也不漏；
- **用 `<=` 的后果**：同一时刻既属于上一个窗口又属于下一个，计数多算一次；令牌多活一个刻度；
- **窗口要有方向**：`abs(start - now)` 会把已经开始过的活动也放进“未来 7 天”；要同时写下界 `now <= start` 和上界；
- **时钟倒退**：记录创建时间晚于 `now`（年龄为负）要当无效处理，别让负数通过 `< 30`；
- **例外要来自合同**：需求写“含两端”（闭区间）才用 `<=`，闭区间的个数要加一；把用的是哪种区间写进测试：边界前一刻、恰好边界、边界后一刻各测一次。

```python
from datetime import datetime, timedelta, timezone
TTL = timedelta(seconds=30)

def token_valid(created: datetime, now: datetime) -> bool:
    return timedelta(0) <= now - created < TTL    # [0, 30)：负龄无效，恰好 30 秒过期

t0 = datetime(2026, 1, 1, tzinfo=timezone.utc)
for s in (-1, 0, 29.9, 30):
    print(s, token_valid(t0, t0 + timedelta(seconds=s)))   # False True True False
```

**知识点：**时间与数字（Time & Numbers）
