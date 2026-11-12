---
slug: product-of-array-except-self
---
## Q
**LC 238 除了自身以外数组的乘积**｜Medium

返回数组 `answer`，`answer[i]` 是 `nums` 中除 `nums[i]` 外所有元素的乘积。不许用除法，`O(n)` 时间，额外空间 `O(1)`（输出不计）。

## A
**一句话。** 先把前缀积写进答案，再从右往左乘上滚动的后缀积。

```python
def product_except_self(nums):
    n = len(nums)
    ans = [1] * n
    for i in range(1, n):            # 先写前缀积
        ans[i] = ans[i - 1] * nums[i - 1]
    suf = 1
    for i in range(n - 1, -1, -1):   # 再乘上滚动的后缀积
        ans[i] *= suf
        suf *= nums[i]
    return ans
```

**复杂度。** 时间 `O(n)`，额外空间 `O(1)`。

**易错点。**
- 用「总乘积 ÷ `nums[i]`」：含 `0` 时 `ZeroDivisionError`，`[-1,1,0,-3,3]` 直接崩溃。
- 前缀积把自己乘进去（`ans[i-1] * nums[i]`）：`[1,2,3,4]` 得 `[24,24,24,24]`，应为 `[24,12,8,6]`。
- 第二趟先 `suf *= nums[i]` 再 `ans[i] *= suf`：后缀把自己乘进去，同样出错，先用后并入。

**追问。**
- 为什么不能用除法？：有 `0` 就不可行，一个 `0` 只有它自己的位置非零，两个以上全为 `0`。
- 只开前缀数组和后缀数组也行吗？：可以，空间 `O(n)`，上面是把后缀压成变量 `suf`。

**同模式。** LC 42 接雨水、LC 724 寻找数组的中心下标、LC 152 乘积最大子数组
