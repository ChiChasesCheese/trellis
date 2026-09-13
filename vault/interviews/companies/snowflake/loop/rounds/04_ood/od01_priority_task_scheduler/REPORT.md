# od01 Priority Task Scheduler — report

## Summary
一个共享同一个类的 4-part 类设计题：优先队列 tie-break（priority → timestamp → id 字典序）→
重复 id "一次执行、永久失效" 的抑制语义 → 并发下 `add`/`execute` 的原子性 → （重建）用操作日志做
快照/重放的持久化。Snowflake 用这道题考"能不能先定好状态与不变量，再一步步往上叠能力"，而不是
一次性堆砌功能。

## Sources & confidence
HIGH——两个 fastprep 页面（`snowflake-priority-task-manager` 与
`snowflake-priority-task-execution-duplicate-ids`，均标注 Full-time Onsite）分别给出 base 版与
duplicate-ID 版的完整 API 和 tie-break 规则，且互相印证是同一道题的两个 part；1point3acres 一手
挂经（t.me/s/usinterview/29167）交叉确认题目形状。Part4 持久化在来源里只是"下一步自然追问"的
提法，没有具体 API——problem.md 明确标注 `snapshot()`/`replay()` 与 `SNAPSHOT` 命令是本仓库**重建**
的，不计入整体置信度。

## Approach by part
1. `TaskScheduler` 内部是一个 `(priority, timestamp)` 惰性堆 + 版本号：`add` 在任务未执行时把新的
   `(priority, timestamp)` 计入一个递增的 per-id version，并 push 一条新堆条目；`execute` 弹堆顶时
   校验该条目的 version 是否仍是该 id 当前的最新版本、以及该 id 是否已执行，两者任一为"否"就丢弃
   继续弹——这样"重复 add 替换旧值"不需要 O(n) 扫堆去删旧条目。
2. 重复 id 抑制只需要一个 `executed: set[str]`：`add` 在 id 已执行时直接 no-op；`execute` 弹出时
   同样检查这个集合。Part1 的"替换"与 Part2 的"抑制"因此是同一份状态机的两个自然推论，不是两套
   逻辑。
3. 并发正确性：把"弹堆顶 + 校验 + 标记已执行"整段包在一把 `threading.Lock` 里，保证两次并发
   `execute()` 不会读到同一个"尚未标记"的中间状态。`add` 也在同一把锁下追加操作日志，让日志顺序
   与实际执行顺序严格一致（为 Part4 服务）。
4. 持久化用操作日志而非序列化堆：`snapshot()` 返回 `add`/`execute` 调用的原始行；`replay()` 从空
   状态重新跑一遍日志。测试对"等价"的定义是行为等价（同样的后续操作产生同样的后续结果），不比较
   内部数据结构。

## Pitfalls hidden tests target
- tie-break 三层顺序，尤其"id 是数字样的字符串"时必须按字典序而不是数值比较（`"10" < "9"`）
- 未执行前重复 `add` 是替换（哪怕看起来像是"追加了一个新任务"）；执行后重复 `add` 是彻底的
  no-op，即使新 priority 极高
- 空池 `execute()` 返回 `""` 而不是抛异常或返回 `None`
- 并发下"恰好一次"：8 个线程抢占式 `execute()`，最终结果集合必须等于全部提交过的 id、且互不重复
- `SNAPSHOT` 前后行为不可区分，包括"已执行的 id 在重建后仍然是已执行状态"这个最容易漏掉的点
- 10^5 条 ADD/EXEC 混合指令必须用堆而不是线性扫描才能进预算

## Complexity & measured cost
`add`/`execute` 均摊 O(log n)（堆操作），`snapshot()` O(log_size)（返回已有列表的拷贝）。10 万条
混合 ADD/EXEC 通过 `run_script` measured ~0.3s / well under 256MB，远低于 2s/256MB 预算。

## Test inventory
22 tests — part1: 11（含 1 io、1 perf、1 fmt）· part2: 4 · part3: 2（并发）· part4: 5（含 1 io）；
edge 11 · fmt 1 · io 3 · perf 1。

## Skills exercised
S09 类设计先定 API 契约再讲状态与不变量 · S10 并发正确性（原子 claim、锁粒度）· S11 持久化与恢复
（操作日志 replay，而非序列化内部结构）· S08 确定性 tie-break（不是"看起来对"的顺序）· S12（间接，
惰性删除思路与缓存淘汰共享）
