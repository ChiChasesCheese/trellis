---
id: tlc-task-scheduler-0-whole
node: c.task-scheduler
type: qa
---
## Q
**LC 621 任务调度器**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 1 次 · 最近 2025-06-16（国内 CodeTop）

CPU 要执行任务列表 `tasks`（字母 `A`–`Z`）和冷却时间 `n`，每个时间单位执行一个任务或待命；两个相同种类任务之间必须间隔至少 `n` 个时间单位。返回完成所有任务的最短时间。`1 <= tasks.length <= 10^4`，`tasks[i]` 是大写字母，`0 <= n <= 100`。例：`tasks = ["A","A","A","B","B","B"], n = 2` → `8`；`tasks = ["A","C","A","B","D","B"], n = 1` → `6`；`tasks = ["A","A","A","B","B","B"], n = 3` → `10`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 出现次数最多的任务决定骨架：`peak - 1` 个长度 `n + 1` 的周期加最后一段并列最多的任务，其余任务填进空隙，答案是它与 `len(tasks)` 的较大者。

**识别。** 「相同元素之间至少隔 `n`」的最短排程问题：先看最频繁的元素，它的间隔最紧。`n` 只有 100、任务种类至多 26，说明答案是公式而不是搜索。

**推导。** 暴力：模拟每个时间点执行谁，贪心地先执行剩余次数最多的、已冷却完毕的任务（堆 + 冷却队列）。浪费：不关心具体顺序，只要知道空闲槽够不够。洞察：把最多的任务 `A` 排好，`A` 之间留出 `n` 个空位，共 `peak - 1` 段；其他任务把空位填满就没有待命，此时答案就是 `len(tasks)`，不够填时答案由骨架长度决定。

**简单解法。** 大根堆 + 冷却队列逐时刻模拟。

```python
import heapq
from collections import Counter, deque


def least_interval_heap(tasks: list[str], n: int) -> int:
    heap = [-c for c in Counter(tasks).values()]  # 大根堆：每次执行剩余次数最多的任务
    heapq.heapify(heap)
    cooling: deque[tuple[int, int]] = deque()     # (可再次执行的时刻, 剩余次数)
    time = 0
    while heap or cooling:
        time += 1
        if heap:
            left = -heapq.heappop(heap) - 1
            if left:
                cooling.append((time + n, left))  # 冷却 n 个时间单位后才能回堆
        if cooling and cooling[0][0] == time:
            heapq.heappush(heap, -cooling.popleft()[1])
    return time
```

时间 `O(T log 26)`（`T` 为答案），空间 `O(26)`；能给出具体排程，但答案本身有闭式公式。

最优解：

```python
from collections import Counter


def least_interval(tasks: list[str], n: int) -> int:
    counts = Counter(tasks).values()
    peak = max(counts)                           # 出现最多的任务的次数
    ties = sum(c == peak for c in counts)        # 有几种任务并列最多
    # 最多的任务把时间切成 peak-1 个长度为 n+1 的完整周期，最后一段只放并列最多的任务
    return max(len(tasks), (peak - 1) * (n + 1) + ties)
```

运行：`["A","A","A","B","B","B"]`、`n = 2` → `8`；`["A","C","A","B","D","B"]`、`n = 1` → `6`；`["A","A","A","B","B","B"]`、`n = 3` → `10`；`"AAAAAABCDEFG"`、`n = 2` → `16`；`"ABC"`、`n = 0` → `3`。

**复杂度。** 时间 `O(T)`（统计次数），空间 `O(26)`。

**拓展优化。**
- 需要输出具体排程时用上面的堆模拟：每个时间点从堆中取剩余最多的，取不到就输出待命。
- 排程要求「同类任务间隔恰好」不同时，改为按周期轮转填充，公式不再成立。

**易错点。**
- 漏掉 `ties`：`["A","A","B","B"]`、`n = 2` 应为 `5`（`A B _ A B`），只算 `(peak - 1) * (n + 1) + 1` 得 `4`。
- 漏掉与 `len(tasks)` 取最大：`["A","A","B","B","C","C"]`、`n = 1` 时公式给出 `5`，实际要 `6`（任务多到不需要待命）。
- 把冷却当成「中间相隔 `n`」写成 `peak * n`：一个周期长度是 `n + 1`（含任务本身）。

**追问。**
- 输出具体排程：堆模拟，或按周期把次数从多到少依次填入。
- 任务有不同冷却时间：公式失效，只能用堆 + 冷却队列模拟。

**同模式。** LC 358 K 距离间隔重排字符串、LC 767 重构字符串、LC 1054 距离相等的条形码、LC 1353 最多可以参加的会议数目。
