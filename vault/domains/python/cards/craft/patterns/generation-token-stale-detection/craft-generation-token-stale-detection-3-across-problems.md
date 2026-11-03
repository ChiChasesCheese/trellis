---
id: craft-generation-token-stale-detection-3-across-problems
node: craft.patterns.generation-token-stale-detection
type: qa
step: 3
---
## Q
**代号令牌 · 熔断器、叫车、库存里同一个「这个结果属于哪一轮」**｜模式

熔断器的 `_gen`、叫车系统的 `release(driver_id, offer_id)`、库存堆条目里的 `expires_at == at`，看起来无关。它们共同防的是哪种错？为什么叫车的释放函数要带 `offer_id`？

## A
**要点。** 防的都是「迟到的操作作用在已经换了一轮的状态上」。做法一致：把轮次显式放进令牌，操作时比较一次。叫车里的清扫任务在要约 1 超时后才跑，而司机早已拒绝要约 1 并接了要约 2；只按 `driver_id` 释放，会把正在跑单的司机打回空闲。

```python
# api-circuit-breaker._record：代号对不上，只计数
if gen != self._gen:
    return

# ride-sharing.release：只在仍被这张要约持有时才释放
if driver is None or driver.held_by != offer_id:
    return False

# inventory-management：堆条目带着当时的到期时间
if entry.status is Status.ACTIVE and entry.expires_at == at:
    self._release(entry)
```

要约 1 的迟到清扫，作用在已经 ON_TRIP（要约 2）的司机上：

```
只按 driver_id  -> 司机状态: AVAILABLE
带 offer_id 比对 -> 司机状态: ON_TRIP
```

**不变。** 令牌由「发出这次操作的一方」在发出时领取，在应用时核对。**变化。** 令牌的形状：整数代号、要约 ID、到期时间戳，核心都是「相等才生效」。

**见于。** api-circuit-breaker、idempotent-transfer、ride-sharing、inventory-management。

**信号。** 有超时、延迟任务、回调、租约、重试；有人会在状态已经换了一轮之后才来「完成」「释放」「回报」。
