---
id: hi-lld-elevator-10-extensions
node: lld.problem-breakdowns.elevator
type: qa
step: 10
---
## Q
**扩展追问：快速电梯、取消请求、并发**｜低层设计 · 题目拆解

面试官追问：加快速（express）电梯、支持取消楼层请求、多个呼叫同时到达，各自该怎么改？

## A
**要点。**

- 快速电梯：不要给 Request 加优先级字段，那会破坏单向扫描。给 Elevator 加 `isExpress` 和允许楼层集合（如 0、5、9），它的 `addRequest` 拒收其他楼层；控制器对这些楼层在快速电梯空闲时优先派它。Request 不用改。
- 取消：加 `removeRequest`，是 `addRequest` 的逆操作，从集合里删掉同一个 Request；`step()` 不变。真实电梯不能取消，因为亮着的按钮告诉后来的人这一站已排队。
- 并发：两个呼叫同时选中同一部「空闲」电梯，选与加必须原子；`step()` 一边遍历一边删，而 `addRequest` 同时在加，会并发修改。

**取舍。** 并发有两种解法：同一把锁罩住 `requestElevator` 和 `step`，简单但互相阻塞；或写入线程安全队列，`step` 开头一次性取空到工作集合，读写分离、无锁。前者好讲，后者更优雅。
