---
id: lct-learn-data-structures-1-1
node: data-structures.1.1
type: qa
step: 1
---
## Q
**常用数据结构 › 前缀和 › 基础**｜学习卡

套路是什么？

## A
**一句话。** 前缀和 `s[0] = 0`、`s[i]` 是前 `i` 个数之和，任意 `a[left:right]` 的和是 `s[right] - s[left]`；最大子数组和就是枚举右端点、减去左边最小的前缀和。

下图：`s[k]` 落在第 `k` 个数的左边界上，一段子数组的和等于它两端边界的前缀和之差。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<text x="14" y="58" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums</text>
<rect x="70" y="40" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="110" y="40" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="130.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="150" y="40" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="190" y="40" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="210.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="230" y="40" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="90.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="130.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="170.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="210.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="250.0" y="84" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="14" y="128" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s</text>
<rect x="55" y="110" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="70" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<line x1="70" y1="92" x2="70" y2="108" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="70" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s[0]</text>
<rect x="95" y="110" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<line x1="110" y1="92" x2="110" y2="108" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="110" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s[1]</text>
<rect x="135" y="110" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="150" y1="92" x2="150" y2="108" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="150" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s[2]</text>
<rect x="175" y="110" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<line x1="190" y1="92" x2="190" y2="108" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="190" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s[3]</text>
<rect x="215" y="110" width="30" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="230" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">9</text>
<line x1="230" y1="92" x2="230" y2="108" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="230" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s[4]</text>
<rect x="255" y="110" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">14</text>
<line x1="270" y1="92" x2="270" y2="108" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="270" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s[5]</text>
<line x1="110" y1="32" x2="110" y2="26" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="230" y1="32" x2="230" y2="26" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="110" y1="32" x2="230" y2="32" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">nums[1:4] = 1+4+1 = 6</text>
<text x="170" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">s[4] - s[1] = 9 - 3 = 6</text>
</svg>

```python
s = list(accumulate(nums, initial=0))    # s[0] = 0，长度 n + 1


def range_sum(left, right):          # LC 303，闭区间
    return s[right + 1] - s[left]


def max_sub_array(nums):             # LC 53
    ans = float('-inf')
    min_pre = pre = 0                # min_pre 含空前缀 s[0]
    for x in nums:
        pre += x
        ans = max(ans, pre - min_pre)    # 先结算：子数组非空
        min_pre = min(min_pre, pre)      # 再更新最小前缀和
    return ans
```

**要点。**
- 为什么对？：`a[left] + … + a[right-1] = s[right] - s[left]`，两个前缀都含前 `left` 个数，相减抵消；右端点固定时，最好的左端点就是最小的 `s[l]`。
- 为什么先结算后更新？：保证参与相减的最小值严格在 `r` 左边，子数组非空。
- LC 1749 怎么改？：取绝对值后顺序无所谓，答案是 `max(s) - min(s)`。
- LC 1310、LC 2559 怎么改？：1310 用前缀异或 `xs[r+1] ^ xs[l]`；2559 先把每个字符串转成 `0 / 1` 再前缀和。

**易错点。**
- 先更新再结算：`[-3,-1]` 应得 `-1`，会得到 `0`（相当于允许空子数组）。
- 用「最大前缀和 − 最小前缀和」求 LC 53：`[1,-2]` 应得 `1`，会得到 `2`，因为最大前缀在最小前缀左边。
- 前缀和少了 `s[0] = 0`，或闭区间写成 `s[right] - s[left]`：`[-2,0,3,-5,2,-1]` 的 `sumRange(0,2)` 应得 `1`。

**对应题目。** LC 53 最大子数组和
