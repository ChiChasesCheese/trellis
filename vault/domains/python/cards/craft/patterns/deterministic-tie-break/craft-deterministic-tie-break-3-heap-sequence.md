---
id: craft-deterministic-tie-break-3-heap-sequence
node: craft.patterns.deterministic-tie-break
type: qa
step: 3
---
## Q
**确定性平局规则 · 堆里优先级相同的元素，为什么要加一个自增序号**｜写法

用 `heapq` 存 `(优先级, 任务对象)`。两个任务优先级相同时，堆会拿第二项比较，会发生什么？任务调度器（DAG runner）里"同时就绪的节点先跑谁"又是怎么保证确定的？

## A
**要点。** 元组比较在第一项相等时继续比第二项。第二项如果是不可比较的对象，直接抛 `TypeError`；即使可比较（比如字符串），"同级按名字字典序"也未必是业务想要的顺序（想要的通常是先来后到）。修法：在元组中间插入一个单调递增的序号 `(优先级, next(seq), 对象)`：序号永远不会相等，比较永远到不了对象，同级严格按到达顺序。DAG 里同理：就绪节点用"首次出现的序号"入堆，同时可选时按声明顺序。

```python
import heapq, itertools
from dataclasses import dataclass

@dataclass
class Job: name: str                          # 不可比较：没有 __lt__

h = []
try:
    for pri, name in [(1, "a"), (1, "b")]:
        heapq.heappush(h, (pri, Job(name)))   # 优先级相同时，比较会落到第二项
except TypeError as e:
    print("同优先级且无序号:", e)

h, seq = [], itertools.count()
for pri, name in [(1, "a"), (0, "x"), (1, "b"), (1, "c")]:
    heapq.heappush(h, (pri, next(seq), Job(name)))   # 序号保证比较永远到不了 Job
print("出堆顺序:", [heapq.heappop(h)[2].name for _ in range(4)])

# dag-runner：就绪节点按"首次出现序号"入堆，而不是按名字
deps = {"build": [], "lint": [], "test": ["build"], "docs": []}      # 声明顺序：build, lint, test, docs
idx = {n: i for i, n in enumerate(deps)}
ready = [idx[n] for n, d in deps.items() if not d]; heapq.heapify(ready)
names = list(deps)
print("同时可选时的顺序:", [names[heapq.heappop(ready)] for _ in range(len(ready))])
```

```
同优先级且无序号: '<' not supported between instances of 'Job' and 'Job'
出堆顺序: ['x', 'a', 'b', 'c']
同时可选时的顺序: ['build', 'lint', 'docs']
```

**为什么。** 最后一行：声明顺序是 build、lint、test、docs；test 依赖 build，所以开始时就绪的是 build、lint、docs，输出按声明顺序，而不是按字母序（docs、build、lint）。把序号而不是名字放进堆，比较是整数比较，既快又确定；输出顺序与图的写法一致，测试可以断言整条序列。TTL 缓存的到期堆里 `(deadline, seq, key)` 也是同一个理由：key 可能不可比较，序号同时给同一时刻到期的条目一个稳定的先后。

**代价。** 一个计数器，几乎免费。需要"取消/更新"堆中条目时，序号还能当作版本号区分新旧条目（见 lazy-deletion-heap 那一叶）。

**易错。** `dataclass(order=True)` 的任务对象字段全参与比较，字段里有不可比较的东西就会炸；把比较字段限定为 `(priority, seq)`，其余用 `field(compare=False)`。
