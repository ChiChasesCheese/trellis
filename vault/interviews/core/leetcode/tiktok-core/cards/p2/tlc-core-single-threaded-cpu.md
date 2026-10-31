---
id: tlc-core-single-threaded-cpu
node: p2.single-threaded-cpu
type: qa
---
## Q
**LC 1834 单线程 CPU**｜Medium · LC TikTok 近 3 个月热度 70/100（全时段 34） · 也在：Amazon

给二维数组 `tasks`，`tasks[i] = [enqueueTime_i, processingTime_i]` 表示第 `i` 项任务在 `enqueueTime_i` 时刻进入任务队列，需要 `processingTime_i` 的时长执行。单线程 CPU 同一时间最多执行一项任务：空闲且队列里没有任务就保持空闲；空闲且队列非空，就选**执行时间最短**的任务开始，执行时间相同则选**下标最小**的；任务一旦开始必须执行完，完成后可以立刻开始下一个。返回 CPU 处理任务的顺序。`n = tasks.length`，`1 <= n <= 10^5`，`1 <= enqueueTime_i, processingTime_i <= 10^9`。例：`tasks = [[1,2],[2,4],[3,2],[4,1]]` → `[0,2,3,1]`；`tasks = [[7,10],[7,12],[7,5],[7,4],[7,2]]` → `[4,3,2,0,1]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 事件模拟加最小堆（min-heap）：把任务按入队时间排序，用指针推进；每次 CPU 空闲时，把所有已到达的任务压进以 `(执行时间, 下标)` 为键的堆，弹出堆顶执行；堆空而下一个任务还没到，时间直接跳到它的到达时刻。`O(n log n)`。

**识别。** 「从一堆**当前可选**的东西里反复取最小」是优先队列（heap）的信号，「执行时间相同取下标小」恰好是元组 `(执行时间, 下标)` 的字典序比较。时间值高达 `10^9`，不能逐秒模拟，必须是**事件驱动**：只在“任务完成”和“CPU 空闲后下一个到达”这两类时刻推进时间。`n = 10^5` 排除每次扫描全部任务的 `O(n^2)`。

**推导。** 暴力：循环里每次扫描所有任务，找出已到达、未执行、执行时间最短的，`O(n^2)`，`10^5` 个任务约 `10^10` 次，超时。浪费在重复扫描已经比较过的任务。按到达时间排序后，任务按顺序“进入候选池”，每个任务只进池一次；池里要反复取最小，用堆，取出 `O(log n)`。

```python
from heapq import heappop, heappush

def get_order(tasks: list[list[int]]) -> list[int]:
    n = len(tasks)
    order = sorted(range(n), key=lambda i: tasks[i][0])   # 任务下标按入队时间排好
    heap: list[tuple[int, int]] = []                      # (执行时间, 下标)：元组比较天然先时间后下标
    res: list[int] = []
    t = p = 0                                             # t 当前时刻；p 下一个还没入队的任务在 order 里的位置
    while len(res) < n:
        if not heap and t < tasks[order[p]][0]:
            t = tasks[order[p]][0]                        # CPU 空闲且队列空：时间直接跳到下一个任务到达
        while p < n and tasks[order[p]][0] <= t:          # 把此刻已到达的任务全部入堆
            i = order[p]
            heappush(heap, (tasks[i][1], i))
            p += 1
        cost, i = heappop(heap)                           # 取最短的；并列时下标小的先出
        t += cost
        res.append(i)
    return res
```

运行：示例 1 → `[0, 2, 3, 1]`，示例 2 → `[4, 3, 2, 0, 1]`，单任务 `[[5,2]]` → `[0]`，`[[1,1],[100,1]]`（中间空闲）→ `[0, 1]`。`n = 10^5` 的随机输入约 `0.06` 秒。

**复杂度。** 时间 `O(n log n)`：排序一次，每个任务入堆、出堆各一次；空间 `O(n)`。

**拓展优化。**
- 平均等待时间（开始时刻减到达时刻）：主解里弹出任务时 `t` 就是它的开始时刻，多累加一项：
```python
from heapq import heappop, heappush


def average_waiting_time(tasks: list[list[int]]) -> float:
    n = len(tasks)
    order = sorted(range(n), key=lambda i: tasks[i][0])
    heap: list[tuple[int, int]] = []                # (执行时间, 下标)
    t = p = served = 0
    wait = 0
    while served < n:
        if not heap and t < tasks[order[p]][0]:
            t = tasks[order[p]][0]                  # 空闲：时间跳到下一个到达
        while p < n and tasks[order[p]][0] <= t:
            i = order[p]
            heappush(heap, (tasks[i][1], i))
            p += 1
        cost, i = heappop(heap)
        wait += t - tasks[i][0]                     # t 即这个任务的开始时刻
        t += cost
        served += 1
    return wait / n
```

**易错点。**
- 忘记空闲时跳时间：`[[1,1],[100,1]]` 在第一个任务完成后堆为空，直接 `heappop` 抛 `IndexError: index out of range`。
- 堆里放 `(执行时间, 入队时间)` 而不是 `(执行时间, 下标)`：并列时按入队时间决胜。`tasks = [[3,2],[1,4],[2,2]]` 得到 `[1, 2, 0]`，正确是 `[1, 0, 2]`（执行时间相同选下标小的）。
- 入堆条件是 `到达时间 <= t`（含等于）：任务在 CPU 恰好完成的那一刻到达，也要参与这一轮选择，示例 1 里任务 `2` 就是这样被选中的。

**追问。**
- `k` 个 CPU：再加一个堆存各 CPU 的空闲时刻，每次取最早空闲的 CPU，其余逻辑相同。
- 任务在线到达、可被抢占（最短剩余时间优先）：事件驱动改成“下一个到达”与“当前任务完成”取更早者，到达时把当前任务的剩余时间放回堆里。

**同模式。** LC 253 会议室 II（堆维护占用）、LC 621 任务调度器、LC 759 员工空闲时间、LC 295 数据流的中位数（两个堆）。
