---
id: hi-pt-dasher-payout-1-facts-not-money
node: qb.lld.dasher-payout.points
type: qa
step: 1
---
## Q
**配送员报酬计算 · 存事实现算钱**｜必会 · 出自：配送员报酬计算 › 深入 1

外部服务持续推来配送事件，报酬是边收事件边往余额里累加，还是保存事件、需要时现算？乱序、重复、更正时哪种更稳？

## A
**选择。** 保存事实（`Event` 与配对后的 `Delivery`），钱每次现算。

**为什么。** 累加的写法遇到乱序、重复、更正就得回滚旧账；现算只要事实表对，钱就对。代价是每次查询重新算，假设一个周期几百单，可以忽略；规模化再加缓存或预聚合。

**结构。** `price_by_acceptance` 是纯函数，`Payroll` 只负责取数据（外部服务通过 `fetch_events` 注入）再调用它。
