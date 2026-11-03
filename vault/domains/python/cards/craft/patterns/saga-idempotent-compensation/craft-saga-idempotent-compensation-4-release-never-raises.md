---
id: craft-saga-idempotent-compensation-4-release-never-raises
node: craft.patterns.saga-idempotent-compensation
type: qa
step: 4
---
## Q
**Saga 与幂等补偿 · 为什么 release、cancel 这类方法要幂等且永不抛**｜模式

订座的 `release`、航班的 `release`、叫车的 `release`，三份参考解的注释都写着「幂等，且永不抛异常，因为它总跑在失败路径上」。这个规则从哪里来？

## A
**要点。** 这些方法的调用点在 `except` 和 `finally` 里：支付失败后放座位、预订失败后放航班、要约超时后放司机。它们被调用时，真正的错误已经发生，同一个清理可能被调两次（重试、超时清扫和用户取消同时到），清理的对象也可能压根没占上。清理再抛异常，既盖住真正的错误原因，又让清理自己中断。

```python
# movie-booking.release：支付失败、退出选座时放回座位
"""主动放弃一张收据，返回退回的座位数。故意做成幂等且不抛异常：
它总跑在失败路径上，再抛异常只会盖掉真正的错误原因。"""

# airline.release：幂等地把订单从这一班摘掉
with self._lock:
    self._drop_seat(ref)
    return self._sold.pop(ref, None) is not None

# ride-sharing.release：只在仍被这张要约持有时才释放
if driver is None or driver.held_by != offer_id:
    return False
```

失败路径上清理一个没占上的 ref：

```
严格释放 -> 调用方看到: KeyError
幂等释放 -> 调用方看到: ConnectionError
重复释放同一个 ref: True False
```

**不变。** 返回值（`bool` 或计数）告诉调用方「这次真的释放了吗」，而不是靠异常。**变化。** 释放的对象：座位、订单座位号、司机。

**见于。** online-shopping、atm、movie-booking、airline、ride-sharing。

**信号。** 方法名叫 release、cancel、rollback、undo、close，且会被放在 `finally` 或 `except` 里调用。
