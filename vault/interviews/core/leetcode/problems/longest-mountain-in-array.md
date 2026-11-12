---
slug: longest-mountain-in-array
---
## Q
**LC 845 数组中的最长山脉**｜Medium

求数组 `arr` 中最长的山脉子数组（严格上升再严格下降，长度至少 3）的长度，没有返回 `0`。

## A
**一句话。** 枚举山顶，从山顶向两侧沿坡走到山脚，处理完直接跳到右脚继续。

```python
def longest_mountain(arr):
    n = len(arr)
    best = 0
    i = 1
    while i < n - 1:
        if arr[i - 1] < arr[i] > arr[i + 1]:   # i 是山顶
            left = i - 1
            while left > 0 and arr[left - 1] < arr[left]:
                left -= 1                       # 上坡到山脚
            right = i + 1
            while right < n-1 and arr[right] > arr[right+1]:
                right += 1                      # 下坡到山脚
            best = max(best, right - left + 1)
            i = right                           # 从右脚继续
        else:
            i += 1
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只要上坡不要下坡：`[1,2,3]` 本应是 `0`，山顶两侧都必须至少一步。
- 用 `<=` 放松成非严格：`[2,2,2]` 平台被当成坡，应为 `0`。
- 扩展不判边界：`left = 0` 时 `arr[left-1]` 读到 `arr[-1]`，`[2,3,1,0]` 得 `5`，应为 `4`。

**追问。**
- 只判断整个数组是不是山脉？：同样先升后降，山顶不能在两端（LC 941）。
- 要返回山脉本身？：记下最优的 `left`、`right`，返回 `arr[left:right+1]`。

**同模式。** LC 941 有效的山脉数组、LC 852 山脉数组的峰值索引、LC 1671 得到山形数组的最少删除次数、LC 128 最长连续序列
