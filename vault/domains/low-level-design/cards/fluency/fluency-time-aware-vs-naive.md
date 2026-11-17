---
id: fluency-time-aware-vs-naive
node: fluency.time-numbers
type: qa
step: 1
---
## Q
数据库里有旧的 `datetime(2026, 11, 17, 9, 0)`（没有时区），新记录带 `+09:00`。服务要比较它们的先后。为什么直接比会抛错？存储和比较时应该统一成什么，`replace(tzinfo=…)` 和 `astimezone(…)` 各管哪种值？

## A
**存带时区的 UTC；无时区贴标签，有时区换算**

- **无时区（naive）与有时区（aware）**：前者只是一组钟面数字，不指向任何时刻；后者指向唯一的时刻。两者混着比较，Python 直接抛 `TypeError`，不去猜；
- **存储约定**：一律存 aware 的 UTC 时刻，展示时才换成用户的时区；服务内部不出现“本地时间”；
- **`replace(tzinfo=UTC)`**：只改标签，钟面数字不动；只用在“我知道这个无时区值本来就是 UTC”的旧数据上；
- **`astimezone(UTC)`**：保持同一时刻，换算钟面；用在已经带时区的值上；对 naive 值它会按机器本地时区去猜，换一台机器结果就变，所以不要对 naive 值用；
- **常见错**：对带 `+09:00` 的值调 `replace(tzinfo=UTC)`，时刻凭空偏了 9 小时，而且不报错。

```python
from datetime import datetime, timezone, timedelta
UTC = timezone.utc

def to_utc(ts: datetime) -> datetime:
    if ts.tzinfo is None:             # 旧数据：约定它本来就是 UTC
        return ts.replace(tzinfo=UTC)
    return ts.astimezone(UTC)         # 同一时刻，换成 UTC 钟面

tokyo = datetime(2026, 11, 17, 9, 0, tzinfo=timezone(timedelta(hours=9)))
print(to_utc(datetime(2026, 11, 17, 9, 0)))   # 2026-11-17 09:00:00+00:00
print(to_utc(tokyo))                          # 2026-11-17 00:00:00+00:00
print(tokyo.replace(tzinfo=UTC))              # 09:00 UTC：错标，差了 9 小时
```

<details class="pt"><summary>延伸</summary>

`datetime.utcnow()` 返回的是 naive 值，容易被误当成 aware；用 `datetime.now(timezone.utc)`。“无时区旧值按 UTC 解释”是一条要写进合同和测试的约定，不是 Python 的默认。

</details>

**知识点：**时间与数字（Time & Numbers）
