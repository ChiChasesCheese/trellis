---
id: tlc-number-of-longest-increasing-subsequence-4-followup
node: a.number-of-longest-increasing-subsequence
type: qa
step: 4
---
## Q
**LC 673 最长递增子序列的个数**｜追问

面试官接着问：（1）`n` 到 `10^5` 怎么办？（2）只求最长长度？（3）要返回其中一个最长子序列？

## A
1. **`n` 很大**：思路是按长度分层。第 `k` 层记录所有长度为 `k+1` 的子序列的结尾值（取负后单调），以及方案数的前缀和；新元素 `x` 用二分找到它所在的层，再在上一层用二分求「结尾值 < `x`」的方案数之和，`O(n log n)`。
```python
def find_number_of_lis_fast(nums: list[int]) -> int:
    neg: list[list[int]] = []     # neg[k]：第 k 层各结尾值取负，按到达顺序不降
    pref: list[list[int]] = []    # pref[k]：对应方案数的前缀和，pref[k][0] = 0
    for x in nums:
        k = bisect_left(range(len(neg)), x, key=lambda t: -neg[t][-1])
        if k == 0:
            c = 1
        else:
            i = bisect_right(neg[k - 1], -x)
            c = pref[k - 1][-1] - pref[k - 1][i]
        if k == len(neg):
            neg.append([])
            pref.append([0])
        neg[k].append(-x)
        pref[k].append(pref[k][-1] + c)
    return pref[-1][-1]
```
2. **只求长度**：LC 300，`tails` 数组加 `bisect_left`。
3. **返回一个最长子序列**：多存 `prev[i]`，从最长位置回溯。

**Python 提醒**：`bisect` 的 `key=` 参数（3.10+）只作用于序列里的元素，不作用于被查找的值 `x`；这里序列是下标 `range(len(neg))`，`key` 把下标映射成该层的最小结尾值，省去先建一个新列表。
