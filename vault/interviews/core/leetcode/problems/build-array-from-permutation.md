---
slug: build-array-from-permutation
---
## Q
**LC 1920 基于排列构建数组**｜Easy

给 `0` 到 `n-1` 的一个排列 `nums`。返回数组 `ans`，`ans[i] = nums[nums[i]]`。进阶：不用额外空间。

## A
**一句话。** 每个位置同时存"旧值 + n × 新值"：取模还原旧值、整除得到新值，一次原地完成。

```python
def build_array(nums):
    n = len(nums)
    for i in range(n):
        # nums[i] 可能已被改，用 % n 还原旧值
        nums[i] += n * (nums[nums[i]] % n)
    for i in range(n):
        nums[i] //= n
    return nums
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 直接 `nums[i] = nums[nums[i]]`：后面的位置会读到已被覆盖的值。
- 读 `nums[nums[i]]` 时不取模：该位置可能已编码成两个数之和。

**追问。**
- 不要求原地时？：`[nums[x] for x in nums]` 一行即可。

**同模式。** LC 1470 重新排列数组、LC 1480 一维数组的动态和、LC 189 轮转数组、LC 283 移动零
