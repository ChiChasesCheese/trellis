---
id: lct-learn-data-structures-2-1-2
node: data-structures.2.1.2
type: qa
step: 1
---
## Q
**常用数据结构 › 差分 › 一维差分 › 进阶**｜学习卡

套路是什么？

## A
**一句话。** 差分让「区间 `[l, r]` 加 `v`」只改 `d[l] += v`、`d[r+1] -= v`，最后做一次前缀和还原；进阶题把每个对象的贡献拆成几个分界点上的变化量（坐标大时只记事件点），统一累加后取峰值或最值。

下图：两次区间加各改两端，`d` 做一次前缀和就还原出每点的覆盖数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="77.0" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="111.0" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="145.0" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="179.0" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="213.0" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="247.0" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="281.0" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<text x="315.0" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<text x="8" y="40" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[2,5]+1</text>
<text x="8" y="52" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[4,6]+1</text>
<text x="8" y="80" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<rect x="60" y="62" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="94" y="62" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="111.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="128" y="62" width="34" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="145.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<rect x="162" y="62" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="179.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="196" y="62" width="34" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="213.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+1</text>
<rect x="230" y="62" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="247.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="264" y="62" width="34" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="281.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="298" y="62" width="34" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="315.0" y="80.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<text x="8" y="150" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">前缀和</text>
<rect x="60" y="132" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="94" y="132" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="111.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="128" y="132" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="162" y="132" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="179.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="196" y="132" width="34" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="213.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="230" y="132" width="34" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="247.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="264" y="132" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="281.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="298" y="132" width="34" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="315.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<line x1="77.0" y1="92" x2="77.0" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="111.0" y1="92" x2="111.0" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="145.0" y1="92" x2="145.0" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="179.0" y1="92" x2="179.0" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="213.0" y1="92" x2="213.0" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="247.0" y1="92" x2="247.0" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="281.0" y1="92" x2="281.0" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="315.0" y1="92" x2="315.0" y2="130" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="196" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">accumulate 还原</text>
<text x="213" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">峰值 2：两个区间重叠处</text>
</svg>

```python
def min_rooms(intervals):            # LC 253：峰值重叠数
    diff = defaultdict(int)
    for start, end in intervals:
        diff[start] += 1             # [start, end) 内占一间
        diff[end] -= 1
    return max(accumulate(diff[t] for t in sorted(diff)))

def brightest(lights):               # LC 2021：坐标大，只看事件点
    diff = defaultdict(int)
    for pos, rng in lights:
        diff[pos - rng] += 1         # 照亮闭区间
        diff[pos + rng + 1] -= 1     # 右端的下一格才熄灭
    best = cur = ans = 0
    for x in sorted(diff):
        cur += diff[x]
        if cur > best:               # 严格大于：并列取坐标小的
            best, ans = cur, x
    return ans
```

**要点。**
- 为什么对？：差分与前缀和互为逆运算，区间加在 `d` 上只动两个位置；`m` 次操作 `O(m)`，再一次前缀和 `O(n)`。亮度只在端点处变化，所以只排序端点，`O(n log n)`。
- 为什么相接的会议不重叠？：区间是半开的 `[start, end)`，字典把同一时刻的 `-1` 与 `+1` 合并成净变化，峰值不会重复计。
- LC 1674 怎么改？：下标换成目标和 `s`，每对 `(a, b)` 的代价是分段常数：`s = a + b` 为 `0`，`s` 在 `[lo+1, hi+limit]` 为 `1`，否则 `2`；在这几个分界点记变化量，前缀和后在 `[2, 2*limit]` 取最小。

**易错点。**
- 右端点差分写在 `r` 而不是 `r + 1`：灯 `[1,0]` 与 `[0,1]`（LC 2021）在 `1` 处都亮，应得 `1`，错写会提前熄灭。
- 相接会议被算重叠：`[[1,5],[5,9]]` 应得 `1`，同坐标分开处理 `+1` 在前会得 `2`。
- LC 1674 漏掉 `s == a + b` 的特殊点：`[1,2,1,2]`、`limit = 2` 应得 `0`，漏掉只得 `2`。

**对应题目。** LC 1674 使数组互补的最少操作次数、LC 2021 街上最亮的位置、LC 253 会议室 II
