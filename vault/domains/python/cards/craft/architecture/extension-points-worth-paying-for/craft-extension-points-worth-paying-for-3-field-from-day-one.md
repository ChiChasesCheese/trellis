---
id: craft-extension-points-worth-paying-for-3-field-from-day-one
node: craft.architecture.extension-points-worth-paying-for
type: qa
step: 3
---
## Q
**值得付费的扩展点 · 调度器第 1 关还没有优先级，堆条目为什么就带上这个字段**｜架构

任务调度器按到期时间排队。第 1 关只要求「到期了就执行」，没人提优先级；第 4 关才加「同一时刻到期的任务按优先级执行」。堆里存的条目第 1 关就多放一个 `priority` 字段，是不是过度设计？

## A
**要点。** 判断标准是扩展时要改什么：条目是 `(到期时间, 优先级, 到达序号, id)` 的元组式比较，优先级是中间多出的一栏，堆的 `heappush`、`heappop` 一行不改，比较自动生效，所以这个字段便宜到几乎免费。真正昂贵的是事后改条目的比较顺序和所有调用点。用 `@dataclass(order=True)` 让字段声明顺序就是比较顺序，加一栏就是加一行声明。

```python
@dataclass(order=True, frozen=True)
class HeapEntry:
    """字段声明顺序就是比较顺序：到期时间 -> 优先级 -> 到达序号 -> id。"""
    due: int
    priority: int
    seq: int          # 到达序号：同时刻同优先级按先来后到
    id: int

h: list[HeapEntry] = []
# 第 1 关：没有优先级概念，调用方全传默认值 0
for seq, (due, tid) in enumerate([(10, 1), (10, 2), (5, 3)]):
    heapq.heappush(h, HeapEntry(due, 0, seq, tid))
print("第 1 关出队:", [heapq.heappop(h).id for _ in range(3)])

# 第 4 关：开放优先级。堆和 heappush/heappop 一行没动，只是调用方传了非零值
for seq, (due, prio, tid) in enumerate([(10, 5, 1), (10, 1, 2), (10, 1, 3)]):
    heapq.heappush(h, HeapEntry(due, prio, seq, tid))
print("同一时刻按优先级、再按到达先后:", [heapq.heappop(h).id for _ in range(3)])
```

第 1 关入队 (10,#1)、(10,#2)、(5,#3)；第 4 关 (10,优先级5,#1)、(10,优先级1,#2)、(10,优先级1,#3)，实际输出：

```
第 1 关出队: [3, 1, 2]
同一时刻按优先级、再按到达先后: [2, 3, 1]
```

**为什么。** 优先级相同时靠 `seq` 决胜，保证先到先服务，同时避免比较落到不可比较的后续字段上（回调函数之间没有大小）。「加第 N 关不改老代码」可以作为设计评审的检查项：新增能力是否只多出一个字段、一个参数、一行数据。

**代价。** 这类预留只在几乎免费时才值得；如果预留一个字段要带上一整套没人用的逻辑，就是为想象的需求付费。
