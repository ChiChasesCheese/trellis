---
slug: find-the-middle-index-in-array
---
## Q
**LC 1991 找到数组的中间位置**｜Easy

整数数组 `nums`。找出最左边的中间下标 `i`，使 `i` 左侧元素之和等于右侧元素之和（空侧之和为 `0`）。没有返回 `-1`。

## A
**一句话。** 先求总和，边扫边累加左侧和，右侧和 = 总和 - 左侧 - 当前，相等即为答案。

```python
def find_middle_index(nums):
    total = sum(nums)
    left = 0
    for i, x in enumerate(nums):
        if left == total - left - x:     # 右侧和
            return i
        left += x
    return -1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 右侧和忘了减 `x`：会把当前元素也算进右侧。
- 先更新 `left` 再比较：左侧不应包含当前元素。

**追问。**
- 有负数还成立吗？：成立，前缀和与总和的运算不依赖符号。

**同模式。** LC 724 寻找数组的中心下标、LC 1 两数之和、LC 560 和为 K 的子数组、LC 238 除了自身以外数组的乘积
