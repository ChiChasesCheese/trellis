---
id: problems-online-shopping-transition-table
node: problems.marketplaces.online-shopping
type: qa
step: 3
tags: [grown]
---
## Q
电商订单有 created/paid/shipped/delivered/cancelled 五个状态。为什么用一张显式的“谁能变成谁”转移表，而不是几个布尔字段，也不是给每个状态建一个类（State 模式）？

## A
布尔字段的问题不是丑，是**它能表达非法状态**：n 个布尔有 2ⁿ 种组合而合法状态只有 5 种，`is_paid and is_cancelled` 同时为真该怎么理解没人答得上；枚举让非法状态根本无法被表示。State 模式的收益在于“同一个方法在不同状态下行为不同”，而订单在各状态下什么也不做，唯一的差别是**允许往哪走**——为纯粹的许可关系建五个类、写十几个空方法，是把一张五行的表摊成五个文件。判据：状态之间只有“允许/不允许”的差别用表，有行为和数据的差别才用类。表还能被程序读（画状态图、统计转移覆盖率）。
