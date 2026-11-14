---
slug: product-of-array-except-self
---
## Q
**LC 238 除了自身以外数组的乘积**｜Medium

返回数组 `answer`，`answer[i]` 是 `nums` 中除 `nums[i]` 外所有元素的乘积。不许用除法，`O(n)` 时间，额外空间 `O(1)`（输出不计）。

## A
**一句话。** 先把前缀积写进答案，再从右往左乘上滚动的后缀积。

**图解。** `answer[i]` = 左边所有数的积 × 右边所有数的积。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 290 180">
<rect x="100" y="14" width="40" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="31.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="140" y="14" width="40" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="31.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="180" y="14" width="40" height="26" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="31.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="220" y="14" width="40" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="240.0" y="31.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="92" y="31" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums</text>
<rect x="100" y="50" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="67.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="140" y="50" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="67.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="180" y="50" width="40" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="67.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="220" y="50" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240.0" y="67.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="92" y="67" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">前缀积</text>
<rect x="100" y="86" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="103.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">24</text>
<rect x="140" y="86" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="103.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<rect x="180" y="86" width="40" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="103.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="220" y="86" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240.0" y="103.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="92" y="103" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">后缀积</text>
<rect x="100" y="122" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="139.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">24</text>
<rect x="140" y="122" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="139.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<rect x="180" y="122" width="40" height="26" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="200.0" y="139.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="220" y="122" width="40" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240.0" y="139.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="92" y="139" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">answer</text>
<text x="100" y="170" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i = 2：左边 1·2 = 2，右边 4，2 × 4 = 8</text>
</svg>

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
