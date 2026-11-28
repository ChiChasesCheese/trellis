---
id: lct-learn-sliding-window-2-3-3
node: sliding-window.2.3.3
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 不定长滑动窗口 › 求子数组个数 › 恰好型滑动窗口**｜学习卡

套路是什么？

## A
**一句话。** “恰好 `k`”不单调，“至少 `k`”单调：恰好 `k` = 至少 `k` 的个数 − 至少 `k+1` 的个数，各用一次“越长越合法”的计数滑窗。

下图：「恰好 k」不单调，但「至少」单调；恰好 = 两个「至少」的集合之差。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 135">
<text x="10" y="34" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">至少 k</text>
<rect x="80" y="20" width="240" height="22" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="10" y="70" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">至少 k+1</text>
<rect x="160" y="56" width="160" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="10" y="106" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">恰好 k</text>
<rect x="80" y="92" width="80" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<line x1="160" y1="16" x2="160" y2="118" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="120" y="107" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">差</text>
<text x="240" y="107" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= at_least(k) − at_least(k+1)</text>
<text x="170" y="132" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两者都单调，各跑一次「越长越合法」计数滑窗</text>
</svg>

```python
def at_least(nums, k):              # 和 >= k 的子数组数，nums >= 0
    ans = left = s = 0
    for right, x in enumerate(nums):
        s += x
        while left <= right and s >= k:     # 缩到刚好不合法
            s -= nums[left]
            left += 1
        ans += left                 # 左端点 0..left-1 都合法
    return ans


def exactly(nums, k):               # 和恰好为 k
    return at_least(nums, k) - at_least(nums, k + 1)
```

**要点。**
- 为什么对？：整数下 `{≥ k}` 是 `{= k}` 与 `{≥ k+1}` 的不相交并，且 `{≥ k+1}` 是 `{≥ k}` 的子集，所以相减恰是恰好 `k`；两个“至少”各自 `O(n)`。
- LC 1248 统计「优美子数组」怎么改？：先把每个数换成 `x & 1`，“恰好 `k` 个奇数”就是 0/1 数组的“和恰好 `k`”，调用 `exactly`。
- LC 992 K 个不同整数的子数组怎么改？：统计量换成种类数（用字典，个数归零要删键），`while len(cnt) >= k` 缩，同样 `f(k) - f(k+1)`。

**易错点。**
- `k = 0` 没有 `left <= right` 保护：`nums = [0,0,0,0,0]`、`k = 0` 应得 `15`，窗口缩空后 `s >= 0` 仍成立，`left` 会越界。
- 1248 忘了取奇偶：`nums = [2,2,2,1,2,2,1,2,2,2]`、`k = 2` 应得 `16`，直接对原值求和得到 `8`。
- 992 只用一个窗口“种类数大于 `k` 就缩，累加 `right-left+1`”：数的是至多 `k` 种，`nums = [1,2,1,2,3]`、`k = 2` 应得 `7`，会得到 `12`。

**对应题目。** LC 1248 统计「优美子数组」、LC 992 K 个不同整数的子数组
