---
id: tlc-longest-mountain-in-array-4-followup
node: b.longest-mountain-in-array
type: qa
step: 4
---
## Q
**LC 845 数组中的最长山脉**｜追问

面试官接着问：（1）进阶要求的一趟扫描、`O(1)` 空间怎么写？（2）要返回最长山脉本身？（3）判断整个数组是不是山脉（LC 941）？

## A
1. **一趟扫描。** 用 `up`（当前山的上坡步数）和 `down`（下坡步数）两个计数器，`itertools.pairwise` 逐对比较相邻元素：
```python
from itertools import pairwise

def longest_mountain_one_pass(arr: list[int]) -> int:
    best = up = down = 0
    for prev, cur in pairwise(arr):
        if down and prev < cur or prev == cur:   # 下坡之后又上坡，或平台：山脉结束
            up = down = 0
        up += prev < cur
        down += prev > cur
        if up and down:
            best = max(best, up + down + 1)
    return best
```
`[2,1,4,7,3,2,5]` → `5`，`[2,2,2]` → `0`，`[1,2,3]` → `0`，`[0,1,0]` → `3`。注意先清零再计数：遇到新的上坡时，之前的山已经结束，这个上升步要算进新山的 `up`。
2. **返回山脉本身。** 山顶扩展版里更新 `best` 时记下 `left` 与 `right`，返回 `arr[left:right + 1]`；计数器版用 `enumerate(pairwise(arr), 1)` 拿到当前下标 `k`，山的起点是 `k - up - down`。
3. **LC 941。** 先沿严格上升走到山顶，检查山顶不在两端，再沿严格下降走到末尾，必须刚好走到最后一个元素：
```python
def valid_mountain_array(arr: list[int]) -> bool:
    n = len(arr)
    i = 0
    while i + 1 < n and arr[i] < arr[i + 1]:
        i += 1                              # 上坡
    if i == 0 or i == n - 1:
        return False                        # 没有上坡，或没有下坡
    while i + 1 < n and arr[i] > arr[i + 1]:
        i += 1                              # 下坡
    return i == n - 1
```
`[2,1]` → `False`，`[3,5,5]` → `False`，`[0,3,2,1]` → `True`。

**Python 提醒**：`up += prev < cur` 把布尔值当整数相加（`True` 是 `1`），可读性取决于团队习惯；面试里也可以写成 `if prev < cur: up += 1`。`itertools.pairwise` 需要 Python 3.10 以上。
