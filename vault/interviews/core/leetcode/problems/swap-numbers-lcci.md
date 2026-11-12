---
slug: swap-numbers-lcci
---
## Q
**面试题 16.01 交换数字**｜Medium

不使用临时变量，交换 `numbers = [a, b]` 中 `a` 与 `b` 的值并返回。

## A
**一句话。** 异或交换：`a ^= b; b ^= a; a ^= b`，靠 `x ^ x = 0` 与 `x ^ 0 = x`。

```python
def swap_numbers(numbers):
    numbers[0] ^= numbers[1]    # a ^ b
    numbers[1] ^= numbers[0]    # b ^ (a ^ b) = a
    numbers[0] ^= numbers[1]    # (a ^ b) ^ a = b
    return numbers
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 两个「位置」是同一个：`x[i] ^= x[j]` 在 `i == j` 时直接清零，交换下标 0 与 0 得 `[0,9]`。值相等但位置不同没事。
- 用乘除交换：遇到 `0` 除零，不能用。
- 加减交换在 C/C++ 有符号溢出是未定义行为，应该用异或。

**追问。**
- 工程里为什么不用？：临时变量在寄存器里更快，三步相互依赖不能并行，可读性差。
- Python 的 `a, b = b, a` 有什么坑？：目标带下标时，`nums[i], nums[nums[i]-1] = ...` 赋第二个目标时 `nums[i]` 已变，先存 `j = nums[i] - 1`。

**同模式。** LC 136 只出现一次的数字、LC 268 丢失的数字、LC 371 两整数之和、面试题 16.07 最大数值
