# q10 · Wiki Minimum Clicks — 有向图 BFS 最短路 + 路径重建

**Type:** 题目主体是对一个"仅题目标题/标签可查"的条目的复原（**reconstructed**），Part2 是完全
原创的 follow-up（**reconstructed**）· **Stage:** OA + Phone Screen（两个池子都报告过）·
**Last asked:** 截至 2026-09 仍在流通 · **Confidence:** MED

> ⚠️ 基础题面本身就是根据标题/标签复原的（来源只给出了标题「Minimum Clicks Between Wiki Pages」
> 和标签 Graph/BFS，没有逐字题面）；Part2（路径重建）是**完全没有 follow-up 报告**的情况下，我
> 自己加的一个自然延伸，同样标记为 (reconstructed)。

## 背景

维基百科页面之间的超链接天然是一个**有向图**：页面 A 有一个指向页面 B 的链接，不代表 B 也链接回
A。题库里这道题在 OA 和电面池子里都出现过（Snowflake 会在两个环节之间复用同一道题），说明它足够
基础、足够快出题——本质就是"给定有向边表，求两点间最短路"的标准 BFS。

## 输入格式（stdin，`main()`）

```
PART n
E
from,to        (重复 E 行，表示一条有向边 from -> to)
start,target
```

## 规则

### Part 1 — 最短点击数（BFS 最短路）**(reconstructed)**

`part1(edges: list[tuple[str, str]], start: str, target: str) -> int`

维基页面是有向图里的节点——一条边 `A -> B` 表示页面 A 有一个指向页面 B 的超链接（单向，B 不一定
链接回 A）。给定边表、起始页 `start` 和目标页 `target`，求从 `start` 沿链接走到 `target` 所需的
最少点击数（走过的边数）。如果不可达，返回 `-1`。如果 `start == target`，答案是 `0`。

用标准 BFS 求最短路：建邻接表；虽然 Part1 只需要距离、tie-break 并不会影响 Part1 的**输出结果**
（距离是唯一的，不受访问顺序影响），但为了和 Part2 保持一致的实现方式，处理一个节点的邻居时依然
按**字母序**遍历（说明见 Part2 的 tie-break 规则，两个 part 用同一套遍历顺序方便复用/对比代码）。

### Part 2 — 路径重建 **(reconstructed，没有对应的原始 follow-up 报告)**

`part2(edges: list[tuple[str, str]], start: str, target: str) -> list[str]`

带父指针的 BFS，返回从 `start` 到 `target`（含两端）的实际最短路径，形式是页面名列表（例如
`["A","B","D","E"]`）。如果不可达返回 `[]`。如果 `start==target`，返回 `[start]`。

**Tie-break（必须严格照此实现，否则路径对不上样例）**：当 BFS 第一次发现一个新节点时，它是通过
"先到先得"的方式被发现的——用 **FIFO 顺序**处理队列，同时每个节点**自己的**邻居列表按**字母序**
遍历。也就是说：先出队的节点、按字母序遍历它的邻居，谁先把某个未访问节点标记为"已发现"，谁就是
它在最短路径树里的父节点。不要用别的 tie-break（比如按边输入顺序），否则会和下面的样例对不上。

## 样例（已用代码逐一验证，Part1/Part2 必须精确匹配）

```
edges = [("A","B"),("A","C"),("B","D"),("C","D"),("D","E")]
start="A", target="E"
-> part1 = 3
-> part2 = ["A","B","D","E"]
   (追踪：从A做BFS；A的邻居排序后=[B,C]，两个都在距离1被发现，父节点都是A，按顺序先入队B再入队C。
   FIFO先出队B：B的邻居=[D]，D在距离2被发现，父节点=B，入队D。出队C：C的邻居D已访问，跳过。
   出队D：D的邻居=[E]，E在距离3被发现，父节点=D。路径：E<-D<-B<-A 反转 = [A,B,D,E]，长度3条边。)

edges = [("A","B"),("C","D")]
start="A", target="D"
-> part1 = -1
-> part2 = []
   (A 和 D 完全不连通。)

edges = [("A","B"),("A","C"),("B","D"),("C","D"),("D","E")]
start="A", target="A"
-> part1 = 0
-> part2 = ["A"]
```

## 隐藏测试边界清单

- 自环边（`A->A`）：不应该导致死循环或算错距离（BFS 的 visited 集合天然防止重复访问）
- 不连通的图（上面样例2）
- 死胡同页面（有入边但没有出边）——`part1`/`part2` 应该能正常判定它不通往任何地方
- 只作为边的目标、从未作为源出现过的页面（例如 `D` 只在 `["...","D"]` 里出现过，从未出现在
  `["D",...]` 里）——它作为普通节点存在，但 `adj.get(node, [])` 要能正确处理"这个节点没有出边"
  的情况
- 重复边（同一条 `from,to` 出现多次）——不应该影响距离或路径，也不应该导致某节点被重复加入队列
- 大规模稀疏图做 perf（约 1e4-1e5 节点/边，`random.Random(0)` 生成的随机图或类 DAG 结构），确认
  BFS 远低于 2 秒预算
- `main()` 的 stdin 格式：`PART n` 之后一行边数 `E`，再 E 行 `from,to`，最后一行 `start,target`——
  用 `run_script` 做 io 测试

## 变体

- 无向版本（超链接互相抵消方向性，等价于双向边）——只需要在建图时把边加两次（正反各一次）。
- 加权版本（有些"链接"权重更高，比如站内链接 vs 外链）——BFS 换成 Dijkstra。
- 只问是否可达（布尔版本），是 Part1 的退化子集。

## 来源与置信度

- https://www.fastprep.io/problems/snowflake-minimum-clicks-between-wiki-pages （Easy，
  Graph/BFS，截至 2026-09 同时在 OA 池和电面池被报告——即 Snowflake 会在两个环节之间复用同一道
  题）。只恢复到标题和标签，没有逐字题面——基础题面（Part1）按标题精确形式化，Part2（路径重建）
  完全是我加的、没有对应 follow-up 报告的原创延伸，两者都标记为 (reconstructed)。置信度：中。

## 考什么

skills: S05 图：多源/单源 BFS、路径重建、确定性 tie-break（FIFO + 字母序邻居）· 有向图边界情况
（自环、死胡同、不连通、仅作为目标出现的节点）
