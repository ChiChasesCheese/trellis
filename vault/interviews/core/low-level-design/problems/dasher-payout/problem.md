# 配送员薪资（Dasher Payout）

外卖平台按配送员在每个状态上花的分钟数付钱：去餐厅的路上、在餐厅等餐、送餐，三种状态的每分钟单价不同；午晚高峰还有倍率。你要写一个薪资内核：收配送事件，算出每一单和每位配送员应得的钱。不需要界面，用 `Payroll` 类，金额一律用 `Decimal`。

一单的生命周期有四个事件，时间点依次是 `ACCEPT`（接单）、`ARRIVE`（到店）、`PICKUP`（取餐）、`DROPOFF`（送达）。相邻事件之间是一段：接单到到店按 `TO_RESTAURANT`，到店到取餐按 `WAITING`，取餐到送达按 `DELIVERING`。一段的钱 = 每分钟单价 x 秒数 / 60。

**分关要求**（做完一关再看下一关）
- 第 1 关（约 25 分钟）：事件与基础计价。
  - `Payroll(plan: PayPlan)`；`PayPlan(rates: Mapping[State, Decimal], peaks=(), min_delivery_pay=Decimal("0"))`，`rates` 缺任何一个状态或有负数抛 `ValueError`。
  - `record(driver_id, delivery_id, event: EventType, at: datetime) -> None`：事件可以乱序到达。订单属于第一次上报它的配送员，别人再报抛 `DriverMismatchError`；同一类事件用同样的时间重复上报被忽略，时间不同抛 `ConflictingEventError`；新事件的时间必须落在生命周期里前后已知事件之间（允许相等），否则抛 `InconsistentTimelineError`。失败的调用不改变任何状态。
  - `delivery_pay(delivery_id) -> Decimal`：只有两端事件都已知的段才计费；整单的钱四舍五入（0.5 进位）到分，只在最后舍入一次。没有这一单抛 `UnknownDeliveryError`。
  - `driver_payout(driver_id) -> Decimal`：该配送员所有订单的 `delivery_pay` 之和；没有订单返回 `Decimal("0.00")`。
  - 例：费率 去餐厅 0.25、等餐 0.10、送餐 0.30。12:00 接单、12:10 到店、12:15 取餐、12:35 送达：`10x0.25 + 5x0.10 + 20x0.30 = 9.00`。
- 第 2 关（约 20 分钟）：高峰倍率。
  - `PeakWindow(start: time, end: time, multiplier: Decimal)`：每天重复的时段，左闭右开；`end == time(0)` 表示到当天午夜（所以跨午夜的窗口写成两个）。`peaks` 里的窗口不能互相重叠、必须 `start < end`（或 `end` 为午夜）、倍率必须为正，否则 `PayPlan` 抛 `ValueError`。
  - 一段跨过窗口边界时在边界处切开，每一小段用自己的倍率（不在任何窗口内的倍率为 1）。一段可以跨过多个窗口，也可以跨天。
  - 例：窗口 11:00 到 14:00 倍率 1.5。10:50 接单、11:10 到店：`0.25 x (10 + 10x1.5) = 6.25`。
- 第 3 关（约 15 分钟）：保底与结算周期。
  - `min_delivery_pay`：四个事件都齐了的订单（已送达）至少付这么多，保底和高峰后的金额比较，未送完的订单不保底。
  - `payout(driver_id, start, end) -> Decimal`：结算周期 `[start, end)`，只统计已送达、`DROPOFF` 时间落在周期内的订单，整单的钱记入该周期（不按每段发生的时间拆）。
- 第 4 关（选做）：更正与明细。
  - `correct_event(delivery_id, event, new_at) -> None`：更正一个已记录事件的时间。没有这一单抛 `UnknownDeliveryError`；事件没记录过抛 `MissingEventError`；时间线矛盾抛 `InconsistentTimelineError` 且保持原样。更正后所有金额和周期汇总随之变化。
  - `delivery_breakdown(delivery_id) -> list[PaySegment]`：按时间顺序列出每个计费小段（已按高峰边界切开）：`state`、`start`、`end`、`multiplier`、`amount`（精确到 4 位小数）。

**评分点**
- 只存事实（每单的四个时间点），钱每次现算：乱序、重复、更正都不需要回滚旧账。
- 金额只在整单的最后舍入一次；内部用精确算术，不用 `float`，也避免 `Decimal` 除以 60 的循环小数。
- 切段逻辑独立成一个函数：给定一段和窗口表，产出若干带倍率的小段；窗口边界的开闭区间处理正确。
- 校验在写入之前完成，失败不留半成品；幂等上报与冲突上报区分开。
- 保底和结算周期各是一处小改动，不需要改动前两关的接口。
- 能解释"整单记入送达所在的周期"这个选择的取舍，以及它与"按每段发生的时间拆分"的区别。
- 时间由调用方传入，测试里没有 `sleep`、没有读系统时钟。
- 能讲出跨时区和夏令时会在哪里出问题。
