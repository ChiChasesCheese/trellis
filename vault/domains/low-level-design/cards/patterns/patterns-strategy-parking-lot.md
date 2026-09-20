---
id: patterns-strategy-parking-lot
node: patterns.strategy
type: qa
step: 5
---
## Q
停车场系统里，"计费策略"和"车位分配策略"为什么都适合用 Strategy 建模？

## A
两者都是"输入契约不变、算法本身会变"：计费会按车型、时长、会员折扣变化；分配会按"离入口最近优先"「按车型匹配车位尺寸」等规则变化。把它们都做成可替换的函数或小类之后，核心的 `ParkingLot.park()` / `checkout()` 完全不用因为新增一种定价或分配规则而修改——只需要新写一个策略、在注册表里加一行。
