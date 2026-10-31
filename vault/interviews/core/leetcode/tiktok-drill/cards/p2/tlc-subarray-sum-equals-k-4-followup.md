---
id: tlc-subarray-sum-equals-k-4-followup
node: p2.subarray-sum-equals-k
type: qa
step: 4
---
## Q
**LC 560 和为 K 的子数组**｜追问

面试官接着问：（1）要找和为 `k` 的**最长**子数组的长度？（2）要统计和能被 `k` 整除的子数组个数？（3）数组是二维矩阵，统计和为 `k` 的子矩阵个数？

## A
1. **最长子数组**（LC 325）：哈希表不再存次数，存前缀和**第一次**出现的下标——越早出现，子数组越长。
```python
def longest_subarray_sum(nums: list[int], k: int) -> int:
    first: dict[int, int] = {0: -1}       # 前缀和 -> 第一次出现的下标；空前缀在 -1
    pre = best = 0
    for i, x in enumerate(nums):
        pre += x
        if (j := first.get(pre - k)) is not None:
            best = max(best, i - j)
        first.setdefault(pre, i)          # 只记第一次
    return best
```
   `[1,-1,5,-2,3]`、`k = 3` 返回 `4`（`[1,-1,5,-2]`）。
2. **能被 `k` 整除**（LC 974）：两个前缀和同余时，它们之差被 `k` 整除。把键换成 `pre % k`，Python 的 `%` 对负数也返回非负余数，直接可用。
```python
from collections import Counter

def subarrays_div_by_k(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})
    pre = ans = 0
    for x in nums:
        pre = (pre + x) % k
        ans += seen[pre]
        seen[pre] += 1
    return ans
```
   `[4,5,0,-2,-3,1]`、`k = 5` 返回 `7`。
3. **子矩阵**（LC 1074）：固定上下两行，把这两行之间每一列的和压成一维数组，在这个一维数组上套用同样的前缀和做法，总共 `O(m^2 n)`。

**Python 提醒**：`dict.setdefault(key, value)` 只在键不存在时写入，正好用来「只记第一次」；`Counter` 里 `seen[x] += 1` 对新键从 `0` 开始，不需要先判断。在 C++/Java 里 `%` 对负数得负余数，要写 `((x % k) + k) % k`，Python 不需要。
