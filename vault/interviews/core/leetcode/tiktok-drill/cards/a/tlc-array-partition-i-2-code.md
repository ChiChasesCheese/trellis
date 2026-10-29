---
id: tlc-array-partition-i-2-code
node: a.array-partition-i
type: qa
step: 2
---
## Q
**LC 561 数组拆分 I**｜写出 Python 实现

长度 `2n`（`1 <= n <= 10^4`，元素在 `[-10^4, 10^4]`）的数组分成 `n` 对，求每对较小值之和的最大值。

## A
**思路。** 排序后把相邻两个数配成一对，每对的较小者就是排序后偶数下标的元素，求和即可。

```python
def array_pair_sum(nums: list[int]) -> int:
    nums = sorted(nums)                 # 不改调用方的列表
    return sum(nums[::2])               # 相邻两两配对，每对的较小者落在偶数下标
```

运行：`[1,4,3,2]` → `4`，`[6,2,6,5,1,2]` → `9`，`[-1,-2]` → `-2`，`[-10000,10000,3,3]` → `-9997`。

**复杂度。** 时间 `O(n log n)`，排序主导；空间 `O(n)`，`sorted` 生成新列表。

**写法要点。** `sorted(nums)` 返回新列表，不修改调用方传进来的数组（需要省内存时才用 `nums.sort()` 原地排序）；步长切片 `[::2]` 一步取出所有偶数下标，等价于 `sum(nums[i] for i in range(0, len(nums), 2))` 但更短更快；负数不影响结论，不需要特判。
