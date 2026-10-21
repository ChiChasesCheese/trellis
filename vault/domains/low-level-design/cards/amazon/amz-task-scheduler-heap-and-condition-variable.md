---
id: amz-task-scheduler-heap-and-condition-variable
node: amazon.amz-task-scheduler
type: qa
step: 3
tags: [grown]
---
## Q
在任务调度器设计里，调度线程怎么知道睡多久？为什么不用 `while True: sleep(0.01)` 轮询？

## A
堆顶就是最早到期的任务：到期了就弹出交给线程池，没到期就 `wait(剩余时间)`；堆空了就无限 `wait`。新任务比堆顶更早时要 `notify` 唤醒调度线程重新算。轮询要么白烧 CPU，要么最多晚 10 毫秒。堆元素用 `(due, seq, task)`，序号 `seq` 避免到期时间相同时去比较任务对象。
```python
def _loop(self):
    with self._cv:
        while not self._closed:
            if not self._heap:
                self._cv.wait()
                continue
            due, _, task = self._heap[0]
            delay = due - self._clock()
            if delay > 0:
                self._cv.wait(delay)
            else:
                heapq.heappop(self._heap)
                self._pool.submit(task.run)
```
