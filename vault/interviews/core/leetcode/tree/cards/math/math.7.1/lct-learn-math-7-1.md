---
id: lct-learn-math-7-1
node: math.7.1
type: qa
step: 1
---
## Q
**数学算法 › 杂项 › 回文数**｜学习卡

套路是什么？

## A
**一句话。** 不转字符串：只反转后一半数位，与前一半比较，反转到 `x <= rev` 就停。

下图：只把后一半数位反转到 `rev`，再和剩下的前一半比较。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<text x="80" y="34" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">x = 1221</text>
<text x="200" y="34" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">rev = 0</text>
<text x="80" y="64" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">x = 122</text>
<text x="200" y="64" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">rev = 1</text>
<text x="140" y="52" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">↓ 末位挪过去</text>
<text x="80" y="94" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">x = 12</text>
<text x="200" y="94" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">rev = 12</text>
<text x="140" y="82" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">↓ 末位挪过去</text>
<text x="170" y="112" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">x ≤ rev 时停：x == rev（偶数位）或 x == rev // 10（奇数位）</text>
</svg>

```python
def is_palindrome(x):
    if x < 0 or (x % 10 == 0 and x != 0):
        return False                 # 负数、以 0 结尾（非 0）都不是
    rev = 0
    while x > rev:                   # 只反转后一半
        rev = rev * 10 + x % 10
        x //= 10
    return x == rev or x == rev // 10   # 偶数位 / 奇数位
```

**要点。**
- 为什么只反转一半？：回文的前一半等于后一半的反转，比较一半足够；整个反转在 32 位下可能溢出，一半永远不会。
- 直接转字符串怎么写？：`s = str(x); return s == s[::-1]`，负号反过来跑到末尾，天然不相等。

**易错点。**
- 漏掉以 `0` 结尾：`x = 10` 会判 `True`，要先排除 `x % 10 == 0 and x != 0`。
- 奇数位只比 `x == rev`：`121` 停在 `x = 1`、`rev = 12`，还要比 `x == rev // 10`。

**对应题目。** LC 9 回文数
