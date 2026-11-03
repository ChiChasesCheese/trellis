---
id: craft-heapq-tuple-ordering-4-dataclass-order
node: craft.idioms.heapq-tuple-ordering
type: qa
step: 4
---
## Q
**heapq 的元组序 · `@dataclass(order=True)` 比较什么，`compare=False` 管什么**｜写法

任务调度器的堆元素从元组换成了 `@dataclass(order=True)`，字段是到期时间、优先级、序号，再加一个要执行的函数。排序顺序是怎么决定的？函数字段为什么必须 `compare=False`？

## A
**要点。** `order=True` 生成 `__lt__` 等方法，把**字段按声明顺序**当成一个元组来比较，所以字段顺序就是排序的优先顺序。想让某个字段不参与（函数、Future 这种没大小关系的东西），写 `field(compare=False)`。好处是扩展不用改堆：多一个排序维度，只是多声明一个字段、放在合适的位置，`heapq` 的比较自动生效，调用堆的代码一行不改。

```python
# 字段声明的顺序就是比较顺序；不该参与比较的字段 compare=False
@dataclass(order=True)
class Task:
    due: int
    priority: int
    seq: int
    fn: Callable[[], Any] = field(compare=False)    # 函数之间没有大小关系

seq = count()
heap: list[Task] = []
def submit(due: int, priority: int, name: str):
    heapq.heappush(heap, Task(due, priority, next(seq), lambda: name))

submit(10, 5, "a")
submit(10, 1, "b")        # 同一时刻, 优先级数字小的先出
submit(10, 1, "c")        # 同一时刻同优先级, 先提交的先出
submit(5, 9, "d")         # 到期更早的最先
print([heapq.heappop(heap).fn() for _ in range(4)])

@dataclass(order=True)
class Wrong:
    fn: Callable[[], Any]                            # 忘了 compare=False
    due: int
try:
    h = [Wrong(lambda: 1, 1)]
    heapq.heappush(h, Wrong(lambda: 2, 1))
except TypeError as e:
    print("函数参与了比较:", e)
```

实际输出：

```
['d', 'b', 'c', 'a']
函数参与了比较: '<' not supported between instances of 'function' and 'function'
```

**为什么。** 命名字段比 `(due, priority, seq, fn)` 元组更不容易搞错位置，类型检查器也能核对；元组写法适合只用一两处的小堆。

**易错。** 忘了给不可比较的字段加 `compare=False`，只在同键时才报错，平时测试发现不了。用 `order=True` 时顺手把可比较字段的顺序写进 docstring。冻结（`frozen=True`）能防止入堆后被改动键值，堆的结构因此不会被悄悄破坏。
