---
id: lct-learn-bits-9
node: bits.9
type: qa
step: 1
---
## Q
**位运算 › 其他**｜学习卡

套路是什么？

## A
**一句话。** 异或的两条性质 `a ^ a = 0`、`0 ^ x = x`：成对的数抵消，剩下的就是答案；两个落单数用异或值的一个 `1` 位把数组分两组。

下图：LC 260，按 `a ^ b` 的一个 1 位把数组分两组，两个落单数各在一组。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<text x="170" y="18" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums = 1 2 1 3 2 5；a ^ b = 3 ^ 5 = 110，取最低位 010</text>
<rect x="20" y="34" width="140" height="70" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="90" y="52" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">这一位为 1</text>
<text x="90" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2  3  2</text>
<text x="90" y="94" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">异或 = 3</text>
<rect x="180" y="34" width="140" height="70" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="250" y="52" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">这一位为 0</text>
<text x="250" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1  1  5</text>
<text x="250" y="94" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">异或 = 5</text>
<text x="170" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a ^ a = 0：成对的数抵消，组内只剩落单的那个</text>
</svg>

```python
def single_number(nums):             # LC 136：成对抵消
    ans = 0
    for x in nums:
        ans ^= x
    return ans

def single_number_iii(nums):         # LC 260：两个落单数 a、b
    both = single_number(nums)       # a ^ b，非零
    low = both & -both               # a、b 在这一位不同
    a = 0
    for x in nums:
        if x & low:                  # 只异或这一位为 1 的一组
            a ^= x
    return [a, both ^ a]
```

**要点。**
- 为什么对？：成对的数异或为 `0`，落单的数留下；两个落单数异或非零，在 `low` 这一位上一个是 `1` 一个是 `0`，被分进不同组，各组内成对的数仍抵消。
- LC 137 怎么改？：每一位上 `1` 的个数对 `3` 取余，余数拼回答案；Python 里第 `31` 位为 `1` 要还原成负数。
- LC 371 怎么改？：反复 `a, b = a ^ b, (a & b) << 1`（无进位和、进位）直到进位为 `0`，用 `32` 位掩码模拟补码。
- LC 201 怎么改？：结果是 `left`、`right` 的二进制公共前缀：同时右移到相等，再左移回去。

**易错点。**
- LC 260 随手按 `x & 1` 分组：`[1,2,1,3,2,5]` 的 `a ^ b = 110`，第 `0` 位相同，分不开，得 `[6,0]`，应为 `[3,5]`。
- LC 137 忘了处理符号：`[-4,1,1,1]` 返回 `4294967292`，应为 `-4`。
- LC 371 不加掩码：`a = -1`、`b = 1` 时进位永不消失，死循环。

**对应题目。** LC 136 只出现一次的数字、LC 137 只出现一次的数字 II、LC 201 数字范围按位与、LC 260 只出现一次的数字 III、LC 371 两整数之和、LC 645 错误的集合、LC 751 IP 到 CIDR
