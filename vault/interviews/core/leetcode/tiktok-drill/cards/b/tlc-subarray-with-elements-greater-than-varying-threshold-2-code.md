---
id: tlc-subarray-with-elements-greater-than-varying-threshold-2-code
node: b.subarray-with-elements-greater-than-varying-threshold
type: qa
step: 2
---
## Q
**LC 2334 元素值大于变化阈值的子数组**｜写出 Python 实现

`nums` 长度 `1 <= n <= 10^5`，`1 <= nums[i], threshold <= 10^9`。返回任意一个长度 `k`，使得存在一个长度为 `k` 的连续子数组，其中每个元素都大于 `threshold / k`；不存在则返回 `-1`。要求 `O(n)`。

## A
**思路。** 条件等价于「子数组最小值 `h` 满足 `h * k > threshold`」。用递增的下标栈，每弹出一个元素就得到以它为最小值的最宽区间 `[left + 1, i - 1]`，宽度 `k = i - left - 1`，检查 `h * k > threshold`。数组末尾补一个哨兵 `0` 来清空栈。

```python
from itertools import chain


def valid_subarray_size(nums: list[int], threshold: int) -> int:
    stack: list[int] = []                          # 下标栈，对应的值严格递增
    for i, x in enumerate(chain(nums, (0,))):      # 末尾补哨兵 0（nums[i] >= 1），把栈里剩下的全弹出
        while stack and nums[stack[-1]] >= x:
            h = nums[stack.pop()]                  # h 是一段区间的最小值
            left = stack[-1] if stack else -1      # 左边第一个比 h 小的位置
            k = i - left - 1                       # h 做最小值时能撑起的最大宽度
            if h * k > threshold:                  # h > threshold / k，乘过去避免浮点
                return k
        stack.append(i)
    return -1
```

运行：`[1,3,4,3,1], 6` → `3`；`[6,5,6,5,8], 7` → `3`（题面允许 `1` 到 `5` 任意满足的长度）；`[1], 1` → `-1`；`[1], 5` → `-1`；`10^5` 个随机数、`threshold = 10^9` 瞬间完成；`1` 到 `10^5` 递增、`threshold = 10^9` → `11271`。

**复杂度。** 时间 `O(n)`：每个下标最多入栈、出栈各一次；空间 `O(n)`。

**写法要点。** `itertools.chain(nums, (0,))` 给迭代器末尾接一个哨兵，不用拷贝出 `nums + [0]`；`enumerate` 同时拿下标和值；`>=` 弹栈使栈内严格递增，相等元素也能得到正确的最大宽度；`h * k > threshold` 用整数乘法代替 `threshold / k`，没有浮点误差；Python 整数不会溢出，用 C++ 要用 `long long`（`10^9 * 10^5` 超过 32 位）。
