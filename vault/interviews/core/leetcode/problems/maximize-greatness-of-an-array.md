---
slug: maximize-greatness-of-an-array
---
## Q
**LC 2592 最大化数组的伟大值**｜Medium

把 `nums` 重排成 `perm`，伟大值是满足 `perm[i] > nums[i]` 的下标数。求最大伟大值。

## A
**一句话。** 田忌赛马：排序后用双指针，`i` 指向最小的还没被超过的数，从小到大拿每个数 `x` 去试，`x > nums[i]` 就配上一对。

**图解。** 排序后，下面一排每个深色数恰好超过上面一排对应的浅色数，共 4 对。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 126">
<text x="54" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">被超过</text>
<rect x="62" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="92" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="107.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="122" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="137.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="152" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="167.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="182" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="197.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="212" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="227.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="242" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="54" y="64.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">出手</text>
<rect x="62" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="92" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="107.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="122" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="137.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="152" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="167.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="182" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="197.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="212" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="227.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="242" y="46" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="16" y="90" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 > 1，3 > 1，3 > 1，5 > 2：配上 4 对</text>
<text x="16" y="108" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没配上的 1、1、1 随便放</text>
</svg>

```python
def maximize_greatness(nums):
    nums.sort()
    i = 0                      # 最小的还没被超过的数
    for x in nums:
        if x > nums[i]:
            i += 1             # 用 x 超过 nums[i]
    return i
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`（不计排序）。

**易错点。**
- 用 `>=`：要求严格大于，相同的数不能配对。
- 以为要真的构造 `perm`：只求个数，没配上的数随便放。

**追问。**
- 为什么用最小的够大的数去超过最小的数？：交换论证，大数留着能超过更大的数，不会更差。
- 另一种算法？：答案是 `n - 最大出现次数`，因为相同的数只能被更大的数超过。

**同模式。** LC 167 两数之和 II - 输入有序数组、LC 455 分发饼干、LC 870 优势洗牌
