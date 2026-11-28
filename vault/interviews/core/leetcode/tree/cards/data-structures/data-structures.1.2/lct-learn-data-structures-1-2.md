---
id: lct-learn-data-structures-1-2
node: data-structures.1.2
type: qa
step: 1
---
## Q
**常用数据结构 › 前缀和 › 前缀和与哈希表**｜学习卡

套路是什么？

## A
**一句话。** 子数组和是两个前缀和之差，所以「和为 `k`」就是找一对前缀和差为 `k`：枚举右端点，用哈希表记左边每种前缀（或其余数）的次数或最早下标，先查后存。

下图：枚举右端点的循环；哈希表里只放左边出现过的前缀和。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 270">
<rect x="97.2" y="7.5" width="145.6" height="25" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cnt[0] = 1（空前缀）</text>
<rect x="115.2" y="55.5" width="109.6" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读 x：pre += x</text>
<polygon points="110.2,118.0 119.2,105.5 220.8,105.5 229.8,118.0 220.8,130.5 119.2,130.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="122.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">pre - k 在表里？</text>
<rect x="187.9" y="152.0" width="148.2" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="262" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ans += cnt[pre - k]</text>
<text x="262" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最长：用最早下标</text>
<rect x="24.8" y="216.0" width="250.5" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="232.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">记录 pre</text>
<text x="150" y="247.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">个数：cnt[pre] += 1；最长：只记第一次</text>
<path d="M 170.0 32.5 L 170.0 55.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,55.5 167.0,49.2 173.0,49.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 80.5 L 170.0 105.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,105.5 167.0,99.2 173.0,99.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 229.8 118.0 L 262.0 118.0 L 262.0 152.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262.0,152.0 259.0,145.7 265.0,145.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="272" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 170.0 130.5 L 110.0 140.0 L 110.0 210.0 L 150.0 216.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,216.0 143.3,218.0 144.2,212.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="98" y="175" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 262.0 192.0 L 262.0 210.0 L 190.0 210.0 L 150.0 216.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,216.0 155.8,212.1 156.7,218.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 24.8 236.0 L 12.0 236.0 L 12.0 68.0 L 115.2 68.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="115.2,68.0 108.9,71.0 108.9,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="30" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下一个</text>
</svg>

```python
def subarray_sum(nums, k):           # LC 560：个数
    cnt = defaultdict(int)
    cnt[0] = 1                       # 空前缀，从头开始的子数组才数得到
    pre = ans = 0
    for x in nums:
        pre += x                     # 当前前缀和 s[r]
        ans += cnt[pre - k]          # 左边 s[r]-k 的个数
        cnt[pre] += 1                # 先查后存
    return ans

def longest_with_sum(nums, k):       # LC 325：最长
    first = {0: -1}                  # 前缀和 -> 最早下标
    pre = ans = 0
    for j, x in enumerate(nums):
        pre += x
        if pre - k in first:
            ans = max(ans, j - first[pre - k])
        if pre not in first:         # 只记第一次，区间才最长
            first[pre] = j
    return ans
```

**要点。**
- 为什么对？：子数组 `(l, r]` 和为 `k` 当且仅当 `s[l] = s[r] - k`；每个子数组由唯一的 `(l, r)` 确定，表里只有已遍历的前缀，天然 `l < r`。
- LC 974、LC 523、LC 2845 怎么改？：键换成余数 `pre % k`（整除 = 余数相等）；523 存最早下标并要求 `j - first >= 2`；2845 先把 `x % modulo == k` 转 `0 / 1`，再查 `(pre - k) % modulo`。
- LC 525、LC 930 怎么改？：525 把 `0` 当 `-1` 求和为 `0` 的最长段；930 元素非负，计数模板原样用（`k = goal`）。
- LC 1074、LC 437 怎么改？：1074 枚举上下两行，按列压成一维再调 `subarray_sum`；437 在树上 DFS，进入时 `cnt[pre] += 1`，离开时减回。

**易错点。**
- 漏掉空前缀：`[3]`、`k = 3` 应得 `1`，没有 `cnt[0] = 1` 得 `0`。
- 先存后查：`[0]`、`k = 0` 应得 `1`，先存会得 `2`。
- 最长问题用最近下标覆盖：`[0,1,1,0]`（LC 525）应得 `4`，覆盖后只得 `2`。

**对应题目。** LC 930 和相同的二元子数组、LC 525 连续数组、LC 523 连续的子数组和、LC 2845 统计趣味子数组的数目、LC 325 和等于 k 的最长子数组长度、LC 1074 元素和为目标值的子矩阵数量、LC 437 路径总和 III、LC 560 和为 K 的子数组、LC 974 和可被 K 整除的子数组
