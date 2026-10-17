---
id: amz-robot-restaurant-stage1-tick-flow-in-code
node: amazon.amz-robot-restaurant
type: qa
step: 3
tags: [grown]
---
## Q
在 Amazon 机器人餐厅设计里，第 1 关「一台机器人把一张单做完并送到」的推进循环怎么写？（离散时间：一刻 tick 是时间的最小单位）

## A
每刻先让机器人走一步，再给空闲机器人派单：
```python
def tick(self) -> None:
    with self._lock:
        self._now += 1
        for robot in self._robots:
            kind = robot.step()          # 扣电、减刻数，到点转移状态
            if kind is not None:
                self._log(kind, robot, robot.order)
        self._dispatch()                 # 队首订单 -> 能接的空闲机器人
```
时间只靠 `tick()` 推进，没有 `sleep`，所以测试可以逐刻断言。
