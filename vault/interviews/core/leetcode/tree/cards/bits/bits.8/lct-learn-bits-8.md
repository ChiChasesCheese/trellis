---
id: lct-learn-bits-8
node: bits.8
type: qa
step: 1
---
## Q
**位运算 › 思维题**｜学习卡

套路是什么？

## A
**一句话。** 看最低位的 `1`：它上面紧挨着还有 `1` 就加上它（整段进位），否则直接减去它。

下图：LC 2571，`n = 39` 共 3 步：加 1、减 8、减 32。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 145">
<rect x="90" y="14" width="24" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="102.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="114" y="14" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="126.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="138" y="14" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="162" y="14" width="24" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="174.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="186" y="14" width="24" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="198.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="210" y="14" width="24" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="222.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="82" y="30" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">39</text>
<rect x="90" y="54" width="24" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="102.0" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="114" y="54" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="126.0" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="138" y="54" width="24" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="150.0" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="162" y="54" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="174.0" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="186" y="54" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="198.0" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="210" y="54" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222.0" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<text x="82" y="70" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">+1 进位</text>
<rect x="90" y="94" width="24" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="102.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="114" y="94" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="126.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="138" y="94" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="162" y="94" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="174.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="186" y="94" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="198.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="210" y="94" width="24" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<text x="82" y="110" text-anchor="end" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-8</text>
<text x="245" y="30" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">上面紧挨 1：加</text>
<text x="245" y="70" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">孤立的 1：减</text>
<text x="245" y="110" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再减 → 0</text>
<text x="170" y="138" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">看最低位的 1：整段 1 用一次加法进位消掉</text>
</svg>

```python
def min_operations(n):
    ops = 0
    while n:
        low = n & -n                 # 最低位的 1
        if n & (low << 1):           # 上面紧挨着还有 1：整段进位
            n += low
        else:                        # 孤立的 1：直接减
            n -= low
        ops += 1
    return ops
```

**要点。**
- 为什么对？：连续 `k >= 2` 个 `1` 逐个减要 `k` 步，加上最低位进位后只要 `2` 步；孤立的 `1` 加上去只是挪到高位，白花一步。
- 有没有一行解？：答案是 `n` 的带符号二进制（NAF）非零位数：`(3 * n ^ n).bit_count()`。

**易错点。**
- 只做减法：`n = 39` 得 `4`（二进制 `1` 的个数），应为 `3`。
- 一律做加法：`n = 5 = 101` 两个 `1` 都孤立，减 `1` 再减 `4` 共 `2` 步，一律加要 `3` 步。

**对应题目。** LC 2571 将整数减少到零需要的最少操作数
