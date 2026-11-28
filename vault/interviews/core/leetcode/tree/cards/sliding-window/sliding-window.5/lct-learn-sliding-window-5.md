---
id: lct-learn-sliding-window-5
node: sliding-window.5
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 三指针**｜学习卡

套路是什么？

## A
**一句话。** 固定右端点，合法的左端点是一个区间，区间两端由几个“最近一次出现的位置”决定；一趟扫描维护这三个位置，每个右端点直接用公式算个数。

下图：LC 2444，固定右端点 `i`，合法左端点在 `(bad, min(last_min, last_max)]` 里。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="30" y="46" width="46" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="53.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<rect x="76" y="46" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="99.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="122" y="46" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="145.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="168" y="46" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="191.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="214" y="46" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="237.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="260" y="46" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="283.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="53.0" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="99.0" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="145.0" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="191.0" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="237.0" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="283.0" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<line x1="53.0" y1="30" x2="53.0" y2="44" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="53.0,44.0 50.0,37.7 56.0,37.7" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="53.0" y="26" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">bad</text>
<line x1="145.0" y1="30" x2="145.0" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="145.0,44.0 142.0,37.7 148.0,37.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="145.0" y="26" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">last_min</text>
<line x1="237.0" y1="30" x2="237.0" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="237.0,44.0 234.0,37.7 240.0,37.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="237.0" y="26" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">last_max</text>
<line x1="283.0" y1="30" x2="283.0" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="283.0,44.0 280.0,37.7 286.0,37.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="283.0" y="26" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<line x1="76.0" y1="96" x2="76.0" y2="102" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="168.0" y1="96" x2="168.0" y2="102" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="76.0" y1="96" x2="168.0" y2="96" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="122.0" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">合法左端点 1、2</text>
<text x="170" y="138" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">minK = 1，maxK = 5</text>
<text x="170" y="158" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">个数 = min(last_min, last_max) - bad = 2 - 0</text>
</svg>

```python
def count_subarrays(nums, min_k, max_k):    # LC 2444
    ans = 0
    bad = last_min = last_max = -1  # 三个“最近位置”，-1 表示没出现
    for i, x in enumerate(nums):
        if not min_k <= x <= max_k:     # 越界元素：左端点必须在它右边
            bad = i
        if x == min_k:
            last_min = i
        if x == max_k:              # min_k == max_k 时两个都要更新
            last_max = i
        # 左端点 l 满足 bad < l <= min(last_min, last_max)
        ans += max(0, min(last_min, last_max) - bad)
    return ans
```

**要点。**
- 为什么对？：以 `i` 结尾的子数组要同时包含 `min_k`、`max_k` 且不含越界元素，左端点必须不超过两者最近出现位置的较小者，且大于最近的越界位置。
- 为什么要 `max(0, …)`？：区间可能为空（还没凑齐或被越界元素隔开），此时贡献是 `0`。

**易错点。**
- 忘了 `max(0, …)`：`nums = [1,3,5,2,7,5]`、`minK = 1`、`maxK = 5` 应得 `2`，不兜底会得到负数。
- `minK == maxK` 时用 `elif`：`nums = [1,1,1,1]`、`minK = maxK = 1` 应得 `10`，`elif` 会得到 `0`。
- 初值用 `0` 而不是 `-1`：`nums = [1,5]`、`minK = 1`、`maxK = 5` 应得 `1`，会得到 `0`。

**对应题目。** LC 2444 统计定界子数组的数目
