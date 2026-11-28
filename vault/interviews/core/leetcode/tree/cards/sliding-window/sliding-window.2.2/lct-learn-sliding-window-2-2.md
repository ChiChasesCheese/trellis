---
id: lct-learn-sliding-window-2-2
node: sliding-window.2.2
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 不定长滑动窗口 › 越长越合法/求最短/最小**｜学习卡

套路是什么？

## A
**一句话。** 求最短且“越长越合法”的窗口：枚举右端点，窗口一合法就一边记录长度一边缩左端点，直到再缩就不合法。

下图：LC 76，窗口一合法就一边记录一边缩，缩到不合法再扩右端。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 225">
<rect x="23.8" y="7.5" width="252.4" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">right 右移：入 s[right]，可能补上缺口</text>
<polygon points="76.2,72.0 85.2,59.5 214.8,59.5 223.8,72.0 214.8,84.5 85.2,84.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已覆盖？missing == 0</text>
<rect x="49.4" y="113.5" width="201.3" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="150" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">记录：best = min(best, 长度)</text>
<rect x="70.8" y="163.5" width="158.3" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="180.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">出 s[left]，left += 1</text>
<path d="M 150.0 32.5 L 150.0 59.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,59.5 147.0,53.2 153.0,53.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 150.0 84.5 L 150.0 113.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,113.5 147.0,107.2 153.0,107.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="158.0" y="103.0" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 150.0 138.5 L 150.0 163.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,163.5 147.0,157.2 153.0,157.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 229.2 176.0 L 300.0 176.0 L 300.0 72.0 L 223.8 72.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="223.8,72.0 230.1,69.0 230.1,75.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 76.2 72.0 L 12.0 72.0 L 12.0 20.0 L 23.8 20.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="23.8,20.0 17.5,23.0 17.5,17.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="22" y="48" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<text x="150" y="216" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先记录再缩：缩到再缩就不合法为止</text>
</svg>

```python
def min_window(s, t):               # LC 76
    need = {}                       # need[c] > 0：窗口还缺 c
    for c in t:
        need[c] = need.get(c, 0) + 1
    missing = len(t)                # 还缺的字符总数（计重）
    best, left = (inf, 0), 0
    for right, c in enumerate(s):
        if need.get(c, 0) > 0:      # 补上一个缺口
            missing -= 1
        need[c] = need.get(c, 0) - 1
        while missing == 0:         # 已覆盖：先记录再缩
            best = min(best, (right - left + 1, left))
            out = s[left]
            need[out] += 1
            if need[out] > 0:       # 出去后又出现缺口
                missing += 1
            left += 1
    n, i = best
    return "" if n == inf else s[i:i + n]
```

**要点。**
- 为什么对？：越长越合法，所以固定右端点时合法的左端点是一个前缀，其右端 `R(r)` 随 `r` 不减；`left` 只前进，每次缩前窗口合法，因此先记录就覆盖了 `R(r)` 处的最短窗口。
- LC 209 长度最小的子数组怎么改？：统计量是窗口和 `s`，合法是 `s >= target`，`while` 里先 `ans = min(ans, right - left + 1)` 再 `s -= a[left]`；只对全正数成立。
- 和“越短越合法”有什么区别？：那边缩到合法才记录，这边合法时才缩，记录写在 `while` 里面。

**易错点。**
- 记录写在 `while` 之外：LC 209 `target = 7`、`nums = [2,3,1,2,4,3]` 应得 `2`，放在外面记的是已缩坏的窗口，会得到 `1`。
- 76 不判多余字符：`s = "aab"`、`t = "ab"` 应得 `"ab"`，见到 `t` 里的字符就 `missing -= 1` 会在 `"aa"` 时误判覆盖。
- 无解忘记换值：LC 209 `target = 100`、`nums = [1,2,3]` 应得 `0`，不处理会返回 `inf`。

**对应题目。** LC 209 长度最小的子数组、LC 76 最小覆盖子串
