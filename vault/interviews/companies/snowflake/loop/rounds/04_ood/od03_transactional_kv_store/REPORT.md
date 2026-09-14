# od03 Transactional In-Memory KV Store — report

## Summary
一个支持嵌套事务的内存 KV store：单事务 begin/commit/rollback → 嵌套合并语义（内层 commit 合并
进外层，只有最外层 commit 才落全局）→ 每线程独立事务栈下的线性一致读。这是"数据库内部"这条
Snowflake 技能线（5/6 份 JD 提到）最直接的玩具版 MVCC 投影。

## Sources & confidence
HIGH-MED——单一来源（PracHub，Hard，Technical Screen，明确标注 Snowflake）但给出完整 API、精确
的 worked example（`[put(a,1), begin, put(a,2), get(a), begin, delete(a), get(a), rollback,
get(a), commit, get(a)]` → `[2, None, True, 2, True, 2]`，problem.md 例1 逐步展开）、以及明确的
"Follow-up 2: Concurrency"段落（每线程事务栈 + first-touch snapshotting，本题 Part3 直接转述）。
1point3acres 上存在结构几乎相同但标注 xAI 的同形题——按 problem.md"背景"一节的说明，这提示"事务型
KV store"是通用面试母题，不代表 Snowflake 独有；不影响本题内容置信度，但建题时保留了这条提醒。

## Approach by part
1. 全局字典 + 一把锁；无事务时 `put`/`delete`/`get` 直接读写全局，`commit`/`rollback` 在无事务
   时返回 `False`（不抛异常，这是候选人常漏掉的一条契约）。
2. 每次 `begin()` 往当前线程的事务栈 push 一个空 overlay 帧；`put`/`delete` 只写栈顶帧；`get`
   从栈顶到栈底逐帧查找，第一个命中的帧决定结果，全部未命中才落到全局状态。`commit()` 弹出栈顶
   帧，用 `dict.update` 把它合并进新的栈顶（或者栈已空时合并进全局）——因为每帧只记录"这次事务
   自己触碰过的 key 的最终值"，合并等价于"父作用域看到了子事务的全部效果"。`rollback()` 只需要
   丢弃栈顶帧：不需要额外的 undo 记录，因为帧本身天然只包含这次事务自己的写入，这正是
   first-touch snapshotting 想要达到的效果，只是用"整帧丢弃"而不是"逐 key 撤销"实现。
3. 并发：`threading.local()` 保证每个线程只操作自己的栈，天然免锁；全局字典的读（无事务时的
   `get`）与最外层 `commit` 的落盘都在同一把锁下完成，保证"提交"这一步对其他线程是原子可见的，
   不会读到部分提交的中间态。

## Pitfalls hidden tests target
- 无事务时 `commit`/`rollback` 返回 `False`，不抛异常
- `delete` 之后 `get` 返回 `None`，与"从未 put 过"不可区分（本题明确约定的简化）
- 内层 `rollback` 必须恢复到"外层自己的、尚未提交的写"，而不是恢复成全局状态或"从未写过"
- 深层嵌套里 rollback 中间层不影响更外层已经做的修改
- 同一事务内对同一 key 反复写/删，一次 `rollback` 整体撤销，不是逐步撤销
- 每个线程的事务栈互相独立：两个线程各自 `begin`+`put` 同一个 key，各自只能看到自己的值
- 未提交的写对其他线程不可见（用一个没有自己事务的旁观线程在 writer 提交前读到旧值来验证）
- 10^5 次混合操作（含深度 ≤20 的嵌套 begin/commit/rollback）2s 预算内完成

## Complexity & measured cost
`get`/`put`/`delete` 均为 O(栈深度)（通常是个位数）；`commit`/`rollback` O(帧大小)。10 万条混合
指令（含嵌套）通过 `run_script` 实测 well under 2s / 256MB。

## Test inventory
17 tests — part1: 8（含 1 io、1 fmt、1 perf）· part2: 6 · part3: 3；edge 6 · fmt 1 · io 2 · perf 1。

## Skills exercised
S09 类设计先定 API 契约（`commit`/`rollback` 用布尔返回值而非异常表达"无事务"）· S10 并发正确性
（per-thread 事务栈、first-touch 语义、提交的原子可见性）· S11（间接，overlay 合并与 WAL/undo-log
思路相通）· S20 自测试
