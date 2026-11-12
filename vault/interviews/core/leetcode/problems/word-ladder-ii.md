---
slug: word-ladder-ii
---
## Q
**LC 126 单词接龙 II**｜Hard

每次改一个字母，且中间词都在 `wordList` 中，找出从 `beginWord` 到 `endWord` 的所有最短转换序列，没有返回 `[]`。

## A
**一句话。** 按层 BFS 记每个词在最短路上的全部父亲，到终点层即停，再从终点沿父亲回溯出所有路径。

```python
def find_ladders(begin, end, word_list):
    words = set(word_list)
    if end not in words:
        return []
    buckets = defaultdict(list)     # "h*t" -> 只差通配位的词
    for w in words | {begin}:
        for i in range(len(w)):
            buckets[w[:i] + "*" + w[i+1:]].append(w)
    parents, seen, layer = {}, {begin}, {begin}
    while layer and end not in layer:
        nxt = defaultdict(list)
        for w in layer:
            for i in range(len(w)):
                for v in buckets[w[:i] + "*" + w[i+1:]]:
                    if v not in seen:   # seen 只含更早的层
                        nxt[v].append(w)
        seen |= nxt.keys()      # 整层扫完再标记
        parents.update(nxt)
        layer = set(nxt)
    if end not in layer:
        return []
    res, path = [], [end]

    def dfs(w):                 # 沿父亲链倒走回 begin
        if w == begin:
            res.append(path[::-1])
            return
        for p in parents[w]:
            path.append(p)
            dfs(p)
            path.pop()

    dfs(end)
    return res
```

**复杂度。** 时间 `O(N·L)` 建桶与 BFS，加输出规模的回溯；空间 `O(N·L)`。

**易错点。**
- 发现邻居就立刻进 `seen`：同层第二个父亲被挡掉，`cog` 的父亲 `dog`、`log` 只剩一个，少一条路径。
- `end` 不在字典：必须先返回 `[]`，否则 BFS 到不了终点。
- 到终点层后继续扩展：白做功，循环条件里加 `end not in layer`。

**追问。**
- 怎么加速？：双向 BFS，每次扩展较小的一侧，在相遇层停止。
- 只数最短路条数呢？：在父亲表上记忆化 `count[w] = sum(count[p] ...)`，不展开路径。

**同模式。** LC 127 单词接龙、LC 433 最小基因变化、LC 752 打开转盘锁、LC 773 滑动谜题
