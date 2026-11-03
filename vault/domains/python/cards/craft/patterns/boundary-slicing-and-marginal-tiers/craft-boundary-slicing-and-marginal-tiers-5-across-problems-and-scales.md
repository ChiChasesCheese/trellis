---
id: craft-boundary-slicing-and-marginal-tiers-5-across-problems-and-scales
node: craft.patterns.boundary-slicing-and-marginal-tiers
type: qa
step: 5
---
## Q
**边界切分与边际阶梯 · 手续费阶梯、云账单、配送员计酬、停车费、区间交集里的同一次切分**｜模式

金额阶梯、用量阶梯、高峰窗口、单价切换、LeetCode 的区间交集，看起来是完全不同的题。它们共享哪个动作？

## A
**要点。** 同一个动作：**找出所有边界，在边界处把一维区间切开，每一小段内部规则恒定，段内各自计算，再合并**。区间可以是金额轴、用量轴，也可以是时间轴；边界可以是档位上限、窗口起止点、价格切换点、日历日的零点。

```python
# billing-tax-engine / amz-aws-billing：沿金额或用量轴，用 lower 追踪上一个边界
top = amount if upper is None else min(amount, upper)
if top > lower: total += _bps(top - lower, bps)   # 此处 bps 是该档费率（基点）
# dasher-payout：沿时间轴，在窗口边界切开，用中点定倍率
points = sorted({start, end, *(c for c in self._boundaries(start, end) if start < c < end)})
# amz-parking-fees：沿时间轴，在价格变化时刻切开，按日累加，每日取整一次
end = min(self._tariff.next_change(at), exited)
# LeetCode 986 区间列表的交集：两个指针，重叠段 = 起点取大、终点取小
lo, hi = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

**见于。** billing-tax-engine、amz-aws-billing、dasher-payout、amz-parking-fees、interval-list-intersections。

**不变的。** 用 `min`/`max` 夹出每段的上下界，`lower` 追踪已经处理到哪里；每段内部规则恒定；最后合并并只取整一次。**变化的。** 轴是什么（金额、用量、时间）；段内的规则（费率、倍率、单价）；合并的方式（求和、取并、再套封顶）。

**信号。** 需求里出现「前 X 免费，超出部分……」「分档」「高峰时段」「夜间费率」「按天封顶」「跨天」；或者你发现自己在写 `if amount > threshold: rate = ...` 并觉得哪里不对。

**尺度对照。** 力扣：区间的交集与合并。低层设计：阶梯累进、窗口切分、取整点单一。分布式与真实产品：云服务的阶梯定价（用量越大单价越低，按月、按指标累计）、电力的阶梯电价、所得税的税率档；变化：用量是**跨机器、跨时间汇总**出来的，周期边界（月初零点，用哪个时区）和迟到的用量（上个月的用量下个月才到）成为主要难点，所以账单系统要把"用量事件"按事件时间归到周期，再对周期汇总一次计价，而不是边到边算。
