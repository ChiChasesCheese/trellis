---
id: amz-parking-fees-followup-daily-cap-per-calendar-day
node: amazon.amz-parking-fees
type: qa
step: 6
tags: [grown]
---
## Q
在 Amazon 停车场计费设计里，面试官追加「每辆车每天最多收一个封顶额」，改哪里？跨多天的停留怎么封？

## A
封顶放在 `Tariff.daily_cap`（按车型的数据），`FeeEngine` 在每个日历日结算时取 `min(当日应收, 封顶)`，切段循环一行不动。因为切段已经在午夜断开，所以天然按日历日封顶。例：摩托车封顶 1000 分，周四 08:00 到周六 08:00，三天各收 1000、1000、800，共 2800；若不分天、整体封一次顶则只收 1000。「入场起 24 小时」的封顶是另一种口径，要在澄清阶段问清。
