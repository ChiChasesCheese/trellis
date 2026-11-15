---
slug: construct-the-minimum-bitwise-array-ii
---
## Q
**LC 3315 构造最小位运算数组 II**｜Medium

质数数组 `nums`，对每个 `nums[i]` 求最小的 `ans[i]` 使 `ans[i] OR (ans[i]+1) == nums[i]`，不存在则为 `-1`。

## A
**一句话。** `v OR (v+1)` 等于把 `v` 最低的 0 变成 1；反过来，`nums[i]` 末尾连续的 1 里去掉最高那个就是最小的 `v`，偶数（只有 2）无解。

**图解。** `11 = 1011`，末尾连续的 1 是 `11`，去掉其中最高的一位得 `1001 = 9`，`9 | 10 = 1011`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 194">
<text x="76" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x = 11</text>
<rect x="84" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="99.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="114" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="129.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="144" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="159.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="174" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="189.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="76" y="64.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">v = 9</text>
<rect x="84" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="99.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="114" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="129.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="144" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="159.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="174" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="189.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="76" y="98.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">v+1 = 10</text>
<rect x="84" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="99.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="114" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="129.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="144" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="159.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="174" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="189.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="76" y="132.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">v | v+1</text>
<rect x="84" y="114" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="99.0" y="132.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="114" y="114" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="129.0" y="132.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="144" y="114" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="159.0" y="132.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="174" y="114" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="189.0" y="132.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="16" y="158" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">深色：末尾连续 1 中最高的一位，去掉它</text>
<text x="16" y="176" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">v + 1 把它补回来，OR 还原成 x</text>
</svg>

```python
def min_bitwise_array(nums):
    ans = []
    for x in nums:
        if x % 2 == 0:          # v | (v+1) 一定是奇数
            ans.append(-1)
            continue
        low0 = ~x & (x + 1)     # x 最低的 0 位
        ans.append(x ^ (low0 >> 1))   # 去掉它下面那个 1
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`（不计输出）。

**易错点。**
- 去掉最低位的 1（`x - 1`）：结果正确但不是最小，`7` 会得到 `6`（`6|7=7`），最小应是 `3`。
- 忘了偶数无解：`v` 与 `v+1` 必有一个奇数，OR 的最低位一定是 1。

**追问。**
- 为什么去掉最高的那个最小？：`v` 必须形如「`x` 末尾连续 1 里去掉某一个」，去掉越高的位，数越小。
- 质数这个条件有什么用？：只是保证除了 2 都是奇数，结论对任意奇数都成立。

**同模式。** LC 191 位1的个数、LC 3314 构造最小位运算数组 I、LC 201 数字范围按位与
