# pc13 · Service Startup Order：练的是"环检测要指名道姓，不能只说有环"

> [!tldr]
> - 一手面经提到"服务启动依赖排序，Kahn 算法"（2026-03 报告，LOW-MED）；**Part 2（并行波次）、Part 3（最早启动时间）均为 (reconstructed)**
> - 这题考的是：Kahn 拓扑排序 + 字典序 tie-break，以及"环检测要报出具体是哪几个服务，不是所有卡住的节点"
> - 三步套路：Kahn 算法用最小堆维护"已就绪"集合 → 卡住时在子图里找真正的环（而不是报告整个卡住集合）→ 叠加并行波次/关键路径两个追问
> - 最值得带走的一个模式：**拓扑排序卡住时，"还没启动的服务"里有些只是在等一个环、自己并不在环上——报错要指名道姓找出真正互相依赖的那一圈，而不是把所有卡住的都算成"有问题"**

## 1. 题目在说什么（人话版）

给一批服务和它们的依赖关系（`(service, dependency)` 表示 `service` 依赖 `dependency`），
求一个满足依赖的启动顺序；多个服务同时就绪时按字典序最小的先启动；如果有循环依赖，
报出环上具体是哪几个服务。

```
services=["db","cache","api","auth"]
deps=[("api","db"),("api","cache"),("cache","db"),("auth","db")]
# db 启动后，auth 和 cache 同时就绪 -> 字典序 auth < cache，先启动 auth
-> ["db", "auth", "cache", "api"]
```

## 2. 读题：把文字变成模型

- **实体**：服务节点、依赖边（有向）。
- **状态**：每个服务的"剩余未满足依赖数"（入度），一个"当前已就绪"的候选集合。
- **一句话建模**：这是标准的 **Kahn 拓扑排序**，加上"就绪集合里选字典序最小"的确定性 tie-break，以及"卡住时报出真正的环"的错误处理。

> [!note] 为什么环检测不能只报告"卡住的节点集合"
> Kahn 算法跑完后，如果还有服务没被处理，说明存在环。但"卡住的节点集合"里，有些节点
> 只是依赖链末端连到了环上（比如 `e` 依赖 `d`，而 `d` 在一个环里，`e` 自己不在环上）。
> 只报告整个卡住集合会误导排查人员去检查不相关的服务；必须在卡住的子图里用 DFS 找出
> 一个真正互相依赖的环。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：建图（`requires`/`enables`），算每个服务的入度，把入度为 0 的放进一个最小堆。
2. **Part 1 最小可用**：每次弹出堆顶（字典序最小）、加入结果、给它的后继减入度，入度归零就入堆；结尾判断是否所有服务都被处理。
3. **加环检测**：没处理完时，在剩下的"卡住集合"子图上做一次迭代（显式栈）DFS，用 3 色标记找一个真正的环。
4. **Part 2/3 叠加**：Part 2 把"逐个弹堆顶"换成"按层处理整批就绪节点"（波次）；Part 3 在处理每个节点时顺便算 `start[s] = max(finish[依赖])`、`finish[s] = start[s] + duration[s]`。

## 4. 代码怎么组织

```
class CycleError(ValueError): cycle: list[str]
_validate(services, deps)
_build(services, deps) -> (requires, enables)
_find_one_cycle(services, requires, stuck) -> list[str]   # 卡住子图里的真实环
startup_order(services, deps)                              # Part 1：Kahn + 最小堆
startup_waves(services, deps)                               # Part 2：按层分波次
startup_times(services, deps, duration)                     # Part 3：关键路径递推
part1 / part2 / part3
```
`_find_one_cycle` 被三个 part 共享；三个 part 的主循环结构几乎一样（Kahn 算法的三种
读法：顺序、分层、带时间戳），差异集中在"弹出一个节点后要多做什么"。

## 5. 核心代码骨架

```python
import heapq

def startup_order(services, deps):
    # Part 1：Kahn 算法，字典序最小优先
    requires, enables = _build(services, deps)
    indeg = {s: len(requires[s]) for s in services}
    heap = sorted(s for s in services if indeg[s] == 0)
    heapq.heapify(heap)
    order = []
    while heap:
        node = heapq.heappop(heap)
        order.append(node)
        for nxt in enables[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    if len(order) != len(services):
        stuck = set(services) - set(order)
        raise CycleError(_find_one_cycle(services, requires, stuck))  # 找真正的环，不是整个 stuck
    return order

def startup_times(services, deps, duration):
    # Part 3：关键路径递推，start[s] = max(finish[依赖])，与 pc09 同构
    requires, enables = _build(services, deps)
    indeg = {s: len(requires[s]) for s in services}
    start, finish = {}, {}
    heap = sorted(s for s in services if indeg[s] == 0)
    heapq.heapify(heap)
    while heap:
        node = heapq.heappop(heap)
        start[node] = max((finish[d] for d in requires[node]), default=0)
        finish[node] = start[node] + duration[node]
        for nxt in enables[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    if len(start) != len(services):
        raise CycleError(_find_one_cycle(services, requires, set(services) - set(start)))
    return start, max(finish.values(), default=0)
```

## 6. 面试里怎么说（边写边讲）

- 开始前：「多个服务同时就绪时我按字典序最小优先，保证输出确定；有环的话我会报出具体是哪几个服务，而不是笼统说'有环'。」
- 写 Part 1 时：「用最小堆维护就绪集合是 `O(n log n + m)`。」
- 引出环检测时：「Kahn 跑完后剩下的节点不全是环的一部分，有些只是在等环，我会在剩下的子图里用 DFS 找一个真正互相依赖的环。」

## 7. 常见跑偏（方法层面，3 条）

- 用普通队列而不是最小堆，导致多个服务同时就绪时顺序不确定。
- 有环时直接把"Kahn 剩下的所有节点"当成环报出去，没有区分"在环上"和"在等环"。
- Part 3 忘了处理"没有任何依赖时 `start` 全为 0，`overall` 是最长单个服务耗时"这个退化情况。

## 8. 同族题 / 延伸

- Part 3 的关键路径递推与 `pc09` Parallel Courses III 同构（把"课程"换成"服务"）。
- 练习命令：`python3 loop/mock.py start pc13`

## 索引行

| [pc13_service_startup_order](pc13_service_startup_order.md) | `../../loop/rounds/03_phone_coding/pc13_service_startup_order/` | 电面 coding | 拓扑排序卡住时，"还没启动的服务"里有些只是在等一个环、自己并不在环上——报错要指名道姓找出真正互相依赖的那一圈，而不是把所有卡住的都算成"有问题" |
