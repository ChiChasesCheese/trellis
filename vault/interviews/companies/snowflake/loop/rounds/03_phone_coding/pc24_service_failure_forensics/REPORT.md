# pc24 Service Failure Forensics — report

## Summary
TrueInterview 87 题清单第 24 项一手三段提纲（二分找最早 error 日志 → BFS/DFS 求级联失败 →
最长传播链）。日志格式、图输入格式、环处理策略均超出预览，**(reconstructed)**。核心设计决定：
Part 3 的"最长路径"在图有环时无定义，显式判环报错而不是静默处理。

## Sources & confidence
MED（聚合站 TrueInterview 同步清单，题面付费，仅预览三段提纲可见）：见
`../../../catalog/raw/github_repos.md` §2/§3。日志格式、图规则、环处理均为重建。

## Approach by part
1. `bisect_left` 在时间戳数组上二分定位"时间戳 >= ts"的第一条日志，再线性扫描到第一条 ERROR；
   诚实说明抽取时间戳数组本身是 O(n) 预处理，真正的二分是 O(log n)。
2. 依赖图建成 `B -> [A, ...]`（B 失败传播到 A），从初始失败点做 BFS，`seen` 集合去重防止菱形依赖
   重复访问、自依赖死循环。
3. Kahn 拓扑排序顺便判环；若排出的节点数少于总节点数即为有环，报出一个环上服务名并 `ValueError`。
   无环时在拓扑序上做"以每个节点结尾的最长路径"DP，打平取字典序最小的完整序列。

## Pitfalls hidden tests target
- Part 1：同一时间戳多条日志、查询时间早于/晚于全部日志、日志里没有任何 ERROR
- Part 2：菱形依赖重复计数、自依赖导致死循环、`initial_failure` 不存在
- Part 3：环没有被检测（会导致无限递归或返回误导性结果）、自环也是一种环、空图、多条并列最长链的
  打平规则
- 三段共用的日志/图解析对格式错误（非法 LEVEL、字段数不对）要抛 `ValueError`

## Complexity & measured cost
Part 1：`O(n)` 抽取时间戳 + `O(log n)` 二分 + `O(k)` 前向扫描（k = 边界到第一个 ERROR 之间的行
数）。Part 2：`O(V+E)` BFS。Part 3：`O(V+E)` 拓扑排序 + DP，但保留完整链做 tie-break 让最坏情况
退化到 `O(V^2)`（每个节点存一条最长为 V 的链）——测试规模下可忽略。perf：20 万行日志端到端
< 2s。

## Test inventory
21 tests — part1 8（含 1 perf、1 io）· part2 6（含 1 io）· part3 8（含 2 io）；
edge 11 · fmt 2 · perf 1 · io 4。

## Skills exercised
S02（二分查找变体：定位满足谓词的边界）· S05（有向图 BFS 传播 + DAG 最长路径 DP + 拓扑排序判环）
· 对"这个问题在有环时没有良定义"的诚实表达，而不是不假思索地推广到有环图。
