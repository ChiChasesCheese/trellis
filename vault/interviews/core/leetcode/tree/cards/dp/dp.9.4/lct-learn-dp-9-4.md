---
id: lct-learn-dp-9-4
node: dp.9.4
type: qa
step: 1
---
## Q
**动态规划 › 状态压缩 DP（状压 DP） › 子集状压 DP**｜学习卡

套路是什么？

## A
**一句话。** 子集状压 DP：`f[S]` 表示集合 `S` 的最优值，通过枚举 `S` 的子集 `sub`（`sub = (sub - 1) & S`）拆成 `sub` 与 `S ^ sub` 两部分转移，总共 `O(3^n)`。

下图：把集合 `S` 拆成子集 `sub` 和剩下的 `S ^ sub` 两部分转移。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="90" y="20" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="101" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="112" y="20" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="123" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="134" y="20" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="156" y="20" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="167" y="36" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<text x="20" y="37" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">S</text>
<rect x="90" y="60" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="112" y="60" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="123" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="134" y="60" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="156" y="60" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="167" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<text x="20" y="77" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">sub</text>
<rect x="90" y="100" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="101" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="112" y="100" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="123" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="134" y="100" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="156" y="100" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="167" y="116" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<text x="20" y="117" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">S ^ sub</text>
<text x="200" y="36" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">sub = (sub - 1) &amp; S</text>
<text x="200" y="52" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">枚举 S 的全部子集</text>
<text x="200" y="80" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">sub 的余额和为 0：</text>
<text x="200" y="96" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[S] = f[S ^ sub] + 1</text>
<text x="170" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所有 S 的子集合计 3^n 个</text>
</svg>

```python
def min_transfers(transactions):     # LC 465 最优账单平衡
    bal = defaultdict(int)
    for x, y, m in transactions:
        bal[x] -= m
        bal[y] += m
    a = [v for v in bal.values() if v]   # 只留没结清的人
    n = len(a)
    s = [0] * (1 << n)               # s[S]：集合 S 的余额和
    for S in range(1, 1 << n):
        s[S] = s[S & (S - 1)] + a[(S & -S).bit_length() - 1]
    f = [0] * (1 << n)               # f[S]：S 里最多几个零和组
    for S in range(1, 1 << n):
        sub = S
        while sub:                   # 枚举 S 的非空子集
            if s[sub] == 0:
                f[S] = max(f[S], f[S ^ sub] + 1)
            sub = (sub - 1) & S
    return n - f[-1]
```

**要点。**
- 为什么对？：一个大小为 `m` 的零和组内部转 `m - 1` 次就能结清，所以总转账数是 `n - 组数`；组越多越好，问题变成把所有人拆成最多的零和组。
- 为什么是 `3^n`？：每个元素要么不在 `S`，要么在 `S` 且不在 `sub`，要么在 `sub`，三种选择，总计 `3^n`。
- 更快的写法怎么改？：`f[S] = max(f[S ^ (1 << i)] for i in S) + (s[S] == 0)`，只拿掉一个元素，`O(n * 2^n)`。

**易错点。**
- 没丢掉余额为 `0` 的人：他们本就结清，留着会让 `n` 变大、答案偏大。
- 枚举子集写成 `range(S)`：会枚举到不是 `S` 子集的数，要用 `(sub - 1) & S`。
- 把空子集算进去：`sub = 0` 的 `s` 也为 `0`，会无限转移自己，`while sub` 要排除。

**对应题目。** LC 465 最优账单平衡
