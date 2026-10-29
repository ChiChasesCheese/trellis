---
id: tlc-product-of-array-except-self-2-code
node: a.product-of-array-except-self
type: qa
step: 2
---
## Q
**LC 238 除了自身以外数组的乘积**｜写出 Python 实现

整数数组 `nums`（`2 <= nums.length <= 10^5`，`-30 <= nums[i] <= 30`），返回数组 `answer`，`answer[i]` 为除 `nums[i]` 外其余元素之积；不能用除法，`O(n)` 时间，额外空间 `O(1)`（输出不计）。

## A
**思路。** 第一趟正向扫描，`ans[i]` 存 `nums[0..i-1]` 的乘积（`left`）；第二趟反向扫描，把 `nums[i+1..]` 的乘积（`right`）乘进 `ans[i]`。两趟都是「先使用、再更新」。

```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    ans = [1] * n
    left = 1
    for i in range(n):                 # 第一趟：ans[i] 存 nums[0..i-1] 的乘积
        ans[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):     # 第二趟：再乘上 nums[i+1..] 的乘积
        ans[i] *= right
        right *= nums[i]
    return ans
```

运行：`[1,2,3,4]` → `[24, 12, 8, 6]`；`[-1,1,0,-3,3]` → `[0, 0, 9, 0, 0]`；`[0,0]` → `[0, 0]`；`[2,3]` → `[3, 2]`。长度 `10^5` 的全 `1` 数组在毫秒级完成。

**复杂度。** 时间 `O(n)`：两趟各 `n` 步；额外空间 `O(1)`：只有 `left`、`right`，输出数组按题意不计。

**写法要点。** `[1] * n` 建立初值，两趟都「先读后写」，不需要 `L`、`R` 两个辅助数组；`range(n - 1, -1, -1)` 写出倒序下标，不用 `reversed(range(n))` 也可以，但要保留下标；Python 整数不溢出，其他语言要按题目保证的 32 位范围放心乘。
