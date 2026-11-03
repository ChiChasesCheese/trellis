---
id: craft-idempotency-key-stores-result-4-owner-failure-release
node: craft.patterns.idempotency-key-stores-result
type: qa
step: 4
---
## Q
**幂等键存结果 · 拥有者失败后键怎么办**｜写法

拥有者占了键，调用网关时超时抛了异常。键还留在表里，没有结果。之后用同一个键重试，或者另一个正在等它的请求，会发生什么？应该怎么处理？

## A
**要点。** 拥有者失败而没有存结果，等于留下一条死记录：之后所有同键请求都等不到结果（或永远等）。拥有者要对自己的失败负责：还没产生副作用就释放键，让重试能重新竞争；并且无论成败都要唤醒等待者，让它们醒来后重新判断。

```python
if owner:
    try:
        slot.result = work()
        return slot.result
    except BaseException:
        if release_on_error:
            with mu:
                del slots[key]          # 释放键，允许重试
        raise
    finally:
        slot.event.set()                # 无论成败都唤醒等待者
```

第一次调用抛 `网关超时`，同一个键再调用一次，实际输出：

```
拥有者失败: 网关超时
release_on_error = False -> 重试结果: 键被死记录占着，永远没有结果
拥有者失败: 网关超时
release_on_error = True -> 重试结果: ok
```

**代价。** 如果失败发生在副作用之后（钱已经扣了），不能直接释放键，否则重试会重复扣款；这时要靠租约（lease）：键带开始时间，超时后新拥有者接手，并且接手前要确认旧拥有者没有提交。参考解里用租约和「旧一轮不能再动钱」检查来处理。

**易错。** 只在 `except` 里唤醒、不在 `finally` 里唤醒，会漏掉非 `Exception` 的退出。
