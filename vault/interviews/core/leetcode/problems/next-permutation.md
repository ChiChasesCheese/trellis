---
slug: next-permutation
---
## Q
**LC 31 下一个排列**｜Medium

把数组原地改成字典序的下一个排列；已是最大则变成最小（升序）。

## A
**一句话。** 从右找第一个比右邻小的 `i`，与右侧刚好比它大的最小数交换，再把 `i` 右边整段反转成升序。

**图解。** 找拐点 `i`，与后缀里刚好比它大的 `j` 交换，再把后缀反转成升序。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 160">
<rect x="60" y="32" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="74.0" y="48.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="88" y="32" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="102.0" y="48.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="116" y="32" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="48.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="144" y="32" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="48.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="172" y="32" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="186.0" y="48.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="200" y="32" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="214.0" y="48.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="228" y="32" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="242.0" y="48.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="256" y="32" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="270.0" y="48.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="284" y="32" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="298.0" y="48.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="52" y="48" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">原</text>
<polyline points="158.0,20 158.0,32" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="158.0,32.0 155.0,26.0 161.0,26.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="158.0" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<polyline points="242.0,20 242.0,32" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="242.0,32.0 239.0,26.0 245.0,26.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="242.0" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">j</text>
<text x="312" y="14" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">降序后缀</text>
<rect x="60" y="72" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="74.0" y="88.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="88" y="72" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="102.0" y="88.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="116" y="72" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="88.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="144" y="72" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="88.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="172" y="72" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="186.0" y="88.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="200" y="72" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="214.0" y="88.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="228" y="72" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="242.0" y="88.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="256" y="72" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="270.0" y="88.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="284" y="72" width="28" height="24" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="298.0" y="88.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="52" y="88" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">交换</text>
<rect x="60" y="112" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="74.0" y="128.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="88" y="112" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="102.0" y="128.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="116" y="112" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="128.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="144" y="112" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="158.0" y="128.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="172" y="112" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="186.0" y="128.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="200" y="112" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="214.0" y="128.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="228" y="112" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="242.0" y="128.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="256" y="112" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="270.0" y="128.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="284" y="112" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="298.0" y="128.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="52" y="128" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">反转</text>
<text x="60" y="154" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i：从右第一个比右邻小　j：后缀里刚好比它大</text>
</svg>

```python
def next_permutation(nums):
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1                     # 找拐点，右边是降序
    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1                 # 降序后缀里第一个更大的
        nums[i], nums[j] = nums[j], nums[i]
    l, r = i + 1, n - 1            # i = -1 时整体反转
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1
        r -= 1
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 比较漏掉等号：有重复元素时，找拐点要用 `>=`，找交换对象要用 `<=`。
- 交换后忘了反转后缀：`[2,3,1,3,3]` 只交换得 `[2,3,3,3,1]`，应为 `[2,3,3,1,3]`。

**追问。**
- 为什么后缀反转后就是最小？：交换后后缀仍是降序，反转即升序，是该前缀下的最小排列。
- 整体降序要特判吗？：不用，`i = -1` 时反转整个数组正好是最小排列。

**同模式。** LC 46 全排列、LC 60 排列序列、LC 556 下一个更大元素 III
