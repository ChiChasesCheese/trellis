---
id: tlc-patterns-monotonic-stack-7-problems
node: patterns.monotonic-stack
type: qa
step: 7
---
## Q
**单调栈与单调队列（Monotonic Stack）｜本组用到单调栈的题**

按变形分类，这个题组里哪些题用单调栈或单调队列？

## A
**下一个更大 / 更小**
- LC 739 每日温度
- LC 581 最短无序连续子数组（栈或两遍扫描找边界）

**以每个元素为最值的区间**
- LC 84 柱状图中最大的矩形
- LC 2334 元素值大于变化阈值的子数组
- LC 42 接雨水（单调栈版本，另有双指针 / DP 版本）

**字典序最小 / 删除字符**
- LC 316 去除重复字母
- LC 1081 不同字符的最小子序列（与 LC 316 相同）
- LC 402 移掉 K 位数字

**栈模拟（相邻抵消）**
- LC 735 小行星碰撞
- LC 1209 删除字符串中的所有相邻重复项 II（栈存 `(字符, 计数)`）
- LC 856 括号的分数

**单调队列**
- LC 239 滑动窗口最大值

提示：先问是「找最近的更大 / 更小」，还是「维护窗口的最值」，前者栈、后者双端队列；再决定存下标、比较符号和哨兵。

**例题：** LC 739 每日温度

`temperatures[i]` 是第 `i` 天温度，求每天要等几天才会出现更高温度，没有则为 `0`；`temperatures.length <= 10^5`。

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    answer = [0] * len(temperatures)
    stack: list[int] = []
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer
```

**例题：** LC 581 最短无序连续子数组

找最短的连续子数组，把它升序排序后整个数组变为升序，返回其长度；`nums.length <= 10^4`，进阶 `O(n)`。

```python
from math import inf
def find_unsorted_subarray(nums: list[int]) -> int:
    n = len(nums)
    start, end = 0, -1
    hi, lo = -inf, inf
    for i in range(n):
        if nums[i] < hi:
            end = i
        else:
            hi = nums[i]
        j = n - 1 - i
        if nums[j] > lo:
            start = j
        else:
            lo = nums[j]
    return end - start + 1
```

**例题：** LC 84 柱状图中最大的矩形

`heights[i]` 是宽为 `1` 的柱子的高度，求柱状图中最大矩形的面积；`heights.length <= 10^5`，`heights[i] <= 10^4`。

```python
def largest_rectangle_area(heights: list[int]) -> int:
    stack: list[int] = []
    best = 0
    for i, h in enumerate([*heights, 0]):
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best
```

**例题：** LC 2334 元素值大于变化阈值的子数组

找一个长度为 `k` 的子数组，其中每个元素都大于 `threshold / k`，返回任意一个满足的长度，没有返回 `-1`；`nums.length <= 10^5`，`nums[i], threshold <= 10^9`。

```python
from itertools import chain
def valid_subarray_size(nums: list[int], threshold: int) -> int:
    stack: list[int] = []
    for i, x in enumerate(chain(nums, (0,))):
        while stack and nums[stack[-1]] >= x:
            h = nums[stack.pop()]
            left = stack[-1] if stack else -1
            k = i - left - 1
            if h * k > threshold:
                return k
        stack.append(i)
    return -1
```

**例题：** LC 42 接雨水

`height[i]` 是宽为 `1` 的柱子的高度，求下雨后一共能接多少雨水；`height.length <= 2 * 10^4`。

```python
def trap(height: list[int]) -> int:
    stack: list[int] = []
    water = 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = height[stack.pop()]
            if not stack:
                break
            left = stack[-1]
            water += (min(height[left], h) - bottom) * (i - left - 1)
        stack.append(i)
    return water
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

**例题：** LC 735 小行星碰撞

正数向右、负数向左、速度相同，相撞时小的爆炸、相等则同归于尽，求碰撞结束后剩下的小行星；`2 <= asteroids.length <= 10^4`。

```python
def asteroid_collision(asteroids: list[int]) -> list[int]:
    stack: list[int] = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            top = stack[-1]
            if top <= -a:
                stack.pop()
            alive = top < -a
        if alive:
            stack.append(a)
    return stack
```

**例题：** LC 1209 删除字符串中的所有相邻重复项 II

反复删除 `k` 个相邻且相等的字母，直到不能再删，返回最终字符串；`s.length <= 10^5`，`2 <= k <= 10^4`。

```python
def remove_duplicates(s: str, k: int) -> str:
    stack: list[tuple[str, int]] = []
    for ch in s:
        if stack and stack[-1][0] == ch:
            _, cnt = stack.pop()
            if cnt + 1 < k:
                stack.append((ch, cnt + 1))
        else:
            stack.append((ch, 1))
    return "".join(ch * cnt for ch, cnt in stack)
```

**例题：** LC 856 括号的分数

平衡括号串 `s`：`()` 得 `1` 分，`AB` 得 `A + B`，`(A)` 得 `2 * A`，求 `s` 的分数；`2 <= s.length <= 50`。

```python
def score_of_parentheses(s: str) -> int:
    stack = [0]
    for ch in s:
        if ch == "(":
            stack.append(0)
        else:
            inner = stack.pop()
            stack[-1] += max(2 * inner, 1)
    return stack[0]
```

**例题：** LC 239 滑动窗口最大值

大小为 `k` 的窗口从左到右滑过 `nums`，返回每个窗口的最大值；`nums.length <= 10^5`，`1 <= k <= nums.length`。

```python
from collections import deque
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    window: deque[int] = deque()
    ans: list[int] = []
    for i, x in enumerate(nums):
        while window and nums[window[-1]] <= x:
            window.pop()
        window.append(i)
        if window[0] <= i - k:
            window.popleft()
        if i >= k - 1:
            ans.append(nums[window[0]])
    return ans
```
