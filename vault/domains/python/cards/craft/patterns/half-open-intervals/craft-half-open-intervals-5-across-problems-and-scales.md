---
id: craft-half-open-intervals-5-across-problems-and-scales
node: craft.patterns.half-open-intervals
type: qa
step: 5
---
## Q
**半开区间 · 会议室、酒店、额度、库存预留、日程里的同一个约定，放大到 API 和存储**｜模式

Meeting Rooms、酒店订房、额度包有效期、库存预留过期、会议日程，都在处理区间。它们共享什么约定？在分布式的接口里，这个约定在哪里出现，又有哪些著名的反例？

## A
**要点。** 同一个约定：区间包含起点、不包含终点。判重叠 `a.start < b.end and b.start < a.end`；相邻区间首尾相接且不冲突；长度 `end - start`；周期分割时间轴。

```python
# LeetCode 252 Meeting Rooms：结束时刻等于下一个开始时刻，不冲突
return all(prev[1] <= cur[0] for prev, cur in pairwise(ordered))
# hotel-booking / meeting-scheduler：判重叠只剩一条
return self.start < other.end and other.start < self.end
# inventory-management：预留有效期左闭右开，恰好到点就算过期
while self._expiry and self._expiry[0][0] <= now:
# credit-token-balance：额度包 at 含、expires_at 不含
at: datetime                       # 从这一刻起可用（含）
expires_at: datetime | None = None  # 到这一刻失效（不含）
```

**见于。** meeting-rooms、hotel-booking、dasher-payout、inventory-management、credit-token-balance、meeting-scheduler。

**不变的。** 起点含、终点不含；所有判断由 `<` 而不是 `<=` 写成；非法（空或反向）区间在构造时拒绝。**变化的。** 区间的轴（日期、时刻、一天里的秒数、序号）。

**信号。** 需求里出现"退房当天""结束时刻就是下一个开始""到期那一刻""恰好""相邻"；或者你的代码里出现 `+ 1`、`- 1`、`<=` 与 `<` 混着写，而它们又没有统一的解释。

**尺度对照。** 力扣：区间题的排序加相邻比较。低层设计：半开区间类型 + 构造时校验。分布式与存储：时间范围查询写成 `ts >= start AND ts < end`，分片的 key 范围常写成 `[low, high)`，让相邻分片恰好首尾相接。**反例**：HTTP 的 `Range: bytes=0-499` 是闭区间（含两端，共 500 字节），SQL 的 `BETWEEN` 也是闭区间；与这些系统对接时，要在边界处显式翻译，内部保持半开。变化：单机里出错只是少算一晚；跨系统时边界约定不一致，会在每个结算周期末、每个分片交界处，悄悄多算或漏算一个事件。
