---
id: tlc-patterns-monotonic-stack-1-signals
node: patterns.monotonic-stack
type: qa
step: 1
---
## Q
**单调栈与单调队列（Monotonic Stack）｜信号**

什么样的题面该想到单调栈？单调队列又对应什么信号？哪些近似信号其实用别的结构？

## A
**单调栈的信号：**
- 「每个元素右边（或左边）**第一个更大 / 更小**的元素」：每日温度 LC 739、下一个更大元素（例：LC 739 每日温度）。
- 要求以每个元素为**最小值（或最大值）的最长区间**：柱状图中最大的矩形 LC 84、LC 2334（例：LC 84 柱状图中最大的矩形）。
- 「**字典序最小**的子序列 / 去掉 `k` 个字符后最小」：栈里保持递增，遇到更小的就弹出前面更大的：LC 316、1081、402（例：LC 316 去除重复字母）。
- **相邻元素相互抵消**的模拟：小行星碰撞 LC 735、删除相邻重复项 LC 1209（例：LC 735 小行星碰撞）。
- 接雨水 LC 42（栈版本按层累计）（例：LC 42 接雨水）。
- 数据范围 `10^5`：暴力 `O(n^2)` 不行（例：LC 853 车队）。

**单调队列（双端队列）的信号：**
- **滑动窗口的最大 / 最小值**：窗口会移动，过期的元素要从队首踢出（LC 239）（例：LC 239 滑动窗口最大值）。

**为什么 `O(n)`**：每个元素最多入栈一次、出栈一次。

**近似信号：**
- 只要一次「全局最大 / 最小」→ 一个变量，不要栈（例：LC 121 买卖股票的最佳时机）。
- 窗口求**和**或**计数** → 普通滑动窗口 / 前缀和（例：LC 643 子数组最大平均数 I）。
- 求区间任意最值、任意查询 → 稀疏表（Sparse Table）、线段树；单调栈只回答「最近的更大 / 更小」（例：LC 3161 物块放置查询）。
- 括号匹配 → 普通栈，不单调（LC 20）（例：LC 20 有效的括号）。
- 区间不是由「相邻最近」决定、而是任意两点 → 排序 / 双指针（例：LC 11 盛最多水的容器）。

**例题：** LC 739 每日温度

数组 `temperatures`（`1 <= length <= 10^5`，`30 <= t <= 100`）表示每天温度，`answer[i]` 是第 `i` 天之后要等几天才会出现更高温度，没有则为 `0`。

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    answer = [0] * len(temperatures)
    stack: list[int] = []              # 还在等更高温度的下标；对应温度自底向顶非严格递减
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:   # t 是它们等到的第一个更高温度
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer                      # 栈里剩下的永远没等到，保持 0
```

**例题：** LC 84 柱状图中最大的矩形

`heights`（`1 <= length <= 10^5`，`0 <= h <= 10^4`）是宽度为 1 的相邻柱子的高度，求柱状图中能勾勒出的最大矩形面积。

```python
def largest_rectangle_area(heights: list[int]) -> int:
    stack: list[int] = []                      # 下标，对应高度严格递增
    best = 0
    for i, h in enumerate([*heights, 0]):      # 末尾补一根高 0 的柱子，把栈清空
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]      # 这根柱子在 i 处找到了右边界
            left = stack[-1] if stack else -1  # 左边第一根更矮的柱子
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best
```

**例题：** LC 316 去除重复字母

字符串 `s`（`1 <= length <= 10^4`，小写字母），去掉重复字母使每个字母只出现一次，在不打乱其余字符相对顺序的前提下让结果字典序最小。

```python
def remove_duplicate_letters(s: str) -> str:
    last = {ch: i for i, ch in enumerate(s)}       # 每个字母最后一次出现的下标
    stack: list[str] = []
    in_stack: set[str] = set()
    for i, ch in enumerate(s):
        if ch in in_stack:                         # 已经放好了，跳过（先放的位置一定不差）
            continue
        while stack and stack[-1] > ch and last[stack[-1]] > i:
            in_stack.discard(stack.pop())
        stack.append(ch)
        in_stack.add(ch)
    return "".join(stack)
```

**例题：** LC 735 小行星碰撞

`asteroids`（`2 <= length <= 10^4`，`-1000 <= v <= 1000`，非零）中绝对值是大小，正负是方向，同向不碰撞；相向碰撞时小的爆炸，一样大则都爆炸。返回最终剩下的小行星。

```python
def asteroid_collision(asteroids: list[int]) -> list[int]:
    stack: list[int] = []                   # 栈里是还活着的小行星，从左到右
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:   # 只有 向右的栈顶 撞 向左的新来者
            top = stack[-1]
            if top <= -a:
                stack.pop()                 # 栈顶爆炸（等大时两个都炸）
            alive = top < -a                # 新来者只有严格更大才活下来
        if alive:
            stack.append(a)
    return stack
```

**例题：** LC 42 接雨水

`height`（`1 <= n <= 2 * 10^4`，`0 <= h <= 10^5`）表示宽度为 1 的柱子高度，求下雨后能接多少雨水。

```python
def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:           # 左边更矮：左格的水位由 left_max 决定
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:                                      # 右边更矮或相等：右格的水位由 right_max 决定
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water
```

**例题：** LC 853 车队

`n`（`1 <= n <= 10^5`）辆车开往距起点 `target` 英里的终点，`position[i]`、`speed[i]` 是各车位置和速度；后车可追上前车但不能超车，追上后以慢车速度并排行驶，成为一个车队。求到达终点的车队数。

```python
def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    fleets = 0
    latest = 0.0                       # 目前所有车队里最晚到终点的时间
    for pos, spd in sorted(zip(position, speed), reverse=True):    # 从离终点最近的车开始
        arrive = (target - pos) / spd  # 这辆车不受阻挡时的到达时间
        if arrive > latest:            # 比前面所有车队都晚：追不上，自成新车队
            fleets += 1
            latest = arrive
    return fleets
```

**例题：** LC 239 滑动窗口最大值

整数数组 `nums`（`1 <= length <= 10^5`）和窗口大小 `k`，窗口每次右移一位，返回每个窗口内的最大值。

```python
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    window: deque[int] = deque()       # 存下标；对应的值从队首到队尾严格递减
    ans: list[int] = []
    for i, x in enumerate(nums):
        while window and nums[window[-1]] <= x:
            window.pop()               # 比 x 小（或相等）且更靠左的数，永远没有机会当最大值
        window.append(i)
        if window[0] <= i - k:         # 队首已经滑出窗口
            window.popleft()
        if i >= k - 1:                 # 窗口满了才记录
            ans.append(nums[window[0]])
    return ans
```

**例题：** LC 121 买卖股票的最佳时机

`prices`（`1 <= length <= 10^5`）是每天股价，选一天买入、之后某天卖出，求最大利润，没有利润返回 `0`。

```python
def max_profit(prices: list[int]) -> int:
    low, best = prices[0], 0          # low：迄今最低价
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best
```

**例题：** LC 643 子数组最大平均数 I

整数数组 `nums`（`1 <= k <= n <= 10^5`，`-10^4 <= v <= 10^4`），求长度恰为 `k` 的连续子数组的最大平均数。

```python
def find_max_average(nums: list[int], k: int) -> float:
    window_sum = sum(nums[:k])
    best = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        best = max(best, window_sum)
    return best / k
```

**例题：** LC 3161 物块放置查询

数轴上有两种操作（`queries.length <= 1.5 * 10^5`）：`[1, x]` 在 `x` 处建障碍物；`[2, x, sz]` 判断区间 `[0, x]` 内能否放下长度为 `sz` 的物块（可贴着障碍物，不真放置）。返回所有类型 2 查询的结果。`x, sz <= min(5 * 10^4, 3 * queries.length)`。

```python
from bisect import bisect_left, bisect_right
def get_results(queries: list[list[int]]) -> list[bool]:
    size = max(q[1] for q in queries) + 1
    tree = [0] * (2 * size)             # 迭代线段树（区间最大值）：叶子 x = 以障碍物 x 结尾的空隙长度
    def update(pos: int, val: int) -> None:
        pos += size
        tree[pos] = val
        while pos > 1:
            pos >>= 1
            tree[pos] = max(tree[2 * pos], tree[2 * pos + 1])
    def query_max(r: int) -> int:       # 下标 [0, r] 上的最大值
        res, lo, hi = 0, size, r + 1 + size
        while lo < hi:
            if lo & 1:
                res = max(res, tree[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                res = max(res, tree[hi])
            lo >>= 1
            hi >>= 1
        return res
    obstacles = [0]                     # 有序的障碍物位置；原点当作哨兵
    ans: list[bool] = []
    for op, x, *rest in queries:
        if op == 1:
            k = bisect_left(obstacles, x)               # obstacles[k-1] 是前驱，obstacles[k] 是后继
            update(x, x - obstacles[k - 1])             # x 左边的空隙：x 到前驱
            if k < len(obstacles):                      # 后继的空隙被 x 截短
                update(obstacles[k], obstacles[k] - x)
            obstacles.insert(k, x)
        else:
            p = obstacles[bisect_right(obstacles, x) - 1]   # [0, x] 内最右的障碍物
            ans.append(max(query_max(p), x - p) >= rest[0])  # 之前的最大空隙，或最后一段 [p, x]
    return ans
```

**例题：** LC 20 有效的括号

字符串 `s`（`1 <= length <= 10^4`）只含 `()[]{}`，判断括号是否按类型和顺序正确闭合。

```python
def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}     # 右括号 -> 它该配的左括号
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:   # 栈空，或栈顶类型对不上
                return False
        else:
            stack.append(ch)
    return not stack                            # 还有没闭合的左括号就是无效
```

**例题：** LC 11 盛最多水的容器

`height`（`2 <= n <= 10^5`，`0 <= h <= 10^4`），选两条垂线与 x 轴围成容器，求最大盛水量。

```python
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        h = min(height[left], height[right])     # 水位由短板决定
        best = max(best, h * (right - left))
        if height[left] < height[right]:         # 移动长板只会让宽度变小、水位不会更高，所以动短板
            left += 1
        else:
            right -= 1
    return best
```
