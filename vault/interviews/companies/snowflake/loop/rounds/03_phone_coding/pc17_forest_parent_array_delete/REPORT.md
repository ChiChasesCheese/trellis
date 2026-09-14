# pc17 Forest Parent Array Delete Node — report

## Summary
TrueInterview 87 题清单第 4 题（2026-06）："Forest Parent Array Delete Node"。预览未说明被删节点的
孩子怎么处理——这是唯一需要重建的选择点，本 kit 选"孩子变成根"。3-part：Part 1 删单节点 · Part 2 删整棵
子树 **(reconstructed)** · Part 3 批量同时删除，语义上不同于依次调用 Part 1 **(reconstructed)**。

## Sources & confidence
MED（TrueInterview 聚合站预览，题面付费，"孩子怎么办"未给出）；Part 2、Part 3 为重建。

## Approach by part
1. 剩余下标按原顺序重新编号；被删节点的直接孩子在新数组里指向自己（变成根），其余节点的 parent 指针
   只做下标翻译。
2. 先用 children 邻接表从 `delete_index` 做一次 DFS/BFS 找出整棵子树，其余同 Part 1 的重新编号逻辑。
3. 对每个存活节点，沿着**原始** parent 指针向上爬，跳过所有在删除集合里的祖先，遇到第一个存活祖先就是
   新父节点；如果一路爬到原根（`parent[x]==x`）还在删除集合里，该节点自己变成根。用一个 worked example
   （链 `0←1←2←3` 批量删 `{1,2}`）具体说明这与"先删 2 再删 1"的结果不同。

## Pitfalls hidden tests target
- 下标越界（负数、`>= n`）三个 Part 都要 `ValueError`
- Part 3 批量里的重复下标 → `ValueError`
- 单节点森林删空、批量删光整片森林 → 返回 `[]`
- 删除一个有孩子的根 vs 删除叶子
- Part 3 与"依次调用 Part 1"结果不同的那类输入（存在多层都被删的祖先链）

## Complexity & measured cost
Part 1 O(n)；Part 2 O(n)（一次 DFS + 重新编号）；Part 3 每个存活节点最坏 O(祖先链长)，随机森林下均摊很小，
最坏是一条链 O(n)。编排者验证：300 组随机森林（大小 1–14）分别与三套独立写的暴力实现（Part1/2 用显式
children 邻接表模拟删除，Part3 用"完整祖先链 + 找第一个存活者"）0 不一致。perf：20 万节点的子树删除
端到端 < 2 s。

## Test inventory
25 tests — part1 8（含 2 参数化）· part2 6（含 1 参数化）· part3 8（含 1 参数化）· io/fmt 3；
edge 15 · fmt 1 · perf 1 · io 3。

## Skills exercised
S01 森林 / parent 数组编码 · S03 删点后重新编号 · 主动澄清题意未说明的语义分支 · 区分"依次"与"同时"
批量操作的语义。
