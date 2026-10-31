---
id: tlc-single-element-in-a-sorted-array-0-whole
node: p2.single-element-in-a-sorted-array
type: qa
---
## Q
**LC 540 有序数组中的单一元素**｜Medium · LC 字节 近 6 个月热度 88/100（全时段 50） · CodeTop 国内累计 2 次 · 最近 2026-04-09（国内 CodeTop）

给一个仅由整数组成的**有序**数组，其中每个元素都会出现两次，唯有一个数只会出现一次。找出并返回只出现一次的那个数。要求 `O(log n)` 时间和 `O(1)` 空间。`1 <= nums.length <= 10^5`，`0 <= nums[i] <= 10^5`。例：`nums = [1,1,2,3,3,4,4,8,8]` → `2`；`nums = [3,3,7,7,10,11,11]` → `10`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 二分查找「下标奇偶性」：单一元素之前，每对相同元素从偶数下标开始（`nums[2k] == nums[2k+1]`）；单一元素之后，每对都从奇数下标开始。取偶数对齐的 `mid`，若 `nums[mid] == nums[mid+1]` 说明这一对完整、单一元素在右边，否则在 `mid` 或更左。`O(log n)`。

**识别。** 「有序」加「要求 `O(log n)`」是二分的信号；「只有一个数出现一次，其余成对」意味着数组长度是奇数，并且成对结构被单一元素“错位”了一次。如果不要求 `O(log n)`，异或全体元素（相同的数两两抵消）就是 `O(n)`、`O(1)` 的解，题目特意要求更快，所以要利用“有序”。

**推导。** 暴力：线性扫描每次跳两格，找第一个 `nums[i] != nums[i+1]`，`O(n)`；异或也是 `O(n)`。能二分的前提是找到一个对下标**单调**的条件。观察：在单一元素之前，第 `2k` 个下标与第 `2k+1` 个下标相等；单一元素之后，这个相等关系变成 `nums[2k] != nums[2k+1]`（因为整体错位了一格）。所以对偶数下标 `m`，条件「`nums[m] != nums[m+1]`」是先假后真的单调谓词，分界点就是单一元素的位置。

**简单解法。** 全体异或：成对的数两两抵消，剩下的就是答案，不管有序。

```python
from functools import reduce
from operator import xor

def single_non_duplicate(nums: list[int]) -> int:
    return reduce(xor, nums)                       # a ^ a = 0，a ^ 0 = a：成对的数全部抵消
```

时间 `O(n)`、空间 `O(1)`；没用上有序性，题面要求 `O(log n)`，只是基线。

最优解：

```python
def single_non_duplicate(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1               # 偶数下标：n 为奇数，n-1 是偶数；之后 lo=mid+2、hi=mid 也保持偶数
    while lo < hi:
        mid = (lo + hi) // 2
        mid -= mid & 1                      # 对齐到偶数下标：mid 必是某一对的左端（或单一元素）
        if nums[mid] == nums[mid + 1]:
            lo = mid + 2                    # 这一对完整：单一元素在右边
        else:
            hi = mid                        # 这一对已被打破：单一元素在 mid 或更左
    return nums[lo]
```

运行：`[1,1,2,3,3,4,4,8,8]` → `2`，`[3,3,7,7,10,11,11]` → `10`，`[5]` → `5`，`[1,2,2]` → `1`，`[1,1,2]` → `2`；`10^5 + 1` 个元素的数组 → `100000`。

**复杂度。** 时间 `O(log n)`；空间 `O(1)`。

**拓展优化。**
- 用 `mid ^ 1` 省掉奇偶对齐：它一步给出「同一对里的另一个下标」，伙伴相等说明还没到单一元素，之后用普通的 `lo = mid + 1`、`hi = mid`。

```python
def single_non_duplicate(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] == nums[mid ^ 1]:             # 左边成对完整（单一元素之前，伙伴一定相等）
            lo = mid + 1
        else:
            hi = mid                               # 伙伴不等：单一元素在 mid 或更左
    return nums[lo]
```

- 在「第几对」上二分：谓词 `nums[2i] != nums[2i+1]` 先假后真，用 `bisect_left` 的 `key` 参数，不用手写循环。

```python
from bisect import bisect_left

def single_non_duplicate(nums: list[int]) -> int:
    pairs = len(nums) // 2                         # 完整的对数；单一元素在最后一个位置时没有「不等」的对
    i = bisect_left(range(pairs), True, key=lambda i: nums[2 * i] != nums[2 * i + 1])
    return nums[2 * i]                             # 第一个被打破的对的左端；全部完整则落在最后一个元素
```

**易错点。**
- 不对齐 `mid`：用 `nums[mid] == nums[mid+1]` 直接判断，奇数 `mid` 的含义变了（它是一对的右端）。`[3,3,7,7,10,11,11]` 得到 `7`，正确是 `10`。
- 更新 `lo = mid + 1`：破坏 `lo` 的偶数性，之后的 `mid` 对齐会错位；一对有两个元素，要跳 `2`。
- 用 `while lo <= hi` 再 `hi = mid`：当 `lo == hi` 时 `hi` 不再变小，死循环；这里循环条件是 `lo < hi`。

**追问。**
- 每个数出现三次、一个数出现一次（LC 137）：异或不再抵消，改成按位统计 `1` 的个数模 `3`。
- 数组无序（LC 136）：不能二分，全体异或就是最优的 `O(n)`、`O(1)`。

**同模式。** LC 34 排序数组中查找元素的第一个和最后一个位置、LC 162 寻找峰值、LC 153 寻找旋转排序数组中的最小值、LC 136 只出现一次的数字。
