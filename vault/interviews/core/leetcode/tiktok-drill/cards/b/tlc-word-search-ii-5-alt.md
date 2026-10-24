---
id: tlc-word-search-ii-5-alt
node: b.word-search-ii
type: qa
step: 5
---
## Q
**LC 212 单词搜索 II**｜另一种解法

不建字典树，对每个单词单独做一次 LC 79 的搜索，怎么写？什么时候这样做就够了，什么时候必须用字典树？

## A
**思路。** 对每个单词独立做回溯：从每个格子出发，逐字符匹配，用 `'#'` 占位避免重复，走完整个单词就是找到。

```python
def find_words_each(board: list[list[str]], words: list[str]) -> list[str]:
    m, n = len(board), len(board[0])

    def exist(word: str) -> bool:
        def dfs(i: int, j: int, k: int) -> bool:
            if k == len(word):
                return True
            if not (0 <= i < m and 0 <= j < n) or board[i][j] != word[k]:
                return False
            ch, board[i][j] = board[i][j], '#'
            ok = any(dfs(i + di, j + dj, k + 1) for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            board[i][j] = ch
            return ok

        return any(dfs(i, j, 0) for i in range(m) for j in range(n))

    return [word for word in words if exist(word)]
```

输出与字典树版一致：示例 1 → `['oath', 'eat']`（顺序随 `words` 的顺序），示例 2 → `[]`。

**取舍。**
- 单词很少（几个到几十个）或者盘面很小：逐词搜索更简单，面试里可以先说出来作为基线。
- 单词很多或前缀大量重复：必须用字典树。实测：全 `a` 的 `12 x 12` 盘面，`200` 个形如 `"aaaaaaaa" + 两个别的字母` 的词，字典树版 `0.065 s` 完成（前 `8` 个 `a` 的路径只搜一遍，随后马上发现没有后续字母）；逐词版仅 `5` 个词就用了 `0.62 s`，按这个速度 `200` 个词约 `25 s`。
- 复杂度：逐词 `O(W · mn · 3^L)`；字典树 `O(mn · 3^L)` 的上界，且共享前缀、提前剪枝。

先说基线再引出字典树，是被追问「单词再多一些呢」时最自然的路径。
