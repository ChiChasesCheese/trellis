---
id: tlc-tops-product-of-array-except-self-0-whole
node: arrays-hashing.product-of-array-except-self
type: qa
---
## Q
**LC 238 除了自身以外数组的乘积**｜Medium · 全公司热度第 65 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150、LeetCode 75

给你一个整数数组 `nums`，返回数组 `answer`，其中 `answer[i]` 等于 `nums` 中除 `nums[i]` 之外其余各元素的乘积。题目数据保证数组 `nums` 中任意元素的全部前缀和后缀的乘积都在 32 位整数范围内。请**不要使用除法**，且在 `O(n)` 时间内完成。`2 <= nums.length <= 10^5`，`-30 <= nums[i] <= 30`。例：`nums = [1,2,3,4]` → `[24,12,8,6]`；`nums = [-1,1,0,-3,3]` → `[0,0,9,0,0]`。进阶：在 `O(1)` 额外空间内完成（输出数组不计入额外空间）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 前缀积 × 后缀积（prefix / suffix product）：除自身以外 = 左边所有数之积 × 右边所有数之积。

**一句话。** `answer[i] = nums[0..i-1] 的乘积 × nums[i+1..n-1] 的乘积`；一趟从左往右把前缀积写进答案数组，再一趟从右往左乘上后缀积。

**识别。** 禁止除法（也避免了含 `0` 的麻烦），「去掉自己」改写成「左边之积 × 右边之积」；这和「去掉自己的和 = 总和 - 自己」不同，乘法没有可用的逆运算。`n <= 10^5`，`O(n)`。

**推导。** 对每个 `i` 重新乘其余所有数，`O(n^2)`。除以总乘积遇到 `0` 就失效，题目也禁止。把问题拆成两半：前缀积数组 `pre[i]` 和后缀积数组 `suf[i]` 各一趟算出，答案 = `pre[i] * suf[i]`。

**简单解法。** 前缀积、后缀积各开一个数组，空间 `O(n)`。

```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    pre = [1] * n                                  # pre[i]：nums[:i] 的乘积
    suf = [1] * n                                  # suf[i]：nums[i+1:] 的乘积
    for i in range(1, n):
        pre[i] = pre[i - 1] * nums[i - 1]
    for i in range(n - 2, -1, -1):
        suf[i] = suf[i + 1] * nums[i + 1]
    return [p * s for p, s in zip(pre, suf)]
```

最优解（额外空间 `O(1)`，输出数组不计）：前缀积直接写进答案数组，后缀积用一个变量滚动。

```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    ans = [1] * n
    for i in range(1, n):
        ans[i] = ans[i - 1] * nums[i - 1]          # ans[i] 先存「左边所有数之积」
    suffix = 1                                     # 当前位置右边所有数之积
    for i in range(n - 1, -1, -1):
        ans[i] *= suffix                           # 乘上右边之积
        suffix *= nums[i]                          # 再把自己并入，供左边的位置使用
    return ans
```

运行：`[1,2,3,4]` → `[24, 12, 8, 6]`；`[-1,1,0,-3,3]` → `[0, 0, 9, 0, 0]`；`[2,3]` → `[3, 2]`；`[0,0]` → `[0, 0]`。

**复杂度。** 时间 `O(n)`；空间 `O(1)` 额外（不计输出数组）。

**易错点。**
- 用「总乘积 ÷ `nums[i]`」：含 `0` 时 `ZeroDivisionError`；`[-1,1,0,-3,3]` 直接崩溃。题目禁止除法正是为了这个。
- 前缀积包含了自己（`ans[i] = ans[i-1] * nums[i]`）：`[1,2,3,4]` 得到 `[24, 24, 24, 24]`，正确是 `[24, 12, 8, 6]`。左边之积不含 `nums[i]`。
- 第二趟先 `suffix *= nums[i]` 再 `ans[i] *= suffix`：右边之积把自己也乘进去，同样得到 `[24, 24, 24, 24]`。先用，后并入。

**同模式。** LC 42 接雨水（前后缀最大值）、LC 724 寻找数组的中心下标、LC 152 乘积最大子数组、LC 560 和为 K 的子数组。
