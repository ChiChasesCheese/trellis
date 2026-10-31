---
id: tlc-patterns-monotonic-stack-5-variants
node: patterns.monotonic-stack
type: qa
step: 5
---
## Q
**单调栈与单调队列｜变形：滑动窗口最大值、小行星碰撞、以每个元素为最小值的区间、柱状图最大矩形**

单调队列怎样处理窗口过期？小行星碰撞为什么也是栈？「以它为最小值的最长区间」怎样在弹栈时得到？

## A
- **单调队列**：队列存下标，值从队首到队尾递减，队首永远是窗口最大值；新元素进来时，比它小且更早的元素永远不会再成为最大值，从队尾弹掉；队首下标滑出窗口 `i - k` 时从队首弹出（例：LC 239 滑动窗口最大值）。
- **碰撞栈**：只有栈顶向右（`> 0`）、新元素向左（`< 0`）才会碰撞；栈顶更小就弹出并继续碰撞，同样大两个都消失，栈顶更大则新来的消失；栈里留下的就是存活者（例：LC 735 小行星碰撞）。
- **弹栈时算区间**：栈里的值递增；元素 `h` 被弹出时，新栈顶是它左边更小的位置，当前下标 `i` 是右边更小或相等的位置，所以以 `h` 为最小值的最长区间长度 `k = i - 左边界 - 1`；若 `h * k > threshold`，这个区间里每个数都 `>= h > threshold / k`，返回 `k`。末尾补一个 `0` 把栈清空（例：LC 2334 元素值大于变化阈值的子数组）。
- **最大矩形**：同样在弹栈时确定每根柱子向左右能扩多远，面积 = 高度 × 宽度 `i - 左边界 - 1`，对所有柱子取最大（例：LC 84 柱状图中最大的矩形）。

**例题：** LC 239 滑动窗口最大值

大小为 `k` 的窗口从数组最左滑到最右，返回每个窗口里的最大值，`1 <= nums.length <= 10^5`。

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

**例题：** LC 735 小行星碰撞

数组中绝对值是大小、正负是方向（正向右、负向左），碰撞时小的爆炸、一样大都爆炸，返回碰撞后剩下的小行星，`2 <= asteroids.length <= 10^4`。

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

**例题：** LC 2334 元素值大于变化阈值的子数组

找长度为 `k` 的子数组，使每个元素都大于 `threshold / k`，返回任意一个满足的 `k`，没有则返回 `-1`，`1 <= nums.length <= 10^5`。

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

**例题：** LC 84 柱状图中最大的矩形

柱子宽度都为 1、高度 `heights[i]`，求柱状图中能勾勒出的矩形的最大面积，`1 <= heights.length <= 10^5`。

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
