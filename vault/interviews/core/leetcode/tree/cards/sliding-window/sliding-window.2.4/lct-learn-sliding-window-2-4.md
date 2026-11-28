---
id: lct-learn-sliding-window-2-4
node: sliding-window.2.4
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 不定长滑动窗口 › 其他（选做）**｜学习卡

套路是什么？

## A
**一句话。** 合法性要由派生量判断：窗口长度减最高频次 ≤ `k` 就能改成全相同；窗口只平移不缩小，最终窗口长度就是答案。

下图：LC 424（k = 1），合法就只扩 `right`；不合法时只出一个，窗口整体平移、长度不变。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 155">
<rect x="30" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="70" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="110" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="150" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="190" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="230" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="270" y="30" width="40" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<text x="50.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="90.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="130.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="170.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="210.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="250.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="290.0" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="30" y="84" width="160" height="20" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="110" y="98" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">最长合法窗口（长 4）</text>
<rect x="70" y="110" width="160" height="20" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="150" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不合法：left、right 一起右移</text>
<text x="170" y="148" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">窗口只扩不缩：长度单调不减，最后的长度就是答案</text>
</svg>

```python
def character_replacement(s, k):    # LC 424
    cnt = [0] * 26                  # 窗口内各字母个数
    left = max_cnt = 0              # max_cnt：历史最高频次，只增不减
    for right, c in enumerate(s):
        i = ord(c) - 65
        cnt[i] += 1                         # 入
        max_cnt = max(max_cnt, cnt[i])      # 只有新进的字母能刷新纪录
        if right - left + 1 - max_cnt > k:  # 要改的字符数超限
            cnt[ord(s[left]) - 65] -= 1     # 出一个，窗口整体右移
            left += 1
    return len(s) - left            # 最终窗口长度
```

**要点。**
- 为什么对？：要改的字符数 = 窗口长 − 最高频次；`max_cnt` 可以偏大，因为窗口要长到 `max_cnt + k + 1` 必须有新纪录，而新纪录出现时它就是窗口真实的最高频次，所以答案不会虚高。
- 为什么用 `if` 不用 `while`？：窗口长度只增不减，每步最多平移一格，不需要循环缩。
- 精确写法怎么写？：`while` 缩到合法，最高频次现算 `max(cnt)`，`O(26n)`，更好懂但更慢。

**易错点。**
- `max_cnt` 写成当前字母的个数：`s = "AAAB"`、`k = 1` 应得 `4`，会得到 `3`。
- `k` 大于等于长度：`s = "ABCDE"`、`k = 10` 应得 `5`。

**对应题目。** LC 424 替换后的最长重复字符
