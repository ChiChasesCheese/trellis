---
id: lct-learn-dp-11-6
node: dp.11.6
type: qa
step: 1
---
## Q
**动态规划 › 优化 DP › 矩阵快速幂优化 DP**｜学习卡

套路是什么？

## A
**一句话。** 线性递推的转移矩阵固定，`f(n) = A^n · f(0)`，用快速幂（平方法）把 `O(n)` 降成 `O(k^3 log n)`。

下图：快速幂把 `n` 拆成二进制，平方出 `M^1, M^2, M^4, …`，只乘需要的那几个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<text x="20" y="24" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">n = 13 = 1101₂</text>
<rect x="30" y="50" width="54" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="57" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">M¹</text>
<text x="57" y="98" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位 0：1</text>
<rect x="104" y="50" width="54" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="131" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">M²</text>
<text x="131" y="98" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位 1：0</text>
<line x1="84" y1="65" x2="102" y2="65" stroke-width="1.2" stroke="currentColor"/>
<polygon points="102.0,65.0 95.7,68.0 95.7,62.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="50" width="54" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="205" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">M⁴</text>
<text x="205" y="98" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位 2：1</text>
<line x1="158" y1="65" x2="176" y2="65" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176.0,65.0 169.7,68.0 169.7,62.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="252" y="50" width="54" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="279" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">M⁸</text>
<text x="279" y="98" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位 3：1</text>
<line x1="232" y1="65" x2="250" y2="65" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,65.0 243.7,68.0 243.7,62.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="42" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每轮 M = M · M（平方）</text>
<text x="170" y="120" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">res = M¹ · M⁴ · M⁸ = M¹³：只乘二进制为 1 的位</text>
<text x="170" y="136" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">log n 次 k×k 矩阵乘法</text>
</svg>

```python
MOD = 10**9 + 7                      # LC 509 的 n 小，取不取模都行

def mul(A, B):
    return [[sum(a * b for a, b in zip(row, col)) % MOD
             for col in zip(*B)] for row in A]

def fib(n):
    # M^n = [[F(n+1), F(n)], [F(n), F(n-1)]]
    M = [[1, 1], [1, 0]]
    res = [[1, 0], [0, 1]]           # 单位矩阵
    while n:                         # 快速幂：log n 轮
        if n & 1:
            res = mul(res, M)
        M = mul(M, M)
        n >>= 1
    return res[0][1]
```

**要点。**
- 为什么对？：`(F(n+1), F(n))` 由 `(F(n), F(n-1))` 左乘同一个矩阵得到，所以 `n` 步等于矩阵的 `n` 次幂，幂用二进制拆分，每轮平方。
- LC 1137 怎么改？：泰波那契要三项，矩阵换成 `3×3`：`[[1,1,1],[1,0,0],[0,1,0]]`；递推带常数项，就给状态再补一维常数 `1`。

**易错点。**
- `res` 初值写成零矩阵：结果恒为 `0`，要用单位矩阵。
- `n` 很大却不取模：矩阵元素指数增长，`n = 10^18` 时数不下，每次乘法后 `% MOD`。

**对应题目。** LC 509 斐波那契数
