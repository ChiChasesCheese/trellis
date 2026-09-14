# pc27 Recipe Sequence Matcher — report

## Summary
Part 1（预处理位置索引找连续子序列）与 Part 2（O(1) 额外空间的双指针重启扫描）是一手原题与原追
问；Part 3（多 recipe 共享前缀用 trie）为 **(reconstructed)**，是多模式字符串匹配场景最常见的
追问方向。

## Sources & confidence
MED（聚合站 TrueInterview 同步清单，题面付费，仅预览的"连续子序列 + O(1) 空间追问"可见）：见
`../../../catalog/raw/github_repos.md` §2/§3。Part 3 为重建。

## Approach by part
1. `token -> [位置]` 哈希索引；对每个 recipe 只检查其首 token 出现的位置，逐一验证后续 token。
2. 严格 O(1) 额外空间：朴素双指针重启扫描，不建任何位置索引或失配表；用 monkeypatch 屏蔽
   `dict`/`set` 验证没有偷懒建结构。
3. 所有 recipe 建一棵 trie，对 `ingredients` 每个起点只走一次 trie，共享前缀天然只比较一次；
   落在同一个终止节点的多个相同 recipe 都会被标记。

## Pitfalls hidden tests target
- 空 recipe 应天然匹配（三个函数一致）
- recipe 比 ingredients 长、recipe 等于整个 ingredients、ingredients 全同一 token（最坏情况
  `O(n*m)` 场景）
- Part 2 偷用 dict/set 代替真正的 O(1) 扫描
- Part 3 多个相同 recipe 落在同一个 trie 终止节点都要标记、共享前缀场景下不重复比较
- 三个函数在 500+ 组随机数据上结果必须完全一致

## Complexity & measured cost
Part 1：预处理 `O(n)`，查询最坏 `O(n*m)`（`m` = recipe 长度）。Part 2：`O(n*m)` 最坏、`O(1)`
辅助空间。Part 3：`O(n * 平均 trie 深度)`，共享前缀被摊还到一次比较。perf：Part 2 在 5 万
token、30 词表随机数据上真实命中一段 30-token 子串，< 2s；Part 3 在 2 万 token、300 个共享前缀
recipe 上 < 2s。

## Test inventory
24 tests — part1 7（含 1 io）· part2 7（含 1 perf、1 io）· part3 6（含 1 perf、1 io/fmt）；
edge 10 · fmt 1 · perf 2 · io 3。

## Skills exercised
S04（字符串/序列匹配：暴力 vs 预处理索引 vs Trie 的取舍）· 对"额外空间"约束的严格遵守（用
monkeypatch 屏蔽内置结构验证）· 多模式匹配共享前缀优化的直觉。
