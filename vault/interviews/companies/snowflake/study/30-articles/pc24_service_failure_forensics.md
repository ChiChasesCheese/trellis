# pc24 · Service Failure Forensics：练的是"二分定位边界 + 传播 BFS + 有环图上诚实拒绝"

> [!tldr]
> - 这题考的是：故障排查三连问——二分找最早的 ERROR 日志、BFS 求级联失败的服务、DAG 上求最长失败传播链；一手三段提纲，日志格式/图规则/环处理均 **(reconstructed)**
> - 三步套路：`bisect_left` 定位时间戳边界后线性找 ERROR → 依赖图上从故障点 BFS 收集所有会失败的服务 → 拓扑排序判环，无环时在拓扑序上做最长路径 DP
> - 最值得带走的一个模式：**在有环图上，"最长路径"这种概念本身没有良定义，显式判环并报错，比强行给出一个误导性的数字更诚实**

## 1. 题目在说什么（人话版）

三段独立又串联的小题：先在已排序的日志里用二分找到某个时间点之后第一条 ERROR；再在"A 依赖 B"
的依赖图上，从一个初始故障服务出发，BFS 找出所有会跟着失败的服务；最后在这张失败传播图上找
"最长传播链"——但如果依赖图本身有环，"最长路径"就没有意义，必须显式报错。

小例子：
```
first_error_at_or_after(logs, "2026-09-01T00:01:30") -> 2   # 跳过 WARN，落在 db 的 ERROR
services_that_will_fail(["auth db","cache auth","api auth"], "db")
    -> ["db", "auth", "cache", "api"]
longest_failure_chain(["auth db","cache auth","api auth","billing api"])
    -> ["db", "auth", "api", "billing"]        # 4 层传播链
longest_failure_chain(["a b","b c","c a"])     # -> ValueError（环）
```

## 2. 读题：把文字变成模型

- **实体**：日志行（时间戳、服务、级别）、依赖边（A 依赖 B）、传播图。
- **输入**：Part 1 是排好序的日志 + 查询时间戳；Part 2/3 是 `"A B"` 形式的依赖边。
- **输出**：日志下标 / 会失败的服务列表 / 最长传播链（或环报错）。
- **状态**：Part 1 无状态（一次二分+扫描）；Part 2 是 BFS 的 `seen` 集合；Part 3 是拓扑排序的
  入度表和"以每个节点结尾的最长链"DP 表。
- **一句话建模**：这是一个 **"三个独立小算法串成一次故障排查叙事"** 的题——二分查边界、图上
  传播、DAG 最长路径，考点各自独立。

> [!note] 为什么 Part 3 要显式拒绝环，而不是"最长简单路径"
> 服务的硬依赖不应该成环（循环依赖本身就是设计错误）。如果图真的有环，"最长路径"可以无限绕圈，
> 概念上未定义；强行改成"最长简单路径"又是 NP-hard。所以本题选择显式检测环并报错，而不是静默
> 截断或卡死。

## 3. 下笔顺序

1. **问清**：日志是否已经按时间戳排好序？依赖方向是"A 依赖 B"还是"B 依赖 A"？
2. **Part 1 最小可用**：`bisect_left` 在时间戳数组上定位第一条"时间戳 >= ts"的日志，再线性扫描
   到第一条 `ERROR`；找不到返回 `-1`。
3. **Part 2 叠加**：建 `B -> [A, ...]`（B 失败传播到 A）的邻接表，从初始故障点 BFS，`seen`
   集合去重防止菱形依赖重复计数、自依赖死循环。
4. **Part 3 叠加**：Kahn 拓扑排序顺便判环（排出节点数 < 总数即有环）；无环时在拓扑序上做
   "以每个节点结尾的最长路径"DP，打平取字典序最小的完整序列。
5. **收尾**：日志同一时间戳多条要保持输入顺序；`initial_failure` 不存在报错；空依赖图报错；
   自环（`"a a"`）同时也是环，必须被判环逻辑捕获。

## 4. 代码怎么组织

```
_parse_line(line) -> (ts, service, level, msg)   # Part 1 的日志解析
first_error_at_or_after(logs, ts)                # Part 1：bisect + 线性扫描
_parse_edges(edges) -> {B: [A, ...]}              # Part 2/3 共用的图构建
services_that_will_fail(edges, initial_failure)  # Part 2：BFS
longest_failure_chain(edges)                     # Part 3：拓扑排序判环 + 最长路径 DP
```
Part 2、Part 3 共用 `_parse_edges`；三段互相独立，唯一的耦合是"依赖图的构建方式"。

## 5. 核心代码（骨架）

```python
def first_error_at_or_after(logs, ts):
    timestamps = [line.split(" ", 3)[0] for line in logs]
    start = bisect.bisect_left(timestamps, ts)
    for i in range(start, len(logs)):
        if logs[i].split(" ", 3)[2] == "ERROR":
            return i
    return -1

def services_that_will_fail(edges, initial_failure):
    graph = _parse_edges(edges)
    seen, order, i = {initial_failure}, [initial_failure], 0
    while i < len(order):
        cur = order[i]; i += 1
        for nxt in graph.get(cur, []):
            if nxt not in seen:
                seen.add(nxt); order.append(nxt)
    return order

def longest_failure_chain(edges):
    graph = _parse_edges(edges)
    nodes = sorted(graph)
    indeg = {n: 0 for n in nodes}
    for b in nodes:
        for a in graph[b]: indeg[a] += 1
    heap = sorted(n for n in nodes if indeg[n] == 0)
    order = []
    while heap:
        n = heapq.heappop(heap); order.append(n)
        for a in graph[n]:
            indeg[a] -= 1
            if indeg[a] == 0: heapq.heappush(heap, a)
    if len(order) != len(nodes):
        raise ValueError("failure graph has a cycle (not a DAG)")
    best = {n: [n] for n in nodes}          # 以 n 结尾的最长（同长取字典序最小）链
    for b in order:
        for a in graph[b]:
            cand = best[b] + [a]
            if (-len(cand), cand) < (-len(best[a]), best[a]):
                best[a] = cand
    return min(best.values(), key=lambda c: (-len(c), c))
```

## 6. 面试里怎么说

- 开始前：「日志已经按时间戳排好序了吗？相同时间戳的多条日志顺序要保留吗？」
- 写 Part 1 时：「先二分定位时间戳边界是 `O(log n)`，从那里往后线性扫第一条 ERROR；如果同一份
  日志要反复查询，抽取时间戳数组这个预处理只需要做一次。」
- 到 Part 3 时：「服务依赖一般不应该成环，如果真的有环，'最长路径'这个概念本身没有定义——我用
  Kahn 拓扑排序顺便判环，有环就直接报错并指出环上的一个服务，而不是静默截断或死循环。」
- 交付时：「样例过了；多条并列最长链时我取字典序最小的那条，保证输出确定。」

## 7. 常见跑偏

- Part 2 用"已报告节点集合"做重复检查却忘了处理自依赖 `"a a"`，导致死循环。
- Part 3 没有判环就直接跑最长路径 DP，遇到环会无限递归或给出一个看似合理但完全错误的数字。
- Part 1 把"二分定位边界"和"线性找 ERROR"合并成一次线性扫描，失去了二分的复杂度优势，也丢了
  "定位满足谓词的边界，再线性确认"这个可迁移的模式。

## 8. 同族题 / 延伸

- 与 `pc21`（Accumulator Interpreter 的调用链防环）同样考"隐式有向图上的环检测"，但 pc21 用
  调用链集合判环，pc24 用拓扑排序判环。
- 与 `q08`（Course Schedule II）同属拓扑排序考法，但 q08 只要一个合法顺序，pc24 还要在拓扑序上
  做最长路径 DP。
- 练习命令：`python3 loop/mock.py start pc24`
