---
id: hi-lld-elevator-3-controller
node: lld.problem-breakdowns.elevator
type: qa
step: 3
---
## Q
**ElevatorController：无队列的立即派发**｜低层设计 · 题目拆解

设计 ElevatorController 的状态和方法时，要不要在控制器里放一个「未分配请求队列」？它的接口应该长什么样？

## A
**要点。** 控制器只持有 `elevators: List<Elevator>`。呼叫一到，立刻选定一部电梯，交给它的请求集合，控制器自己不再保留状态。

```python
class ElevatorController:
    def __init__(self) -> None:
        self.elevators: list[Elevator] = [Elevator() for _ in range(3)]
    def request_elevator(self, floor: int, type: RequestType) -> bool: ...
    def step(self) -> None:   # 把时间推进一格
        for e in self.elevators:
            e.step()
```

**取舍。** 立即派发简单，面试里够用；但若被问「所有电梯都忙怎么办」，就得换成控制器持有待处理队列、电梯来拉取的模型。

**易错。** `request_elevator` 的参数用 `RequestType`（并拒绝 DESTINATION），而不是 `Direction`：楼层呼叫不可能是 IDLE，用 Direction 会放进非法值，只能靠运行时检查。
