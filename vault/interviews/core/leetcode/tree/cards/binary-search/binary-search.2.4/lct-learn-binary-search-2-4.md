---
id: lct-learn-binary-search-2-4
node: binary-search.2.4
type: qa
step: 1
---
## Q
**二分算法 › 二分答案 › 最小化最大值**｜学习卡

套路是什么？

## A
**一句话。** 最小化最大值就是二分盖子 `cap`：问“所有段的和都压在 `cap` 以下，最少要分几段”，段数随 `cap` 增大不增，`段数 <= k` 单调。

下图：LC 410（k = 2），给定盖子 `cap` 时贪心地数最少段数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="30" y="46" width="56" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="58.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="86" y="46" width="56" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="114.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="142" y="46" width="56" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="198" y="46" width="56" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="226.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="254" y="46" width="56" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="282.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<line x1="30" y1="40" x2="30" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="198" y1="40" x2="198" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="30" y1="40" x2="198" y2="40" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="114.0" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">段和 14 ≤ 18</text>
<line x1="198" y1="40" x2="198" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="310" y1="40" x2="310" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="198" y1="40" x2="310" y2="40" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">段和 18 ≤ 18</text>
<text x="170" y="98" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">cap = 18：放不下就另起一段 → 2 段 ≤ k</text>
<text x="170" y="118" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">cap 越大段数越少：check 单调，二分最小的 cap</text>
<text x="170" y="136" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">范围 (max - 1, sum]</text>
</svg>

```python
def split_array(nums, k):           # LC 410
    def check(cap):                 # 每段和 <= cap，最少分几段 <= k
        parts, cur = 1, 0
        for x in nums:
            if cur + x > cap:       # 放不下，另起一段
                parts += 1
                cur = 0
            cur += x
        return parts <= k
    left = max(nums) - 1            # 盖子小于最大元素，一定压不住
    right = sum(nums)               # 一整段一定压得住
    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            right = mid             # 压得住，试更低的盖子
        else:
            left = mid
    return right
```

**要点。**
- 为什么对？：盖子越大，贪心需要的段数越少，所以 `check` 单调；贪心尽量把一段装满，得到的是给定盖子下的最少段数。
- 为什么是 `parts <= k` 而不是 `== k`？：段数更少时可以继续拆分，最大值不会变大，`<=` 才保证单调。
- 同类题怎么改？：只换 `check`：商店分配、袋子里的球、最小体力路径、打家劫舍 IV，都是“盖子 `mid`，判断所有最大值是否都 `<= mid`”。

**易错点。**
- `left` 取 `0` 而 `check` 不拦超大元素：`nums = [1,10]`、`k = 2` 应得 `10`，`cap = 5` 时会被误判可行，返回 `1`。
- `check` 写成 `parts == k`：`nums = [1,1,1,1]`、`k = 3` 应得 `2`，单调性被破坏，会得到 `4`。
- `parts` 起点写 `0`：`nums = [5,5]`、`k = 1` 应得 `10`，会在 `cap = 5` 时误判可行，返回 `5`。

**对应题目。** LC 410 分割数组的最大值
