---
id: problems-parking-lot-allocation-function-not-class
node: problems.machines.parking-lot
type: qa
step: 3
tags: [grown]
---
## Q
停车场设计里“离入口最近优先”和“把车流分摊到各层”这两种车位分配规则，为什么适合写成两个普通函数，而不是一个 `AllocationStrategy` 抽象基类配两个实现类？

## A
这两种分配规则在多次调用之间都不需要记住任何东西——不缓存上次分配到哪一层，不维护计数器，纯粹是“给车辆和当前空闲车位表，算出选哪一个”的一次性计算。`abc.ABC`/`typing.Protocol` 该在“确实有好几种实现、且实现之间共享状态或还需要额外方法”时才用；给一次性计算包一层抽象类，只是多了一层从来不会被复用的壳。函数签名 `Callable[[Vehicle, FreeByFloor], ParkingSpot | None]` 本身就是接口，调用方直接传函数即可。
