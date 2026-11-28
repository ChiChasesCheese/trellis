---
id: lct-learn-sliding-window-2-1-1
node: sliding-window.2.1.1
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 不定长滑动窗口 › 越短越合法/求最长/最大 › 基础**｜学习卡

套路是什么？

## A
**一句话。** 求「越短越合法」的最长连续子数组：枚举右端点，窗口一旦不合法就右移左端点直到合法，此时就是以 `right` 结尾的最长合法窗口，`left` 只前进不回头，`O(n)`。

下图：LC 3，新元素让窗口不合法时右移 `left` 直到合法，此时就是以 `right` 结尾的最长窗口。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="50" width="37" height="28" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="38.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a</text>
<rect x="57" y="50" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="75.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="94" y="50" width="37" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="112.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="131" y="50" width="37" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="149.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a</text>
<rect x="168" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="186.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="205" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="223.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="242" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="279" y="50" width="37" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297.5" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<line x1="149.5" y1="34" x2="149.5" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="149.5,48.0 146.5,41.7 152.5,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="149.5" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">right</text>
<line x1="38.5" y1="34" x2="38.5" y2="48" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="38.5,48.0 35.5,41.7 41.5,41.7" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="38.5" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧 left</text>
<line x1="75.5" y1="96" x2="75.5" y2="82" stroke-width="1.2" stroke="currentColor"/>
<polygon points="75.5,82.0 78.5,88.3 72.5,88.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="75.5" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新 left</text>
<text x="250" y="100" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">新进的 a 重复了：</text>
<text x="250" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">缩 left 直到合法</text>
<text x="170" y="145" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">合法后：ans = max(ans, right - left + 1)</text>
</svg>

```python
def longest(a):                      # LC 3：无重复字符
    ans = left = 0
    cnt = defaultdict(int)           # 窗口内各元素个数
    for right, x in enumerate(a):
        cnt[x] += 1                  # 入
        while cnt[x] > 1:            # 不合法：只有新进的 x 可能违规
            cnt[a[left]] -= 1        # 出
            left += 1
        ans = max(ans, right - left + 1)   # 窗口合法，更新答案
    return ans
```

**要点。**
- 为什么对？：越短越合法，所以使 `[l, r]` 合法的最小左端点 `L(r)` 随 `r` 不减，左端点不用回头；`while` 恰停在 `L(r)`；任何最优子数组以某个 `right` 结尾，长度不超过 `right - L(right) + 1`。
- 怎么换题？：只改统计什么和何时不合法：LC 904 用字典，`len(cnt) > 2` 就缩，个数减到 `0` 要删键；LC 1004 只数 `0` 的个数，`zeros > k` 就缩；LC 1493 窗口至多一个 `0`，答案是最大窗口长度减一。
- 怎么判断适用？：问自己「合法窗口去掉一端还合法吗」；求最短且条件是下限（和至少）则是越长越合法，要在缩的循环里更新答案。

**易错点。**
- 更新答案放进 `while` 里：`"bb"` 右端点 `1` 时窗口还不合法，会记下长度 `2`，应得 `1`。
- LC 904 减到 `0` 不删键：`[1,2,3,2,2]` 应得 `4`，种类数一直数成 `3`。
- LC 1493 忘了减一：`[1,1,1]` 必须删一个，应得 `2`；`[0,0,0]` 应得 `0`。

**对应题目。** LC 904 水果成篮、LC 1493 删掉一个元素以后全为 1 的最长子数组、LC 3 无重复字符的最长子串、LC 1004 最大连续1的个数 III
