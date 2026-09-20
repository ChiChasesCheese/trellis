---
id: structure-state-entry-exit-actions
node: structure.state-machines
type: qa
step: 4
---
## Q
进入 SHIPPED 状态要发邮件通知客户、停掉取消倒计时、释放预留库存——这些副作用应该写在哪里，先后顺序要遵守什么规则？

## A
写在状态机本身内部，不是每个调用方各自记得做一遍——否则每个调用 `transition_to` 的地方都要背下完整的副作用清单。

规则是**先校验守卫、再切换状态、最后执行副作用**，副作用要在状态真正落地**之后**才运行：

```python
def ship(self) -> None:
    if not self._can_ship():
        raise ValueError("cannot ship")
    self._state = State.SHIPPED       # 先切状态
    self._release_reservation()       # 再执行副作用
    self._notify_customer()
```

如果顺序反过来，副作用先跑、状态切换又失败（比如中途抛异常），就会出现"邮件发了，但订单其实还没真的变成 SHIPPED"这种不一致。
