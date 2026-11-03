---
id: hi-pt-parking-lot-system-2-compat-table
node: qb.lld.parking-lot-system.points
type: qa
step: 2
---
## Q
**停车场管理系统 · 车型与车位兼容表**｜必会 · 出自：停车场管理系统 › 深入 1

摩托可以停小型位，大型车不能停小型位。这种规则放在继承里还是数据里？怎么分配？

## A
**要点。** `COMPAT` 表：车型 → 按偏好顺序的车位类型（摩托 SMALL、REGULAR、LARGE；小车 REGULAR、LARGE；卡车 LARGE）。先试最合适的类型再升级，贪心地把大车位留给大车。
**为什么。** 停车规则是数据不是行为，用表更易修改；继承（Car 继承 Vehicle 各自判断）会让类层次膨胀。
