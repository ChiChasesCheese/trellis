---
id: tlc-maximum-product-subarray-2-code
node: p4.maximum-product-subarray
type: qa
step: 2
---
## Q
**LC 152 乘积最大子数组**｜写出 Python 实现

整数数组 `nums`（长度 `1` 到 `2 * 10^4`，元素 `-10` 到 `10`，任意子数组乘积都在 32 位整数内），返回乘积最大的非空连续子数组的乘积。要求 `O(n)` 时间、`O(1)` 空间。

## A
**思路。** 遍历时维护以当前位置结尾的最大乘积 `hi` 和最小乘积 `lo`。对每个新元素 `x`，候选是 `x` 本身、`hi * x`、`lo * x`；新的 `hi` 取三者最大，`lo` 取三者最小。答案取各位置 `hi` 的最大值。

```python
def max_product(nums: list[int]) -> int:
    best = hi = lo = nums[0]                # hi/lo：以当前位置结尾的最大/最小乘积
    for x in nums[1:]:
        cand = (x, hi * x, lo * x)          # 要么从 x 重新开始，要么接在前面的最大/最小乘积后面
        hi, lo = max(cand), min(cand)       # 负数会让最小变最大，所以两个都要带着走
        best = max(best, hi)
    return best
```

运行：`[2,3,-2,4]` → `6`，`[-2,0,-1]` → `0`，`[-2]` → `-2`，`[-2,3,-4]` → `24`，`[0,2]` → `2`，`[-1,-2,-3,0]` → `6`。

**复杂度。** 时间 `O(n)`：一趟扫描，每步常数次乘法和比较；空间 `O(1)`。

**写法要点。**
- 先把三个候选放进元组 `cand`，再 `max(cand)`、`min(cand)`：比 `if x < 0: hi, lo = lo, hi` 的交换写法更不容易漏掉 `0` 和重新开始的情形，也不需要分支。
- `hi, lo = max(cand), min(cand)` 一次赋值，两个值都基于旧的 `hi`、`lo`（候选在赋值前已算好）。
- `best = hi = lo = nums[0]` 用第一个元素初始化，答案可能是负数，不能从 `0` 开始。
- `for x in nums[1:]` 切片会复制数组，`n = 2 * 10^4` 无碍；想省复制可用 `itertools.islice(nums, 1, None)`。
