---
id: problems-parking-lot-display-board-zero-touch
node: problems.machines.parking-lot
type: qa
step: 7
tags: [grown]
---
## Q
停车场设计要新增一块按楼层显示空闲车位数的展示牌（`DisplayBoard`），如果 `ParkingLot` 从一开始就提供了 `subscribe(observer)` 这个订阅车位事件变化的挂钩，加这块展示牌需要改动 `ParkingLot` 的代码吗？这证明了设计的什么性质？

## A
不需要。`DisplayBoard` 在构造时调用一次 `lot.subscribe(self._on_event)` 把自己注册成观察者，`park`/`unpark` 在车位状态变化后调用已经存在的通知钩子，`ParkingLot` 本身一行代码都不用改。这证明了“对扩展开放、对修改关闭”不是一句口号：只要提前把“状态变化时通知谁”这个挂钩做成参数化的（一个订阅者列表），新的消费者就能以纯新增的方式接进来，而不需要回头改已经测试通过、正在跑的旧代码。
