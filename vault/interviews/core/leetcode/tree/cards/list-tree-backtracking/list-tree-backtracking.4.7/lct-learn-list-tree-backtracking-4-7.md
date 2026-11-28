---
id: lct-learn-list-tree-backtracking-4-7
node: list-tree-backtracking.4.7
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 回溯 › 折半搜索**｜学习卡

套路是什么？

## A
**一句话。** 折半搜索（meet in the middle）：`2^n` 太大时把元素分成两半，各枚举 `2^(n/2)` 个子集和，再用排序加二分把两半配对，复杂度从 `2^n` 降到约 `2^(n/2) * n`。

下图：两半各自枚举，再用排序 + 二分配对。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="83.3" y="7.5" width="173.4" height="25" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">nums：2n 个，2^(2n) 太大</text>
<rect x="23.6" y="55.0" width="122.8" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">左半 n 个</text>
<text x="85" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">枚举 2^n 个子集和</text>
<rect x="193.6" y="55.0" width="122.8" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">右半 n 个</text>
<text x="255" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">枚举 2^n 个，排序</text>
<rect x="101.0" y="125.0" width="137.9" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="141.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对左边每个和 a</text>
<text x="170" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">在右边二分找最配的 b</text>
<path d="M 83.3 20.0 L 85.0 20.0 L 85.0 55.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,55.0 82.0,48.7 88.0,48.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 256.7 20.0 L 255.0 20.0 L 255.0 55.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,55.0 252.0,48.7 258.0,48.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 85.0 95.0 L 85.0 145.0 L 101.0 145.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="101.0,145.0 94.7,148.0 94.7,142.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 255.0 95.0 L 255.0 145.0 L 239.0 145.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="239.0,145.0 245.3,142.0 245.3,148.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="184" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2^(2n) → 约 2^n · n</text>
</svg>

```python
def minimum_difference(nums):        # 分成各 n 个的两组，差最小
    n = len(nums) // 2
    total = sum(nums)

    def sums(arr):                   # [c]：选 c 个的所有和
        by = [[0]] + [[] for _ in arr]
        for x in arr:
            for c in range(len(arr) - 1, -1, -1):  # 倒序
                by[c + 1] += [s + x for s in by[c]]
        return by

    L, R = sums(nums[:n]), sums(nums[n:])
    best = inf
    for c in range(n + 1):           # 左选 c 个，右必须选 n - c 个
        rs = sorted(R[n - c])
        for a in L[c]:
            i = bisect_right(rs, total // 2 - a)
            for b in rs[max(i - 1, 0):i + 1]:  # 插入点两侧
                best = min(best, abs(total - 2 * (a + b)))
    return best
```

**要点。**
- 为什么对？：每个子集恰好拆成「左半的选法 + 右半的选法」，两半独立枚举再配对不漏不重；目标和 `a + b` 最接近 `total / 2`，最优的 `b` 必在 `total // 2 - a` 的插入点两侧。
- 没有「各 n 个」的限制怎么改？：不用按个数分组，两半各只排一个列表；这类问题（LC 1049）也可直接用背包 DP。
- 最接近目标值怎么改？：同样两半枚举和、排序、二分找 `target - a` 的邻居。

**易错点。**
- 忽略「各 `n` 个」：`[1,1,1,3]` 单取 `3` 得 `0`，应为 `2`，所以必须按个数分组配对。
- 初值写成 `abs(total)`：它未必是合法分法，用 `inf`。
- 暴力 `combinations(nums, n)`：`n = 15` 约 `1.55 * 10^8` 种，超时。

**对应题目。** LC 2035 将数组分成两个数组并最小化数组和的差
