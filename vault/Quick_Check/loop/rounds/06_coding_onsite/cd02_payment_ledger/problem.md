# cd02 · PaymentLedger — 一个小型支付/退款记账类

**类型：** 现场 coding / "Programming Exercise"（45 分钟，类设计，3 部分）· **阶段：** 2026 夏季实
习 Virtual Onsite，coding 轮 · **最近出现：** 2026（programhelp.net VO 记录，2026 年内未标注具体日
期）· **出现频率：** 1 个直接来源（programhelp.net，完整方法列表 + 5 条追问）· **置信度：** 中
高——方法名、幂等的 `payment_id` 规则、部分退款支持，以及全部 5 条追问方向均直接来自源材料；确切的
签名（参数名/类型）、时间戳格式、错误契约（哪些失败抛异常 vs. 返回 `False`），以及持久化方法都是
本 problem.md 自己的还原，目的是把源材料一段话的描述变成具体、可测试的行为。

## 背景
Stripe 内部工具团队有时需要一个小型、自包含的账本对象——不依赖数据库、不依赖框架——来追踪单个商户
的支付与退款，并回答两个问题："我们实际拥有多少营收"和"这个日期范围内发生了什么"。这就是那个对象，
以面试风格分三个阶段逐步构建。

## 类
```python
class PaymentLedger:
    def add_payment(self, payment_id: str, amount_cents: int, ts_iso: str, customer: str) -> bool: ...
    def add_refund(self, refund_id: str, payment_id: str, amount_cents: int, ts_iso: str) -> bool: ...
    def get_total_revenue(self) -> int: ...
    def get_payments_by_date(self, start_iso: str, end_iso: str) -> list[dict]: ...
    def export_json(self) -> str: ...
    @classmethod
    def load_json(cls, blob: str) -> "PaymentLedger": ...
```
所有金额均为**整数分**，绝不使用浮点数。所有时间戳使用同一固定 profile：
`YYYY-MM-DDTHH:MM:SS`（naive——没有 `Z`，没有 UTC 偏移；原因见"Variants"）。不符合此格式的时间戳，
或者指代日历上无效的日期/时间的时间戳（`2026-02-30T00:00:00`、`2026-01-01T25:00:00`），均视为无效。

## 规则

### Part 1 — 支付与营收
`add_payment(payment_id, amount_cents, ts_iso, customer)`：记录一笔新支付并返回 `True`。**如果
`payment_id` 已经记录过，则视为无操作——返回 `False`**（幂等重试，而非错误）；原始记录保持不变。
`ts_iso` 在每次调用时都会被校验，且该检查发生在重复检查*之前*——因此对一次重复调用传入无效时间戳，
仍然会抛出 `ValueError`，而不是返回 `False`。`get_total_revenue()` 返回所有已记录支付金额之和
（Part 1 阶段还不存在退款，所以这里就是普通求和）。

### Part 2 — 部分退款
`add_refund(refund_id, payment_id, amount_cents, ts_iso)`：对一笔已存在的支付执行退款并返回
`True`。规则按以下顺序：
1. 首先校验 `ts_iso`（格式不合法时抛出 `ValueError`，先于任何其他检查）。
2. **如果 `refund_id` 已经处理过，则视为无操作——返回 `False`**（与 `add_payment` 相同的幂等重试
   契约）。
3. **如果 `payment_id` 不存在，抛出 `KeyError(payment_id)`**——这是一种不同于幂等重复的失败模
   式；对一笔从未存在过的支付发起退款是调用方的 bug，而不是重试。
4. **如果这笔退款会使该支付的累计退款超过原始的 `amount_cents`，抛出 `ValueError`。** 精确相等
   （正好退掉剩余余额）是允许的。多笔部分退款会累加到同一个运行总额上。
`get_total_revenue()` 变为 `sum(amount_cents) - sum(所有成功的退款)`——一笔已被全额退款的支付贡献
`0`，绝不会为负。

### Part 3 — 日期范围查询与持久化
`get_payments_by_date(start_iso, end_iso)`：两端边界均**闭区间**。先校验两个时间戳（任一格式不合法
时抛出 `ValueError`——在触及任何支付数据之前）。返回 `list[dict]`，每笔匹配的支付一条记录，形状
精确为：
```python
{"payment_id": str, "amount_cents": int, "ts": str, "customer": str, "refunded_cents": int}
```
按 **`ts`（时间顺序）、再按 `payment_id`（普通字符串顺序）**作为 tie-break 排序。
`export_json() -> str` 序列化账本的完整状态（各笔支付、其退款总额，以及已应用的退款 id 集合——需要
这个集合，才能让重新加载后的账本仍然拒绝重复的退款重放）。
`PaymentLedger.load_json(blob: str) -> PaymentLedger` 是其逆操作：一个全新的账本，其
`get_total_revenue()` 和 `get_payments_by_date(...)` 与原账本完全一致，并且在之后的任何调用中仍然
执行同样的去重/超额退款规则。

## 命令流测试框架（用于 `main()` / io 测试）
`main()` 每行读取一条命令，针对同一个 `PaymentLedger` 为每条命令打印一行输出：
```
PAY <payment_id> <amount_cents> <ts_iso> <customer>     -> PAY <payment_id> OK|DUP
REFUND <refund_id> <payment_id> <amount_cents> <ts_iso>  -> REFUND <refund_id> OK|DUP|ERROR <msg>
REVENUE                                                  -> REVENUE <cents>
RANGE <start_iso> <end_iso>                              -> RANGE <count>
                                                             <payment_id> <amount_cents> <ts> <customer> <refunded_cents>
                                                             ... (count lines, same sort as get_payments_by_date)
```
`customer` 是一个不含空白的单一 token（例如 `cus_a1b2`），绝不是带空格的展示名。
一个格式错误的 `PAY` 时间戳会打印 `PAY <payment_id> ERROR <message>`，而不是 `OK`/`DUP`；一个格式
错误的 `RANGE` 边界会打印 `RANGE ERROR <message>`，且后面不再跟任何行。

## 实例演算
全部通过运行 `solution.py` 验证。

### Example 1（Part 1）
```python
L = PaymentLedger()
L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a")  # -> True
L.add_payment("p2", 500,  "2026-01-02T09:00:00", "cus_b")  # -> True
L.add_payment("p1", 999,  "2026-01-03T00:00:00", "cus_a")  # -> False (duplicate id, ignored)
L.get_total_revenue()                                       # -> 1500
```

### Example 2（Part 2）
```python
L.add_refund("r1", "p1", 300, "2026-01-05T00:00:00")  # -> True  (300 <= 1000)
L.add_refund("r2", "p1", 400, "2026-01-06T00:00:00")  # -> True  (300+400=700 <= 1000)
L.get_total_revenue()                                  # -> 1500 - 700 = 800
L.add_refund("r3", "p1", 400, "2026-01-07T00:00:00")  # -> raises ValueError (700+400=1100 > 1000)
L.add_refund("r1", "p1", 300, "2026-01-08T00:00:00")  # -> False (r1 already applied)
L.add_refund("rX", "ghost", 100, "2026-01-08T00:00:00")  # -> raises KeyError('ghost')
```

### Example 3（Part 3）
```python
L.get_payments_by_date("2026-01-01T00:00:00", "2026-01-02T23:59:59")
# -> [
#      {"payment_id": "p1", "amount_cents": 1000, "ts": "2026-01-01T10:00:00", "customer": "cus_a", "refunded_cents": 700},
#      {"payment_id": "p2", "amount_cents": 500,  "ts": "2026-01-02T09:00:00", "customer": "cus_b", "refunded_cents": 0},
#    ]
blob = L.export_json()
L2 = PaymentLedger.load_json(blob)
L2.get_total_revenue() == L.get_total_revenue()          # -> True
L2.get_payments_by_date(...) == L.get_payments_by_date(...)  # -> True
```

### Example 4（command stream）
```
PAY p1 1000 2026-01-01T10:00:00 cus_a
PAY p2 500 2026-01-02T09:00:00 cus_b
PAY p1 999 2026-01-03T00:00:00 cus_a
REFUND r1 p1 300 2026-01-05T00:00:00
REVENUE
RANGE 2026-01-01T00:00:00 2026-01-02T23:59:59
```
```
PAY p1 OK
PAY p2 OK
PAY p1 DUP
REFUND r1 OK
REVENUE 1200
RANGE 2
p1 1000 2026-01-01T10:00:00 cus_a 300
p2 500 2026-01-02T09:00:00 cus_b 0
```

## 隐藏测试已知会针对的边界情况
- 重复的 `payment_id` 返回 `False`，且**不会**覆盖 amount/ts/customer。
- 恰好退掉剩余余额是被允许的（边界：`refunded + amount == amount_cents`），多一分钱则抛出
  `ValueError`。
- 对同一笔支付的两笔（或更多笔）部分退款能正确累加到上限。
- 重复的 `refund_id` 是幂等的（`False`），即便该支付理论上还能吸收更多退款——去重检查发生在金额
  检查之前。
- 对一个从未添加过的 payment id 发起退款：`KeyError`，与幂等重复的 `False` 路径可区分。
- 空账本上的 `get_total_revenue()` 为 `0`；一笔已全额退款的支付贡献 `0`，而不是负数。
- `get_payments_by_date` 的边界两端都是闭区间；恰好落在 `start_iso` 或 `end_iso` 上的支付会被
  包含在内；超出任一边界一秒钟的支付会被排除。
- 无效的时间戳形状：缺少 `T` 分隔符（`2026-01-01 00:00:00`）、日历上无效的日期
  （`2026-02-30T00:00:00`）、日历上无效的时间（`2026-01-01T25:00:00`），以及非字符串值——都是
  `ValueError`，且在每一个接受时间戳的入口（`add_payment`、`add_refund`、`get_payments_by_date`）
  都会抛出。
- `export_json`/`load_json` 往返保留退款总额*以及*已应用的 `refund_id` 集合——一个由 `load_json`
  重建出来的账本，仍然拒绝一次重放的重复退款，并且仍然正确执行超额退款上限。
- 大型账本：10^5 笔支付，一次窄窗口的 `get_payments_by_date` 查询——不能随查询次数相对账本规模呈
  二次方增长。

## 现实中见过的变体
- programhelp.net 自己的追问列表（见 Sources）给出了五条扩展方向，已被折叠进下面的"面试官会怎么追
  问"，而不是当作基础需求处理：部分退款的边界情况（在本题中已作为 Part 2 的核心规则，而非追问）、
  大规模场景下的查询优化、非法时间戳处理（在本题中已作为核心 `ValueError` 契约，而非追问）、区间
  查询（Part 3 核心），以及持久化到真实数据库（本 problem.md 用 `export_json`/`load_json` 作为该
  追问的内存态类比，因为真实数据库集成无法离线测试）。
- 时区感知变体：`ts_iso` 带有 UTC 偏移或 `Z` 后缀；比较之前必须先归一化到同一个时区（本题未实现——
  只支持 naive 时间戳；见"面试官会怎么追问"#4）。
- 一种更严格的变体会校验 `amount_cents >= 0` 并直接拒绝负数金额（本题未强制——零金额的支付/退款
  是合法的边界情况，负数金额在本版本中属于超出范围/未定义）。

## 本题考察什么
技能点：S02 固定时间戳 profile 下的解析/校验 · S03 分阶段揭示的类 API，而非自由函数 · S06 整数分
金额，绝不用浮点数累加 · S08 确定性多键排序 · S09 精确的命令流输出格式 · S17 错误契约设计（幂等无
操作 vs. `KeyError` vs. `ValueError`——三种不同情形对应三种不同的失败形态） · S18 校验与防御性输
入处理 · S20 序列化往返正确性

## 来源
- `loop/raw/cn_forums.md` 第 104 行："programhelp.net《Stripe 2026 Summer Intern VO》Coding 轮
  （45 分钟）：设计一个轻量级支付交易记录系统，实现 `PaymentLedger` 类：`Add_payment()`、
  `Add_refund()`、`Get_total_revenue()`、`Get_payments_by_date()`；需按 `payment_id` 防重复记录；
  支持部分退款（扣减金额）。追问包括：①处理部分退款金额小于原支付的情况 ②海量数据场景下的查询优
  化 ③非法时间戳格式的错误处理 ④按时间范围查询（如取某月数据）⑤数据持久化到数据库。评估重点：
  面向对象设计、边界处理、代码清晰度、可扩展性、权衡意识——不是复杂算法。"
  [programhelp.net/en/vo/stripe-intern-vo-coding-integration/]

## 面试官会怎么追问
1. 上面第①条追问原文是"处理部分退款金额**小于**原支付的情况"——这其实已经是本题 Part 2 的核心规则
   （累计退款 ≤ 原金额），面试现场如果你先只实现了"退一次全额退款"，这就是面试官会追的第一个问题：
   "如果客户只想退一部分钱呢？如果退两次呢？"
2. 第②条"海量数据场景下的查询优化"：现在 `get_payments_by_date` 是线性扫描全部 payment。如果要支
   持 10^7 笔记录上的高频区间查询，你会怎么维护一个按 `ts` 排序的索引（比如 `bisect` 二分定位区
   间边界，或者按天分桶）？插入新 payment 时索引怎么增量维护，而不是每次查询都重新排序一遍？
3. 第③条"非法时间戳格式的错误处理"：现在只有一种严格格式 `YYYY-MM-DDTHH:MM:SS` 会被接受。如果上游
   系统会同时发来"2026-01-01"（无时间部分）、Unix 时间戳（整数秒）、甚至字符串"null"这三种格式混
   杂的历史数据，你的校验/解析层要怎么演进成"尽量兼容、明确拒绝"而不是"越写越多 if"？
4. 时区：现在假设所有时间戳都是同一个隐含时区的 naive 时间。如果 `ts_iso` 可能带 UTC 偏移
   （`+08:00`）或者 `Z` 后缀，你的区间比较逻辑要怎么改？两个不同时区的时间戳能直接按字符串排序吗
   （不能——这是一个常见陷阱，值得主动指出）？
5. 第⑤条"数据持久化到数据库"：`export_json`/`load_json` 只是内存态的序列化。如果换成真的 SQL 数
   据库，`add_payment`/`add_refund` 的"先校验后写入"逻辑要怎么变成事务？两个并发请求同时对同一笔
   `payment_id` 调用 `add_payment` 会不会产生竞态（都读到"不存在"然后都写入）？你会用什么手段防止
   （唯一约束 + 捕获冲突异常，而不是先查后写）？
6. 审计：如果央行/监管要求每一次退款操作都有不可篡改的审计记录（谁在什么时候退了多少钱、退款前后
   余额各是多少），你现在的 `_payments` 字典只保留"最终状态"（`refunded` 累计值），要怎么改成同时
   保留每一笔退款事件的完整历史，而不影响 `get_total_revenue()` 的 O(1) 均摊读取？
