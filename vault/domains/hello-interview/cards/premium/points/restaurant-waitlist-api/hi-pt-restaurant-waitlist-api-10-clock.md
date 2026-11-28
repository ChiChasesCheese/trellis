---
id: hi-pt-restaurant-waitlist-api-10-clock
node: qb.lld.restaurant-waitlist-api.points
type: qa
step: 10
---
## Q
**餐厅候位 API · 注入时钟**｜追问 · 出自：餐厅候位 API › 深入 5

等位估计要用到"现在几点"。为什么把时钟做成构造参数？测试里怎么用？

## A
**做法。** `clock: Callable[[], datetime]` 作为构造参数注入，代码里只调 `self._clock()`，不直接调 `datetime.now()`。

**测试。** 用一个可拨动的假时钟，`now += timedelta(minutes=30)` 就能验证 18:30 的估计，完全不用 `sleep`。

**对比。** 直接调系统时钟的代码，无法测试等位估计（注入时钟）。
