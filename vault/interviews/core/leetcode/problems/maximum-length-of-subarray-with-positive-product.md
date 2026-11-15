---
slug: maximum-length-of-subarray-with-positive-product
---
## Q
**LC 1567 乘积为正数的最长子数组长度**｜Medium

整数数组 `nums`，求乘积为正数的最长连续子数组长度。

## A
**一句话。** 只关心符号：`pos`、`neg` 分别是以当前数结尾、乘积为正、为负的最长长度；遇正数两者各加一（`neg` 为 0 时仍为 0），遇负数两者互换再加一，遇 0 清零。

**图解。** `[0,1,-2,-3,-4]`：到 `-3` 时 `neg` 是 2（`[1,-2]`），乘上负数变成 `pos = 3`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 160">
<text x="48" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums</text>
<rect x="56" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="86" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-2</text>
<rect x="146" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="161.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-3</text>
<rect x="176" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="191.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-4</text>
<text x="48" y="64.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">pos</text>
<rect x="56" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="86" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="146" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="161.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="176" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="191.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="48" y="98.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">neg</text>
<rect x="56" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="86" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="116" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="146" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="161.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="176" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="191.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="16" y="124" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">遇负数：pos、neg 互换再加一</text>
<text x="16" y="142" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">neg 2（[1,-2]）乘 -3 变成 pos 3</text>
</svg>

```python
def get_max_len(nums):
    pos = neg = ans = 0        # 以当前数结尾，积为正 / 负
    for x in nums:
        if x > 0:
            pos, neg = pos + 1, (neg + 1 if neg else 0)
        elif x < 0:
            pos, neg = (neg + 1 if neg else 0), pos + 1
        else:
            pos = neg = 0      # 0 把子数组切断
        ans = max(ans, pos)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- `neg` 为 0 时也加一：没有以前一个数结尾的负积子数组，正数后面仍然没有。
- 先更新 `pos` 再用新 `pos` 算 `neg`：两者要同时更新。

**追问。**
- 不用 DP？：按 0 切段，每段负数个数为偶数则整段可取，否则去掉第一个负数之前或最后一个负数之后的部分取较长者。
- 求最大乘积？：同样记以当前数结尾的最大积和最小积，就是 LC 152。

**同模式。** LC 152 乘积最大子数组、LC 53 最大子数组和
