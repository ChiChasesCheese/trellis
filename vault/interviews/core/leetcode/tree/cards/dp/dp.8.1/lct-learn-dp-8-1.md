---
id: lct-learn-dp-8-1
node: dp.8.1
type: qa
step: 1
---
## Q
**动态规划 › 区间 DP › 最长回文子序列**｜学习卡

套路是什么？

## A
**一句话。** 区间 DP：`dfs(i, j)` 是子串 `s[i..j]` 的最优值，从两端向中间缩：两端字符相等就包住内层，不等就丢掉一端取较优。

下图：`(i, j)` 只依赖更短的区间（左、下、左下三格），所以 `i` 倒序、`j` 正序填表。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<rect x="40" y="26" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57.0" y="43.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="74" y="26" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="108" y="26" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="142" y="26" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="176" y="26" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="40" y="52" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="74" y="52" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="91.0" y="69.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="108" y="52" width="34" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="142" y="52" width="34" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="159.0" y="69.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i,j</text>
<rect x="176" y="52" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="40" y="78" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="74" y="78" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="108" y="78" width="34" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="125.0" y="95.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="142" y="78" width="34" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="176" y="78" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="40" y="104" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="74" y="104" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="108" y="104" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="142" y="104" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="159.0" y="121.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="176" y="104" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="40" y="130" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="74" y="130" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="108" y="130" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="142" y="130" width="34" height="26" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="176" y="130" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="193.0" y="147.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<line x1="137.0" y1="87.0" x2="149.0" y2="75.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="149.0,75.0 146.6,81.6 142.4,77.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="159.0" y1="87.0" x2="159.0" y2="78.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="159.0,78.0 162.0,84.3 156.0,84.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="133.0" y1="65.0" x2="142.0" y2="65.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="142.0,65.0 135.7,68.0 135.7,62.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="40" y="18" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">j →</text>
<text x="26" y="44" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i</text>
<text x="220" y="40" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两端相等：</text>
<text x="220" y="56" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">左下 (i+1, j-1) + 2</text>
<text x="220" y="84" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">不等：max(下, 左)</text>
<text x="220" y="112" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对角线 = 1</text>
<text x="220" y="128" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">i 从大到小算</text>
</svg>

```python
def longest_palindrome_subseq(s):
    @cache
    def dfs(i, j):                   # s[i..j] 的最长回文子序列长度
        if i > j:
            return 0                 # 空串
        if i == j:
            return 1                 # 单个字符
        if s[i] == s[j]:             # 两端相同：包住内层
            return dfs(i + 1, j - 1) + 2
        return max(dfs(i + 1, j), dfs(i, j - 1))   # 丢一端

    return dfs(0, len(s) - 1)
```

**要点。**
- 为什么对？：回文子序列的最外层若是 `s[i]` 与 `s[j]` 配对，则里面是 `s[i+1..j-1]` 的回文子序列；否则 `s[i]` 或 `s[j]` 至少有一个没被选，丢掉它不损失；状态数 `O(n^2)`，每个 `O(1)`。
- LC 1216 怎么改？：问最少删几个变回文，等于 `n - 最长回文子序列`，所以删 `k` 次可行等价于 `n - LPS <= k`。
- 写成递推怎么改？：`i` 倒序、`j` 正序（`j > i`），因为 `dp[i][j]` 依赖 `dp[i+1][*]` 与 `dp[i][j-1]`。

**易错点。**
- 子序列与子串混淆：两端不等时子串是 `0`，子序列要继续取较大者。
- 递推时循环顺序错：`i` 正序会读到还没算的 `dp[i+1][j-1]`，必须 `i` 从大到小。
- 边界漏掉 `i > j`：`"aa"` 中 `dfs(1, 0)` 要返回 `0`，`dfs(i+1, j-1) + 2` 才得 `2`。

**对应题目。** LC 516 最长回文子序列、LC 1216 验证回文串 III
