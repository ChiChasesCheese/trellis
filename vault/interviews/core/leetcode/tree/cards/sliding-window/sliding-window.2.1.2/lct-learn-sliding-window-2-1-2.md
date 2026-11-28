---
id: lct-learn-sliding-window-2-1-2
node: sliding-window.2.1.2
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 不定长滑动窗口 › 越短越合法/求最长/最大 › 进阶（选做）**｜学习卡

套路是什么？

## A
**一句话。** 求最长且“越短越合法”的窗口：枚举右端点，不合法就缩左端点，合法时记最长；进阶题只是把“合法”换成派生量（种类数、窗口和），或先转化成单调。

下图：LC 340，`b` 进来后有 3 种字符，缩到只剩 2 种；判断合法用的是派生量 `len(cnt)`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="70" y="40" width="40" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="90.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">e</text>
<rect x="110" y="40" width="40" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="130.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">c</text>
<rect x="150" y="40" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<rect x="190" y="40" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="210.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">b</text>
<rect x="230" y="40" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="210.0" y1="24" x2="210.0" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210.0,38.0 207.0,31.7 213.0,31.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="210.0" y="20" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">right</text>
<line x1="170.0" y1="86" x2="170.0" y2="72" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,72.0 173.0,78.3 167.0,78.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170.0" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">left</text>
<text x="20" y="58" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k = 2</text>
<text x="14" y="128" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cnt</text>
<rect x="50" y="112" width="66" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="83" y="129" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">e: 1</text>
<rect x="120" y="112" width="66" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="153" y="129" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">c: 0 删键</text>
<rect x="190" y="112" width="66" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="223" y="129" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">b: 1</text>
<text x="270" y="129" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">len = 2</text>
<text x="170" y="158" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">合法 = 种类数 len(cnt) ≤ k；计数归零必须删键</text>
</svg>

```python
def longest_k_distinct(s, k):       # LC 340；LC 159 即 k = 2
    cnt = {}
    ans = left = 0
    for right, c in enumerate(s):
        cnt[c] = cnt.get(c, 0) + 1          # 入
        while len(cnt) > k:                 # 不合法：缩
            out = s[left]
            cnt[out] -= 1                   # 出
            if cnt[out] == 0:
                del cnt[out]                # 归零必须删键
            left += 1
        ans = max(ans, right - left + 1)
    return ans
```

**要点。**
- 为什么对？：窗口缩短时种类数不会增加，所以每个右端点的最小合法左端点不减，`left` 只前进，总共 `O(n)`。
- LC 1838 最高频元素的频数怎么改？：先排序（顺序无关，答案是排序后的一段连续窗口），派生量换成窗口和，`nums[right] * 窗口长 - 窗口和 > k` 就缩。
- LC 395 至少有 K 个重复字符怎么改？：下限约束不单调，所以枚举窗口里恰有 `t` 种字符（1 到 26）；固定 `t` 后“种类数 ≤ t”单调，种类数等于 `t` 且每种都 ≥ `k` 时更新答案。

**易错点。**
- 个数归零不删键：`s = "eceba"`、`k = 2` 应得 `3`，不删键则 `len(cnt)` 永远偏大，窗口被缩空。
- 1838 忘了排序：`nums = [13,1,8,4]`、`k = 5` 应得 `2`，不排序会得到 `4`。
- 395 直接套“不合法就缩”：`s = "aaabbb"`、`k = 3` 应得 `6`，直接缩会把窗口缩空得到 `0`。

**对应题目。** LC 1838 最高频元素的频数、LC 395 至少有 K 个重复字符的最长子串、LC 340 至多包含 K 个不同字符的最长子串、LC 159 至多包含两个不同字符的最长子串
