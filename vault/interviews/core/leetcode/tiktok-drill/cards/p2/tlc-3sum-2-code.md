---
id: tlc-3sum-2-code
node: p2.3sum
type: qa
step: 2
---
## Q
**LC 15 三数之和**｜写出 Python 实现

`nums` 长度 `3 <= n <= 3000`，元素范围 `-10^5` 到 `10^5`。返回所有和为 `0` 的不重复三元组（值的组合不重复），顺序不限，要求 `O(n^2)`。

## A
**思路。** 排序。外层枚举第一个数，同值只处理第一次；内层用左右指针在其右侧找两数之和为 `-nums[i]`。找到解后两个指针各移一步，并让左指针跳过相同的值，避免重复三元组。

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    n = len(nums)
    result: list[list[int]] = []
    for i in range(n - 2):
        if nums[i] > 0:                            # 排好序后最小的数都 > 0，三数之和不可能为 0
            break
        if i > 0 and nums[i] == nums[i - 1]:       # 同一个"第一个数"只处理一次，去重
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = nums[i] + nums[lo] + nums[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:   # 跳过重复的第二个数；第三个数随之唯一确定
                    lo += 1
    return result
```

运行：`[-1,0,1,2,-1,-4]` → `[[-1,-1,2],[-1,0,1]]`；`[0,1,1]` → `[]`；`[0,0,0]` → `[[0,0,0]]`；`[0,0,0,0]` → `[[0,0,0]]`；`[-2,0,1,1,2]` → `[[-2,0,2],[-2,1,1]]`；随机 `n = 3000` 的数组约 `0.1` 秒。

**复杂度。** 时间 `O(n^2)`；空间 `O(1)`（不计排序副本和输出）。

**写法要点。** `sorted(nums)` 返回副本，不改调用方的列表（`nums.sort()` 会原地改）；`range(n - 2)` 保证后面至少还有两个数；`lo += 1; hi -= 1` 之后只跳过左边的重复，因为 `lo` 变了，满足条件的 `hi` 也唯一确定；`nums[i] > 0` 的提前 `break` 是剪枝，不影响正确性；结果里放新建的列表 `[nums[i], nums[lo], nums[hi]]`。
