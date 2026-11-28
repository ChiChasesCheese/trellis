---
id: lct-learn-math-1-6
node: math.1.6
type: qa
step: 1
---
## Q
**数学算法 › 数论 › 最大公约数（GCD）**｜学习卡

套路是什么？

## A
**一句话。** 辗转相除求 GCD：`gcd(a, b) = gcd(b, a % b)`；字符串重复结构、倒水可量出的体积，都化成长度或容量的 GCD 问题。

下图：辗转相除，余数为 0 时左边就是 GCD。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<rect x="15" y="30" width="64" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="47" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">(48, 18)</text>
<rect x="97" y="30" width="64" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="129" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">(18, 12)</text>
<line x1="81" y1="45" x2="95" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="95.0,45.0 88.7,48.0 88.7,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="179" y="30" width="64" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="211" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">(12, 6)</text>
<line x1="163" y1="45" x2="177" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="177.0,45.0 170.7,48.0 170.7,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="261" y="30" width="64" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="293" y="50" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">(6, 0)</text>
<line x1="245" y1="45" x2="259" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="259.0,45.0 252.7,48.0 252.7,42.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="22" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">gcd(a, b) = gcd(b, a % b)</text>
<text x="290" y="78" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">gcd = 6</text>
<text x="170" y="104" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">字符串：s + t == t + s 时，前缀长 gcd(|s|, |t|)</text>
<text x="170" y="122" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">倒水：target 是 gcd(x, y) 的倍数且 ≤ x + y</text>
</svg>

```python
def gcd(a, b):                       # 辗转相除
    while b:
        a, b = b, a % b
    return a

def gcd_of_strings(s, t):            # LC 1071
    if s + t != t + s:               # 不是同一个串的重复
        return ""
    return s[:gcd(len(s), len(t))]

def can_measure(x, y, target):       # LC 365 裴蜀定理
    return target <= x + y and target % gcd(x, y) == 0
```

**要点。**
- 为什么对？：`s + t == t + s` 当且仅当两串是同一个串的重复，此时最大公因子长度就是两长度的 GCD；水壶能量出的量是 `gcd(x, y)` 的倍数，且不超过 `x + y`。
- 多个字符串怎么改？：`reduce` 两两合并，任一步得 `""` 后一直是 `""`。

**易错点。**
- 不做拼接检查直接取 GCD 长度的前缀：`("LEET", "CODE")` 得 `"LEET"`，应为 `""`。
- LC 365 漏掉 `target <= x + y`：`x = 1`、`y = 2`、`target = 4` 会错答 `True`。

**对应题目。** LC 365 水壶问题、LC 1071 字符串的最大公因子
