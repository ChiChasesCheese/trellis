---
slug: split-array-largest-sum
---
## Q
**LC 410 分割数组的最大值**｜Hard

把非负数组 `nums` 切成 `k` 个非空连续段，使各段和的最大值最小，求这个最小值。

## A
**一句话。** 二分答案（每段和的上限 `cap`），贪心数最少要几段，段数 `<= k` 就够用。

**图解。** 二分的是上限 `cap`：`cap` 越大段数越少，满足「段数 ≤ k」的最小 `cap` 就是答案。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 175">
<rect x="30.0" y="38" width="94.54545454545455" height="16" rx="0" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<rect x="124.54545454545455" y="38" width="165.45454545454544" height="16" rx="0" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<line x1="30" y1="54" x2="290" y2="54" stroke-width="1" stroke="currentColor"/>
<line x1="30.0" y1="36" x2="30.0" y2="56" stroke-width="1" stroke="currentColor"/>
<text x="30.0" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">10</text>
<line x1="124.54545454545455" y1="36" x2="124.54545454545455" y2="56" stroke-width="1.6" style="stroke:var(--accent,#3b6fd4)"/>
<text x="124.54545454545455" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">18</text>
<line x1="290.0" y1="36" x2="290.0" y2="56" stroke-width="1" stroke="currentColor"/>
<text x="290.0" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">32</text>
<text x="30.0" y="32" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">max = 10</text>
<text x="290.0" y="32" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">sum = 32</text>
<text x="77.27272727272728" y="50" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">段数 &gt; k</text>
<text x="207.27272727272728" y="50" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">段数 ≤ k</text>
<rect x="110" y="96" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124.0" y="112.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="138" y="96" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="152.0" y="112.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="166" y="96" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="180.0" y="112.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="194" y="96" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="208.0" y="112.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="222" y="96" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="236.0" y="112.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<line x1="194" y1="92" x2="194" y2="124" stroke-width="3" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="222" y1="92" x2="222" y2="124" stroke-width="3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="102" y="112" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cap = 17</text>
<text x="258" y="112" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3 段 ✗</text>
<rect x="110" y="132" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124.0" y="148.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="138" y="132" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="152.0" y="148.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="166" y="132" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="180.0" y="148.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="194" y="132" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="208.0" y="148.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="222" y="132" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="236.0" y="148.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<line x1="194" y1="128" x2="194" y2="160" stroke-width="3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="102" y="148" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cap = 18</text>
<text x="258" y="148" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 段 ✓</text>
</svg>

```python
def split_array(nums, k):
    def groups(cap):           # 每段和 <= cap 时最少几段
        cnt, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                cnt += 1
                cur = 0
            cur += x
        return cnt

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if groups(mid) <= k:   # 段数少可继续拆，最大值不变大
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(n log sum)`，空间 `O(1)`。

**易错点。**
- 下界取 `0` 或 `1`：比 `cap` 大的元素被当成自己一段，`[1,4,4]`, `k=3` 得 `1`，应为 `4`。
- 判定写成 `== k`：`[1,4,4]`, `k=3` 得 `9`，应为 `4`，条件是 `<= k`。
- 区间写成 `lo <= hi` 却返回 `hi`：示例一得 `17`，应为 `18`。

**追问。**
- 有负数呢？：贪心判定和单调性都失效，只能用划分 DP，`O(kn²)`。
- 反过来最大化最小值呢？：同一框架，判定改成「能否凑出 `k` 份且每份至少 `cap`」，方向相反。

**同模式。** LC 1011 在 D 天内送达包裹的能力、LC 875 爱吃香蕉的珂珂、LC 1482 制作 m 束花所需的最少天数、LC 774 最小化去加油站的最大距离
