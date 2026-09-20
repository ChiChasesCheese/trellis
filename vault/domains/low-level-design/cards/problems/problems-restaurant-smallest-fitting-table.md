---
id: problems-restaurant-smallest-fitting-table
node: problems.booking.restaurant
type: qa
step: 1
tags: [grown]
---
## Q
餐厅管理设计里，一拨两人的散客到店，如果同时有一张两人桌和一张四人桌都空着，会被安排到哪一张，这条规则背后的原则是什么？

## A
会被安排到两人桌——`FloorManager` 在所有容量够坐这拨人的空桌里，按 `(容量, 桌号)` 排序取最小的一张。原则是把大桌子留给真正需要它们的大团体：如果两人随手占了四人桌，下一拨四人的散客就要么等，要么被拆散，这张桌子的容量被浪费了。用 `(capacity, id)` 而不是只用 `capacity` 排序，是为了在多张同容量的桌子之间给出确定的选择，不依赖字典的迭代顺序，保证测试结果可复现。
