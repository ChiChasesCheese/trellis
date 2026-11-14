---
slug: word-search
---
## Q
**LC 79 单词搜索**｜Medium

在字符网格里，判断 `word` 能否由水平或竖直相邻的格子依次连成，同一格在一条路径里不能重复使用。

## A
**一句话。** 回溯（DFS）：每格作起点逐字符匹配，走过的格临时标成 `"#"`，回溯时还原。

**图解。** 从起点沿相邻格逐字匹配，走过的格暂记 `#`，这条路失败就还原。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 130">
<rect x="20" y="14" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="37.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="54" y="14" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="88" y="14" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="122" y="14" width="34" height="34" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="139.0" y="35.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">E</text>
<rect x="20" y="48" width="34" height="34" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="37.0" y="69.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">S</text>
<rect x="54" y="48" width="34" height="34" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="69.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">F</text>
<rect x="88" y="48" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="69.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="122" y="48" width="34" height="34" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="139.0" y="69.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">S</text>
<rect x="20" y="82" width="34" height="34" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="37.0" y="103.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="54" y="82" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="103.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D</text>
<rect x="88" y="82" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="103.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">E</text>
<rect x="122" y="82" width="34" height="34" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="139.0" y="103.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">E</text>
<polyline points="37.0,40.0 71.0,40.0 105.0,40.0 105.0,74.0 105.0,108.0 71.0,108.0" fill="none" stroke-width="1.6" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="71.0,108.0 77.0,105.0 77.0,111.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="176" y="32" text-anchor="start" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">word = ABCCED</text>
<text x="176" y="56" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">逐字走相邻格</text>
<text x="176" y="78" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">走过的格暂记 #</text>
<text x="176" y="100" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">这条路失败就还原</text>
</svg>

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])
    cnt = Counter(chain.from_iterable(board))
    if Counter(word) - cnt:       # 字母不够，直接失败
        return False
    if cnt[word[0]] > cnt[word[-1]]:
        word = word[::-1]         # 从稀有的一端起手

    def dfs(r, c, k):             # 站在 (r,c)，要匹配 word[k]
        if board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        board[r][c] = "#"         # 标记本路径已用
        found = any(
            0 <= nr < rows and 0 <= nc < cols
            and dfs(nr, nc, k + 1)
            for nr, nc in ((r+1, c), (r-1, c),
                           (r, c+1), (r, c-1)))
        board[r][c] = word[k]     # 回溯：还原
        return found

    return any(dfs(r, c, 0)
               for r in range(rows) for c in range(cols))
```

**复杂度。** 时间 `O(mn · 3^L)`，空间 `O(L)`。

**易错点。**
- 不标记已用的格：`[["a","b"]]` 找 `"aba"` 得 `True`，应为 `False`。
- 失败后不还原 `"#"`：残留的 `"#"` 会堵死后面的起点，漏掉本来存在的路径。
- 先递归后判越界：负下标不报错却读到另一侧的格子，要显式检查 `0 <= nr`。

**追问。**
- 为什么先数字母、反转单词？：`6x6` 全 `a` 的棋盘找 `14` 个 `a` 加一个 `b`，不剪枝要试遍指数条路径才失败。
- 同时找多个单词？：建前缀树（Trie），一次 DFS 匹配全部，共享前缀只搜一次。

**同模式。** LC 212 单词搜索 II、LC 200 岛屿数量、LC 130 被围绕的区域、LC 980 不同路径 III
