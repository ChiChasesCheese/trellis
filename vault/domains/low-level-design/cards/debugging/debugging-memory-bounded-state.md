---
id: debugging-memory-bounded-state
node: debugging.memory
type: qa
step: 4
---
## Q
调度器用堆存待执行任务，“取消”只是从字典里删掉，堆里的条目留着（弹出时再跳过）。取消得多了，内存会怎样？怎么让它有上限？

## A
**惰性删除会留下残骸：要么定期重建，要么限制总量，让内存只跟活跃数据成正比**

- **堆不能删中间元素**：取消时只在 `live` 字典里去掉，堆里的条目变成“墓碑”，弹出时发现已不在 `live` 里就跳过；
- **没有清理的话，墓碑会一直累积**：任务反复提交又取消，堆越来越大，永远等不到它们到期被弹出；
- **重建**：墓碑数超过活跃数的某个倍数，就用 `live` 重新建一个堆（`heapify` 是 O(n)，摊到每次取消上很小）；
- **同类问题**：保留历史的流处理器要有上限，只保留状态（上一个栈、上一个时间戳），不把流过的全部采样攒起来；需要最近 N 条用 `deque(maxlen=N)`；
- **验证方式**：写测试反复提交取消十万次，断言堆的长度不超过活跃数的常数倍。

```python
import heapq

class Scheduler:
    def __init__(self): self.h, self.live = [], {}
    def add(self, tid, due):
        self.live[tid] = due; heapq.heappush(self.h, (due, tid))
    def cancel(self, tid):
        self.live.pop(tid, None)                      # 堆里留下墓碑
        if len(self.h) > 2 * len(self.live) + 16:     # 墓碑太多：用活跃的重建
            self.h = [(d, t) for t, d in self.live.items()]; heapq.heapify(self.h)

s = Scheduler()
for i in range(100_000): s.add(i, i); s.cancel(i)
print(len(s.h), len(s.live))      # 6 0：堆的长度被限制住，不是 100000
```

代码省略了取任务的 `pop`：它弹出条目时，跳过 `live` 里已经没有（或到期时间对不上）的墓碑。

**知识点：**内存问题（Memory Leaks）
