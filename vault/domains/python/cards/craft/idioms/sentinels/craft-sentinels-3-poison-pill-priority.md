---
id: craft-sentinels-3-poison-pill-priority
node: craft.idioms.sentinels
type: qa
step: 3
---
## Q
**哨兵 · 关闭线程池的毒丸为什么优先级是 inf**｜写法

优先级线程池关闭时，往队列里放「毒丸」（poison pill）：工人取到它就退出。有人把毒丸的优先级写成 0，有人写成 `math.inf`。两者对「关闭前已经排队的任务」分别意味着什么？

## A
**要点。** 毒丸是队列里的哨兵任务，含义是「在它之后没有更多工作了」。小根堆里数值越小越先取出，所以优先级 `inf` 保证它排在所有真实任务之后：工人先把排队的任务做完再看到毒丸。写成 0 就排在最前面，工人一取到就退出，排队的任务被默默丢弃。

```python
import math, queue
from dataclasses import dataclass, field

@dataclass(order=True)
class Task:
    priority: float
    seq: int
    name: str = field(compare=False)

def run(pill_priority: float) -> list[str]:
    q: queue.PriorityQueue[Task] = queue.PriorityQueue()
    for i, name in enumerate(["t1", "t2", "t3"]):
        q.put(Task(priority=5, seq=i, name=name))
    q.put(Task(pill_priority, 99, "STOP"))           # 关闭时放入毒丸
    done = []
    while True:
        t = q.get()
        if t.name == "STOP":                         # 工人看到毒丸就退出
            return done
        done.append(t.name)

print(run(math.inf))      # 排在所有真实任务之后：先做完再停
print(run(0))             # 优先级 0：排在最前，任务全被丢下
```

实际输出：

```
['t1', 't2', 't3']
[]
```

**为什么。** 要立即停止、放弃排队任务时是另一条路径：先把队列里未开始的任务取出并标记失败，再放毒丸。「温和关闭」和「强制关闭」用同一个哨兵，区别只在毒丸前面有没有任务。

**易错。** 每个工人需要一颗毒丸，N 个工人放 N 颗，否则有人永远阻塞在 `get()`。毒丸的 `seq` 也要唯一，否则同优先级时比较会落到不可比较的字段上。
