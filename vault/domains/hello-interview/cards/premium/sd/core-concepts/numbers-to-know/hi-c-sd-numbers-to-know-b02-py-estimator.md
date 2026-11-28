---
id: hi-c-sd-numbers-to-know-b02-py-estimator
node: sd.core-concepts.numbers-to-know.beyond
type: qa
step: 2
---
## Q
**必知数字 · 把估算写成小脚本**｜拓展 · 加分
怎么用几行 Python 把 QPS 与存储估算做得可复核？心算时有哪些近似技巧？

## A
**模式。** 把假设显式写成参数的估算器。
```python
from dataclasses import dataclass

SECONDS_PER_DAY = 86_400        # 心算时取 1e5，高估约 16%，足够数量级


@dataclass
class Load:
    dau: int                     # 日活用户
    actions_per_user: float      # 每人每天动作次数
    peak_factor: float = 3.0     # 峰值是平均的几倍：业务假设，必须说出来

    @property
    def avg_qps(self) -> float:
        return self.dau * self.actions_per_user / SECONDS_PER_DAY

    @property
    def peak_qps(self) -> float:
        return self.avg_qps * self.peak_factor


def storage_tb(records: int, bytes_each: int, replicas: int = 1) -> float:
    return records * bytes_each * replicas / 1e12


w = Load(dau=10_000_000, actions_per_user=5)
print(f"{w.avg_qps:,.0f}/s  {w.peak_qps:,.0f}/s")      # 579/s  1,736/s
print(f"{storage_tb(500_000_000, 1000, 3):.1f} TB")    # 1.5 TB
```
- **为什么写成参数：** 每个假设（日活、人均次数、峰值倍数、副本数）都是显式名字，面试官改一个条件你能立刻重算，也不会把推导藏在心里。
- **心算技巧：** 一天约 10 万秒（实际 8.64 万）；1 百万/天 ≈ 12 次/秒；1 KB × 1 百万 = 1 GB；2^10 ≈ 10^3 用来换算单位。
- **永远乘上峰值系数与副本数：** 平均值会让你低估容量，副本让存储乘 3。
- **结果要和上限对照：** 算出的数字立刻与硬件上限比较（"约 2 TB，一台数据库装得下"），算数是为了做决定。
