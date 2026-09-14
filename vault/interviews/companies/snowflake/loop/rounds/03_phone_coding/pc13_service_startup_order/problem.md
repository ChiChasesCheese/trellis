# pc13 · 服务启动顺序（Kahn 拓扑排序）— 环检测要指名道姓

> 电面题。Part 1 是一手报道的原题（"服务启动依赖排序，用 Kahn 算法"）；Part 2（并行启动波次）、Part 3（每个服务的最早启动时间）是拓扑排序类题最常见的两个追问，**(reconstructed)**。

## 背景

一份 2026-03 的面经汇总明确提到 Snowflake 电面例题："服务启动 / 依赖排序（Kahn 算法）"，与同一来源确认过的 Course Schedule II 复用主题一致（服务启动 ≈ 课程先修）。原帖没有给出具体题面细节，Part 1 按 Kahn 算法的标准形态重建。

真正的坑不是"会不会写 BFS 拓扑排序"，而是：**多个服务同时满足启动条件时，顺序必须确定**（本题定成"字典序最小优先"）；**有环时不能只说"有环"，要报出具体是哪几个服务困在环里**——而且要把"困在环里"和"在等一个环"这两种情况分清楚（等环的服务不算环的一部分）。

## 输入

- `services: list[str]`：服务名列表，不重复。
- `deps: list[tuple[str, str]]`：每项 `(service, dependency)` 表示 `service` 依赖 `dependency`（`dependency` 必须先启动）。
- 依赖引用了不存在的服务、服务依赖自己、`services` 有重复 → 抛 `ValueError`。

## API 契约（英文签名）

```python
class CycleError(ValueError):
    cycle: list[str]   # 环上的服务，按依赖顺序：cycle[i] 依赖 cycle[i+1]，cycle[-1] 依赖 cycle[0]

def startup_order(services: list[str], deps: list[tuple[str, str]]) -> list[str]
def startup_waves(services: list[str], deps: list[tuple[str, str]]) -> list[list[str]]
def startup_times(
    services: list[str], deps: list[tuple[str, str]], duration: dict[str, int]
) -> tuple[dict[str, int], int]
```

## 规则

### Part 1 — Kahn 拓扑排序，字典序最小优先

用 Kahn 算法：每一步从"依赖已全部启动"的候选集合里取**字典序最小**的服务名启动。如果启动不完所有服务（说明有环），**不是简单报错，而是抛 `CycleError`，`.cycle` 属性给出环上的服务列表**（用 3 色标记的 DFS 在"卡住的服务"子图里找一个真正的环，不是把所有卡住的服务都当成环——有些服务只是在等一个环，自己并不在环上）。

### Part 2 — 并行启动波次 **(reconstructed)**

把服务分成若干"波次"：第 1 波是所有无依赖的服务；第 `i+1` 波是"依赖全部在前 `i` 波里启动过"的服务。同一波内的服务可以同时启动，波内按字典序排列（顺序不影响并行语义，只是为了输出确定）。有环时同样抛 `CycleError`。

### Part 3 — 每个服务的最早启动时间 **(reconstructed)**

额外给出 `duration: dict[str, int]`（每个服务自身的启动耗时，`services` 里每个名字都要有对应值，非负）。返回 `(每个服务的最早启动时刻, 全部服务就绪的时刻)`：
```
start[s]  = max(finish[d] for d in s 的直接依赖, 默认 0)
finish[s] = start[s] + duration[s]
overall   = max(finish[s] for s in services)
```
这与 pc09 Parallel Courses III 的关键路径递推是同一个套路，只是把"课程"换成了"服务"。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**（简单依赖图，字典序 tie-break 起作用）
```
services = ["db", "cache", "api", "auth"]
deps = [("api","db"), ("api","cache"), ("cache","db"), ("auth","db")]
# db 启动后，auth 和 cache 同时就绪 -> 字典序 auth < cache，先启动 auth
startup_order  -> ["db", "auth", "cache", "api"]
startup_waves  -> [["db"], ["auth", "cache"], ["api"]]
```

**例 2**（环检测报出具体是哪几个服务）
```
services = ["a", "b", "c"]
deps = [("a","b"), ("b","c"), ("c","a")]
startup_order -> 抛 CycleError, .cycle == ["a", "b", "c"]
```

**例 3**（无依赖时全部并列，按字典序输出）
```
services = ["zeta", "alpha", "beta"]
deps = []
startup_order -> ["alpha", "beta", "zeta"]
startup_waves -> [["alpha", "beta", "zeta"]]
```

**例 4**（每个服务的最早启动时间；cache 必须等 db 完全启动完才能开始）
```
services = ["db", "cache", "api"]
deps = [("api","db"), ("api","cache"), ("cache","db")]
duration = {"db": 5, "cache": 3, "api": 2}
startup_times -> ({"db": 0, "cache": 5, "api": 8}, 10)
# db: 0~5；cache 等 db 完（5）才能开始，5~8；api 等 db(5) 和 cache(8) 都完，8~10
```

**例 5**（环里的服务和"在等环"的服务要分清）
```
services = ["a", "b", "c", "d", "e"]
deps = [("b","c"), ("c","d"), ("d","b"), ("e","d")]
# b-c-d 三个互相依赖成环；e 依赖 d，只是在等这个环，自己不在环上
startup_order -> 抛 CycleError, .cycle == ["b", "c", "d"]   # 不包含 e
```

## `main()` 命令流

```
PART 1                      PART 3
S 4                          S 3
db                           db
cache                        cache
api                          api
auth                         D 3
D 4                          api db
api db                       api cache
api cache                    cache db
cache db                     T 3
auth db                      db 5
→ db                         cache 3
  auth                       api 2
  cache                      → 10
  api                          api 8
                                cache 5
                                db 0
```

有环时 Part 1/2/3 都输出一行 `CYCLE <c1> <c2> ...`（环上服务，依赖顺序）。

## 边界清单

- `services` 有重复名字 → `ValueError`
- `deps` 引用了不存在的服务、服务依赖自己 → `ValueError`
- 无任何依赖：全部服务在同一波，按字典序输出（例 3）
- 多个服务同时就绪时必须按字典序 tie-break（例 1）
- 有环：报出的是**环本身**，不是"所有还没启动的服务"（例 5，`e` 不该出现在 `.cycle` 里）
- 环可能不止一个；只需要报出任意一个真实的环
- Part 3 的 `duration` 缺服务、多余服务、负数 → `ValueError`
- Part 3 没有任何依赖时，每个服务的 `start` 都是 0，`overall` 是最长单个服务的 `duration`
- 空 `services` 列表：三个 part 都应正常返回空结果，不报错
- 大图（测试用 5000 个服务、~1.5 万条依赖）2 秒内跑完

## 追问

1. **为什么环检测要单独找"真正的环"，而不是直接报告 Kahn 剩下的所有节点？** 剩下的节点里，有些只是依赖链末端连到了环上（例 5 的 `e`），报告它们会误导排查人员去检查不相关的服务；只报真正互相依赖的环才是可操作的信息。
2. **能不能把所有环都报出来？** 可以，把 `_find_one_cycle` 改成循环调用、每次找到一个环后从"卡住集合"里移除环上的节点，直到集合为空——但要小心多个环共享节点（比如两个环通过一个公共节点相连）的情况，报告格式需要相应设计。
3. **服务重启（幂等性）算不算这里的"启动"？** 本题只建模"冷启动一次"的依赖顺序，不涉及运行时的健康检查/重试；那是更贴近系统设计的话题（分布式作业调度器同族问题）。
4. **如果依赖关系在启动过程中动态变化（服务注册/发现）？** 需要每次有新依赖声明时重新做一次局部拓扑检查（只影响新加的边所在的连通分量），而不是整图重跑；这是"增量拓扑排序"的经典追问方向。
5. **Part 3 里如果两个服务可以并行启动但只有有限的启动并发数（类似 pc09 Part 3 的 k 个工位）？** 同一个 list-scheduling 启发式套路：按"到终点最长剩余链"排优先级，事件驱动模拟；参考 pc09 的 追问 3。

## 来源与置信度

- **LOW-MED**：https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/（2026-03-16），电面例题列出"服务启动依赖排序，Kahn 算法"，无更多细节；因为与同来源确认过的 Course Schedule II 复用主题一致，定为 LOW-MED 而不是纯 LOW。见 `../../../../catalog/raw/coding_phone_onsite.md` #20。
- Part 2（并行波次）、Part 3（每服务启动时间）未见一手报道，按拓扑排序类题目最常见的追问方向重建，已在题面标注 **(reconstructed)**；Part 3 的递推与 pc09 Parallel Courses III 同构。

## 考什么

S05 图：拓扑排序 / Kahn 算法 · 确定性 tie-break 的设计（字典序最小优先）· 环检测不能止步于"有没有环"，要能指出具体是哪些节点。
