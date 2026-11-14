---
slug: 3sum
---
## Q
**LC 15 三数之和**｜Medium

给整数数组 `nums`，返回所有和为 `0` 且不重复的三元组。

## A
**一句话。** 先排序，固定第一个数，在其右边用对撞双指针找两数之和，三处跳过重复值。

**图解。** 固定 `i`，`lo`、`hi` 从两端向中间收，按和的正负决定动哪边。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 150">
<rect x="40" y="46" width="36" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="64.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-4</text>
<rect x="76" y="46" width="36" height="28" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="94.0" y="64.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="112" y="46" width="36" height="28" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="64.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="148" y="46" width="36" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="166.0" y="64.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="184" y="46" width="36" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="202.0" y="64.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="220" y="46" width="36" height="28" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="238.0" y="64.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<polyline points="94.0,30 94.0,46" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="94.0,46.0 91.0,40.0 97.0,40.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="94.0" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<polyline points="130.0,30 130.0,46" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="130.0,46.0 127.0,40.0 133.0,40.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="130.0" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">lo</text>
<polyline points="238.0,30 238.0,46" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="238.0,46.0 235.0,40.0 241.0,40.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="238.0" y="26" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">hi</text>
<polyline points="122.0,88 148.0,88" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="148.0,88.0 142.0,91.0 142.0,85.0" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="246.0,88 220.0,88" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="220.0,88.0 226.0,85.0 226.0,91.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="150" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">−1 + (−1) + 2 = 0 → 记录</text>
<text x="150" y="136" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s &lt; 0：lo 右移　s &gt; 0：hi 左移</text>
</svg>

```python
def three_sum(nums):
    nums = sorted(nums)
    n = len(nums)
    res = []
    for i in range(n - 2):
        if nums[i] > 0:              # 最小数都 > 0，不可能为 0
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue                 # 第一个数去重
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                res.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1          # 第二个数去重
    return res
```

**复杂度。** 时间 `O(n^2)`，空间 `O(1)`。

**易错点。**
- 和后一个比较去重（`nums[i] == nums[i+1]`）：`[-1,0,1,2,-1,-4]` 丢掉 `[-1,-1,2]`。
- 找到解后只移一个指针：会死循环或重复输出。

**追问。**
- 最接近目标的三数之和？：同样排序加双指针，记录差的绝对值最小的和（LC 16）。
- 四数之和、`k` 数之和？：递归固定前 `k-2` 个数，最后两个用双指针，`O(n^(k-1))`。

**同模式。** LC 1 两数之和、LC 16 最接近的三数之和、LC 18 四数之和、LC 167 两数之和 II
