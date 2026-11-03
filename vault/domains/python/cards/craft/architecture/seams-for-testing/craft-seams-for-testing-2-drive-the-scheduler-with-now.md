---
id: craft-seams-for-testing-2-drive-the-scheduler-with-now
node: craft.architecture.seams-for-testing
type: qa
step: 2
---
## Q
**测试接缝 · 定时任务调度器怎样不 sleep 就能测「三天后」**｜架构

任务调度器有一个后台线程，在真实时间上等到期再执行任务。要测「每天一次的日报三天后跑了几次」，总不能真的等三天，也不想在测试里开线程、靠 sleep 对时间。接缝应该开在哪里？

## A
**要点。** 把「到期的任务执行」抽成一个同步入口 `run_pending(now)`：调用者传入当前时间，在调用者的线程里执行所有到期任务并返回执行了谁。后台线程只是在真实时间上反复调用同一条路径，所以测试走的就是生产代码，只是时间由测试给定，可以一步快进。

```python
class Scheduler:
    def __init__(self) -> None:
        self._heap: list[tuple[datetime, int, str, timedelta | None]] = []
        self._seq = 0
        self.log: list[str] = []

    def schedule(self, name: str, due: datetime, period: timedelta | None = None) -> None:
        self._seq += 1
        heapq.heappush(self._heap, (due, self._seq, name, period))

    def run_pending(self, now: datetime) -> list[str]:
        """同步执行所有到期任务，不开线程，不 sleep。后台线程只是在真实时间上反复调它。"""
        ran = []
        while self._heap and self._heap[0][0] <= now:
            due, _, name, period = heapq.heappop(self._heap)
            ran.append(name)
            if period is not None:
                self.schedule(name, due + period, period)   # 周期任务排下一次
        return ran

t0 = datetime(2026, 1, 1, 9, 0)
s = Scheduler()
s.schedule("日报", t0 + timedelta(hours=1), period=timedelta(hours=24))
s.schedule("一次性", t0 + timedelta(minutes=5))
print(s.run_pending(t0))                                # 还没到点
print(s.run_pending(t0 + timedelta(minutes=5)))
print(s.run_pending(t0 + timedelta(days=3, hours=1)))   # 一步快进三天
```

实际输出：

```
[]
['一次性']
['日报', '日报', '日报', '日报']
```

**为什么。** 日报在 +1 小时、+25、+49、+73 小时各到期一次，快进 73 小时时全部补跑，所以是 4 次。这也暴露了一个设计问题：错过的周期是补跑还是跳过，在这个入口里一眼就能测出来。

**易错。** 同步入口里不要夹带线程相关的逻辑（唤醒、加锁等待）；这些留在线程循环里，否则测试又得带上线程。
