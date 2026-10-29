---
id: uth-devtools-git-objects-3-pack
node: devtools.git-objects
type: qa
step: 3
---
## Q
**packfile：给相似对象只存差量**｜Git · pack-objects

一个大文件每次改一行，提交 100 次，仓库为什么没膨胀 100 倍？

## A
**背景。** 按“每个版本存一份完整 blob”，一个大文件改 100 次就要存 100 份几乎一样的内容。打包（pack）时，git 找相似的对象，只存“和基对象的差别”，叫差量（delta）。

**结构。** `git pack-objects` 把对象排序，在滑动窗口内找最相似的对象当基，只存差量：`OFS_DELTA` 记基对象的相对偏移，`REF_DELTA` 记基对象的哈希。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 220">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">差量链 最长 50 层</text>
<rect x="14" y="28" width="80" height="28" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="54" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">基对象</text>
<text x="54" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">10 KB</text>
<rect x="112" y="28" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="142" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">差量</text>
<text x="142" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">0.1 KB</text>
<line x1="112" y1="42" x2="101" y2="42" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M96.0,42.0 L102.8,38.7 L102.8,45.3 Z" fill="currentColor" stroke="none"/>
<rect x="190" y="28" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">差量</text>
<text x="220" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">0.1 KB</text>
<line x1="190" y1="42" x2="179" y2="42" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M174.0,42.0 L180.8,38.7 L180.8,45.3 Z" fill="currentColor" stroke="none"/>
<rect x="268" y="28" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="298" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">差量</text>
<text x="298" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">0.1 KB</text>
<line x1="268" y1="42" x2="257" y2="42" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M252.0,42.0 L258.8,38.7 L258.8,45.3 Z" fill="currentColor" stroke="none"/>
<text x="20" y="110" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">一个差量里只有两种指令</text>
<rect x="20" y="120" width="300" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="136" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">基对象</text>
<rect x="20" y="160" width="130" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="85" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">复制 一段</text>
<rect x="150" y="160" width="40" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">插入</text>
<rect x="190" y="160" width="130" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="255" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">复制 一段</text>
<line x1="85" y1="144" x2="85" y2="160" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.45"/>
<line x1="255" y1="144" x2="255" y2="160" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.45"/>
<text x="170" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">新版本 = 复制旧的 加 插入新的</text>
</svg>
```

**细节。**

- 排序依次按：类型、文件名哈希、大小（大的在前），同名的 blob 就排到了一起
- 默认窗口 `pack.window` 是 10，差量链最长 `pack.depth` 是 50
- 差量内容是两种指令：从基对象复制一段区间；插入新数据

**为什么。** 窗口越大越省空间，但打包越慢、越吃内存，默认值是折中；git 不追踪文件，只靠相似度找基对象。

**例题：** LC 72 编辑距离

返回把 `word1` 转换成 `word2` 所需的最少操作数，每次操作可以插入、删除或替换一个字符。例：`"horse"` → `"ros"` 是 3（替换 h，删除 r，删除 e）。

```python
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # dp[i][j]：word1[:i] 变成 word2[:j] 的最少操作数
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                        # 第 0 列：word1[:i] -> 空串，删 i 个
    for j in range(n + 1):
        dp[0][j] = j                        # 第 0 行：空串 -> word2[:j]，插 j 个
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]         # 末尾相同，不花操作
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1],   # 替换
                                   dp[i - 1][j],       # 删除 word1[i-1]
                                   dp[i][j - 1])       # 插入 word2[j-1]
    return dp[m][n]
```
