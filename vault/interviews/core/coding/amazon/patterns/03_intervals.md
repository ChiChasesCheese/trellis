# 03 · 区间（Intervals：排序 + 扫描）

> 本讲覆盖：LC 56 Merge Intervals · 253 Meeting Rooms II · 435 Non-overlapping Intervals · 1235 Maximum Profit in Job Scheduling（Hard）
> 前置：`sorted(key=...)`、元组比较、第 02 讲的「指针只前进」。`heapq` 在第 05 讲细讲，这里只用 `heappush / heapreplace`。
> 读完你应该能：(1) 口述「为什么先按起点排序就够了」；(2) 区分三类问题——合并、计数重叠、选最多不重叠；(3) 说清楚贪心在什么时候失效（带权 → DP）。

## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

LC 56：把一堆区间 `[start, end]` 合并成互不重叠的区间。最笨的做法：两两比较，只要两个区间重叠就合并成一个，然后重新开始，直到没有任何一对重叠为止。

两两比较是 O(n²) 次，而且**合并会产生新的重叠**（`[1,4]` 与 `[5,6]` 不重叠，但 `[3,5]` 把它们连起来了），所以还要反复扫描——最坏 O(n³)。

### 1.2 慢在哪里

慢在「顺序是乱的」：一个区间可能和任何位置的另一个区间重叠，所以只能全体两两检查。

> 因果链：如果区间按**起点**排好序，那么对当前这个「正在扩张的块」`[a, b]`，下一个区间 `[s, e]` 只可能有两种情况：`s <= b`（重叠，把块的右端扩到 `max(b, e)`），或 `s > b`（不重叠）。而且**一旦不重叠，后面所有区间的起点都 ≥ s > b，也都不会和这个块重叠**——这个块可以封存了。→ 排序 O(n log n) + 一次扫描 O(n)。

### 1.3 三类问题，三个工具

| 问题 | 工具 | 例题 |
|---|---|---|
| 合并重叠区间 | 按起点排序，一次扫描维护「最后一个块」 | 56 |
| 同一时刻最多有几个区间重叠（需要几间会议室） | 扫描线（sweep line）：起点 +1，终点 −1；或最小堆存「正在占用的房间的结束时间」 | 253 |
| 最少删掉几个区间使其互不重叠 / 最多保留几个 | **按终点排序**的贪心（越早结束，给后面留的空间越多） | 435 |
| 每个区间有权重，选互不重叠且总权重最大 | 贪心失效 → 按终点排序 + DP + 二分 | 1235 |

> 为什么 435 要按终点、56 要按起点？56 要把**连着的**东西粘起来，起点顺序保证相邻性；435 要「尽早结束」，终点才是衡量「占了多少未来」的指标。

## 2. 模板与逐行讲解

```python
# Template: sort by start, then one pass comparing each interval with the LAST block only
def sweep_blocks(intervals):
    blocks = []
    for start, end in sorted(intervals):
        if blocks and start <= blocks[-1][1]:       # overlaps the last block
            blocks[-1][1] = max(blocks[-1][1], end)
        else:
            blocks.append([start, end])
    return blocks

# Template: counting overlap with +1/-1 events (sweep line)
def max_overlap(intervals):
    events = sorted([(s, 1) for s, e in intervals] + [(e, -1) for s, e in intervals])  # -1 sorts before +1 at a tie
    cur = best = 0
    for _, delta in events:
        cur += delta
        best = max(best, cur)
    return best

assert sweep_blocks([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]
assert max_overlap([[0, 30], [5, 10], [15, 20]]) == 2
assert max_overlap([[1, 5], [5, 8]]) == 1
```

逐行讲解：

1. `sorted(intervals)`：元组 / 列表按字典序比较，先比起点再比终点；返回新列表，不改输入（原地排序用 `intervals.sort()`，面试里要说明你是否允许修改输入）。
2. `blocks and start <= blocks[-1][1]`：先判空再取 `[-1]`；`<=` 代表「首尾相接也算重叠」——**这是与面试官约定的契约**（LC 56 合并 `[1,4]` 与 `[4,5]`，LC 435 则不算重叠）。
3. `max(blocks[-1][1], end)`：新区间可能完全被包含在块里（`[1,10]` 与 `[2,3]`），不能直接把右端改成 `end`。
4. 扫描线：`(e, -1)` 排在 `(s, 1)` 前面（`-1 < 1`），所以终点和起点在同一时刻重合时，先释放再占用——对应「一场会议刚结束，下一场可以接着用同一间会议室」。
5. 事件里元组的第二项既是 `delta` 又是同刻排序的 tie-breaker——这是一个很实用的小技巧，但要在口头上讲明白，否则面试官会以为是偶然。

## 3. 完整手算（Worked trace）

输入故意乱序：`[[8,10],[1,3],[15,18],[2,6]]`。排序后依次处理：

```python
def merge_trace(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            old = list(merged[-1])
            merged[-1][1] = max(merged[-1][1], end)
            print(f"[{start},{end}] overlaps {old} -> extend to {merged[-1]}   blocks={merged}")
        else:
            merged.append([start, end])
            print(f"[{start},{end}] starts after the last block -> new block      blocks={merged}")
    return merged

assert merge_trace([[8, 10], [1, 3], [15, 18], [2, 6]]) == [[1, 6], [8, 10], [15, 18]]
```

```text
[1,3] starts after the last block -> new block      blocks=[[1, 3]]
[2,6] overlaps [1, 3] -> extend to [1, 6]   blocks=[[1, 6]]
[8,10] starts after the last block -> new block      blocks=[[1, 6], [8, 10]]
[15,18] starts after the last block -> new block      blocks=[[1, 6], [8, 10], [15, 18]]
```

读法：`[2,6]` 的起点 2 ≤ 当前块 `[1,3]` 的终点 3，所以块变成 `[1, max(3,6)] = [1,6]`；`[8,10]` 的起点 8 > 6，开新块；以后的区间起点只会更大，所以 `[1,6]` 已经封存。

## 4. 题目

```python
import bisect
import heapq
```

### 4.1 LC 56 · Merge Intervals（Medium，频率 77）

```python
# solutions/56_merge_intervals.py
def merge(intervals):
    merged = []
    for start, end in sorted(intervals):             # sorted() copies: input is not mutated
        if merged and start <= merged[-1][1]:        # overlaps (or touches) the last block
            merged[-1][1] = max(merged[-1][1], end)  # max: the new one may be fully inside
        else:
            merged.append([start, end])
    return merged
```

- **一句话洞见**：按起点排序后，只需把每个区间和「最后一个块」比较。
- **复杂度**：时间 O(n log n)（排序），空间 O(n)（输出；不计输出则 O(1) 额外，若原地排序）。

**资深追问**

- **规模 ×1000**：排序主导。数据放不下内存时外排序；分布式：按起点做范围分区（range partition），每个分区独立合并，最后只需要处理**相邻分区边界**上被切断的块。
- **流式输入**：若区间按起点有序到达，可以边读边合并，并在新区间起点 > 当前块终点时**输出（flush）该块**，内存 O(1)；无序到达则需要有序结构（平衡树 / 区间树）支持「插入并合并」（即 LC 57 Insert Interval），每次 O(log n + 被合并的个数)。
- **内存**：原地合并：排序后用写指针覆盖，O(1) 额外空间。
- **并发**：线程安全的「区间集合」服务：读多写少用读写锁；或用不可变快照（copy-on-write），写入时生成新版本。
- **接口 / 边界**：闭区间还是半开区间？`[1,4]` 与 `[4,5]` 是否合并（本题合并）？输入是否保证 `start <= end`？是否允许修改输入？返回 `list` 还是 `tuple`？浮点端点怎么比较？
- **测试**：首尾相接、包含、重复、乱序、单个、空；性质：输出有序、互不重叠、并集不变——可以和「把每个整数点标记为已覆盖」的暴力法对拍。

### 4.2 LC 253 · Meeting Rooms II（Medium，频率 62）

```python
# solutions/253_meeting_rooms_ii.py
def min_meeting_rooms(intervals):
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = best = 0
    j = 0                                   # next meeting to end
    for s in starts:
        while ends[j] <= s:                 # a meeting ending exactly at s frees its room first
            j += 1
            rooms -= 1
        rooms += 1
        best = max(best, rooms)
    return best


def min_meeting_rooms_heap(intervals):
    heap = []                               # end times of rooms currently in use
    for s, e in sorted(intervals):
        if heap and heap[0] <= s:           # earliest-finishing room is free: reuse it
            heapq.heapreplace(heap, e)
        else:
            heapq.heappush(heap, e)         # need a new room
    return len(heap)
```

- **一句话洞见**：房间数 = 任意时刻同时进行的会议数的最大值。把起点、终点分别排序，起点处 +1，在它之前先释放所有已结束（`end <= start`）的会议。第二种写法：最小堆存「每个在用房间的结束时间」，堆顶最早结束，能复用就 `heapreplace`。
- **复杂度**：时间 O(n log n)，空间 O(n)（堆版本空间 O(最大并发数)）。

**资深追问**

- **规模 ×1000**：排序 O(n log n)。分布式：按时间范围分区，每个分区算局部「同时进行数」序列，需要带上「分区开始时已经打开的会议数」（carry-in），它是前面所有分区 `(+1 的数量 − −1 的数量)` 的前缀和。
- **流式 / 在线**：会议按起点顺序到来时，堆版本天然在线；任意顺序到来（日历预订）要用「有序映射 + 差分」：`delta[t] += 1/-1`，查询时求前缀和的最大值（LC 731 / 732 的思路）。
- **内存**：堆版本只保存正在进行的会议（≤ 答案），比排序两个数组 O(n) 更省。
- **并发**：「预订房间」是 check-then-act，必须原子：对资源加锁，或乐观并发（版本号 + 重试）。要求返回具体分配的房间号时，堆里放 `(end, room_id)`。
- **接口**：首尾相接是否共用房间（本题 `end <= start` 可以）；返回房间数还是分配方案？会议是否允许长度为 0？
- **测试**：首尾相接、完全相同、嵌套、单个、空；用「枚举每个时间点统计」的暴力法对拍（文件里已有）；两种实现互相对拍。

### 4.3 LC 435 · Non-overlapping Intervals（Medium，频率 43）

```python
# solutions/435_non_overlapping_intervals.py
def erase_overlap_intervals(intervals):
    intervals = sorted(intervals, key=lambda iv: iv[1])   # earliest end first leaves most room
    kept = 0
    last_end = float("-inf")
    for start, end in intervals:
        if start >= last_end:        # touching ([1,2],[2,3]) is NOT an overlap here
            kept += 1
            last_end = end
    return len(intervals) - kept
```

- **一句话洞见**：按**终点**排序，能放就放（`start >= last_end`）：结束越早，给后面留的空间越大。证明用交换论证（exchange argument）：任何最优解里，把第一个区间换成「结束最早的那个」不会让后面的选择变差。
- **复杂度**：时间 O(n log n)，空间 O(1) 额外（排序后）。

**资深追问**

- **规模 ×1000**：同 56；排序主导，外排序 + 一次扫描。
- **流式**：在线版本没有最优的贪心（对手可以让你做出错误选择）；如果区间按终点顺序到来，贪心是在线最优的。
- **内存**：只需要 `last_end` 和计数，O(1)。
- **并发**：与 56 同；若多个调度器共享同一时间线，需要原子的「检查并占用」。
- **接口**：首尾相接是否算重叠（本题不算）；要返回**被删除的区间**还是个数？有并列时保留哪个？加上权重就是 LC 1235（下一题），贪心不再成立。
- **测试**：`[[1,2],[2,3]]`（相接）、全相同、嵌套、空；用「枚举所有子集」的暴力法对拍（文件里已有）。

### 4.4 LC 1235 · Maximum Profit in Job Scheduling（Hard，频率 51）

```python
# solutions/1235_maximum_profit_in_job_scheduling.py
def job_scheduling(start_time, end_time, profit):
    jobs = sorted(zip(end_time, start_time, profit))      # by end time
    ends = [e for e, _, _ in jobs]
    dp = [0] * (len(jobs) + 1)                            # dp[i]: best profit using the first i jobs
    for i, (e, s, p) in enumerate(jobs, 1):
        k = bisect.bisect_right(ends, s, 0, i - 1)        # jobs that end at or before s are compatible
        dp[i] = max(dp[i - 1], dp[k] + p)                 # skip job i, or take it on top of dp[k]
    return dp[-1]
```

- **一句话洞见**：按终点排序，`dp[i]` = 前 i 个任务能得到的最大利润；任务 i 要么不选（`dp[i-1]`），要么选（它的利润 + 所有「终点 ≤ 它的起点」的任务里的最优，用二分找到分界点）。
- **为什么贪心失效**：435 里「所有区间等价」所以越早结束越好；这里区间有权重，早结束的小利润任务可能挡住大利润任务。
- **复杂度**：时间 O(n log n)，空间 O(n)。

**资深追问**

- **规模 ×1000**：排序 + 每个任务一次二分，O(n log n)。分布式比较难（DP 是顺序依赖）；可以按独立资源（机器 / 日历）拆开并行。
- **流式**：任务按终点顺序到来时可以做在线 DP：维护单调的 `(end, best)` 列表（只保留利润严格递增的点），每个新任务二分查找、必要时追加，O(log n)/个。
- **内存**：只需保留「利润严格增长」的 `(end, best)` 点，而不是每个任务一格。
- **并发**：DP 本身是串行的；服务化时是「提交任务 → 异步求最优」，用不可变快照避免读写冲突。
- **接口**：利润是否可以为 0 / 负（负的任务永远不选）？要返回最大利润还是选中的任务集合（需要记录父指针回溯）？`start < end` 是否保证？首尾相接可以连选（本题可以）。
- **测试**：与枚举所有子集的暴力对拍（文件里已有）；全部重叠、全部不重叠、相接。

## 5. 常见 bug

1. **用 `<` 还是 `<=` 搞反**：56 里首尾相接要合并（`<=`），253 里首尾相接可以复用房间（`end <= start`），435 里相接不算重叠（`start >= last_end`）。**先问契约，再写比较号。**
2. **合并时直接把右端改成 `end`**：嵌套区间 `[1,10]`、`[2,3]` 会把块缩短。用 `max`。
3. **没排序**或**按错了键**：56 / 253 按起点，435 / 1235 按终点。
4. **253 把起点和终点各自排序后就以为它们配对**：它们**不再配对**，但这没关系——我们只关心「某时刻有几个打开」。
5. **修改了调用者的输入**：`intervals.sort()` 会原地改；如果不被允许，用 `sorted()`。
6. **1235 的二分边界错**：`bisect_right(ends, s, 0, i - 1)` 里 `hi = i - 1` 是为了不把任务自己算进去；终点等于 `s` 的任务是**兼容**的，所以用 `bisect_right`。
7. **Python 比较 `float("-inf")` 初始化**：`last_end = float("-inf")` 比用 `None` 少一个分支。

## 6. 自测题

1. 为什么合并区间要按起点排序？如果按终点排序会怎样？
   <details><summary>答案</summary>按起点排序保证「与当前块不重叠的区间之后全都不重叠」，所以只需看最后一个块。按终点排序时，后面出现的区间可能起点很小、跨过前面的多个块，需要回头合并多个，扫描就不再是一次。</details>
2. 253 里为什么堆的大小就等于答案？
   <details><summary>答案</summary>堆里放的是「当前仍被占用的房间的结束时间」；能复用就替换（大小不变），不能复用就新增。最终堆大小 = 过程中需要的最大房间数。</details>
3. 什么时候区间贪心「按终点」，什么时候「按起点」？
   <details><summary>答案</summary>要把重叠的部分粘成块 / 逐个检查相邻性 → 按起点；要在一条时间线上尽可能多地放不冲突的区间 → 按终点。</details>
4. 小编程：给一个区间 `new` 和一个已合并有序的区间列表，插入并保持合并（LC 57）。
   <details><summary>答案</summary>三段：把所有 `end < new.start` 的原样放进结果；把与 `new` 重叠的全部合并进 `new`（`start = min`，`end = max`）；再把剩下的放进去。O(n)。</details>
5. 1235 为什么不能像 435 那样贪心？举一个反例。
   <details><summary>答案</summary>任务 A `[1,3]` 利润 1，任务 B `[2,10]` 利润 100。按终点贪心先选 A 就挡住了 B，最优是只选 B。</details>
6. 资深追问：日历服务每秒收到上万个预订请求，如何判断是否冲突？
   <details><summary>答案</summary>用有序结构（平衡树 / `SortedList`）按起点存已确认的区间，新请求二分找前驱和后继检查冲突，O(log n)；并发下对该资源（房间 / 用户）加锁或使用乐观并发（版本号 + 重试）。</details>
