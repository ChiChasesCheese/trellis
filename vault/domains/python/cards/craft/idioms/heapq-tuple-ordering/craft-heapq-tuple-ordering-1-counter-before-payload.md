---
id: craft-heapq-tuple-ordering-1-counter-before-payload
node: craft.idioms.heapq-tuple-ordering
type: qa
step: 1
---
## Q
**heapq 的元组序 · 为什么堆元素要在载荷前放一个自增序号**｜写法

用 `heapq` 做定时任务队列，元素写成 `(到期时间, 任务对象)`。测试里一直能跑，上线后某天两个任务恰好同一时刻到期，程序抛了 `TypeError`。为什么？序号放在哪里、怎么解决？

## A
**要点。** `heapq` 是小顶堆（min-heap），它直接用 `<` 比较元素。元素是元组时，元组比较逐项进行：第一项不相等就结束，**相等才去比第二项**。到期时间相同，就会去比任务对象，而函数、普通对象之间没有大小关系，抛 `TypeError`。解决：在载荷之前放一个单调递增的序号（`itertools.count`）。序号永远不重复，比较在序号处必然结束，载荷永远不会被比较。

```python
class Job:                                   # 载荷：两个 Job 之间没有大小关系
    def __init__(self, name): self.name = name

# 朴素版：(到期时间, 载荷)。到期时间相同时，堆会去比较第二项
heap: list = []
heapq.heappush(heap, (5, Job("a")))
try:
    heapq.heappush(heap, (5, Job("b")))
except TypeError as e:
    print("同一时刻就崩:", e)

# 加一个单调递增的序号放在载荷之前：序号永远不相同，比较在序号处就结束
tie = count()
heap = []
for name in ["a", "b", "c"]:
    heapq.heappush(heap, (5, next(tie), Job(name)))
print("同时刻按提交顺序弹出:", [heapq.heappop(heap)[2].name for _ in range(3)])

# 序号还有一个作用：同键时先进先出。heapq 本身不稳定，同键的顺序由载荷决定
h = [(1, "x"), (1, "a")]
heapq.heapify(h)
print("没有序号: 先进的 x 反而后出:", heapq.heappop(h))
```

实际输出：

```
同一时刻就崩: '<' not supported between instances of 'Job' and 'Job'
同时刻按提交顺序弹出: ['a', 'b', 'c']
没有序号: 先进的 x 反而后出: (1, 'a')
```

**为什么。** 序号还给了你想要的语义：同键先进先出。`heapq` 本身不稳定（stable），同键时顺序由后面的字段决定，加了序号才是确定的「先提交的先执行」。

**易错。** 只在开发环境用不同的时间值测试，永远发现不了这个 bug，它只在相同键的那一刻才出现。写堆就应该顺手写一个「全部同键」的测试。
