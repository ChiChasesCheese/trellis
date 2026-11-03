---
id: craft-half-open-intervals-1-checkout-day-is-free
node: craft.patterns.half-open-intervals
type: qa
step: 1
---
## Q
**半开区间 · 酒店 3 号退房的人和 3 号入住的人，为什么应该不冲突**｜模式

酒店订房：一位客人 1 号入住、3 号退房（住 1、2 两晚）；另一位 3 号入住、5 号退房。这两个订单应该能放进同一间房。如果把日期区间当成"包含两端"的闭区间 `[1, 3]`，判断重叠和计算晚数会遇到什么？更简单的约定是什么？

## A
**要点。** 把区间约定为**半开** `[check_in, check_out)`：包含起点，不包含终点。退房当天不算占用，所以 3 号退房的人和 3 号入住的人天然不重叠。判重叠只剩一条，不需要任何 `+1`/`-1` 或特判：`a.start < b.end and b.start < a.end`。晚数 = `check_out - check_in`，逐晚遍历是 `while d < check_out`。

```python
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class ClosedStay:                 # [check_in, check_out]：两端都算占用
    check_in: date; check_out: date
    def overlaps(self, o): return self.check_in <= o.check_out and o.check_in <= self.check_out
    @property
    def nights(self): return (self.check_out - self.check_in).days + 1     # 又要补一个 +1

@dataclass(frozen=True)
class Stay:                       # [check_in, check_out)：退房当天不算占用
    check_in: date; check_out: date
    def overlaps(self, o): return self.check_in < o.check_out and o.check_in < self.check_out
    @property
    def nights(self): return (self.check_out - self.check_in).days
    def each_night(self):
        d = self.check_in
        while d < self.check_out: yield d; d = date.fromordinal(d.toordinal() + 1)

d = lambda day: date(2026, 11, day)
for cls in (ClosedStay, Stay):
    a, b = cls(d(1), d(3)), cls(d(3), d(5))             # 1 号入住 3 号退房；3 号入住 5 号退房
    print(f"{cls.__name__:10} 1-3 与 3-5 重叠？{a.overlaps(b)}  1-3 住 {a.nights} 晚（应为 2）")
print("半开区间逐晚:", [x.day for x in Stay(d(1), d(3)).each_night()])
```

对比闭区间版本（`<=`，晚数要 `+1`）：

```
ClosedStay 1-3 与 3-5 重叠？True  1-3 住 3 晚（应为 2）
Stay       1-3 与 3-5 重叠？False  1-3 住 2 晚（应为 2）
半开区间逐晚: [1, 2]
```

**为什么。** 闭区间下"3 号"同时属于两个订单，要么拒绝一个合法的订单，要么在每处判断里补特例（把终点减 1 再比较）；而且这个 `-1`/`+1` 会漏在某个角落（晚数、逐晚遍历、费用）。半开区间把"差"直接就是长度：`end - start`。

**代价。** 终点是"开"的这件事必须在所有接口上约定一致，并写进类型的文档里；用户界面说"入住 1 号到 3 号"时，展示层可能要显示成 1–2 号。内部全部半开，在边界处翻译，比内部混用两种约定安全得多。

**判据。** 两个相邻区间应该能首尾相接（退房/入住、会议散场/开始、上一个周期结束/下一个开始）吗？应该，就用半开。
