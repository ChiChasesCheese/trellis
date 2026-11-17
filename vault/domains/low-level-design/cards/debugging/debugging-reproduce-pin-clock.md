---
id: debugging-reproduce-pin-clock
node: debugging.reproduce
type: qa
step: 2
---
## Q
优惠券“只在当天 23:59:59 之前有效”，用户反馈偶尔在最后一秒被拒绝。这类只在特定时刻出现的缺陷，怎么在测试里稳定复现？为什么不该在代码里直接调用 `datetime.now()`？

## A
**时间是输入：把时钟注入进来，测试里钉在出问题的那一刻**

- **隐藏的输入无法重放**：函数内部读 `datetime.now()`，每次运行条件都不同，月底、夏令时切换、到点的那一秒都碰不到；
- **注入一个“取当前时间”的函数**：生产默认用真时钟，测试传 `lambda: 固定时刻`；
- **专挑边界时刻**：恰好到点、差一秒、跨日、跨月、闰年 2 月 29 日；
- **时区要带上**：带时区的 `datetime` 和不带的不能直接比较（会抛 `TypeError`），线上是 UTC、笔记本是本地时区，是常见的“只有我这里不复现”的来源；
- **第三方库**（如 `freezegun`）能冻结时间，但标准库的做法零依赖，也更显式。

```python
from datetime import datetime, timezone

class Coupon:
    def __init__(self, expires, clock=lambda: datetime.now(timezone.utc)):
        self.expires, self.clock = expires, clock

    def valid(self):
        return self.clock() < self.expires        # 到点那一刻算过期？

exp = datetime(2026, 11, 17, 23, 59, 59, tzinfo=timezone.utc)
for now in (exp.replace(second=58), exp, exp.replace(second=59, microsecond=1)):
    print(now.time(), Coupon(exp, clock=lambda: now).valid())
# 23:59:58 True / 23:59:59 False / 23:59:59.000001 False
```

注入时钟让“到点那一刻”变成一行输入；至于该用 `<` 还是 `<=`，是规格要回答的问题，复现只负责把它暴露出来。

**知识点：**稳定复现（Reproduce）
