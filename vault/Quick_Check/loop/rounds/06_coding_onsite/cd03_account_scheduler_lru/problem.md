# cd03 · AccountScheduler — 可用性、定时锁、LRU 自动选择(类 API)

**类型:** 现场面试编程题 · **阶段:** 虚拟现场面试 "常规编码"(60 分钟,3 个 part + 追问) · **最近一次:** 2026-03-27(1point3acres 题库)
**出现频率:** 3 处独立提及(1point3acres 题库 "AccountScheduler LRU";linkjob 2025-12-07/2026 现场面试报告 "is_available / acquire(duration) / LRU auto-select";process_and_jd.md 现场面试表格) · **置信度:** 中等 —— 三步递进结构(`is_available` → `acquire` → LRU 自动选择)及方法名在各来源间一致;确切的构造函数形态、异常行为以及 LRU 平局裁决规则**为本轮重建**(下文已标注),是 `problems/q26_account_scheduler_lru`(该题用带 `RELEASE` 的命令流 API,`add_account`/id 顺序平局裁决)的刻意变体:本轮在构造时就固定账户池,对未知 id 抛异常而不是返回哨兵布尔值,LRU 平局裁决按**构造顺序**而非 id 字符串顺序——不要直接照搬 q26 的解法,两者的约定是刻意不同的。

## 背景
Stripe 的测试模式工具维护一个小型、固定的沙盒账户池,供集成任务借用一段时间。
一个任务可能询问某个特定账户是否空闲、把它锁定 `duration` 秒,或者只是请求
*任意*一个空闲账户——这种情况下调度器会分配出**最近最少使用**的那一个,以便
负载均匀分散,不会让某个账户被反复压榨。账户 id 的池子是预先已知的(没有
动态 `ADD`),这正是本题作为*类设计*练习而非流处理练习的关键:面试官想看到的
是干净的状态(一个字典)、站得住脚的异常策略,以及从"是否空闲"→"锁定它"→
"帮我挑一个"的清晰主线。

## 类 API
```python
class AccountScheduler:
    def __init__(self, accounts: list[str]) -> None
    def is_available(self, account_id: str, t: int) -> bool
    def acquire(self, account_id: str, t: int, duration: int) -> bool
    def acquire_any(self, t: int, duration: int) -> str | None
```
`accounts` 列出所有合法 id,顺序即调用者关心的 LRU 平局裁决顺序(见 Part 3)。
`t` 和 `duration` 都是普通整数(秒);全程没有货币,没有浮点数。

## 规则
### Part 1 — 注册表与可用性
内部状态只有一个字典 `locked_until: dict[str, int]`,初始为空(没有条目 = 从未
锁定 = 在任意 `t` 都可用)。`is_available(account_id, t)` 在以下条件为真时返回
`True`:`account_id not in locked_until or t >= locked_until[account_id]`——也就是说,
在 `t0` 时刻加锁 `duration` 秒覆盖的区间是 `[t0, t0 + duration)`,是**排它性结束**:
`is_available(id, t0+duration)` 为 `True`,`is_available(id, t0+duration-1)` 为
`False`。用一个不在构造函数 `accounts` 列表中的 `account_id` 调用 `is_available`
(或 `acquire`、`acquire_any`)会抛出 `KeyError`。

### Part 2 — `acquire`:定时锁定
`acquire(account_id, t, duration)` 把账户锁定在 `[t, t+duration)` 区间,如果它在
`t` 时刻可用则返回 `True`;否则返回 `False` 且不改变任何状态。`duration <= 0`
会抛出 `ValueError`,**在**检查可用性**之前**就抛出(不管状态如何,坏调用就是
坏调用)。一次成功的 acquire 会设置 `locked_until[account_id] = t + duration`,
并记录 `last_used[account_id] = t`(供 Part 3 使用)。未知 `account_id` 抛出
`KeyError`,和 Part 1 一样,只有在两者都错的情况下"谁的优先级更高"才有意义——
参考解先校验 `duration`,因为它不需要碰 `locked_until` 就能完成检查;两种顺序
都说得通,但顺序必须被明确选定并写清楚,而不是碰巧被解释器先命中哪个分支
决定。**参考顺序:先 `duration`,后未知 id。**

### Part 3 — `acquire_any`:LRU 自动选择
在 `t` 时刻可用的账户中(按 Part 1 的规则),挑一个并像 `acquire` 一样锁定它
(同样 `duration <= 0` → `ValueError`),然后返回它的 id。选择顺序:
1. **从未被获取过的账户优先**——一个从未有过*成功* `acquire`(Part 2 或此前的
   `acquire_any`)的账户,永远排在有过的账户之前,不管后者多久之前用过。
2. 在从未被获取过的候选账户之间,按**构造顺序**平局裁决——即 id 在传给
   `__init__` 的 `accounts` 列表中的位置,**不是**字母顺序。
3. 在此前被获取过的候选账户之间,按 `last_used` **升序**排序(用得最早的胜出);
   平局(`last_used` 相等)同样按构造顺序裁决。

如果 `t` 时刻没有任何账户可用,返回 `None` 且不改变任何状态。失败的
`is_available` 检查、失败的 `acquire`,或单纯的 `is_available` 查询都不会更新
`last_used`——只有*成功*加锁才会。

### `main()` — 命令流
```
AVAIL <id> <t>            -> true | false | ERROR
ACQ <id> <t> <duration>   -> true | false | ERROR
ANY <t> <duration>        -> <id> | none | ERROR
```
整次运行中账户池是固定的:**第一行**是 `ACCOUNTS <id1> <id2> ...`(空格分隔,
构造顺序 = LRU 平局裁决顺序),后续所有行都是命令。类抛出的任何
`KeyError`/`ValueError`、任何未知动词、参数个数错误,或非整数的
`t`/`duration`,都会为该行打印 `ERROR` 并继续处理(这个流层面的错误策略只是
`main()` 层的便利做法——类本身永远抛异常,从不吞掉异常)。空行会被忽略。

## 示例演算
```
ACCOUNTS a b
AVAIL a 0        -> true
ACQ a 0 10       -> true            (锁定 a: [0, 10))
AVAIL a 9        -> false
AVAIL a 10       -> true            (排它性结束)
ACQ a 5 5        -> false           (t=5 时仍处于锁定状态)
ANY 5 10         -> b               (a 已锁定;b 从未使用过)
ANY 5 10         -> none            (两者现在都已锁定/不可用)
ANY 15 5         -> a               (a 在 15 时刻再次空闲;last_used a=0 < b=5)
ACQ b 16 100     -> true
AVAIL b 17       -> false
ANY 20 1         -> a               (a: last_used=15;b: last_used=16 -> a 更旧)
```
```
ACCOUNTS c b a
ANY 0 1          -> c               (全部从未使用过 -> 按构造顺序 c,b,a)
ANY 0 1          -> b
ANY 0 1          -> a
ANY 0 1          -> none            (全部锁定至 1)
ANY 1 1          -> c               (全部空闲,last_used 全为 0 -> 再次按构造顺序)
ACQ a 1 1        -> true            (a: last_used=1)
ANY 2 1          -> b               (last_used b=0 < c=a=1 -> LRU 优先于构造顺序)
```
```
ACCOUNTS x
ACQ x 0 0        -> ERROR           (duration <= 0 -> ValueError,被 main() 捕获)
AVAIL y 0        -> ERROR           (y 未知 -> KeyError,被 main() 捕获)
ACQ x ten 5      -> ERROR           (t 非整数)
FROB x           -> ERROR           (未知动词)
```

## 隐藏测试已知会针对的边界情况
- 排它性的锁定结束(`t0+duration` 时空闲,`t0+duration-1` 时不空闲);恰好在到期时刻
  重新加锁应成功
- 未知 `account_id` 在 `is_available`、`acquire`、`acquire_any` 中都会抛出 `KeyError`,
  因为这是调用者的错误,不是 `main()` 的错误(类从不吞异常——只有 `main()` 会)
- `duration <= 0` 在 `acquire` 和 `acquire_any` 中都会抛出 `ValueError`,即使原本也不会
  有任何账户可用(先校验,再看状态)
- LRU:从未使用的排在已使用的前面,无论"多久之前"对从未使用的账户毫无意义
- 从未使用的平局裁决是**构造顺序**,不是 id 字符串顺序(`ACCOUNTS c b a` 得到
  `c, b, a`,而不是 `a, b, c`)——这是本轮约定与 q26 分歧最大的一处
- 已使用账户之间 `last_used` 相等时同样按构造顺序裁决
- 失败的 `acquire` / 单纯的 `is_available` 查询绝不会碰 `last_used`
- 当所有账户都锁定时 `acquire_any` -> `None`;恰好有一个到期后 -> 就是那一个
- 单账户池;空命令流;一个所有账户在 t=0 时都被使用过的池(平局)
- 跨调用非单调的 `t`(查询纯粹靠与 `locked_until`/`last_used` 的比较来回答,绝不依据
  "目前的墙上时钟"——较晚调用之后出现较早的 `t` 也必须被正确回答)
- 10^5 条命令、最多 10^4 个账户的池必须在预算内舒适地运行

## 现实中出现过的变体
- linkjob 的措辞暗示了一个隐式时钟(`now()` 内置在调度器里)而不是每次调用都显式传入
  `t` 参数——逻辑相同,把时钟作为构造函数默认值注入而不是参数;作为一个现场追问提及。
- `problems/q26_account_scheduler_lru` 是同一个前提的 OA 版姐妹题:动态 `ADD`/`RELEASE`,
  用布尔哨兵值而非异常,id 顺序的 LRU 平局裁决。在 60 分钟现场面试中要求这种形态的
  面试官,往往倾向于固定池并改用异常——两种都有据可查;本 problem.md 明确采用
  异常 + 固定池 + 构造顺序的解读,并明确说出来,而不是悄悄地二选一。

## 本题考察内容
技能点:S03 类 + 字典建模 · S05 严格与非严格时间比较 · S08 确定性平局裁决
(构造顺序,而非"显而易见"的 id 顺序) · S10 事件流上的状态 ·
S18 校验/异常策略(抛异常 vs 返回哨兵值,以及哪个检查先运行) ·
S19 增量式设计(Part 1 → 2 → 3 各自恰好新增一项能力) · S20 自测

## 来源
- 1point3acres 题库 "AccountScheduler LRU"(现场面试,最近一次 2026-03-27)—— `loop/raw/en_forums.md` §6.2(C4 AccountScheduler)
- https://www.linkjob.ai/interview-questions/stripe-technical-interview/(VO AccountScheduler —— is_available / acquire(duration) / LRU auto-select)
- `loop/raw/en_forums.md` §6.2 第 ~276-277 行;与 `problems/q26_account_scheduler_lru/problem.md` 交叉核对(姐妹 OA 变体,明确不在此重复——见"现实中出现过的变体")

## 面试官会怎么追问
1. "如果要支持 `release(id)` 提前解锁,`last_used` 要不要跟着变?" — 期望候选人复述 q26 里已经验证过
   的答案:不变,因为"释放"不是"使用",提前释放的账户应该保留它原来的 LRU 位置,否则会被立刻选中
   造成"刚放出来又立刻抢回去"的抖动。
2. "10^5 次 `acquire_any` 调用,`accounts` 池有 10^4 个,现在这版是不是每次都要扫一遍?怎么优化到
   `O(log n)`?" — 期望候选人提出两个堆(free 堆 + locked 堆)+ 版本号懒删除,和 q26 的做法一致,并能
   讲清楚"锁刚好在这次调用之前过期"要怎么先把它挪回 free 堆。
3. "如果两次调用之间 `t` 反而变小了(时钟回拨),现在的实现还对吗?" — 正确答案是"对,因为状态判断
   全部基于存储的 `locked_until`/`last_used` 和传入的 `t` 直接比较,没有对'调用顺序=时间顺序'做
   任何假设";引导候选人现场证明这一点,而不是含糊带过。
4. "为什么未使用账户的 tie-break 是构造顺序,而不是 id 字符串顺序?这在生产环境里有什么意义?" —
   考察候选人是否理解"构造顺序"往往编码了业务优先级(比如账户池按可信度/容量排列),而不是随手选一
   个排序键;也是在检验候选人是否会照抄 q26 的 id-order 答案而不读题。
5. "多线程环境下多个 job 同时调 `acquire_any`,会不会两个线程选中同一个账户?怎么修?" — 期望候选人
   识别出"选择"和"加锁"必须是一个原子操作(读-判断-写的竞态),提出用一把锁包住整个
   `acquire_any` 方法体,或者用 CAS 风格的重试。
6. "为什么 `duration <= 0` 要在检查 unknown id 之前验证?如果反过来会有什么后果?" — 检验候选人是否
   真的对"校验顺序"这种细节做过取舍,而不是巧合地写对了;正确的讨论点是"两种顺序都能自洽,但必须
   写进文档并保持一致,不能一部分方法先查 id 一部分先查 duration"。
7. "如果账户池要支持运行时增删(变回 q26 那种 `ADD`),你的 Part 3 tie-break 还成立吗?" — 期望候选人
   意识到"构造顺序"在动态池下不再有意义,需要换成"首次注册顺序"这种新的单调递增序列(比如一个自增
   计数器),而不是死记当前的静态顺序。
