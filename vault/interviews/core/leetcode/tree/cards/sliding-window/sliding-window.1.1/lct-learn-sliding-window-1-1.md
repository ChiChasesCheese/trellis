---
id: lct-learn-sliding-window-1-1
node: sliding-window.1.1
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 定长滑动窗口 › 基础**｜学习卡

套路是什么？

## A
**一句话。** 窗口长度固定为 `k` 时，右端点 `i` 一确定，左端点就是 `i - k + 1`，窗口每右移一格只「进一个、出一个」，统计量 `O(1)` 增量更新，一次遍历 `O(n)`。

下图：右端点 `i` 每右移一格，窗口进一个、出一个；`left = i - k + 1`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="57" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="94" y="50" width="37" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="112.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="131" y="50" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="149.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="168" y="50" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="186.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="205" y="50" width="37" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="223.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">9</text>
<rect x="242" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="279" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<line x1="131.5" y1="44" x2="131.5" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="241.5" y1="44" x2="241.5" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="131.5" y1="44" x2="241.5" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="186.5" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">窗口 [left, i]，k = 3</text>
<line x1="223.5" y1="96" x2="223.5" y2="82" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="223.5,82.0 226.5,88.3 220.5,88.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="223.5" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i：① 入</text>
<line x1="149.5" y1="96" x2="149.5" y2="82" stroke-width="1.2" stroke="currentColor"/>
<polygon points="149.5,82.0 152.5,88.3 146.5,88.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="149.5" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">left</text>
<text x="112.5" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">③ 出</text>
<line x1="112.5" y1="80" x2="112.5" y2="108" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="170" y="144" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">① cur += a[i] → ② 窗口满就更新答案 → ③ cur -= a[left]</text>
</svg>

```python
def fixed_window_max(a, k):
    ans = -inf                       # 可能全为负，不能用 0 起步
    cur = 0                          # 窗口内的统计量（这里是和）
    for i, x in enumerate(a):        # i 是窗口右端点
        cur += x                     # 1. 入
        left = i - k + 1             # 窗口 [left, i] 恰有 k 个元素
        if left < 0:                 # 窗口还没长到 k
            continue
        ans = max(ans, cur)          # 2. 更新答案
        cur -= a[left]               # 3. 出：之后窗口只有 k - 1 个
    return ans
```

**要点。**
- 为什么对？：相邻窗口共享中间 `k - 1` 个元素，只差最左出、最右进；顺序固定为入、更新答案、出，换了顺序就会拿 `k ± 1` 个元素更新答案。统计量必须可逆（和、个数、频次表），最值不行。
- LC 1423 怎么改？：只能从两端拿 `k` 张，等于留下中间长 `n - k` 的窗口，求窗口和的最小值 `m`，答案是总和减 `m`。
- LC 1151 怎么改？：窗口长度等于 `1` 的总数 `w`，统计量是窗口内 `1` 的个数，答案是 `w` 减最大值（窗口内每个 `0` 要换一个 `1` 进来）。
- LC 643 怎么改？：就是模板，和最大即平均最大，最后除一次 `k`。

**易错点。**
- 答案初值写 `0`：`[-1]`、`k = 1` 应得 `-1`。
- 出窗口下标写成 `i - k`：`[1,2,3]`、`k = 2` 应得 `3, 5`，会在 `i = 1` 时减去 `a[-1]`。
- 窗口没满就更新答案：`[5,-10]`、`k = 2` 应得 `-5`，不是 `5`。

**对应题目。** LC 1423 可获得的最大点数、LC 1151 最少交换次数来组合所有的 1、LC 643 子数组最大平均数 I
