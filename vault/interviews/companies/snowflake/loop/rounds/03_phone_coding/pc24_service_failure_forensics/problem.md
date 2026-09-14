# pc24 · Service Failure Forensics — 三段式故障排查：二分找日志、传播 BFS、最长链 DAG

> TrueInterview 一手三段提纲；日志格式、图的具体规则与所有细节均超出预览，**(reconstructed)**。

## 背景

TrueInterview 同步的 Snowflake Algo 题单第 24 项，预览只给出三段的骨架：**二分找最早的 ERROR
日志 → BFS/DFS 求所有会级联失败的服务 → DFS 求最长失败传播链**。这是一个把"服务故障排查"包装成
三道独立小题的电面题：先在日志里定位事故起点，再在依赖图上模拟级联，最后回答"这次事故最长牵连了几
层"。

## 输入

- Part 1：`logs: list[str]`，已按时间戳升序排好（相同时间戳保持输入顺序，不额外排序），每行格式
  `"<ts> <service> <LEVEL> <message>"`；`<ts>` 是可字典序比较的字符串（如
  `2026-09-01T00:03:12`）；`<LEVEL> ∈ {INFO, WARN, ERROR}`；`<message>` 可以为空、可以含空格。
  查询一个时间戳 `ts`。
- Part 2：`edges: list[str]`，每条 `"A B"` 表示 **A 依赖 B**（B 挂了 A 就跟着挂）；一个初始失败的
  服务 `initial_failure`。
- Part 3：与 Part 2 相同的 `edges`，不需要额外输入。

## API 契约（英文签名）

```python
def first_error_at_or_after(logs: list[str], ts: str) -> int
def services_that_will_fail(edges: list[str], initial_failure: str) -> list[str]
def longest_failure_chain(edges: list[str]) -> list[str]
```

## 规则

### Part 1 — 二分定位最早的 ERROR（原题骨架）

先用 `bisect_left` 在时间戳上二分，找到"时间戳 >= ts"的第一条日志的位置（`O(log n)` 次比较）；
从那个位置往后线性扫描第一条 `LEVEL == ERROR` 的日志，返回其下标；找不到返回 `-1`。**诚实说明**：
把每行日志的时间戳字段抽出来建索引本身是 `O(n)`（一次性的预处理），真正做二分查找定位"时间戳边界"
是 `O(log n)`；如果同一份日志要被反复查询多次，这个抽取时间戳的预处理只需要做一次就能摊还到所有
查询上——面试里如果被追问"到底是不是 O(log n)"，要能讲清楚这个区别，而不是含糊带过。

### Part 2 — 级联失败的 BFS/DFS（原题骨架）

从 `initial_failure` 出发，沿着"B 挂了 A 跟着挂"的方向做 BFS，返回**包括 `initial_failure`
自己**在内、按 BFS 首次发现顺序排列的所有会失败的服务。`initial_failure` 从未出现在任何
`edges` 里 → `ValueError`。

### Part 3 — 失败传播 DAG 上的最长链，含环处理 **(reconstructed)**

把全部 `edges` 看成一张图（`B → A` 表示"B 失败会传播到 A"），求**最长路径**（不是最长简单环，
是最长的"一条接一条传播下去"的服务序列）。**服务的硬依赖一般不应该成环**（A 依赖 B 依赖 A 是循环
依赖，本身就是一个设计错误）；如果输入的 `edges` 真的构成了环，"最长路径"这个概念本身就没有定义
（可以无限绕环），所以本题**显式检测环并抛 `ValueError`**，而不是静默截断或卡死——这是
"reconstructed"部分里最重要的设计决定，必须在题面里讲清楚，否则候选人会以为要处理"最长简单路径"
这种 NP-hard 问题。

**实现**：Kahn 拓扑排序顺便判环（排出的节点数 < 总节点数就是有环，报告一个在环上的服务名）；再在
拓扑序上做一次"以每个节点结尾的最长路径" DP（类似 DAG 最长路径的标准做法），打平时取**字典序最小
的完整序列**。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**（Part 1，日志）
```python
logs = [
  "2026-09-01T00:00:00 auth INFO started",
  "2026-09-01T00:01:00 auth WARN slow_response",
  "2026-09-01T00:02:00 db ERROR connection_refused",
  "2026-09-01T00:03:00 auth ERROR timeout",
  "2026-09-01T00:04:00 cache INFO ok",
]
first_error_at_or_after(logs, "2026-09-01T00:00:00") -> 2
first_error_at_or_after(logs, "2026-09-01T00:01:30") -> 2   # 跳过 WARN，落在 db ERROR
first_error_at_or_after(logs, "2026-09-01T00:04:30") -> -1  # 查询时间晚于所有日志
```

**例 2**（Part 2，级联失败）
```python
edges = ["auth db", "cache auth", "api auth"]   # auth 依赖 db；cache、api 依赖 auth
services_that_will_fail(edges, "db")   -> ["db", "auth", "cache", "api"]
services_that_will_fail(edges, "auth") -> ["auth", "cache", "api"]   # db 本身没受影响
```

**例 3**（Part 3，最长传播链）
```python
edges = ["auth db", "cache auth", "api auth", "billing api"]
longest_failure_chain(edges) -> ["db", "auth", "api", "billing"]   # 4 层：db→auth→api→billing
```

**例 4**（Part 3，环被显式拒绝）
```python
edges = ["a b", "b c", "c a"]
longest_failure_chain(edges)  # -> ValueError("failure graph has a cycle involving 'a' (not a DAG)")
```

## `main()` 命令流

```
PART 1
N 5
2026-09-01T00:00:00 auth INFO started
2026-09-01T00:01:00 auth WARN slow_response
2026-09-01T00:02:00 db ERROR connection_refused
2026-09-01T00:03:00 auth ERROR timeout
2026-09-01T00:04:00 cache INFO ok
Q 2026-09-01T00:01:30
→ 2

PART 2
N 3
auth db
cache auth
api auth
S db
→ db auth cache api

PART 3
N 4
auth db
cache auth
api auth
billing api
→ db auth api billing
```

有环时 Part 3 输出一行 `CYCLE <service>`（例如 `CYCLE a`）。

## 边界清单

- Part 1：查询时间早于所有日志（从头开始扫）、晚于所有日志（`-1`）、日志里完全没有 ERROR（`-1`）
- Part 1：同一时间戳有多条日志（保持输入顺序，二分定位到该时间戳段的最左边，再往后找 ERROR）
- Part 1：日志行 `LEVEL` 不是 `INFO/WARN/ERROR` → `ValueError`
- Part 2：`initial_failure` 不在任何 `edges` 里 → `ValueError`
- Part 2：菱形依赖（两条路径都能到达同一个服务）只应出现一次，不重复
- Part 2：自依赖 `"a a"`（不应死循环，`seen` 集合天然防止）
- Part 3：空 `edges` → `ValueError`（没有任何服务可言）
- Part 3：单节点、无边（`["a a"]` 自环——同时也是"环"，必须被判环逻辑捕获）
- Part 3：多条并列最长链时取字典序最小的那条
- Part 3：环检测要报出**某一个**在环上的服务名，不要求报出整个环

## 追问

1. **Part 1 如果要支持"任意区间 [t1, t2] 内第一条 ERROR"呢？** 同样先二分定位 `t1`，再线性扫描到
   第一条 `ERROR`，扫描时额外检查时间戳是否超过 `t2`（用 `bisect_left` 定位 `t2` 的上界更快）。
2. **Part 2 BFS 换成 DFS 结果一样吗？** "会失败的服务集合"一样，但发现顺序不同；本题只要求
   BFS 顺序作为确定性输出。
3. **Part 3 为什么不允许环，而是直接报错？** 因为"最长路径"在有环图上无定义（可以绕环任意多
   圈），把它强行定义成"最长简单路径"是 NP-hard；服务依赖出现环本身就是一个更严重的问题（循环依
   赖），报错比返回一个误导性的数字更诚实。
4. **如果两个服务同时是事故的"根因"（多个初始失败点）呢？** Part 2 的 `initial_failure` 目前只
   支持单点；多点版本是从多个起点同时开始 BFS（多源 BFS），`seen` 集合逻辑不变。
5. **最长链要不要按"传播所需时间"加权？** 如果每条边有传播延迟，就是 DAG 上的最长带权路径，DP
   转移把 `+1` 换成 `+weight(b, a)` 即可，拓扑排序判环的部分完全不变。

## 来源与置信度

- **MED**：TrueInterview 同步的 Snowflake Algo 87 题清单第 24 项「Service Failure Forensics」，
  经 `kevin-2023-code/Tech-Interview-Questions`（聚合站，题面付费，仅预览的三段提纲可见），见
  `../../../catalog/raw/github_repos.md` §2 第 24 行、§3 "pc24"。
- 预览只给出"三段：二分找最早 error 日志 → BFS/DFS 求级联失败 → DFS 求最长传播链"这一句提纲；
  日志的具体格式、图的输入格式、环的处理策略、边界情况全部为重建，已标注 **(reconstructed)**。

## 考什么

S02（二分查找的变体：找满足谓词的边界，再线性确认）· S05（有向图 BFS/DFS 传播、DAG 最长路径 DP）
· 环检测与"这个问题在有环时没有良定义"的诚实表达（不是所有图论问题都能推广到有环情形）。
