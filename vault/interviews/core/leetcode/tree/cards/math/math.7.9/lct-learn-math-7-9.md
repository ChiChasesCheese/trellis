---
id: lct-learn-math-7-9
node: math.7.9
type: qa
step: 1
---
## Q
**数学算法 › 杂项 › 确定数位**｜学习卡

套路是什么？

## A
**一句话。** 按位数分段：`1` 位数占 `9` 位，`2` 位数占 `180` 位……先跳过整段定位位数，再算出是哪个数的第几位。

下图：按位数分段，`n` 先跳过整段，再落到具体的数和数位。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="15" y="40" width="60" height="30" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="45.0" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1 位数</text>
<text x="45.0" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9 位</text>
<rect x="75" y="40" width="110" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="130.0" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 位数</text>
<text x="130.0" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">180 位</text>
<rect x="185" y="40" width="140" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3 位数</text>
<text x="255.0" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2700 位</text>
<line x1="87" y1="20" x2="87" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="87.0,38.0 84.0,31.7 90.0,31.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="87" y="16" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">n = 15：跳过 9 位后 n = 6</text>
<text x="170" y="114" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">数 = 10 + (6-1) // 2 = 12；第 (6-1) % 2 = 1 位 → 2</text>
<text x="170" y="132" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先整段跳过，再定位到哪个数的第几位</text>
</svg>

```python
def find_nth_digit(n):
    length, count, start = 1, 9, 1   # 本段：length 位数共 count 个
    while n > length * count:
        n -= length * count          # 整段跳过
        length += 1
        count *= 10
        start *= 10
    num = start + (n - 1) // length  # 落在哪个数
    return int(str(num)[(n - 1) % length])
```

**要点。**
- 为什么对？：每段内的数位数相同，所以第 `n` 位落在第 `(n-1)//length` 个数的第 `(n-1)%length` 位（都从 `0` 数起）；分段只有 `O(log n)` 段。
- 要返回第 `n` 位所属的整数怎么改？：`num` 就是。

**易错点。**
- 用 `n // length` 而不是 `(n - 1) // length`：段边界上错一个数，`n = 9` 应得 `9`。
- 循环条件写成 `n >= length * count`：`n` 恰为整段末尾时多跳一段，`n = 9` 抛 `IndexError`。
- 位内偏移用 `n % length`：`n = 10` 应得 `1`（数字 `10` 的首位）。

**对应题目。** LC 400 第 N 位数字
