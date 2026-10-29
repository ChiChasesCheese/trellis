---
id: uth-devtools-diff-1-myers
node: devtools.diff
type: qa
step: 1
---
## Q
**diff 怎么找最少的增删**｜Git · xdiff · 2.56

两个文件各有上万行，diff 怎么快速找出最少的增删行？

## A
**背景。** diff 要回答：旧文件怎样改成新文件，增删的行最少？例：旧 `A B C D`，新 `A C D E`：删 B、加 E，共 2 处。办法是找两个文件的最长公共子序列（LCS，两边按顺序都出现的最长一串行），LCS 以外的行就是要增删的。教科书的动态规划要填 n×m 个格子，两个上万行的文件就是上亿格。

**结构。** Myers 算法：画一张编辑图，向右走是删一行，向下走是插一行，两边相同的行走对角线、不花代价；目标是用最少的横纵步，从左上走到右下。它按步数 D = 0, 1, 2 … 逐层推进，每条对角线只记走得最远的点。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 228">
<line x1="70" y1="52" x2="70" y2="196" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="120" y1="52" x2="120" y2="196" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="170" y1="52" x2="170" y2="196" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="220" y1="52" x2="220" y2="196" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="270" y1="52" x2="270" y2="196" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="70" y1="52" x2="270" y2="52" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="70" y1="88" x2="270" y2="88" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="70" y1="124" x2="270" y2="124" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="70" y1="160" x2="270" y2="160" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="70" y1="196" x2="270" y2="196" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="95" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">A</text>
<text x="145" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">B</text>
<text x="195" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">C</text>
<text x="245" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">D</text>
<text x="50" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">A</text>
<text x="50" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">C</text>
<text x="50" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">D</text>
<text x="50" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">E</text>
<text x="170" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">旧文件</text>
<text x="26" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">新</text>
<line x1="70" y1="52" x2="120" y2="88" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<line x1="170" y1="88" x2="220" y2="124" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<line x1="220" y1="124" x2="270" y2="160" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<polyline points="70,52 120,88 170,88 220,124 270,160 270,196" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="70" cy="52" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="70" cy="88" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="70" cy="124" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="70" cy="160" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="70" cy="196" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="120" cy="52" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="120" cy="88" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="120" cy="124" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="120" cy="160" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="120" cy="196" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="170" cy="52" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="170" cy="88" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="170" cy="124" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="170" cy="160" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="170" cy="196" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="220" cy="52" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="220" cy="88" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="220" cy="124" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="220" cy="160" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="220" cy="196" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="270" cy="52" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="270" cy="88" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="270" cy="124" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="270" cy="160" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="270" cy="196" r="2.2" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="218" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">右 = 删 下 = 插 虚线斜边 = 相同 免费</text>
</svg>
```

**细节。**

- 时间 O(N·D)：N 是两个文件的行数之和，D 是增删的行数；改动越少越快
- 只允许增删时，最少增删数 = 两文件行数之和 − 2 × LCS 长度
- git 用中点分治（从中间切成两半各自求解）把空间降到线性；搜索代价过大（至少 256 步）会启发式截断，结果未必最短，`--minimal` 才强制最短

**为什么。** 教科书 LCS 动态规划要填 n×m 个格子，Myers 利用“两个版本通常差得很少”。

**例题：** LC 1143 最长公共子序列

返回两个字符串的最长公共子序列（保持相对顺序，可以不连续）的长度，没有则返回 0。`1 <= text1.length, text2.length <= 1000`。例：`"abcde"` 与 `"ace"` → 3。

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    # dp[i][j]：text1[:i] 与 text2[:j] 的 LCS 长度；第 0 行、第 0 列保持 0（空串）
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i, a in enumerate(text1, 1):
        for j, b in enumerate(text2, 1):
            if a == b:
                dp[i][j] = dp[i - 1][j - 1] + 1             # 末尾相同：一起算进去
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # 不同：丢掉其中一个串的末尾
    return dp[m][n]
```
