---
id: craft-bounded-deque-1-maxlen-is-the-exit
node: craft.idioms.bounded-deque
type: qa
step: 1
---
## Q
**有界 deque · 为什么历史记录用 deque(maxlen) 而不是 list**｜写法

通知服务要保留最近的发送记录，死信队列要保留最近的失败消息。用 `list.append` 记，进程跑几天内存就涨到几百兆；加一个「超过就删第一个」，又拖慢热路径。`deque(maxlen=N)` 把这两件事怎么一并解决？

## A
**要点。** 双端队列（deque）两端插入删除都是 O(1)。给它设 `maxlen` 之后，满了再从右边追加，会自动把最左边（最旧）的一个挤掉，容器永远不会超过 N 个。这等于给「只增不减的容器」加了一个出口：内存有上界，不用写清理代码。

```python
import timeit
from collections import deque

history: deque[str] = deque(maxlen=3)
for i in range(5):
    history.append(f"e{i}")                    # 满了：自动挤掉最左（最旧）的
print(list(history), len(history), history.maxlen)

unbounded: list[str] = []
for i in range(5):
    unbounded.append(f"e{i}")
    if len(unbounded) > 3:
        del unbounded[0]                       # 手动出口：O(n)，剩下的整体前移
print(unbounded)

N = 100_000
def with_list():
    xs = list(range(N))
    for _ in range(N // 2): xs.pop(0)
def with_deque():
    d = deque(range(N))
    for _ in range(N // 2): d.popleft()
t_list, t_deque = timeit.timeit(with_list, number=1), timeit.timeit(with_deque, number=1)
print(f"list.pop(0): {t_list:.3f}s  deque.popleft: {t_deque:.3f}s")
```

实际输出（耗时随机器而变，量级才是要点）：

```
['e2', 'e3', 'e4'] 3 3
['e2', 'e3', 'e4']
list.pop(0): 0.405s  deque.popleft: 0.001s
```

**为什么。** 两个写法的结果相同，差别在代价：`list` 删除第一个元素要把后面所有元素前移，一次 O(n)；`deque` 内部是块链表，从左端取出是 O(1)。要限制大小的「滑动窗口」「最近 N 条」都是这个形状。

**代价。** `maxlen` 的淘汰是静默的，不会通知你丢了什么：满了丢谁、丢了多少，要自己负责记录。
