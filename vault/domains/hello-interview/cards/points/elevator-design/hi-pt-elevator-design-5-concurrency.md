---
id: hi-pt-elevator-design-5-concurrency
node: qb.lld.elevator-design.points
type: qa
step: 5
---
## Q
**电梯系统 · 并发：单写者原则**｜必会 · 出自：电梯系统 › 深入 3

多个楼层的乘客同时按按钮，电梯状态怎么避免加锁？

## A
**要点。** 单写者原则：外部线程只往线程安全的请求队列放请求对象，由控制器的调度线程在 `tick` 里取出并修改电梯状态，所以 `Elevator` 内部不需要锁，也没有「边移动边被修改」的竞争。
**读。** 显示屏通过快照或观察者通知。
