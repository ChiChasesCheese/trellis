# od03 · Transactional In-Memory KV Store — nested transactions, per-thread linearizable reads

**类型：** 技术筛（PS，45–60 min，3 part + 追问）· **最近：** 2026-08
**置信度：** HIGH-MED（单一来源但细节具体，见文末）

## 背景
一个支持事务的内存 KV store，是"数据库内部"这条 Snowflake JD 主线（5/6 份 JD 提到）最直接的
面试投影：`begin`/`commit`/`rollback` 的嵌套语义、以及"每个线程看到自己未提交的修改、看不到别的
线程未提交的修改"这条隔离规则，几乎是 MVCC 的一个玩具版本。来源明确把这题分成三步：单事务 →
嵌套事务 → 多线程线性一致，并且第三步给出了推荐实现思路（每线程一个 undo-log 栈）。

**须知**：1point3acres 上存在一道结构几乎相同、但标注给 xAI 的"Transactional Key-Value Store"
题（`https://www.1point3acres.com/interview/problems/post/7100152`，登录墙，只能看到步骤大纲
"Step 1: Simple Transactions, Step 2: Nested Transactions, Step 3: Real-World Issues"）。这类
"事务型 KV store"是一个足够通用的面试母题，很可能在多家公司独立出现；这不推翻 Snowflake 标注的
PracHub 来源，但建题时不应假设这题是 Snowflake 独有——它更像是"数据库内部"这条技能线的通用考法。

## API 契约（英文签名）
```python
class TransactionalKVStore:
    def get(self, key: str) -> int | None: ...
    def put(self, key: str, value: int) -> None: ...
    def delete(self, key: str) -> None: ...
    def begin(self) -> None: ...       # start a new (possibly nested) transaction scope
    def commit(self) -> bool: ...      # False if no active transaction
    def rollback(self) -> bool: ...    # False if no active transaction
```
值全部是 `int`；`key` 是 1–100 字符的字符串。

## 规则

### Part 1 — 单事务
没有 `begin()` 时，`put`/`delete` 直接作用在全局状态上，`get` 读全局状态。`begin()` 打开一个事务
作用域；作用域内的 `put`/`delete`/`get` 都只影响/看到**这个事务自己**的修改（尚未影响全局状态）。
`commit()` 把这个事务的修改一次性落到全局状态，返回 `True`；`rollback()` 撤销这个事务的全部修改
（回到 `begin()` 之前的状态），返回 `True`。没有活跃事务时调用 `commit()`/`rollback()` 返回
`False`，不抛异常。

### Part 2 — 嵌套事务
`begin()` 可以在已有事务内再次调用，开启一层更深的嵌套作用域。规则：
- 内层事务里的写操作，对**同一调用栈里更晚发生的**读操作立即可见（同一事务内自己写自己读）。
- `rollback()` 只撤销**最内层**（最近一次 `begin()`）事务自己做的修改，回到该层 `begin()` 之前
  的状态（可能是外层事务已经做过的修改，也可能是全局状态——取决于嵌套深度）。
- `commit()` 把最内层事务的修改**合并进上一层**（父作用域），而不是直接落到全局状态——只有
  最外层的 `commit()` 才真正把修改写入全局状态。换句话说，`commit()` N 层嵌套需要调用 N 次才能
  真正持久化。
- 来源原文例子：
  `[put(a,1), begin, put(a,2), get(a), begin, delete(a), get(a), rollback, get(a), commit, get(a)]`
  → `[2, None, True, 2, True, 2]`（只有产生返回值的调用——`get`/`commit`/`rollback`——贡献一项
  输出；见下方"Worked examples"逐步展开）。

### Part 3 — 并发：每线程事务栈，线性一致读
多线程共享同一个 `TransactionalKVStore` 实例。规则（来源原文，转述）：
- 每个线程有自己独立的事务栈；一个线程的未提交修改，在它自己的后续读里立即可见，但对**其他
  线程**不可见，直到该线程的最外层事务 `commit()`。
- 实现思路（来源推荐）：一份共享的全局字典 + 每线程一个 undo-log 栈；某个 key 在当前事务里第一次
  被写时，先把它"改之前的值"记进 undo-log（first-touch snapshotting），这样 `rollback()` 只需要
  把 undo-log 里记录的旧值写回去；读操作从**当前线程自己的栈**由内到外找最新的修改，找不到才落到
  全局共享状态。
- 线性一致性的可测试定义（本题采用）：任意时刻，从任意线程读到的全局已提交状态，必须等于某个
  真实发生过的"提交顺序"下的状态（不会读到"部分提交"的中间态，也不会因为读写竞争而丢更新）——
  用多线程各自开事务、写不相交的 key 集合、`commit()`，最终断言全局状态等于所有已提交写的并集
  来验证。

## Worked examples

**例 1（Part2，来源原文例子逐步展开）**
```
put(a, 1)     -- 无输出，全局 a=1
begin()       -- 无输出，进入 L1
put(a, 2)     -- 无输出，L1 里 a=2（全局仍是 1，尚未提交）
get(a)        -- 2          （读到 L1 自己的写）
begin()       -- 无输出，进入 L2（嵌套在 L1 里）
delete(a)     -- 无输出，L2 里 a 被标记删除
get(a)        -- None        （L2 看到自己的删除）
rollback()    -- True        （撤销 L2；回到 L1 的状态：a=2）
get(a)        -- 2          （L1 的 a=2 恢复可见）
commit()      -- True        （L1 提交进全局；全局 a=2）
get(a)        -- 2          （全局状态）
```
→ `[2, None, True, 2, True, 2]`

**例 2（Part1，无事务时 commit/rollback 返回 False，且不抛异常）**
```
get(a)
commit()
rollback()
put(a, 5)
get(a)
```
→ `[None, False, False, 5]`

**例 3（Part2，多层嵌套 commit 需要逐层进行才能落到全局）**
```
begin()
put(k, 10)
begin()
put(k, 20)
commit()      -- 合并进 L1，L1 里 k=20；全局仍未变
get(k)        -- 20（在 L1 里）
rollback()    -- 撤销整个 L1（包括合并进来的 k=20）；回到全局状态（k 从未设置）
get(k)
```
→ `[True, 20, True, None]`

## `main()` 命令流
```
GET <key>
PUT <key> <value>
DELETE <key>
BEGIN
COMMIT
ROLLBACK
```
`PUT`/`DELETE`/`BEGIN` 无输出。`GET` 输出值的字符串形式，`None` 时输出字面量 `None`。
`COMMIT`/`ROLLBACK` 输出 `True`/`False`。

## 边界清单
- 没有任何 `begin()` 时 `commit()`/`rollback()` 都返回 `False`，绝不抛异常
- `get` 一个从未 `put` 过的 key 返回 `None`；`get` 一个已 `delete` 的 key 也返回 `None`
  （`delete` 后再 `get` 与"从未存在"不可区分，这是本题对 delete 语义的约定）
- 事务内 `delete` 一个"外层事务里刚 `put` 但尚未提交"的 key，`rollback` 之后必须恢复到外层那次
  `put` 的值，而不是"从未 put 过"
- 深度 ≥3 的嵌套；每一层都做互不相同 key 的写，`rollback` 中间层不影响更外层已经做过的修改
- 同一个 key 在同一事务内被反复 `put`/`delete`：`rollback` 只需要恢复到"进入这个事务之前"的那
  一个值，不需要逐次撤销中间的每一次写（first-touch snapshotting 的意义所在）
- 并发：多线程各自开独立事务、写不相交的 key 集合，最终全局状态是所有提交的并集，不丢任何一次
  提交、也不出现"读到别的线程未提交值"的情况
- 10^5 次 `get`/`put`/`delete`/`begin`/`commit`/`rollback` 混合操作、嵌套深度不超过操作数，在
  2s 预算内完成

## 并发追问
1. "两个线程同时对同一个 key 做 `put` 又立刻 `commit`，最终值是谁的？" —— 期望候选人说清楚
   "谁的 commit 后发生，谁的值就是最终值"（last-committer-wins，用一把保护"合并进全局状态"这
   一步的锁来保证提交本身是原子的），而不是含糊带过。
2. "`rollback` 用 first-touch snapshotting，如果同一个 key 在事务里被写了 100 次，是不是要存
   100 份 undo 记录？" —— 期望候选人指出"只在第一次触碰时记一次旧值"，后续同 key 的写不再记录
   （标准 undo-log/MVCC 优化），并现场证明这样仍能正确 rollback。
3. "如果要把这个 KV store 扩展成跨线程共享同一个嵌套事务（而不是每线程独立事务栈），线性一致性
   还成立吗？" —— 期望候选人指出"跨线程共享事务"需要把整个事务边界的加锁范围扩大到跨越多次方法
   调用，退化为长事务持锁，讨论这会带来的吞吐/死锁问题，是这道题一个合理但没有标准答案的开放
   追问。

## 变体
- 见上方"背景"关于 xAI 同形题的说明——这是通用事务型 KV store 母题的合理变体，不代表 Snowflake
  独有，练习时不必假设每个细节都专属 Snowflake。
- 来源的"Real-World Issues"（xAI 版 Step 3 的标题）暗示还可能追问"key 过期/TTL"或"事务超时自动
  rollback"，未见二次印证，不建入本题。

## 来源与置信度
- https://prachub.com/coding-questions/design-transactional-in-memory-key-value-store （Hard,
  Technical Screen，明确标注公司 Snowflake；给出精确的 Follow-up 2 并发段落，本题 Part3 直接
  转述）
- https://www.1point3acres.com/interview/problems/post/7100152 （同构题，标注 xAI，登录墙，仅
  三步大纲可见——用于"不要假设唯一性"的提醒，不作为本题内容来源）
- `catalog/raw/ood.md` #2、`catalog/CATALOG.md` Table B od03 行；置信度 **HIGH-MED**：单一来源但
  给出完整 API、精确 worked example 与并发段落，细节具体到可以直接建题。

## 考什么
S09 类设计先定 API 契约（`commit`/`rollback` 的布尔返回值 vs 异常的取舍）· S10 并发正确性（每
线程事务栈、first-touch snapshotting、线性一致读）· S11（间接，undo-log 与 WAL 思路相通）· S20
自测试
