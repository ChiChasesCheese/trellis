---
id: tlc-max-consecutive-ones-iii-4-followup
node: b.max-consecutive-ones-iii
type: qa
step: 4
---
## Q
**LC 1004 最大连续1的个数 III**｜追问

面试官接着问：（1）要返回具体该翻哪些位置？（2）数据是流式的，不能回头读 `nums[left]`，怎么办？（3）改成「必须删掉恰好一个元素」（LC 1493）怎么改？

## A
1. **返回翻转位置**：更新答案时一并记下起点，`if right - left + 1 > best: best, start = right - left + 1, left`。最后在 `range(start, start + best)` 里挑出 `nums[i] == 0` 的下标，就是该翻的位置。
2. **流式，不能回看旧元素**：只保存窗口里 `0` 的下标，放进 `deque`（最多 `k` 个）。新来一个 `0` 时若队列已满 `k` 个，就让 `left = zeros.popleft() + 1`（越过最老的那个 `0`）；其余元素不必保存。内存 `O(k)`：

```python
from collections import deque
from collections.abc import Iterable


def longest_ones_stream(nums: Iterable[int], k: int) -> int:
    zeros: deque[int] = deque()            # 窗口内 0 的下标，从老到新
    best = left = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros.append(right)
            if len(zeros) > k:
                left = zeros.popleft() + 1 # 越过最老的 0，窗口重新合法
        best = max(best, right - left + 1)
    return best
```
3. **LC 1493**：把 `k` 固定为 `1`，答案是窗口长度减一（必须删一个元素；全是 `1` 的数组也要删一个）。

**Python 提醒**：不要用 `nums[left:right + 1].count(0)` 求窗口内 `0` 的个数——切片复制加计数每步 `O(窗口长度)`，总复杂度退化成 `O(n^2)`。
