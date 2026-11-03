---
id: craft-effective-dated-versions-1-price-by-event-time
node: craft.patterns.effective-dated-versions
type: qa
step: 1
---
## Q
**生效时间版本 · 费率变了，旧交易该按哪个版本算**｜写法

支付平台的手续费率从第 200 秒起由 2.9% 降到 2.5%。一笔发生在第 150 秒的交易，因为对账延迟，到第 300 秒才被处理。「按当前最新费率算」会得到什么？按交易发生时生效的版本算，数据该怎么存？

## A
**要点。** 费率是随时间分段的函数，不是一个变量。每次发布都新增一个版本（生效时间，规则），按生效时间升序存放；查询时用**交易自己的时间**去找最后一个不晚于它的版本。这样结果只取决于（交易，版本表），与处理时刻无关，重放、重算、迟到都得到同样的答案。

```python
from bisect import bisect_right
from dataclasses import dataclass

@dataclass(frozen=True)
class Schedule:
    starts: tuple[int, ...] = ()      # 各版本生效时间，严格升序
    rates: tuple[int, ...] = ()       # 同下标：该版本的费率（bps）

class Engine:
    def __init__(self): self.s = Schedule()
    def publish(self, effective_from, bps):
        if self.s.starts and effective_from <= self.s.starts[-1]:
            raise ValueError("生效时间必须晚于上一个版本")
        self.s = Schedule(self.s.starts + (effective_from,), self.s.rates + (bps,))
    def quote(self, amount, ts):
        s = self.s                                   # 读一次，之后都用这份快照
        v = bisect_right(s.starts, ts)               # 生效时间 <= ts 的版本个数 = 版本号
        if v == 0: raise LookupError(f"ts={ts} 没有生效的规则")
        return v, amount * s.rates[v - 1] // 10_000

e = Engine()
e.publish(100, 290); e.publish(200, 250)             # 第 200 秒起费率从 2.9% 降到 2.5%
print("ts=150:", e.quote(10_000, 150))               # 还在版本 1
print("ts=200:", e.quote(10_000, 200), "<- 恰好等于生效时间，属于新版本")
print("迟到的旧交易 ts=150，现在才处理:", e.quote(10_000, 150))
try: e.quote(10_000, 50)
except LookupError as ex: print(ex)
```

发布两个版本（100 起 2.9%，200 起 2.5%）后：

```
ts=150: (1, 290)
ts=200: (2, 250) <- 恰好等于生效时间，属于新版本
迟到的旧交易 ts=150，现在才处理: (1, 290)
ts=50 没有生效的规则
```

**为什么。** 按处理时刻的最新费率算，迟到的交易会被多收或少收，而且重放同一批交易两次，因为中间发布过新版本，会得到两个不同的账单，没法审计。没有任何版本覆盖的时间点要明确报错（`v == 0`），而不是悄悄按 0 费率收。

**代价。** 版本表只增不删（旧版本永远要能复算旧账）；查询需要二分，O(log 版本数)。
