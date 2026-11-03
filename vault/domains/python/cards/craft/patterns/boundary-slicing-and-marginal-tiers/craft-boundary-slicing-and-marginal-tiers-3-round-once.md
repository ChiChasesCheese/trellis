---
id: craft-boundary-slicing-and-marginal-tiers-3-round-once
node: craft.patterns.boundary-slicing-and-marginal-tiers
type: qa
step: 3
---
## Q
**边界切分与边际阶梯 · 切成很多小段以后，在哪里取整**｜模式

停车费按小时计价，白天 250 分/小时，夜里 100 分/小时。车在 05:59:30 进、06:00:30 出，跨过价格切换点，各停 30 秒。切成两段后，每段的钱是小数（夜里那 30 秒 0.83 分，白天 30 秒 2.08 分），收费必须是整数分，向上取整。每段各自取整，还是合计之后取整？

## A
**要点。** 只在**最后一步取整一次**。每小段只累加「单价 × 秒数」这个精确的整数，在需要出账的粒度（这里是每个日历日）上一次性换算、向上取整；再套这个粒度上的封顶。中间任何一步取整，都会把「向上取整」的误差累积进来：切的段越多，多收越多，而且切法（在哪里有边界）会改变总价，这是不该发生的。

```python
from datetime import datetime, timedelta

rate_at = lambda t: 100 if t.hour >= 22 or t.hour < 6 else 250      # 分/小时：夜里 22:00-06:00 便宜

def next_change(t):
    """下一个会让单价或日历日变化的时刻。"""
    day = datetime(t.year, t.month, t.day)
    return min(c for c in (day + timedelta(hours=6), day + timedelta(hours=22), day + timedelta(days=1)) if c > t)

def day_charges(entered, exited, cap=1200):
    units, at = {}, entered                               # 单位：分/小时 × 秒
    while at < exited:
        end = min(next_change(at), exited)
        units[at.date()] = units.get(at.date(), 0) + rate_at(at) * int((end - at).total_seconds())   # 先累加，不取整
        at = end
    out = []
    for day in sorted(units):
        raw = -(-units[day] // 3600)                      # 向上取整到分，每日只取整一次
        out.append((str(day), raw, min(raw, cap)))        # 再套当日封顶
    return out

def per_slice_ceil(entered, exited):                      # 对照：每一小段各自向上取整
    total, at = 0, entered
    while at < exited:
        end = min(next_change(at), exited)
        total += -(-rate_at(at) * int((end - at).total_seconds()) // 3600); at = end
    return total

e, x = datetime(2026, 11, 3, 5, 59, 30), datetime(2026, 11, 3, 6, 0, 30)    # 跨越单价切换点，各 30 秒
print("每日一次取整:", day_charges(e, x))
print("每小段各自取整的总额:", per_slice_ceil(e, x), "（两段 30 秒各向上取整成 1 分）")
```

```
每日一次取整: [('2026-11-03', 3, 3)]
每小段各自取整的总额: 4 （两段 30 秒各向上取整成 1 分）
```

**为什么。** 用 `-(-x // n)` 做整数向上取整，全程整数运算，没有浮点误差（`0.1 + 0.2` 那类）。两种取整的差是 1 分，看起来小，但乘上订单量，是商户对账时一定会追问的差额；而且「同一次停车被你的切点数量影响总价」在逻辑上站不住。

**怎么选粒度。** 取整点选在**业务上出账的单位**：停车是每个日历日（封顶也按日），账单是每一行规则，云账单是每个指标每个周期。粒度之内全部精确，粒度之间才取整。系统里取整点只有一处（`_to_minor`），换舍入规则（银行家舍入 vs 向上取整）只改一处。

**对照。** 账单引擎里 `Decimal` 的 `_bps(...)` 全程保持全精度，行之间才 `quantize` 一次；分账里用最大余数法保证取整后的和仍等于总数。
