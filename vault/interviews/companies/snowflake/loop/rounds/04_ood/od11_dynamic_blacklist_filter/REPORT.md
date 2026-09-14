# od11 Dynamic Blacklist Filter System — report

## Summary
两条并发流（黑名单增删 / 输入值）的过滤器：Part 1 单线程按时间戳重放、同刻打平规则
（mutation 先于 input，reconstructed）→ Part 2 多 owner 引用计数 + 前缀通配符
（reconstructed）→ Part 3 并发正确性，读写锁 + 线性一致性的可测试定义（reconstructed）。
两条来源（TrueInterview、1point3acres 面经索引）都只到标题级，规则细节几乎全部重建。

## Sources & confidence
MED（TrueInterview 同步清单第 10 题，标题+格式标签）+ medium（1point3acres 标题级索引，无正
文）。两条独立标题来源互相印证"这题存在"，但都没有给出任何规则文本；problem.md 逐条标注
**(reconstructed)**。

## Approach by part
1. `BlacklistFilter` 是一个集合；`process_events` 先按 `(timestamp, mutation_before_input)`
   稳定排序再重放，只对 `IN` 事件产生输出。
2. `RefCountedPatternFilter` 用 `(owner, pattern)` 集合去重 + `pattern -> 引用计数` 字典；
   `offer` 遍历当前引用计数 > 0 的规则做精确匹配或前缀匹配（`pattern.endswith("*")`）。
3. `ThreadSafeBlacklistFilter` 用一把 `RLock` 包住每次 `add`/`remove`/`offer`，并在同一把
   锁内把操作追加进 `linearization_log`（`seq` 严格递增 = 真实生效顺序）；`replay_sequential` 对
   着这份日志做单线程重放，用来证明并发执行等价于某个合法的串行历史。

## Pitfalls hidden tests target
- 乱序时间戳必须先排序；同刻 mutation 先于 input
- `remove` 一个不存在的值/owner 是空操作，不报错
- 多 owner 引用计数：任一 owner 还在拉黑就必须保持拦截；同一 owner 重复 add 不重复计数
- 前缀通配符不能误匹配不相关前缀（`10.0.*` 不匹配 `10.100.0.0`）
- 并发 add/remove 的最终状态必须等于把 `linearization_log()` 顺序重放的结果（用 10 线程 200
  次操作的随机交错验证）
- 并发下 `offer` 永远不抛异常、永远返回 `bool`

## Complexity & measured cost
Part1/2 每次操作 O(1)（集合/字典）或 O(规则数)（`offer` 里遍历规则做匹配）；Part3 每次操作
O(1) 加锁开销。10 万条乱序事件的排序+重放在 perf 预算（2s）内完成（实测远低于该预算）。

## Test inventory
24 tests — part1 7 · part2 7 · part3 6（3 个并发相关）；edge 12 · perf 1 · io 3 · fmt 1。

## Skills exercised
S09 类设计先定契约（同刻打平顺序）· S10 并发正确性（读写锁、引用计数原子性、线性一致性）·
流处理"乱序事件 + 按时间点查询"的通用模式。
