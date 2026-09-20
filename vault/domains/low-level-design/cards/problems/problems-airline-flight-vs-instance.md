---
id: problems-airline-flight-vs-instance
node: problems.booking.airline
type: qa
step: 1
tags: [grown]
---
## Q
在航班管理（Airline Management）设计里，为什么要把“航班”拆成 `Flight` 和 `FlightInstance` 两个类，而不是只用一个 `Flight` 类给座位加一个日期字段？

## A
`Flight` 描述的是排班表上不随日期变化的规则（航班号、起降机场、机型、承运人），`FlightInstance` 才是把这条规则钉到某一天上、真正持有库存和锁的对象。不变的规则数据和每天都在变的库存状态生命周期完全不同：只用一个类要么把规则数据按日期复制成几百份，要么把库存状态硬塞进不该有状态的对象里，两条路都会让“同一航线不同日期库存不同”这件事无法干净地表达。
