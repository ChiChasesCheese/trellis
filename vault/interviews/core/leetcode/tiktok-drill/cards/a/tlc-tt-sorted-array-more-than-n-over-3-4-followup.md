---
id: tlc-tt-sorted-array-more-than-n-over-3-4-followup
node: a.tt-sorted-array-more-than-n-over-3
type: qa
step: 4
---
## Q
**有序数组中出现次数超过 n/3 的数**｜追问

面试官接着问：（1）阈值换成 `n / k`，怎么推广；（2）如果数组无序，还要 `O(n)` 时间、`O(1)` 空间怎么做；（3）数组存在磁盘或远端，读一次很贵，这个解法有什么好处？

## A
1. **推广到 `n / k`**：`step = max(1, n // k)`，候选仍是每隔 `step` 取一个下标上的值，数量 `O(k)`，总成本 `O(k log n)`。

```python
from bisect import bisect_left, bisect_right


def more_than_kth(nums: list[int], k: int) -> list[int]:
    n = len(nums)
    step = max(1, n // k)                                # n < k 时每个值都超过 n/k，step 取 1 逐个检查
    cands = {nums[i] for i in range(0, n, step)}
    return sorted(v for v in cands if k * (bisect_right(nums, v) - bisect_left(nums, v)) > n)
```

`more_than_kth([1,1,2,4,4], 3)` → `[1, 4]`。
2. **无序数组**：Boyer–Moore 多数投票的推广（LC 229 是 `k = 3`）。维护 `k - 1` 个候选和计数器：遇到候选就加一，有空位就放进去，否则所有计数器减一；扫完后再扫一遍验证候选的真实次数是否超过 `n / k`。`O(n)` 时间、`O(k)` 空间。
3. **磁盘 / 远端**：二分和抽样都只做 `O(log n)` 次随机读，常数次候选 × 两次二分；扫描需要顺序读完整个文件。有序文件上的这个做法几乎不受 `n` 影响。

**Python 提醒**：`bisect_left` / `bisect_right` 只在输入已排序时才正确，不会检查；一个值的出现次数是 `bisect_right - bisect_left`，等价于 `list.count` 但只要 `O(log n)`，而 `list.count` 是 `O(n)`。`range(0, n, 0)` 会抛 `ValueError`，所以 `step` 必须至少是 `1`。
