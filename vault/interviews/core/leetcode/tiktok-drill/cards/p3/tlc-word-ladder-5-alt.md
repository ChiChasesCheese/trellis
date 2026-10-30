---
id: tlc-word-ladder-5-alt
node: p3.word-ladder
type: qa
step: 5
---
## Q
**LC 127 单词接龙**｜另一种解法

单向 BFS 在分支多、距离远时搜索量很大。有没有更快的做法？什么时候选哪一种？

## A
**双向 BFS。** 从 `begin_word` 和 `end_word` 同时向中间搜索，每轮扩展较小的一侧；一旦扩展出的候选落在另一侧的集合里，就相遇了。若平均每个单词有 `b` 个邻居、最短距离为 `d`，单向 BFS 访问约 `b^d` 个单词，双向只访问约 `2·b^(d/2)` 个。

```python
def ladder_length_bidirectional(begin_word: str, end_word: str, word_list: list[str]) -> int:
    words = set(word_list)
    if end_word not in words:
        return 0
    words.discard(begin_word)
    words.discard(end_word)
    front, back = {begin_word}, {end_word}    # 从两端同时搜索
    steps = 1
    while front and back:
        if len(front) > len(back):            # 永远扩展较小的一侧
            front, back = back, front
        nxt: set[str] = set()
        for word in front:
            for i in range(len(word)):
                for ch in string.ascii_lowercase:
                    cand = word[:i] + ch + word[i + 1:]
                    if cand in back:          # 两侧相遇
                        return steps + 1
                    if cand in words:
                        words.remove(cand)
                        nxt.add(cand)
        front = nxt
        steps += 1
    return 0
```

要点：`steps` 起始为 `1`；每轮扩展后加一；在候选落入 `back` 时返回 `steps + 1`；`begin_word` 与 `end_word` 都从 `words` 里去掉，避免被当作普通邻居再加入；`front` 与 `back` 交换后含义互换，但两侧是对称的，所以答案不变。

**怎么选。** 面试里先写单向 BFS（20 行，容易写对、容易讲清），然后在被追问「还能更快吗」时说出双向 BFS 并写出这段；当字典较小或最短距离很短（`d ≤ 3`）时，差别不大。在 `N = 5000`、`L = 10` 的上限，两者都在秒级内完成。**通配符桶**是第三种做法：把邻居发现从 `26L` 次拼接降到 `L` 次桶查询，适合字典固定、查询很多的场景。
