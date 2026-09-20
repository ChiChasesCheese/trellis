---
id: problems-parking-lot-spot-owns-state
node: problems.machines.parking-lot
type: qa
step: 1
tags: [grown]
---
## Q
在停车场（Parking Lot）设计里，车位的占用状态应该放在 `ParkingSpot` 对象自己身上，还是让 `ParkingLot` 另外维护一个 `occupied: set[str]` 集合？为什么？

## A
放在 `ParkingSpot` 自己身上（比如一个 `vehicle: Vehicle | None` 字段，`is_free` 是基于它的一个只读属性）。另开一个集合看起来像是给查询加了缓存，实际是引入了两份必须手动保持一致的状态——`park`/`unpark` 任何一处少更新一处，集合和车位的真实占用就会对不上，而这种 bug 通常只在并发路径下才会暴露。车位状态只留一份真源，`ParkingLot` 需要空闲表时现场遍历一次车位即可，车位数在几百到几千的量级完全够用。
