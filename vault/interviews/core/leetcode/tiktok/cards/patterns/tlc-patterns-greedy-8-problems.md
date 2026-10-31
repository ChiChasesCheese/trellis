---
id: tlc-patterns-greedy-8-problems
node: patterns.greedy
type: qa
step: 8
---
## Q
**贪心（Greedy）｜本组用到贪心的题**

按变形分类，这个题组里哪些题属于贪心？

## A
**可达范围 / 跳跃**
- LC 55 跳跃游戏
- LC 45 跳跃游戏 II
- LC 134 加油站

**逐位决策（高位优先）**
- LC 402 移掉 K 位数字（单调栈实现）
- LC 316 去除重复字母、LC 1081 不同字符的最小子序列（单调栈实现）

**带通配符的合法性**
- LC 678 有效的括号字符串

**排序 + 扫描**
- LC 122 买卖股票的最佳时机 II（累加所有上涨）
- LC 121 买卖股票的最佳时机（高频）
- LC 56 合并区间、LC 253 会议室 II（区间排序）
- LC 435 无重叠区间（高频）

**贪心 + 堆**
- LC 767 重构字符串
- LC 1834 单线程 CPU（高频）

**贪心不成立 ⇒ DP**
- LC 322 零钱兑换
- LC 198 打家劫舍

**TikTok 变体**
- 用给定数字组成小于 N 的最大数（高位优先，从最长公共前缀往回找第一个能变小的位）

提示：先找反例；找不到就尝试交换论证；仍不确定就写 DP 兜底。

**例题：** LC 55 跳跃游戏

`nums[i]` 是在下标 `i` 最多能向前跳的距离，从下标 `0` 出发，判断能否到达最后一个下标；`nums.length <= 10^4`。

```python
def can_jump(nums: list[int]) -> bool:
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True
```

**例题：** LC 45 跳跃游戏 II

同跳跃游戏，保证能到达最后一个下标，求最少跳跃次数；`nums.length <= 10^4`，`nums[i] <= 1000`。

```python
def jump(nums: list[int]) -> int:
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps
```

**例题：** LC 134 加油站

环形路线上 `gas[i]` 是加油量，`cost[i]` 是到下一站的耗油，油箱无限、起始为空；返回能绕一圈的唯一起点，不存在返回 `-1`；`n <= 10^5`。

```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    total = tank = start = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        diff = g - c
        total += diff
        tank += diff
        if tank < 0:
            start, tank = i + 1, 0
    return start if total >= 0 else -1
```

**例题：** LC 402 移掉 K 位数字

数字字符串 `num` 移掉 `k` 位使剩下的数最小，结果去掉前导零，全移掉返回 `"0"`；`1 <= k <= num.length <= 10^5`。

```python
def remove_kdigits(num: str, k: int) -> str:
    stack: list[str] = []
    for d in num:
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    stack = stack[: len(stack) - k]
    return "".join(stack).lstrip("0") or "0"
```

**例题：** LC 316 去除重复字母

小写字符串 `s`，去掉重复字母使每个字母只出现一次，保持相对顺序且字典序最小；`s.length <= 10^4`。

```python
def remove_duplicate_letters(s: str) -> str:
    last = {ch: i for i, ch in enumerate(s)}
    stack: list[str] = []
    in_stack: set[str] = set()
    for i, ch in enumerate(s):
        if ch in in_stack:
            continue
        while stack and stack[-1] > ch and last[stack[-1]] > i:
            in_stack.discard(stack.pop())
        stack.append(ch)
        in_stack.add(ch)
    return "".join(stack)
```

**例题：** LC 1081 不同字符的最小子序列

返回小写字符串 `s` 的字典序最小的子序列，要求包含 `s` 中每种字符恰好一次（与 LC 316 相同）；`s.length <= 1000`。

```python
def smallest_subsequence(s: str) -> str:
    last = {ch: i for i, ch in enumerate(s)}
    stack: list[str] = []
    in_stack: set[str] = set()
    for i, ch in enumerate(s):
        if ch in in_stack:
            continue
        while stack and stack[-1] > ch and last[stack[-1]] > i:
            in_stack.discard(stack.pop())
        stack.append(ch)
        in_stack.add(ch)
    return "".join(stack)
```

**例题：** LC 678 有效的括号字符串

字符串只含 `(`、`)`、`*`，其中 `*` 可当 `(`、`)` 或空串，判断是否是有效括号串；`s.length <= 100`。

```python
def check_valid_string(s: str) -> bool:
    lo = hi = 0
    for ch in s:
        lo += 1 if ch == '(' else -1
        hi += 1 if ch != ')' else -1
        if hi < 0:
            return False
        lo = max(lo, 0)
    return lo == 0
```

**例题：** LC 122 买卖股票的最佳时机 II

`prices[i]` 是第 `i` 天股价，可多次买卖但同时最多持有一股，求最大利润；`prices.length <= 3 * 10^4`。

```python
from itertools import pairwise
def max_profit(prices: list[int]) -> int:
    return sum(max(today - yesterday, 0) for yesterday, today in pairwise(prices))
```

**例题：** LC 56 合并区间

合并所有重叠区间（端点相接也算重叠），返回互不重叠的区间数组；`intervals.length <= 10^4`，端点 `<= 10^4`。

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    merged: list[list[int]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

**例题：** LC 253 会议室 II

会议时间 `intervals[i] = [start, end]`，一个会议结束的时刻可立刻开始下一个，求最少需要几间会议室；`intervals.length <= 10^4`。

```python
import heapq
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    ends: list[int] = []
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)
        else:
            heapq.heappush(ends, end)
    return len(ends)
```

**例题：** LC 767 重构字符串

重新排列小写字符串 `s`，使相邻字符都不同，可以就返回任意一种，不行返回 `""`；`s.length <= 500`。

```python
from collections import Counter
from heapq import heapify, heappop, heappush
def reorganize_string(s: str) -> str:
    heap = [(-cnt, ch) for ch, cnt in Counter(s).items()]
    heapify(heap)
    out: list[str] = []
    held = (0, "")
    while heap:
        cnt, ch = heappop(heap)
        out.append(ch)
        if held[0]:
            heappush(heap, held)
        held = (cnt + 1, ch)
    return "".join(out) if len(out) == len(s) else ""
```

**例题：** LC 322 零钱兑换

`coins` 是面额（每种数量无限），求凑成 `amount` 的最少硬币数，凑不出返回 `-1`；`coins.length <= 12`，`amount <= 10^4`。

```python
def coin_change(coins: list[int], amount: int) -> int:
    inf = amount + 1
    dp = [0] + [inf] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < inf else -1
```

**例题：** LC 198 打家劫舍

一排房屋 `nums[i]` 是现金，相邻两间不能同时偷，求最大金额；`nums.length <= 100`，`nums[i] <= 400`。

```python
def rob(nums: list[int]) -> int:
    skip = take = 0
    for x in nums:
        skip, take = max(skip, take), skip + x
    return max(skip, take)
```

**例题：** LC 435 无重叠区间

区间数组 `intervals`，返回最少需要移除多少个区间才能让剩下的两两不重叠（只在端点接触不算重叠）；`1 <= intervals.length <= 10^5`。

```python
from math import inf
from operator import itemgetter
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    kept, end = 0, -inf
    for start, finish in sorted(intervals, key=itemgetter(1)):
        if start >= end:
            kept += 1
            end = finish
    return len(intervals) - kept
```

**例题：** LC 121 买卖股票的最佳时机

`prices[i]` 是第 `i` 天的股价，选一天买入、之后的某天卖出，返回最大利润，不能获利返回 `0`；`1 <= prices.length <= 10^5`。

```python
def max_profit(prices: list[int]) -> int:
    low, best = prices[0], 0
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best
```

**例题：** LC 1834 单线程 CPU

`tasks[i] = [enqueueTime, processingTime]`；CPU 空闲时从已到达的任务里选执行时间最短的（并列取下标最小），一次只做一项且不可中断；返回任务的执行顺序；`1 <= n <= 10^5`，时间 `<= 10^9`。

```python
from heapq import heappop, heappush
def get_order(tasks: list[list[int]]) -> list[int]:
    n = len(tasks)
    order = sorted(range(n), key=lambda i: tasks[i][0])
    heap: list[tuple[int, int]] = []
    res: list[int] = []
    t = p = 0
    while len(res) < n:
        if not heap and t < tasks[order[p]][0]:
            t = tasks[order[p]][0]
        while p < n and tasks[order[p]][0] <= t:
            i = order[p]
            heappush(heap, (tasks[i][1], i))
            p += 1
        cost, i = heappop(heap)
        t += cost
        res.append(i)
    return res
```

**例题：** 用给定数字组成小于 N 的最大数

给正整数 `N` 和数字数组 `digits`（每个数字可重复使用），拼出严格小于 `N` 的最大整数，无前导零，拼不出返回 `-1`；`N <= 10^18`。

```python
from bisect import bisect_left
def largest_below(n: int, digits: list[int]) -> int:
    """由 digits 中的数字（可重复使用）拼出严格小于 n 的最大非负整数，没有则返回 -1。"""
    allowed = sorted(set(digits))
    top = allowed[-1]
    s = str(n)
    length = len(s)
    usable = set(allowed)
    p = 0
    while p < length and int(s[p]) in usable:
        p += 1
    for i in range(min(p, length - 1), -1, -1):
        j = bisect_left(allowed, int(s[i]))
        if j and (allowed[j - 1] or i or length == 1):
            return int(s[:i] + str(allowed[j - 1]) + str(top) * (length - i - 1))
    if length > 1:
        return int(str(top) * (length - 1))
    return -1
```
