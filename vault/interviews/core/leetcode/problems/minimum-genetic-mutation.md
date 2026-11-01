---
slug: minimum-genetic-mutation
---
## Q
**LC 433 最小基因变化**｜Medium

基因序列可以表示为一条由 8 个字符组成的字符串，其中每个字符都是 `'A'`、`'C'`、`'G'`、`'T'` 之一。一次基因变化就是序列中一个字符发生了变化。基因库 `bank` 记录了所有有效的基因变化，只有基因库中的基因才是有效的基因序列（变化后的基因必须位于 `bank` 中）。给你两个基因序列 `start` 和 `end`，以及基因库 `bank`，找出并返回能够使 `start` 变化为 `end` 所需的最少变化次数，无法完成则返回 `-1`。起始序列 `start` 默认是有效的，但不一定出现在基因库中。`start.length == end.length == 8`，`0 <= bank.length <= 10`，`bank[i].length == 8`，所有字符串仅由 `'A'`、`'C'`、`'G'`、`'T'` 组成。例：`start = "AACCGGTT", end = "AACCGGTA", bank = ["AACCGGTA"]` → `1`；`start = "AACCGGTT", end = "AAACGGTA", bank = ["AACCGGTA","AACCGCTA","AAACGGTA"]` → `2`；`start = "AAAAACCC", end = "AACCCCCC", bank = ["AAAACCCC","AAACCCCC","AACCCCCC"]` → `3`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 隐式图上的广度优先搜索（BFS）求最短步数。

**一句话。** 把每个基因序列看作图的节点，改变一个字符且结果在基因库中就连一条边，从 `start` 做 BFS，第一次碰到 `end` 时的层数就是最少变化次数。

**识别。** 「每次只改一个字符，求最少步数」是无权图最短路径，BFS 逐层扩展保证第一次到达的步数最小；节点就是字符串，邻居由「改一个字符」生成，不需要显式建图。

**推导。** DFS / 回溯能找到路径但不保证最短，需要枚举所有路径。BFS 按步数分层，先到者最短。邻居生成：8 个位置 × 另外 3 个字符，共 24 个候选，只有在基因库里的才合法；用集合判断成员 `O(1)`，用 `seen` 避免回头。

```python
def min_mutation(start: str, end: str, bank: list[str]) -> int:
    valid = set(bank)                              # 合法基因，O(1) 判断
    queue = deque([(start, 0)])                    # (当前序列, 已变化次数)
    seen = {start}                                 # start 不必在基因库中，但要防止回头
    while queue:
        gene, steps = queue.popleft()
        if gene == end:
            return steps                           # BFS 第一次到达 end：步数最少
        for i in range(8):
            for c in "ACGT":
                nxt = gene[:i] + c + gene[i + 1:]  # 把第 i 位换成 c
                if nxt in valid and nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + 1))
    return -1
```

运行：示例一 → `1`，示例二 → `2`，示例三 → `3`，`("AAAAAAAA", "AAAAAACC", ["AAAAAACC"])` → `-1`，`("AACCGGTT", "AACCGGTT", [])` → `0`。

**复杂度。** 时间 `O(|bank| * 8 * 4 * 8)`，每个入队的序列生成 32 个候选并各做一次长度 8 的字符串操作；空间 `O(|bank|)`。

**拓展优化。**
- 基因库很大时，从 `start` 和 `end` 同时做双向 BFS，每次扩展较小的一侧，搜索量从 `b^d` 降到约 `2 * b^(d/2)`。
- 基因库很小（这里 `<= 10`）时，也可以直接遍历 `bank`，把「与当前序列恰好相差一个字符」的序列当作邻居，免去 24 个候选的生成。

**易错点。**
- 不要求变化结果在基因库里：`("AAAAAAAA", "AAAAAACC", ["AAAAAACC"])` 会返回 `2`（经过不在库中的 `AAAAAAAC`），正确 `-1`。
- 要求 `start` 也在基因库里：示例一的 `start` 不在 `bank` 中，却是合法的起点。
- 没有 `seen` 集合：序列可以互相变回去，队列会无限增长。
- 先判断 `end not in bank` 再返回 `-1` 会把 `start == end` 的情况（应为 `0`）也判成 `-1`。

**同模式。** LC 127 单词接龙、LC 752 打开转盘锁、LC 126 单词接龙 II、LC 773 滑动谜题。
