---
id: tlc-word-ladder-ii-5-alt
node: a.word-ladder-ii
type: qa
step: 5
---
## Q
**LC 126 单词接龙 II**｜另一种解法

除了「BFS 记录父亲、DFS 回溯」，还有什么常见解法？什么时候选它？（`1 <= wordList.length <= 500`，单词长度 `1` 到 `5`）

## A
**BFS 求距离，再用距离引导 DFS。** 第一步是普通 BFS，求每个词到 `beginWord` 的最短距离 `dist`；第二步从 `endWord` 做 DFS，只走「`dist` 恰好少一」的边，走到 `beginWord` 就得到一条最短路。

```python
from collections import defaultdict, deque
from collections.abc import Iterator


def find_ladders(begin_word: str, end_word: str, word_list: list[str]) -> list[list[str]]:
    words = set(word_list)
    if end_word not in words:
        return []
    buckets: defaultdict[str, list[str]] = defaultdict(list)
    for w in words | {begin_word}:
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)

    def neighbors(w: str) -> Iterator[str]:
        for i in range(len(w)):
            yield from buckets[w[:i] + "*" + w[i + 1:]]

    dist = {begin_word: 0}                      # 第一步：普通 BFS 求每个词到 begin 的最短距离
    queue = deque([begin_word])
    while queue:
        w = queue.popleft()
        for v in neighbors(w):
            if v not in dist:
                dist[v] = dist[w] + 1
                queue.append(v)
    if end_word not in dist:
        return []

    res: list[list[str]] = []
    path = [end_word]

    def dfs(w: str) -> None:                    # 第二步：从 end 倒着走，只走“距离恰好少 1”的边
        if w == begin_word:
            res.append(path[::-1])
            return
        for v in neighbors(w):
            if dist.get(v, -1) == dist[w] - 1:
                path.append(v)
                dfs(v)
                path.pop()

    dfs(end_word)
    return res
```

示例 1 同样得到两条最短路；`("hit", "cog", ["hot","dot","dog","lot","log"])` → `[]`；由 `a` 到 `d` 组成的全部 `4` 位单词，`aaaa` 到 `dddd` → `24` 条，与主解法一致。

**怎么选。**
- 它不需要显式的 `parents` 表，BFS 部分是最普通的写法，更容易一次写对；DFS 里用距离过滤，也很直观。
- 代价是 BFS 不会在到达终点的那一层停止（上面会遍历整张可达图），DFS 每一步都要重新枚举邻居并查 `dist`，常数略大。
- 面试默认写主解法（按层停止、只存父亲）；当图很小、要求写得快且不易错时，这种两步法同样可以接受；字典很大时两者都应考虑双向 BFS。
