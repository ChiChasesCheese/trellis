---
id: tlc-longest-mountain-in-array-2-code
node: p4.longest-mountain-in-array
type: qa
step: 2
---
## Q
**LC 845 数组中的最长山脉**｜写出 Python 实现

整数数组 `arr`（长度 `1` 到 `10^4`，元素 `0` 到 `10^4`）。山脉子数组是长度至少 `3`、先严格上升到山顶再严格下降的连续子数组。返回最长山脉子数组的长度，没有则返回 `0`。要求 `O(n)` 时间、`O(1)` 空间。

## A
**思路。** 遍历下标 `1` 到 `n - 2`，找山顶（比左右邻居都严格大）。找到后向左沿上坡、向右沿下坡走到山脚，更新答案，然后直接跳到右脚继续；不是山顶就前进一格。

```python
def longest_mountain(arr: list[int]) -> int:
    n = len(arr)
    best = 0
    i = 1
    while i < n - 1:
        if arr[i - 1] < arr[i] > arr[i + 1]:     # i 是山顶：两边严格更低
            left = i - 1
            while left > 0 and arr[left - 1] < arr[left]:
                left -= 1                         # 沿上坡走到山脚
            right = i + 1
            while right < n - 1 and arr[right] > arr[right + 1]:
                right += 1                        # 沿下坡走到山脚
            best = max(best, right - left + 1)
            i = right                             # 山脚右端不可能是山顶，直接从这里继续
        else:
            i += 1
    return best
```

运行：`[2,1,4,7,3,2,5]` → `5`，`[2,2,2]` → `0`，`[1,2,3]` → `0`，`[0,1,0]` → `3`，`[1,2,1,2,1]` → `3`，`[2,1,4,7,3,2,5,1,0]` → `5`。

**复杂度。** 时间 `O(n)`：山顶之间的坡不重复扫描；空间 `O(1)`。

**写法要点。**
- Python 支持链式比较：`arr[i - 1] < arr[i] > arr[i + 1]` 同时检查两侧，等价于 `arr[i-1] < arr[i] and arr[i] > arr[i+1]`，读起来就是“山顶”。
- 用 `while` 而不是 `for`：`i` 需要根据情况跳到 `right`。
- `right` 的循环条件是 `right < n - 1`，保证 `arr[right + 1]` 不越界；`left > 0` 同理。
- 一趟扫描 `O(1)` 空间的替代：`up`、`down` 计数器配合 `itertools.pairwise`，见追问。
- 另一种思路是两个辅助数组 `up[i]`、`down[i]` 记录每个位置的上坡步数与下坡步数，答案是两者都大于 `0` 的位置上的 `up + down + 1` 的最大值，`O(n)` 空间。
