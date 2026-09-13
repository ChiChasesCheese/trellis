# q10 Wiki Minimum Clicks — report

## 摘要

来源只留下了标题「Minimum Clicks Between Wiki Pages」和标签 Graph/BFS，且这道题同时出现在 OA
和电面池子里（Snowflake 会在两个环节之间复用同一道题）。基础题面（Part1：有向图最短路）是按标题
精确形式化的标准 BFS；Part2（返回实际路径）没有任何 follow-up 报告，是我加的自然延伸——加了明确
的确定性 tie-break 规则（FIFO + 邻居字母序），确保存在多条最短路时候选人和参考实现给出同一条路径。

## 来源与置信度

- https://www.fastprep.io/problems/snowflake-minimum-clicks-between-wiki-pages （Easy，
  Graph/BFS，截至 2026-09 同时被报告在 OA 池和电面池）—— 只恢复到标题/标签，没有逐字题面。
- Part1 基础题面：按标题精确复原，标记为 (reconstructed)。
- Part2 路径重建：完全原创，没有对应的 follow-up 报告，标记为 (reconstructed)。
- 置信度：中。三个 worked example（含 tie-break 追踪）都用独立脚本跑过 part1/part2 验证。

## 逐 part 思路

- **Part1**：`start==target` 直接返回 `0`；否则标准 BFS，队列存 `(node, dist)`，用 `visited`
  集合防止重复入队；每个节点的邻居列表先按字母序排好（虽然对 Part1 的距离结果没有影响，但保留这个
  遍历顺序是为了和 Part2 用同一套建图/遍历代码，也方便以后要求"最短路里字典序最小的那一条"之类的
  扩展）。发现 `target` 时立即返回 `dist+1`，不需要跑完整个 BFS。
- **Part2**：同样的 BFS，但用一个 `parent` 字典记录每个节点第一次被发现时的前驱。关键是**发现
  顺序**——用 FIFO 队列，且当前节点自己的邻居按字母序遍历——这样"谁先把某个节点标记为已访问"是完全
  确定的。一旦发现 `target`，立即清空队列并跳出（后续 BFS 不会再改变 `target` 的父指针，这只是个
  提前终止的优化，不影响正确性）。最后从 `target` 沿 `parent` 反向回溯拼出路径，反转后返回。

## 隐藏测试针对的坑

- **自环 `A->A`**：如果没有 `visited` 检查会导致重复入队甚至死循环；测试直接验证距离/路径正确且
  不受自环影响。
- **死胡同页面**（有入边没有出边）：BFS 到达它之后 `adj.get(node, [])` 必须返回空列表而不是抛
  `KeyError`——用 `defaultdict(list)` + `.get(node, [])` 双保险。
- **只作为边目标、从未作为源出现的页面**：这类节点在邻接表里可能根本没有 key（如果只用普通
  `dict` 遍历边构建，且从未以它为起点添加边），必须确认从它出发查询"它是否有出边"时不会报错。
- **重复边**：`visited` 集合天然去重，不会导致某节点被多次加入 BFS 队列或路径重复。
- **多条等长最短路的确定性**：`test_alphabetical_neighbor_order_tiebreak_is_deterministic`
  故意把边的**输入顺序**打乱（先写 `A->C` 再写 `A->B`），验证 tie-break 依据的是邻居列表本身
  排序后的字母序，而不是边在输入里出现的顺序——这是最容易被想当然实现（比如直接按边输入顺序建邻接
  表且不排序）踩中的坑。
- `main()` 的 blank-line 输出：Part2 不可达时要输出一个空行（`",".join([]) + "\n"` == `"\n"`），
  而不是不输出任何内容或输出 `"None"`。

## 复杂度与实测

BFS：O(V+E) 时间、O(V+E) 空间。perf 测试用 5 万节点的稀疏图（显式一条链 `P0->P1->...->P(n-1)`
保证连通性上界，再叠加 5 万条随机边做噪声/可能的捷径）——这是图类问题，按 REPONT 要求把规模定在
1e4-1e5 区间（而不是通用的 1e5-1e6），因为节点是字符串、邻接表构建和排序本身有额外开销，5 万节点
规模已经足以在 Python 里体现 BFS 的线性复杂度而不会让测试本身变慢；本地实测 5 万节点/约 10 万条边
的 BFS（含 stdin 解析、邻接表排序、路径重建）在 run_script 子进程往返下约 0.3-0.5s，远低于 2s
预算。

## 测试清单

21 个测试 —— part1: 10 个（含 2 个 io、1 个 perf）；part2: 11 个（含 1 个 io、1 个 perf、1 个
fmt）；额外覆盖 edge 9 个（自环、死胡同、重复边、仅作目标节点、不连通分量）。全部针对
`solution.py` 通过；针对 `starter.py`（`IMPL=starter`）确认产生 16 个真实断言失败（并非
collection error），其余 5 个因为 stub 返回 `-1`/`[]` 恰好命中"不可达"类边界期望而"意外通过"。

## 技能 ids

S05（图：BFS 最短路、路径重建、确定性 tie-break（FIFO + 字母序邻居）、有向图边界情况处理）
