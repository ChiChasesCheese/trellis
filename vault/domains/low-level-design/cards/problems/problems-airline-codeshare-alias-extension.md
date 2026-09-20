---
id: problems-airline-codeshare-alias-extension
node: problems.booking.airline
type: qa
step: 8
tags: [grown]
---
## Q
航班管理设计里，代码共享（codeshare）航班——同一架飞机在另一家航司目录里挂着不同航班号——是怎么加进设计的，为什么不碰订座代码？

## A
`Flight` 加一个 `marketed_as` 字段记市场航班号，`AirlineService.schedule` 把这些市场航班号登记成指向同一个 `FlightInstance` 对象的别名，而不是新建一份库存。因为改动只发生在“航班号 → 对象”这张目录索引上，`hold`、`reserve_across`、`board` 等所有操座位的代码一行都不用改——这正是“新需求不碰已有代码”的验收标准：如果给共享航班单独建一份库存，两边各卖各的，加起来会卖穿实际座位数。
