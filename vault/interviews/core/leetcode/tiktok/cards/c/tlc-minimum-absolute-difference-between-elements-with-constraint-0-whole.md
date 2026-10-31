---
id: tlc-minimum-absolute-difference-between-elements-with-constraint-0-whole
node: c.minimum-absolute-difference-between-elements-with-constraint
type: qa
---
## Q
**LC 2817 限制条件下元素之间的最小绝对差**｜Medium · LC TikTok 全时段热度 26/100

给定下标从 0 开始的整数数组 `nums` 和整数 `x`，找出两个下标 `i`、`j` 满足 `abs(i - j) >= x`，使 `abs(nums[i] - nums[j])` 最小，返回这个最小值。`1 <= nums.length <= 10^5`，`1 <= nums[i] <= 10^9`，`0 <= x < nums.length`。例：`nums = [4,3,2,4], x = 2` → `0`（取 `nums[0]` 和 `nums[3]`）；`nums = [5,3,2,10,15], x = 1` → `1`；`nums = [1,2,3,4], x = 3` → `3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 从左到右扫描下标 `i`，把「与 `i` 距离至少 `x`」的元素（即 `nums[i - x]` 及更早）依次放进有序列表，用二分找 `nums[i]` 的前驱和后继，答案是所有差值的最小值。

**识别。** 「下标距离至少 `x`」意味着每个位置的候选集合随 `i` 增大只会增加；「值之差最小」就是在有序集合里找最近邻。有序集合 + 二分是标准做法。

**推导。** 暴力：枚举所有下标对，`O(n^2)`，`n = 10^5` 不可行。洞察：对固定的 `i`，只需要候选集合里离 `nums[i]` 最近的两个值（前驱和后继）；候选集合只增不删，所以用有序列表 `insort` 维护即可。

```python
from bisect import bisect_left, insort
from math import inf


def min_absolute_difference(nums: list[int], x: int) -> int:
    seen: list[int] = []                         # 升序列表：已经与当前下标距离 >= x 的所有值
    best = inf
    for i in range(x, len(nums)):
        insort(seen, nums[i - x])                # nums[i-x] 现在与 nums[i] 距离恰好 x，可以加入候选
        v = nums[i]
        k = bisect_left(seen, v)                 # 在有序候选里找 v 的前驱和后继
        if k < len(seen):
            best = min(best, seen[k] - v)        # 后继：>= v 的最小值
        if k > 0:
            best = min(best, v - seen[k - 1])    # 前驱：< v 的最大值
    return best
```

运行：`[4,3,2,4]`, `x = 2` → `0`；`[5,3,2,10,15]`, `x = 1` → `1`；`[1,2,3,4]`, `x = 3` → `3`；`[5]`, `x = 0` → `0`；`x = 0` 时同一下标自己与自己也满足 `abs(i - j) >= 0`，所以结果总是 `0`；随机 `10^5` 个数、`x = 1` 在不到 1 秒内跑完。

**复杂度。** 时间 `O(n log n + n * s)`，其中 `insort` 的元素搬移 `s` 是内存拷贝，实测 `10^5` 规模很快；空间 `O(n)`。

**拓展优化。**
- 面试要求严格 `O(n log n)` 时说明：平衡树 / 跳表 / `sortedcontainers.SortedList`（第三方库）可以做到 `O(log n)` 插入；标准库没有，需要自己实现或用线段树对离散化后的值做区间查询。
- 一旦 `best == 0` 可以立刻返回。

**易错点。**
- 把 `nums[i]` 自己也加进候选：违反距离约束，`nums = [1,2,3,4]`, `x = 3` 会得到 `0`，应为 `3`。
- 只看后继不看前驱（或相反）：`nums = [5,3,2,10,15]` 里 `nums[2] = 2` 的最近邻 `3` 是前一个，漏掉前驱会偏大。
- 把 `x = 0` 当成要求 `i != j`：题目允许 `abs(i - j) >= 0`，即 `i = j`，所以答案恒为 `0`；解法里先加入 `nums[i - x]` 自然得到这个结果。

**追问。**
- 绝对差最小的下标对本身：在更新 `best` 时记录下标，需要把值和下标一起存成 `(值, 下标)`。
- 要求 `abs(i - j) <= x`（窗口内最近的值）：改成滑动窗口，需要支持删除，用 `SortedList` 或延迟删除的堆。

**同模式。** LC 220 存在重复元素 III、LC 1 两数之和、LC 2386 找出数组的第 K 大和、LC 456 132 模式、LC 658 找到 K 个最接近的元素。
