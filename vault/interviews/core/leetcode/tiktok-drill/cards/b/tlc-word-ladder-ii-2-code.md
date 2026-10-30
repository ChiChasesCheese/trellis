---
id: tlc-word-ladder-ii-2-code
node: b.word-ladder-ii
type: qa
step: 2
---
## Q
**LC 126 单词接龙 II**｜写出 Python 实现

`beginWord`、`endWord` 和 `wordList`（`1 <= wordList.length <= 500`，单词等长 `1` 到 `5`，只含小写字母，`beginWord != endWord`，`wordList` 互不相同）。返回所有从 `beginWord` 到 `endWord` 的最短转换序列（相邻单词差一个字母，除 `beginWord` 外都在 `wordList` 中），没有则返回 `[]`。

## A
**思路。** 通配符桶找邻居。按层 BFS，`nxt[v]` 收集本层所有能到 `v` 的父亲，整层扫完再把 `nxt` 的键并入 `seen`；到达 `endWord` 的层就停。然后从 `endWord` 用 DFS 沿 `parents` 倒着走到 `beginWord`，每走通一条就把路径反转后加入结果。

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

运行：示例 1 → `[['hit', 'hot', 'lot', 'log', 'cog'], ['hit', 'hot', 'dot', 'dog', 'cog']]`；没有 `cog` → `[]`；`("a", "c", ["a","b","c"])` → `[['a', 'c']]`；`("hot", "dog", ["hot","dog"])` → `[]`；`501` 个单词的长链 → `1` 条路径，不溢出。

**复杂度。** BFS 约 `O(N * L)` 个桶项加扫描；回溯 `O(最短路条数 * 路径长度)`；空间 `O(N * L)` 加输出。

**写法要点。** `defaultdict(list)` 做桶和每层的 `nxt`，读不到的键自动新建空列表；`words | {begin_word}` 把起点也放进桶，保证它与字典词互为邻居；`seen |= nxt.keys()` 把字典的键视图并入集合，一次完成；`parents.update(nxt)` 把本层的父亲表合并进总表；`dfs` 里 `path` 是共享列表，回溯用 `append`/`pop`，记录结果时用 `path[::-1]` 拷贝并反转；`layer = set(nxt)` 让下一层成为集合，去重自动完成。
