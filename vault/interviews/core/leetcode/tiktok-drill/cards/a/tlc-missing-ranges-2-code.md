---
id: tlc-missing-ranges-2-code
node: a.missing-ranges
type: qa
step: 2
---
## Q
**LC 163 缺失的区间**｜写出 Python 实现

升序、互不相同的整数数组 `nums`（`0 <= nums.length <= 100`，元素都在 `[lower, upper]` 内，`-10^9 <= lower <= upper <= 10^9`），返回区间 `[lower, upper]` 内所有缺失数的最小有序区间列表，每个区间写成 `[a, b]`。要求 `O(n)`，不遍历值域。

## A
**思路。** 在 `nums` 前补哨兵 `lower - 1`，后补 `upper + 1`。顺序扫描，`prev` 记上一个已知数；当前数 `x` 与 `prev` 之差 `>= 2`，说明中间有缺口 `[prev + 1, x - 1]`。

```python
from itertools import chain


def find_missing_ranges(nums: list[int], lower: int, upper: int) -> list[list[int]]:
    ans: list[list[int]] = []
    prev = lower - 1                           # 哨兵：把 lower 之前的一格当作"已出现"
    for x in chain(nums, (upper + 1,)):        # 末尾追加 upper + 1，统一处理最后一段
        if x - prev >= 2:                      # 相邻已知数之间隔着至少一个数
            ans.append([prev + 1, x - 1])
        prev = x
    return ans
```

运行：`[0,1,3,50,75]`, `0`, `99` → `[[2, 2], [4, 49], [51, 74], [76, 99]]`；`[-1]`, `-1`, `-1` → `[]`；`[]`, `1`, `1` → `[[1, 1]]`；`[]`, `-5`, `5` → `[[-5, 5]]`。

**复杂度。** 时间 `O(n)`：每个元素处理一次；额外空间 `O(1)`，输出不计。

**写法要点。** `itertools.chain(nums, (upper + 1,))` 把哨兵「接」在迭代器末尾，不复制列表、不修改调用者的 `nums`；`prev = lower - 1` 让第一个元素和后面的元素走同一条判断，循环里没有 `if i == 0` 之类的特判。
