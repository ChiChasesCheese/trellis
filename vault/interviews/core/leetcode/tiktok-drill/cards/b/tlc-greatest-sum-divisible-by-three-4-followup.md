---
id: tlc-greatest-sum-divisible-by-three-4-followup
node: b.greatest-sum-divisible-by-three
type: qa
step: 4
---
## Q
**LC 1262 可被三整除的最大和**｜Medium · 字节高频｜追问

面试官接着问：（1）有没有更简单、更省空间的做法？（2）改成被一般的 `k` 整除？（3）只求「有几种选法」呢？

## A
1. **贪心**：设总和 `total`，余数 `r = total % 3`。`r == 0` 全选；否则只需删去**损失最小**的一组：一个余数为 `r` 的最小数，或两个余数为 `3 - r` 的最小数之和，取较小者；两种都不存在则答案 `0`。
```python
def max_sum_div_three_greedy(nums: list[int]) -> int:
    total = sum(nums)
    r = total % 3
    if r == 0:
        return total
    same = sorted(x for x in nums if x % 3 == r)            # 余数与 total 相同的数
    other = sorted(x for x in nums if x % 3 == 3 - r)       # 余数互补的数
    cuts = ([same[0]] if same else []) + ([other[0] + other[1]] if len(other) >= 2 else [])
    return total - min(cuts) if cuts else 0
```
   `[3,6,5,1,8]` → `18`，`[4]` → `0`，`[1,2,3,4,4]` → `12`。空间可以压到 O(1)：见 Python 工具箱「DP 降维」。
2. **一般的 `k`**：状态数变成 `k`，转移 `dp[i][r] = max(dp[i - 1][r], dp[i - 1][(r - x) % k] + x)`，`O(nk)`。贪心在 `k > 3` 时不再成立，因为要删的数的组合多了。
3. **计数**：把 `max` 换成加法，`dp[i][r] = dp[i - 1][r] + dp[i - 1][(r - x) % k]`，`dp[0][0] = 1`，对大数取模。

**Python 提醒**：`sorted(x for x in nums if x % 3 == r)` 排序整个子列表是 `O(n log n)` 时间、`O(n)` 空间；要严格 `O(n)` 时间、`O(1)` 空间，用一趟循环同时维护两类余数各自的最小和次小值。
