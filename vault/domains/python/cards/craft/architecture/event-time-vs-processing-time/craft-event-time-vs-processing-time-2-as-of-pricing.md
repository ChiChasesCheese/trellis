---
id: craft-event-time-vs-processing-time-2-as-of-pricing
node: craft.architecture.event-time-vs-processing-time
type: qa
step: 2
---
## Q
**事件时间 vs 处理时间 · 出账时的价格该按用量发生时取，还是按出账时取**｜架构

云计费系统的价格会调整：第 0 到 99 秒单价 10，第 100 秒起单价 8。一条用量记录发生在 t=50，系统在 t=200 才出账。计算这条记录的金额时，用哪个时刻去查价格？明天重算同一张账单，结果应该变吗？

## A
**要点。** 用事件时间：用量发生时哪个价格版本生效，就用哪个。这样一张账单是「事实 + 版本表」的纯函数：只要这两样不变，今天、明天、一年后重算结果都一样，审计可以复现。用处理时间则结果取决于什么时候出账，同一笔用量会因为晚几天出账而变价。

```python
VERSIONS = [(0, 10), (100, 8)]                  # (生效时刻, 单价)
starts = [v[0] for v in VERSIONS]

def price_at(t):                                # as-of 查询：t 时刻生效的版本
    return VERSIONS[bisect_right(starts, t) - 1][1]

usage = [(50, 3), (120, 2)]                     # (用量发生时刻, 数量)
now = 200                                       # 出账时刻
print("按发生时刻取价:", sum(q * price_at(t) for t, q in usage))
print("按处理时间取价:", sum(q * price_at(now) for t, q in usage))
```

实际输出：

```
按发生时刻取价: 46
按处理时间取价: 40
```

**为什么。** 46 = 3×10 + 2×8，每条用量按自己发生时的价格；40 把 t=50 的用量也按新价格 8 算，少收了 6。账务里这叫 as-of 查询（某时刻当时的状态）。

**信号。** 看到交易记录里有 `ts`（发生时间）字段，或者价格、汇率、税率、费率有生效日期，就该用发生时刻去查，而不是 `now()`。
