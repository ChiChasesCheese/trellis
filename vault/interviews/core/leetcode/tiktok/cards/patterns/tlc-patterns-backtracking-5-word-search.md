---
id: tlc-patterns-backtracking-5-word-search
node: patterns.backtracking
type: qa
step: 5
---
## Q
**回溯（Backtracking）｜单词搜索（LC 79）：网格里的回溯与"原地标记"**

在网格里沿相邻格子拼出单词，每个格子最多用一次。怎样标记已使用的格子？不撤销标记会怎样？

## A
从每个格子出发 DFS，匹配 `word[i]`；走过的格子**临时改成特殊字符**，回来时再改回去，省掉 `visited` 数组。

```python
def exist(board: list[list[str]], word: str) -> bool:
    m, n = len(board), len(board[0])
    def dfs(r: int, c: int, i: int) -> bool:
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        ch, board[r][c] = board[r][c], "#"   # 标记已用
        found = any(0 <= a < m and 0 <= b < n and dfs(a, b, i + 1)
                    for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)))
        board[r][c] = ch                   # 撤销：别的起点还要用这个格子
        return found
    return any(dfs(r, c, 0) for r in range(m) for c in range(n))
B = [list("ABCE"), list("SFCS"), list("ADEE")]
print(exist(B, "ABCCED"), exist(B, "SEE"), exist(B, "ABCB"))   # True True False
```

约束 `m, n <= 6`、`len(word) <= 15`：每个格子最多向 3 个方向继续，最坏 `O(mn · 3^L)`，剪枝让实际远小于此。

**反例：不撤销标记。** 把 `board[r][c] = ch` 删掉，并且在找到答案后直接返回：
- 对同一块棋盘先查 `"ABCCED"` 再查 `"SEE"`：第一次查询已经把沿途格子改成了 `#`，第二次返回 `False`，正确是 `True`。
- 即使单次查询，从不同起点出发的分支也会互相污染。

- 常见优化：先统计棋盘与单词的字符频次，单词里某字符比棋盘多就直接 `False`；单词首尾字符在棋盘上频次不同，可以反转单词再搜，减少分支。
- `any(...)` 对生成器短路：找到一条路径就不再展开其余方向。
- LC 212 单词搜索 II：多个单词一起搜，要把单词放进字典树，在 DFS 里沿着字典树走。
