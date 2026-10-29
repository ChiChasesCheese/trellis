---
id: tlc-reverse-subarray-to-maximize-array-value-5-alt
node: a.reverse-subarray-to-maximize-array-value
type: qa
step: 5
---
## Q
**LC 1330 翻转子数组得到最大的数组值**｜Hard · 字节高频｜另一种解法

不用线段的几何技巧，有没有更直接的做法？它的复杂度是多少，什么时候可以用？

## A
**暴力 + `O(1)` 增益。** 枚举所有 `(l, r)`，翻转后只有两端的相邻差变化，用四个元素直接算增益，不实际翻转：

```python
from itertools import pairwise


def max_value_brute(nums: list[int]) -> int:
    n = len(nums)
    total = sum(abs(a - b) for a, b in pairwise(nums))
    best = 0
    for l in range(n):
        for r in range(l + 1, n):          # 翻转 nums[l..r]，只有两端的相邻差会变
            gain = 0
            if l > 0:                      # (nums[l-1], nums[l]) 变成 (nums[l-1], nums[r])
                gain += abs(nums[l - 1] - nums[r]) - abs(nums[l - 1] - nums[l])
            if r < n - 1:                  # (nums[r], nums[r+1]) 变成 (nums[l], nums[r+1])
                gain += abs(nums[l] - nums[r + 1]) - abs(nums[r] - nums[r + 1])
            best = max(best, gain)
    return total + best
```

`[2,3,1,5,4]` → `10`，`[2,4,9,24,2,1,10]` → `68`，`[1,5,4]` → `7`。

**复杂度。** 时间 `O(n^2)`：`n = 3000` 约 0.5 秒，`n = 3 * 10^4` 按平方放大约 50 秒；空间 `O(1)`。

**怎么选。** 先写这一版：它直接把题意翻译成代码，不容易错，可以拿来在小数据上检查线性解法的公式；`n` 很小时（几千以内）也够用。`n = 3 * 10^4` 时必须用主解的 `O(n)`：把中间情形的配对最大化拆成「最大左端点」和「最小右端点」两个独立的最值。
