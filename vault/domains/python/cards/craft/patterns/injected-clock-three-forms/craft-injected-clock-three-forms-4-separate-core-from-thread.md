---
id: craft-injected-clock-three-forms-4-separate-core-from-thread
node: craft.patterns.injected-clock-three-forms
type: qa
step: 4
---
## Q
**注入时钟 · 后台线程怎么办：把调度逻辑和线程分开**｜模式

任务调度器要有一个后台线程，到点执行任务。直接写成线程里 `while: sleep; 检查; 执行`，测试只能真的等。怎样让「调度逻辑」可以不 sleep 就测试，而线程仍然存在？

## A
**要点。** 拆成两层：核心（core）只做「给我一个 now，把到期任务取出来」，不碰线程也不读时钟；线程层只是在真实时间上反复调用核心的同一条路径。测试直接调核心的 `run_pending(now)`，时间想设成多少就是多少。

```python
class Core:
    def run_pending(self, now: float) -> list[int]:
        ran = []
        while self._heap and self._heap[0][0] <= now:    # 小顶堆：最早的在堆顶
            ran.append(heapq.heappop(self._heap)[1])
        return ran

class Scheduler:
    def _loop(self):
        while not self.stop.wait(0.01):                   # 线程只负责「等」
            self.ran += self.core.run_pending(time.monotonic())
```

不开线程，直接驱动核心：

```
t=4.99 : []
t=5.0  : [1]
t=10.0 : [2, 3]
```

**为什么。** 边界（4.99 不触发、5.0 触发）可以一行断言；线程层只剩「调用核心」这一行，里面几乎没有逻辑，也就几乎不需要测试。

**代价。** 多一层间接；线程层与核心之间的并发（取消、停止）仍要单独测。任务调度器的 `Scheduler` 和 `_SchedulerCore` 就是这样分的。
