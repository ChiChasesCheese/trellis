---
id: lct-learn-dp-7-1
node: dp.7.1
type: qa
step: 1
---
## Q
**动态规划 › 其他线性 DP › 一维 DP**｜学习卡

套路是什么？

## A
**一句话。** 一维 DP 的关键是想清楚「最后一步」：按日期枚举最后一张票覆盖多久，`f[d]` 由 `f[d - 覆盖天数]` 加票价转来。

下图：`f[d]` 按最后一张票的覆盖天数，从三个更早的位置转移。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<line x1="14" y1="80" x2="326" y2="80" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<circle cx="30" cy="80" r="5" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="30" y="100" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">f[d-30]</text>
<circle cx="170" cy="80" r="5" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="100" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">f[d-7]</text>
<circle cx="250" cy="80" r="5" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="250" y="100" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">f[d-1]</text>
<circle cx="300" cy="80" r="5" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="300" y="100" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[d]</text>
<path d="M 250 74 Q 273.5 52 297 74" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="297.0,74.0 290.9,70.6 295.8,67.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="338" y="56" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">+1 天票</text>
<path d="M 170 74 Q 233.5 30 297 74" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="297.0,74.0 290.5,71.5 294.8,67.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="212" y="36" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">+7 天票</text>
<path d="M 30 74 Q 163.5 8 297 74" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="297.0,74.0 290.1,72.6 293.7,67.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="110" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">+30 天票</text>
<text x="170" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">最后一张票覆盖到 d：从 1 / 7 / 30 天前转移</text>
<text x="170" y="138" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不出行的日子：f[d] = f[d-1]</text>
</svg>

```python
def min_cost_tickets(days, costs):
    travel = set(days)
    last = days[-1]
    f = [0] * (last + 1)         # f[d]：覆盖前 d 天出行日的最小花费
    for d in range(1, last + 1):
        if d not in travel:
            f[d] = f[d - 1]      # 不出行，不用买票
        else:                    # 最后一张票覆盖 1 / 7 / 30 天
            f[d] = min(f[d - 1] + costs[0],
                       f[max(0, d - 7)] + costs[1],
                       f[max(0, d - 30)] + costs[2])
    return f[last]
```

**要点。**
- 为什么对？：出行日 `d` 必须被某张票盖住，最后一张票覆盖 `1/7/30` 天，前面的出行日是独立子问题；非出行日继承前一天。
- LC 32 怎么改？：栈存下标，栈底放哨兵 `-1`：`(` 压下标；`)` 先弹栈，栈空则它成为新的分界线压入，否则长度是 `i - 栈顶`。
- LC 650 怎么改？：答案是 `n` 的所有质因数（含重复）之和：因子 `p` 对应一次复制加 `p-1` 次粘贴，共 `p` 步。
- LC 3389 怎么改？：枚举最终频次 `t`，对 26 个字母做「变 `0` / 变 `t`」两状态 DP，前一个字母多出的字符推给后一个字母可省一步。

**易错点。**
- 回退下标不夹到 `0`：第 `3` 天读 `f[-4]`，Python 不报错但取到数组尾部。
- 7 日票当成覆盖 `d..d+7`：实际是 7 个自然日 `d..d+6`。
- LC 32 没有哨兵 `-1`：`"()"` 得 `0`，从头就有效的段算不出长度。

**对应题目。** LC 983 最低票价、LC 32 最长有效括号、LC 650 只有两个键的键盘、LC 3389 使字符频率相等的最少操作次数
