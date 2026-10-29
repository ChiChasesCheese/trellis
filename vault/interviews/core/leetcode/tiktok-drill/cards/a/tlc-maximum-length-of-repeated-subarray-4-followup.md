---
id: tlc-maximum-length-of-repeated-subarray-4-followup
node: a.maximum-length-of-repeated-subarray
type: qa
step: 4
---
## Q
**LC 718 最长重复子数组**｜追问

面试官接着问：（1）要返回这个子数组本身而不是长度？（2）两个数组长度到 `10^5`，`O(m·n)` 不行了怎么办？（3）改成最长公共子序列（LC 1143）要改什么？（4）空间能不能更小？

## A
1. **返回子数组**：记录取得最大值时在 `nums1` 中的结束位置，最后切片 `nums1[end - best:end]`。主解法的外层下标 `i` 就是结束位置（`dp[i][j]` 以 `nums1[i-1]` 结尾，切片右端 `i` 不含），更新最大值时同时保存 `end = i`，`([1,2,3,2,1], [3,2,1,4,7])` 得到 `[3, 2, 1]`。
2. **大规模**：公共子数组的长度有**单调性**——存在长度 `L` 的公共子数组，就存在长度 `L - 1` 的；所以对 `L` 二分，每次用哈希检查两个数组是否有相同的长度 `L` 窗口。下面用元组当哈希键，简单直观；真正的大输入要换成滚动哈希（rolling hash，窗口哈希 `O(1)` 更新），整体 `O((m + n) log min(m, n))`。

```python
def find_length_hash(nums1: list[int], nums2: list[int]) -> int:
    def common(length: int) -> bool:
        seen = {tuple(nums1[i:i + length]) for i in range(len(nums1) - length + 1)}
        return any(tuple(nums2[j:j + length]) in seen
                   for j in range(len(nums2) - length + 1))

    lo, hi = 0, min(len(nums1), len(nums2))    # 公共子数组长度有单调性：长度 L 存在则 L-1 也存在
    while lo < hi:
        mid = (lo + hi + 1) // 2               # 上取整，避免 lo = mid 时死循环
        if common(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

`([1,2,3,2,1], [3,2,1,4,7])` → `3`，`([0]*1000, [0]*1000)` → `1000`。用元组切片每次检查是 `O(n·L)`，所以只适合中等规模；滚动哈希才是线性检查。
3. **最长公共子序列**：转移改成不匹配时继承 `max(dp[i-1][j], dp[i][j-1])`，答案取 `dp[m][n]`，不再需要全局最大值。
4. **省空间**：空间可以压到 O(n)：见 Python 工具箱「DP 降维」。
5. 极限做法：后缀自动机（suffix automaton）或后缀数组，`O(m + n)` 到 `O((m + n) log)`，一般只作为方向提一句。

**Python 提醒**：列表不可哈希，不能直接放进 `set`，要先转成 `tuple`；二分用"上取整" `(lo + hi + 1) // 2`，因为分支里有 `lo = mid`，向下取整会在 `hi = lo + 1` 时停滞。
