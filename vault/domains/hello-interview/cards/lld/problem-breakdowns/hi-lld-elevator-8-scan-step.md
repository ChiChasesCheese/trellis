---
id: hi-lld-elevator-8-scan-step
node: lld.problem-breakdowns.elevator
type: qa
step: 8
---
## Q
**SCAN 的 step()：五种情形**｜低层设计 · 题目拆解

写出 SCAN 版 `Elevator.step()` 的逻辑，每一步为什么那样排顺序？

## A
```python
def step(self) -> None:
    if not self.requests:                 # 1 无事可做，别往下漂
        self.direction = Direction.IDLE; return
    if self.direction is Direction.IDLE:  # 2 先定方向：取最近请求，平局取低楼层（要确定性）
        nearest = min(self.requests, key=lambda r: (abs(r.floor - self.floor), r.floor))
        self.direction = Direction.UP if nearest.floor > self.floor else Direction.DOWN
    pick = RequestType.PICKUP_UP if self.direction is Direction.UP else RequestType.PICKUP_DOWN
    here = {Request(self.floor, pick), Request(self.floor, RequestType.DESTINATION)}
    if here & self.requests:              # 3 停靠：只收同向呼叫和目的地
        self.requests -= here
        if not self.requests: self.direction = Direction.IDLE
        return                            # 停靠这一拍不移动
    if not self.has_requests_ahead(self.direction):   # 4 前方没请求，换向，下一拍再判断
        self.direction = Direction.DOWN if self.direction is Direction.UP else Direction.UP
        return
    self.floor += 1 if self.direction is Direction.UP else -1   # 5 走一层
```

**易错。** 不要用 `iterator().next()` 从哈希集合取元素，顺序不确定，模拟跑不稳；停靠后忘了 `return` 会边停边走。
