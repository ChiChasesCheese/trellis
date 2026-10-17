# 数岛屿 II 与逐行流式输入（Number of Islands II and row-streaming）

> 来源：1p3a 1191823（NG onsite，2026-10-03）https://www.1point3acres.com/bbs/thread-1191823-1-1.html ；1p3a 题库条目 `number-of-islands-max-area-streaming`（3 个来源，最近 2026-10-03）；LC 305 题面镜像 https://leetcode.ca/all/305.html （官方页为付费题，常数范围未取到，下文标 **(reconstructed)**）。
> 相关：已有 Anki 卡 `streaming-island-count`（只讲逐行流式）；本讲把它和 305 连起来。代码：`../../coding/solutions/305_number_of_islands_ii.py`、`code/amz_streaming_islands.py`。

## 面经原话
- 回帖里面试官的追问：「follow up1:如果矩阵是流式一行一行进来的怎么办 union find嘛？」（1p3a 1191823 r2）。帖子正文被积分墙挡住，主问题是 LC 200 一类的数岛屿，这个追问把它推到并查集。
- LC 305 本身：「A 2d grid map of m rows and n columns is initially filled with water」，每次 `addLand` 后报告岛屿数；镜像页给出 follow-up「O(k log mn)」。数据范围 **(reconstructed)**：面经和镜像都没有给，按 m*n 可以大到不能每次重扫来处理。

## 开场先问的澄清问题
1. 岛屿是四连通还是八连通？（默认四连通。）
2. 同一个格子被重复 `addLand` 怎么办？（岛屿数不变。）
3. 流式版本：一行读完才能看下一行，还是一次一个格子？内存允许多大——能存整张图吗？
4. 要的是岛屿数，还是还要最大面积？

## 先补一点基础：并查集（Union-Find）
- **是什么**：把元素分成若干「集合」，支持 `find(x)`（x 在哪个集合，用一个代表元表示）和 `union(a, b)`（合并两个集合）。
- **为什么需要**：「两块陆地是不是同一个岛」本质是「它们是不是同一个集合」。用 BFS 每次重新数要 O(mn)；并查集每次只处理新格子的 4 个邻居。
- **怎么工作**：每个元素存一个 `parent`；代表元的 parent 是自己。`find` 沿 parent 往上走到代表元；路径压缩（path compression）让以后更短；按大小合并（union by size）让树矮。均摊 O(α(n))，α 是反阿克曼函数，可视为常数。

## 最笨解
每次 `addLand` 之后，对整张图做一遍 DFS 数岛屿。k 次操作 × O(mn) = O(k·m·n)。输入 m*n 很大、k 很大时直接超时——例如 1 万次操作 × 100 万格。

## 逐步改进
1. **问题**：重复劳动。新加一格陆地只会影响它自己和 4 个邻居所在的岛。
2. **想法**：新格子先当作「新岛」（岛数 +1）；对每个已是陆地的邻居，若两者代表元不同就合并，每成功合并一次岛数 −1。
3. **为什么对**：新格子最多把 4 个互不相连的岛连成一个，增量恰好是 1 − (成功合并次数)。
4. **稀疏存储**：`parent` 用字典，只存陆地格子，内存 O(k) 而不是 O(mn)。重复添加直接返回当前岛数。

### 最终代码（LC 305）
```python
def num_islands_ii(m, n, positions):
    parent = {}                                       # only land cells exist in the structure (sparse, O(#adds) memory)
    size = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    islands, answer = 0, []
    for r, c in positions:
        cell = (r, c)
        if cell in parent:                            # duplicate addLand: nothing changes
            answer.append(islands)
            continue
        parent[cell], size[cell] = cell, 1
        islands += 1                                  # a brand-new island ...
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb = (r + dr, c + dc)
            if nb in parent:
                ra, rb = find(cell), find(nb)
                if ra != rb:                          # ... which every successful merge reduces by one
                    if size[ra] < size[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    size[ra] += size[rb]
                    islands -= 1
        answer.append(islands)
    return answer
```

复杂度：k 为操作数，每次 O(4·α) ，总 O(k·α(k))；内存 O(k)。

## 逐行流式：从 305 到 streaming
305 是「格子一个个变成陆地」，流式是「一行行把整行给你，而且你存不下整张图」。共同点：都是 **只往一个方向增长** 的输入，所以并查集合适。不同点：流式可以丢弃信息。

- 只需要上一行每个格子的标签（label）：新一行的格子只会和「正上方」「正左方」连通。
- 一个连通块一旦不再出现在最新一行里，它永远不会再长大——可以结算（islands += 1，最大面积取 max）并从并查集里删掉。
- 因此内存 O(n)（n 是行宽），与行数无关。

```python
class StreamIslands:
    def __init__(self, width):
        self.n = width
        self.prev = [0] * width                           # label of each cell in the previous row (0 = water)
        self.parent, self.area = {}, {}                   # only components still touching the previous row live here
        self.next_id = 1
        self.closed = 0                                   # islands that can no longer grow
        self.max_area = 0

    def _find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def feed(self, row):
        cur = [0] * self.n
        for c, cell in enumerate(row):
            if not cell:
                continue
            cur[c] = self.next_id
            self.parent[self.next_id], self.area[self.next_id] = self.next_id, 1
            self.next_id += 1
            for other in (self.prev[c], cur[c - 1] if c else 0):   # neighbour above, neighbour on the left
                if other:
                    a, b = self._find(cur[c]), self._find(other)
                    if a != b:
                        self.parent[a] = b
                        self.area[b] += self.area.pop(a)
        alive = {self._find(x) for x in cur if x}
        for root in [r for r in self.area if r not in alive]:     # touches no cell of this row: finished
            self.closed += 1
            self.max_area = max(self.max_area, self.area.pop(root))
        self.parent = {x: self._find(x) for x in cur if x}        # forget old ids, keep this row's roots
        for root in alive:
            self.parent[root] = root
        self.prev = cur

    def result(self):                                     # (islands, largest area) of everything fed so far
        live = list(self.area.values())
        return self.closed + len(live), max([self.max_area] + live)
```

示例：行 `[1,1,0,0,1] [0,1,0,1,1] [0,0,0,0,0] [1,0,1,1,0]` 读完得到 (4 个岛, 最大面积 3)；U 形 `[1,0,1] [1,0,1] [1,1,1]` 的两条臂直到最后一行才合并，结果 (1 个岛, 面积 7)——这是为什么「被合并的老标签」不能提前结算。

## senior 追问
1. **输入是一列一列来**：把「行」换成「列」，代码不变；如果行宽远大于行数，转置能把内存从 O(宽) 降到 O(高)。
2. **要支持「删除陆地」**：并查集不支持拆分。改成离线：知道全部操作的时间线后倒着做（把删除变成添加），或用 offline dynamic connectivity（线段树分治）。
3. **多线程/分片**：矩阵按行带切成 p 份，每份独立数，再在分界线上合并——只需要把相邻两份的边界行标签做一次并查集合并。
4. **要最大面积、每个岛的外接矩形**：在代表元上多存 `area`、`min/max` 坐标，合并时累加（本讲代码已存面积）。
5. **八连通**：邻居从 4 个变成 8 个（流式时是左上、上、右上、左），其余不变。
6. **内存仍然不够（行宽也巨大）**：按列块切，边界处合并，和第 3 条同构。

## 自测题
1. 为什么新格子要先令岛数 +1 再合并，而不是先看邻居再决定？
<details><summary>答案</summary>每次成功合并减 1 的规则对 0~4 个邻居统一成立；先看邻居要分情况讨论（0、1、2、3、4 个不同岛）。</details>
2. 重复 `addLand(0,0)` 两次，答案分别是什么？
<details><summary>答案</summary>`[1, 1]`：第二次因为已在 `parent` 中直接返回当前岛数。</details>
3. 流式版本里，为什么「一个标签不在最新一行」就可以结算？
<details><summary>答案</summary>后续行只能通过最新一行的格子接触到它；最新一行没有它的任何格子，就永远不会再连上。</details>
4. U 形输入为什么会让「提前结算」出错？
<details><summary>答案</summary>左右两条臂在中间几行互不相连，各自看起来像独立的岛，只有最后一行才把它们连起来；所以只能在「真的不在最新一行」时结算，不能在「暂时没连上」时结算。</details>
