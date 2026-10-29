---
id: uth-python-list-3-pointers
node: python.list
type: qa
step: 3
---
## Q
**list 里存的是指针**｜Python · CPython 3.14

`a = [[0]] * 3` 之后执行 `a[0].append(1)`，为什么三个内层列表同时变了？`sys.getsizeof([None]*1000)` 为什么是 8056？

## A
**背景。** `list` 要能装任何类型，而各种对象大小不一，没法塞进等宽的格子。办法：格子里只放等宽的「地址」（指针），对象本身另放别处。

**结构。** 每个格子是一个 8 字节的指针。`[x] * n` 只是把同一个指针复制 n 份，三个格子指向同一个内层列表。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="20" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a = [[0]] * 3</text>
<rect x="30" y="26" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<line x1="47" y1="50" x2="81" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81.0,84.0 75.7,82.2 79.2,78.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="64" y="26" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<line x1="81" y1="50" x2="81" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81.0,84.0 78.5,79.0 83.5,79.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="98" y="26" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<line x1="115" y1="50" x2="81" y2="84" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81.0,84.0 82.8,78.7 86.3,82.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="52" y="86" width="60" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82" y="103" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[0]</text>
<text x="190" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个内层对象</text>
<text x="20" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[[0] for _ in range(3)]</text>
<rect x="30" y="152" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<line x1="47" y1="176" x2="47" y2="196" stroke-width="1.2" stroke="currentColor"/>
<polygon points="47.0,196.0 44.5,191.0 49.5,191.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="30" y="198" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="47" y="215" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[0]</text>
<rect x="64" y="152" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<line x1="81" y1="176" x2="81" y2="196" stroke-width="1.2" stroke="currentColor"/>
<polygon points="81.0,196.0 78.5,191.0 83.5,191.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="64" y="198" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="81" y="215" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[0]</text>
<rect x="98" y="152" width="34" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<line x1="115" y1="176" x2="115" y2="196" stroke-width="1.2" stroke="currentColor"/>
<polygon points="115.0,196.0 112.5,191.0 117.5,191.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="98" y="198" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="115" y="215" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[0]</text>
<text x="190" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各有自己的内层</text>
</svg>
```

**细节。**

- 实测 `a` 变成 `[[0, 1], [0, 1], [0, 1]]`。
- 8056 = 对象头 56 字节 + 1000 × 8 字节指针。

**为什么。** 存指针让一个列表能装任意类型，代价是多一层间接寻址、缓存不友好；数值计算才会改用 `array` 或 NumPy。

**坑。** 二维 DP 数组要写 `[[0] for _ in range(3)]`，不能用乘法。

**例题：** LC 62 不同路径

机器人在 `m x n` 网格左上角，每次只能向下或向右走一步，求走到右下角有多少条不同路径。例：`m = 3, n = 7` 得 `28`。

```python
from math import comb


def unique_paths(m: int, n: int) -> int:
    # dp[i][j]：从左上角走到 (i, j) 的路径数
    dp = [[1] * n for _ in range(m)]                 # 第一行、第一列都只有 1 条路
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]   # 最后一步从上来，或从左来
    return dp[m - 1][n - 1]


def unique_paths_comb(m: int, n: int) -> int:
    return comb(m + n - 2, m - 1)                    # 一共走 m+n-2 步，选出 m-1 步向下
```
