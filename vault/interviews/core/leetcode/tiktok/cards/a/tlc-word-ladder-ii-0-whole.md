---
id: tlc-word-ladder-ii-0-whole
node: a.word-ladder-ii
type: qa
---
## Q
**LC 126 单词接龙 II**｜Hard · 近一年被问：美国 2 次、国内 1 次 · 最近 2026-10-25（面试记录）

给两个单词 `beginWord`、`endWord` 和字典 `wordList`。转换序列是 `beginWord -> s1 -> s2 -> ... -> sk` 的单词序列：相邻两个单词恰好有一个字母不同；`s1` 到 `sk` 都必须在 `wordList` 中（`beginWord` 不必在）；`sk == endWord`。找出并返回所有从 `beginWord` 到 `endWord` 的最短转换序列（每个序列是单词列表 `[beginWord, s1, ..., sk]`），不存在时返回空列表。`1 <= beginWord.length <= 5`，`endWord.length == beginWord.length`，`1 <= wordList.length <= 500`，`wordList[i].length == beginWord.length`，所有单词只含小写字母，`beginWord != endWord`，`wordList` 中的单词互不相同。例：`beginWord = "hit"`，`endWord = "cog"`，`wordList = ["hot","dot","dog","lot","log","cog"]` → `[["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]`（顺序任意）；`wordList = ["hot","dot","dog","lot","log"]`（没有 `cog`）→ `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先做按层的 BFS，对每个单词记录它在最短路上的所有「上一层父亲」；到达 `endWord` 所在的那一层就停止；再从 `endWord` 沿父亲链做 DFS 回溯，展开成全部最短路径。邻居用通配符桶（`h*t`）查找。

**识别。** 「最短路径」是 BFS；「所有最短路径」要在 BFS 中保留同一层的多个父亲，再回溯展开；「相差一个字母」的邻接关系可以用通配符桶（每个位置换成 `*`）一次找到，而不是对每个词枚举 `26 * L` 个替换；`wordList <= 500`、单词长度 `<= 5`，图很小，但最短路的数量可能很大，输出规模决定下界。

**推导。** 暴力：DFS 枚举所有从起点出发的简单路径，再取最短的，路径数指数级；BFS 队列里存整条路径，每次扩展都复制路径，同层还要放开访问标记 → 浪费：BFS 过程中保存了大量最终不会成为最短路的路径前缀，路径复制的成本也被放大 → 洞察：最短路全体构成一张「层图」，只要知道每个词在最短路上的所有父亲（上一层、且与它相差一个字母的词），从 `endWord` 倒着走就是全部最短路。BFS 只存父亲关系，不存路径；同层的多个父亲必须全部记录，所以 `seen` 要等整层扫描完再更新；到达 `endWord` 这一层就停，更深的层不可能再有最短路。

```python
from collections import defaultdict


def find_ladders(begin_word: str, end_word: str, word_list: list[str]) -> list[list[str]]:
    words = set(word_list)
    if end_word not in words:
        return []
    buckets: defaultdict[str, list[str]] = defaultdict(list)   # "h*t" -> 所有只差通配位的词
    for w in words | {begin_word}:
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)

    parents: dict[str, list[str]] = {}          # 词 -> 它在最短路上的所有上一层父亲
    seen = {begin_word}
    layer = {begin_word}
    while layer and end_word not in layer:      # 按层 BFS，到达 end 的那一层就停
        nxt: defaultdict[str, list[str]] = defaultdict(list)
        for w in layer:
            for i in range(len(w)):
                for v in buckets[w[:i] + "*" + w[i + 1:]]:
                    if v not in seen:           # seen 只含更早的层，所以 nxt[v] 收集的是同一层的全部父亲
                        nxt[v].append(w)
        seen |= nxt.keys()                      # 整层扫完再标记：同层多个父亲才不会丢
        parents.update(nxt)
        layer = set(nxt)
    if end_word not in layer:
        return []

    res: list[list[str]] = []
    path = [end_word]

    def dfs(w: str) -> None:                    # 沿父亲链倒着走到 begin，每走通一条就是一条最短路
        if w == begin_word:
            res.append(path[::-1])
            return
        for parent in parents[w]:
            path.append(parent)
            dfs(parent)
            path.pop()

    dfs(end_word)
    return res
```

运行：示例 1 → `[['hit', 'hot', 'lot', 'log', 'cog'], ['hit', 'hot', 'dot', 'dog', 'cog']]`；没有 `cog` → `[]`；`("a", "c", ["a","b","c"])` → `[['a', 'c']]`；`("hot", "dog", ["hot","dog"])` → `[]`；由 `501` 个单词构成的长度为 `501` 的最短路径（相邻单词相差一个字母，其余无邻接）→ `1` 条路径，递归深度约 `501`，没有溢出。

**复杂度。** BFS 为 `O(N * L)` 个桶项加每个词的邻居扫描，`N` 为单词数，`L` 为长度；回溯为 `O(最短路条数 * 路径长度)`，由输出规模决定；空间 `O(N * L)` 加输出。

**易错点。**
- 发现邻居就立刻加入 `seen`：同一层的第二个父亲会被挡掉。示例 1 里 `cog` 的两个父亲 `dog`、`log` 在同一层，先处理的那个把 `cog` 标记为已见，另一个丢失，只得到 `[['hit','hot','dot','dog','cog']]` 一条，正确是两条。
- `endWord` 不在字典里：必须先判断并返回 `[]`，否则 BFS 永远到不了终点。
- 到达终点层后继续扩展：多做无用功；`while` 条件里加上 `end_word not in layer` 就停。

**追问。**
- 双向 BFS：从两端同时扩展较小的一侧，在相遇的层停止，分支多时搜索量小得多。
- 只统计最短路条数：在父亲表上做记忆化求和，`count[w] = sum(count[p] for p in parents[w])`，不需要展开路径。
- 字典很大：通配符桶的预处理是线性的，查询邻居不再是 `26 * L` 次试探。

**同模式。** LC 127 单词接龙、LC 433 最小基因变化、LC 752 打开转盘锁、LC 1091 二进制矩阵中的最短路径、LC 773 滑动谜题。
