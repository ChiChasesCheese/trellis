---
id: craft-condition-wait-predicate-loop-4-predicate-across-problems
node: craft.patterns.condition-wait-predicate-loop
type: qa
step: 4
---
## Q
**条件变量等待循环 · 队列、发布订阅、调度器里等待的条件是什么**｜模式

阻塞队列等「有空位」，发布订阅的 BLOCK 策略等「最慢订阅者越过队头」，调度线程等「到下一个到期点」。三个等待写法很不一样，共同的规则是什么？带超时的等待怎么写才不会越等越久？

## A
**要点。** 共同规则：（1）谓词是状态，在 `while` 里检查；（2）想清楚「是什么变化会让谓词成立」，只在那些地方通知；（3）超时用绝对截止时间。发布订阅里日志变短不是等待者要的，而是「最慢的游标越过队头」才允许覆盖队头，所以通知点在游标前进的地方，而不是任意出队的地方。

```python
# bounded-blocking-queue.put
while len(self._items) >= self._capacity and not self._closed:
    self._wait_for(self._not_full, deadline, "put")

# pub-sub BLOCK：谓词是最慢游标没越过队头
while self._min_cursor() <= self._start_seq:
    remaining = None if deadline is None else deadline - time.monotonic()
    if remaining is not None and remaining <= 0:
        raise BackpressureError(...)
    self._not_full.wait(remaining)

# amz-emergency-pubsub：把谓词交给 wait_for
return self._cond.wait_for(lambda: not self._heap and not self._in_flight, timeout)
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

每次醒来都用完整的 timeout 重新等，被频繁 notify 时可能永远不返回；绝对截止每次只等剩余时间：

```
每次重等: 要求最多等 0.3s，1s 后仍未返回
绝对截止: 要求最多等 0.3s，1s 后在 0.35s 返回 False
```

**见于。** bounded-blocking-queue、pub-sub、amz-emergency-pubsub、task-scheduler。

**信号。** 一个线程要等「某个状态成立」才继续；你想写 `while not ready: time.sleep(0.01)`（轮询）；你写了 `cv.wait(timeout)` 却没有外层循环。
