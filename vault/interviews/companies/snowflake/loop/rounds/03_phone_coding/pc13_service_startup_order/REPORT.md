# pc13 Service Startup / Dependency Ordering — report

## Summary
一手面经提到的"服务启动依赖排序，Kahn 算法"电面题，细节未知，按标准 Kahn 拓扑排序重建 Part 1；Part 2（并行波次）、Part 3（每服务最早启动时间）是同类追问 **(reconstructed)**。

## Sources & confidence
LOW-MED（linkjob.ai 2026-03-16 汇总，仅题目名，因与同来源 Course Schedule II 复用主题一致而不算纯 LOW）；Part 2/3 未见一手报道，按拓扑排序类题目最常见追问重建，Part 3 与 pc09 Parallel Courses III 同构。

## Approach by part
1. Kahn 算法用最小堆维护"依赖已全部启动"的候选集合，每步弹出字典序最小的服务。启动不完时，不只是报告"卡住的节点集合"，而是在卡住的子图里用迭代（显式栈）+ 3 色标记 DFS 找一个真正的环，把"在等环"和"在环上"分开。
2. 复用 Kahn 的层次结构：每一层"当前可启动的服务"就是一个波次，波内排序仅为了输出确定，不代表启动先后。
3. 用最小堆按拓扑序处理节点，`start[s] = max(finish[依赖])`、`finish[s] = start[s] + duration[s]`——与 pc09 的关键路径递推同构，只是图的语义从"课程先修"换成"服务依赖"。

## Pitfalls hidden tests target
- 多个服务同时就绪时的确定性 tie-break（字典序最小）
- 环检测要报出**具体是哪几个服务**，且要排除只是"在等环"的服务（专门构造了一个 5 节点图验证这一点）
- `services` 重复、依赖引用不存在的服务、自依赖 → `ValueError`
- Part 3 的 `duration` 键集合必须与 `services` 完全一致、非负
- 空 `services` 列表三个 part 都要能正常返回，不报错
- 大图（5000 服务、约 1.5 万条依赖）2 秒内完成，验证 Kahn 实现是 O(n+m) 而不是意外的 O(n²)

## Complexity & measured cost
Part 1/2 均 O(n log n + m)（最小堆维护 tie-break）；Part 3 同样是 O(n log n + m)。5000 节点、~1.5 万条边的随机 DAG 实测 Part 1 ~0.004s、Part 2 ~0.004s，远低于 2s 预算。编排者用递归版拓扑序校验（`_valid_topo_order`）和独立的递归环检测（`_has_cycle_brute`）在 150 组随机小图上分别交叉验证拓扑序合法性和环检测的正确性，Part 3 额外用记忆化递归验证每个服务的 `finish` 值，0 不一致。

## Test inventory
26 tests — part1 11（含 2 样例、1 perf、2 io）· part2 5（含 2 样例、1 fmt）· part3 7（含 1 样例、1 io）；edge 15 · fmt 1 · perf 1 · io 3。

## Skills exercised
S05 图：拓扑排序 / Kahn 算法 · 确定性 tie-break 设计 · 环检测的"报出具体成员"而非"是否有环"
