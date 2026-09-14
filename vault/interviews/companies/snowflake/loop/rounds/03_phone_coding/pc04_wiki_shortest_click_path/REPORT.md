# pc04 Wiki Shortest Click Path — report

## Summary
Snowflake 电面池里的"Web Crawler Shortest Path Reconstruction"与 OA/电面双池的"Minimum Clicks Between Wiki Pages"是同一族：有向图上从起始页点到目标页的最少点击。本题做成 3-part 递进：Part1 BFS 距离 → Part2 在所有最短路径里取**字典序最小**的那条 → Part3 边是现抓的（`fetch` 可能抛异常），失败页当死路并计数，爬取不中断 **(reconstructed)**。

## Sources & confidence
MED——fastprep "Web Crawler Shortest Path Reconstruction"（Phone Screen，2026-09）与 linkjob 2026-03 两个来源；fastprep "Minimum Clicks Between Wiki Pages" 同时出现在 OA 与电面池（`catalog/raw/coding_oa.md` #29、`coding_phone_onsite.md` #5）。Part2 的字典序要求是本题为"重建路径"加的确定性约束；Part3 的抓取失败语义为重建，题面已标注。

## Approach by part
1. 标准 BFS，`start == end` 返回 0，扩展到 `end` 时立即返回 `d + 1`，不可达 -1。
2. **反向 BFS 求每个节点到终点的距离，再从起点正向走，每步只在"距离恰好减 1"的邻居里选最小名字。** 正向贪心"每步选最小邻居"是错的：它可能选中一个名字更小但离终点更远或到不了终点的邻居，BFS 距离一旦定下就没法回头。反向距离表保证被选中的邻居仍在某条最短路上。
3. 懒加载 BFS：出队时才调用 `fetch`；异常计一次失败并 `continue`；新邻居按名字排序后入队、首次发现即定前驱。**拿不到整张图就没法反向 BFS，所以 Part3 只保证"某一条"确定性的最短路，不保证全局字典序最小**——这是面试里要主动讲出的取舍。

## Pitfalls hidden tests target
- Part2 用正向贪心在"小名字邻居通向死胡同"的图上给出错误路径（专门构造的反例测试）
- `start == end`：Part1 返回 0、Part2 返回 `[start]`、Part3 返回 `([start], 0)`
- 不可达：Part1 -1、Part2 空行、Part3 `-` 加失败数
- Part3 起点本身抓取失败：路径为空、失败数 1
- Part3 失败页之后仍能从其它已发现页面继续找到路径
- 自环与重复边不影响距离与路径
- 输入格式：第一行是**边数**，随后恰好这么多行边，再一行 `start end`

## Complexity & measured cost
三个 part 都是 O(V + E)；Part2 两次遍历加路径长度的邻居筛选，仍是线性。perf 测试在 10⁵ 量级节点上端到端（stdin 解析 + 输出）远低于 2 s。

## Test inventory
37 个标记 · part1 5 · part2 9 · part3 7 · edge 11 · fmt 1 · perf 1 · io 3。

## Fix log
- 2026-09-13（编排者验收）：`test_part2_output_format_exact` 的边数写成 `"3"` 却列了 4 条边，参考解按 3 条读导致把 `C D` 当成起终点；测试改为 `"4"`（与同文件 io 测试一致），解法未改。

## Skills exercised
S05 图 BFS / 路径重建 / 字典序 · S08 在复杂度不变的前提下加强保证（反向距离表）· S10 失败隔离（抓取失败不打断整体流程）
