---
id: lct-learn-bits-1
node: bits.1
type: qa
step: 1
---
## Q
**位运算 › 基础题**｜学习卡

套路是什么？

## A
**一句话。** 位运算基础：`n & (n - 1)` 清掉最低位的 `1`，`n & -n` 取出最低位的 `1`，`i >> 1` 是去掉最低位的子问题。

下图：`n - 1` 把最低位的 1 及以下全部翻转，于是 `n & (n-1)` 清掉它，`n & -n` 只留下它。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="100" y="14" width="24" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="112.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="124" y="14" width="24" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="136.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="148" y="14" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="172" y="14" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="184.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<text x="92" y="30" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">n = 12</text>
<rect x="100" y="44" width="24" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="112.0" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="124" y="44" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="136.0" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="148" y="44" width="24" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="160.0" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="172" y="44" width="24" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="184.0" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<text x="92" y="60" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">n - 1</text>
<rect x="100" y="74" width="24" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="112.0" y="90" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="124" y="74" width="24" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="136.0" y="90" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<rect x="148" y="74" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="90" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="172" y="74" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="184.0" y="90" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<text x="92" y="90" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">n &amp; (n-1)</text>
<rect x="100" y="104" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="112.0" y="120" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="124" y="104" width="24" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="136.0" y="120" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="148" y="104" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="120" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="172" y="104" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="184.0" y="120" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<text x="92" y="120" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">n &amp; -n</text>
<text x="210" y="92" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">清掉最低位的 1</text>
<text x="210" y="122" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">取出最低位的 1</text>
<text x="210" y="36" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">n - 1：最低的 1 变 0</text>
<text x="210" y="50" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">它下面的 0 全变 1</text>
</svg>

```python
def popcount(n):                     # LC 191
    cnt = 0
    while n:
        n &= n - 1                   # 清掉最低位的 1
        cnt += 1
    return cnt

def is_power_of_two(n):              # LC 231
    return n > 0 and n & (n - 1) == 0

def count_bits(n):                   # LC 338
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return ans
```

**要点。**
- 为什么对？：`n - 1` 把最低位的 `1` 变成 `0`、其右边的 `0` 全变成 `1`，相与后这一段全为 `0`、高位不变，所以恰好少一个 `1`。
- LC 190 怎么改？：固定循环 `32` 次：`res = res << 1 | n & 1`，`n >>= 1`；不能用 `while n`，前导零会丢。

**易错点。**
- `popcount` 里写成 `n & -n`：它保留最低位的 `1`，`n` 永不归零，死循环。
- `is_power_of_two` 漏掉 `n > 0`：`0 & -1 == 0`，`n = 0` 会误返回 `True`。
- `count_bits` 数组长度写成 `[0] * n`：要覆盖 `0..n`，`n = 2` 时 `ans[2]` 越界。

**对应题目。** LC 190 颠倒二进制位、LC 191 位 1 的个数（Number of 1 Bits）、LC 231 2 的幂、LC 338 比特位计数
