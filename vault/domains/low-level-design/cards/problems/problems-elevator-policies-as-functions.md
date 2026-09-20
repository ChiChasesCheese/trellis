---
id: problems-elevator-policies-as-functions
node: problems.machines.elevator
type: qa
step: 5
tags: [grown]
---
## Q
电梯系统里有两个可替换点——“这部梯下一站去哪”和“这个外呼派给哪部梯”。在 Python 里用什么形式表达它们最合适？为什么不用抽象基类？

## A
用普通函数，签名本身就是接口。两组算法在调用之间都不需要记住任何东西（该记的方向已经在传进去的快照里），所以 `abc.ABC` 或 `typing.Protocol` 只会多一层从不被复用的壳。只有当策略需要跨调用保存状态（比如轮流派梯要记住上次派给了谁），或者要对外暴露第二个方法（比如“为什么派给它”的解释接口），才升级成带 `__call__` 的类，而调用方代码一个字都不用改。另一半同样重要：这是两个独立的可替换点，揉进一个 `schedule()` 会导致想换派梯规则就不得不碰 SCAN 的代码。

```python
ServicePolicy = Callable[[CarSnapshot], int | None]
DispatchPolicy = Callable[[HallCall, Sequence[CarSnapshot]], str | None]

car = ElevatorCar('A', policy=scan, clock=clock)
bank = ElevatorBank(cars, dispatch=directional_dispatch, clock=clock)
```
