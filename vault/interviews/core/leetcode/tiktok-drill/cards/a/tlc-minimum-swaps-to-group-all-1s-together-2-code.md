---
id: tlc-minimum-swaps-to-group-all-1s-together-2-code
node: a.minimum-swaps-to-group-all-1s-together
type: qa
step: 2
---
## Q
**LC 1151 最少交换次数来组合所有的 1**｜写出 Python 实现

二进制数组 `data`（长度 `1` 到 `10^5`，元素是 `0` 或 `1`），每次可交换任意两个位置的元素，返回把所有 `1` 聚成连续一段所需的最少交换次数。

## A
**思路。** 令 `w` 为 `1` 的总数。长度为 `w` 的窗口里，`0` 的个数就是需要的交换次数；用滑动窗口求窗口内 `1` 的最大个数 `best`，答案是 `w - best`。

```python
def min_swaps(data: list[int]) -> int:
    w = sum(data)                         # 窗口宽度 = 1 的总数
    cur = sum(data[:w])                   # 第一个窗口里已有的 1
    best = cur
    for i in range(w, len(data)):
        cur += data[i] - data[i - w]      # 右端进一个、左端出一个
        best = max(best, cur)
    return w - best                       # 窗口里的 0 的个数 = 需要换进来的 1 的个数
```

运行：`[1,0,1,0,1]` → `1`，`[0,0,0,1,0]` → `0`，`[1,0,1,0,1,0,0,1,1,0,1]` → `3`，`[1,0,1,0,1,0,1,1,1,0,1,0,0,1,1,1,0,0,1,1,1,0,1,0,1,1,0,0,0,1,1,1,1,0,0,1]` → `8`，`[0,0,0]` → `0`，`[1,0,0,0,1,1,1]` → `1`。

**复杂度。** 时间 `O(n)`：求和一遍加滑动一遍；空间 `O(1)`，不计 `data[:w]` 的临时切片。

**写法要点。** 因为元素只有 `0/1`，`sum` 直接得到 `1` 的个数，窗口增量就是 `data[i] - data[i - w]`，不需要计数字典；`range(w, len(data))` 从第二个窗口起步，第一个窗口单独初始化，循环里没有 `if`。想用前缀和写成声明式：`pre = list(accumulate(data, initial=0))`，然后 `max(pre[i + w] - pre[i] for i in range(len(data) - w + 1))`，窗口求和变成两次索引，适合要反复查询窗口的场景。
