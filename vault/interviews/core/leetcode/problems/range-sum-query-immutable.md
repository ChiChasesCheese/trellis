---
slug: range-sum-query-immutable
---
## Q
**LC 303 区域和检索 - 数组不可变**｜Easy

数组不变，多次询问 `sumRange(left, right)`（闭区间和）。

## A
**一句话。** 前缀和：`s[i]` 是前 `i` 个数之和，区间和 `= s[right+1] - s[left]`，每次查询 `O(1)`。

```python
class NumArray:
    def __init__(self, nums):
        self.s = [0]            # s[i] = nums[0..i-1] 之和
        for x in nums:
            self.s.append(self.s[-1] + x)

    def sumRange(self, left, right):
        return self.s[right + 1] - self.s[left]
```

**复杂度。** 构造 `O(n)`，查询 `O(1)`，空间 `O(n)`。

**易错点。**
- 不留开头的 `0`：`left = 0` 要特判，`s[left - 1]` 会读到最后一个。
- 写成 `s[right] - s[left]`：少了 `nums[right]`。

**追问。**
- 数组会被修改（LC 307）？：树状数组或线段树，修改和查询都 `O(log n)`。
- 二维（LC 304）？：`s[i+1][j+1] = s[i][j+1] + s[i+1][j] - s[i][j] + a[i][j]`，查询用容斥。

**同模式。** LC 560 和为 K 的子数组、LC 304 二维区域和检索 - 矩阵不可变、LC 1480 一维数组的动态和
