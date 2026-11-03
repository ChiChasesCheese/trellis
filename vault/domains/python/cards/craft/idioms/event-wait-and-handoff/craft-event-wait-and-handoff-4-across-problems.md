---
id: craft-event-wait-and-handoff-4-across-problems
node: craft.idioms.event-wait-and-handoff
type: qa
step: 4
---
## Q
**Event 的等待与交接 · 监听器、幂等转账、阻塞队列、缓存里同一类等待**｜写法

文件监听器的轮询线程、幂等转账里重复请求等第一个请求、阻塞队列的 `take`、缓存的单飞回源，都在「等一件事发生」。它们等的东西和等法各有什么不同，哪里是共通的规则？

## A
**要点。** 共通的规则只有一条：**被唤醒不代表条件成立**，所以等待总写在循环里、醒来重新检查。不同的是等的对象：一个「停止」信号、一个「结果」、一个「队列状态」。前两个用 `Event`（一次性的开关），队列状态用 `Condition`（反复成立又失效）。

```python
# amz-file-watcher：等 interval 秒，或被 stop() 叫醒
if self._stop.wait(interval):
    return

# idempotent-transfer：重复请求等第一个请求出结果，超时就让调用方稍后重试
if not rec.done.wait(self._wait):
    raise StillRunning("第一个请求仍在处理")
if rec.result is not None:
    return rec.result
# 拥有者失败并释放了键：回到循环重新竞争

# bounded-blocking-queue：Condition + while + 剩余时间
while not self._items and not self._closed:
    self._wait_for(self._not_empty, deadline, "take")
```

选 `Event` 还是 `Condition`：事件发生一次、之后一直成立（完成、停止），用 `Event`，等待者不必持锁；条件会反复变化（队列空了又满），需要 `Condition`，并且 `wait` 要在持有它的锁时调用。线程池的 `Future` 用 `Event` 表示「完成」，把结果交给任意多个 `result()` 调用者。

**见于。** amz-file-watcher、idempotent-transfer、bounded-blocking-queue、ttl-cache、thread-pool。

**信号。** 代码里出现 `time.sleep` 轮询某个标志，或者「别的线程做完之前这里要等」。
