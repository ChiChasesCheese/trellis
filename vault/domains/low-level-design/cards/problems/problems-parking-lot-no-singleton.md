---
id: problems-parking-lot-no-singleton
node: problems.machines.parking-lot
type: qa
step: 5
tags: [grown]
---
## Q
停车场设计里，“现实中一栋楼只有一个停车场”这个业务事实，是否意味着 `ParkingLot` 类应该用 `__new__` 拦截构造、做成 Singleton？为什么？

## A
不应该。业务上唯一和代码结构上是否拦截构造是两回事：Singleton 会让测试没法同时造两座互不干扰的停车场（比如一个测并发、一个测计费），第二次构造要么报错要么悄悄返回第一次的对象，测试之间会共享隐藏状态。更根本的问题是 Singleton 把“这是唯一实例”这件事藏进了构造过程，调用方看着 `ParkingLot(spots, ...)` 这行代码完全看不出全局唯一这条约束。真需要进程内唯一一份时，在应用启动的组合根里手动创建一次、往下传，比在类内部锁死构造过程更诚实。
