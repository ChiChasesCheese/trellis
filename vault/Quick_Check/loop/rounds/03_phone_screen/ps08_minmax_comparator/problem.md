# ps08 · Min/Max with comparator

**类型：** 电面（技术） · **阶段：** 45 分钟技术电面，4 个部分 · **最近一次出现：** 2020-01（都柏林）
**出现频率：** 1 处独立来源（rampatra 的 2020 年都柏林电面记录），明确点名全部四个部分
· **可信度：** 中等（part *结构*是逐字转录 —— "Part 1 取最小值；Part 2 按参数取最小或
最大；Part 3 用比较器；Part 4 处理并列" —— 但下面具体的记录 schema 和演示样例数字是
本报告的重构，因为原始记录里没有样例数据；标注在"未解决点"中）

## 背景
Stripe 的内部工具经常需要"按某个字段给我极值记录"—— 最早未解决的争议、今天金额最高的
交易、需要复核舍入误差的最小金额支付。朴素版本把某个字段写死。本题把它逐步推进到一个
完全通用的极值查找器：先是固定字段，然后是参数化的字段+方向，再然后是调用方任意提供的
比较器（这样调用方就能表达单个 `key` 字符串无法表达的多字段 tie-break），最后是当多条
记录并列为极值时该怎么办 —— 前三种设计都悄悄地各自选出一个赢家，直到有人要求你把它们
全部列出来。

## 输入（支付记录）
每行一条记录：`id,amount,created_at,country`。
- `id`：不透明的字符串标识符，输入中不保证有序，按普通字符串比较（`sorted()` 顺序 ——
  `"B" < "a"`、`"user10" < "user2"`）。
- `amount`：十进制字符串（可以为负，比如退款），解析为 `decimal.Decimal` —— 绝不用
  `float`，这样即使在使用这份数据的其他流水线中做过运算，两条记录在数值上仍可以精确相等。
- `created_at`：ISO-8601 时间戳，`Z` 或显式 UTC 偏移量（`2024-01-15T10:00:00Z` 或
  `2024-01-15T10:00:00+00:00`），解析为 `datetime.datetime`。
- `country`：短字符串，按字典序比较（不校验是否为真实 ISO 国家代码 —— 任何字符串都
  接受，并按字符串排序）。

解析记录时空行被忽略。记录**不会**按 `id` 去重 —— 如果同一个 `id` 出现在两行，它们是
两条恰好共享 `id` 的不同记录，两者都有资格在 Part 4 中被算作"并列"。

## 输出（`main()` 的 stdin 协议）
第一行是 `PART 1`..`PART 4`。
- `PART 1`：之后的行只有记录。
- `PART 2` / `PART 4`：**下一行**是控制行 `<key> <mode>`（`key` ∈
  `{amount, created_at, country}`，`mode` ∈ `{min, max}`），之后的行是记录。
- `PART 3`：之后的行只有记录 —— 比较器在 `main()` 中是固定的（见下方 Part 3）；纯函数
  `extreme_with` 本身接受任意比较器，测试套件也直接调用它，不仅仅通过 stdin。

输出是每行一个 id（`PART 1`/`2`/`3`：恰好一行）或若干行（`PART 4`：每条并列记录一行，
按 `id` 升序）。**空记录输入始终恰好打印一行：`NONE`。**

## 规则

### Part 1 — `min_by_amount(records: list[Record]) -> str | None`
返回 `amount` 最小的记录的 `id`。并列时返回输入顺序中**第一个**这样的记录（一个固定的
简单 tie-break —— Part 4 改变了这个契约，见下文）。空列表返回 `None`；`part1(lines)`
把它渲染为 `["NONE"]`。

### Part 2 — `extreme(records: list[Record], key: str, mode: str) -> str | None`
把 Part 1 泛化到三个字段中的任意一个和任意方向。`key="amount"` 按数值比较 `Decimal`；
`key="created_at"` 按时间顺序比较解析后的时间戳；`key="country"` 按字典序比较字符串。
`mode="min"`/`"max"` 选择方向。tie-break 与 Part 1 相同（输入顺序中第一个）。未知的
`key` 或 `mode` 抛 `ValueError`。

### Part 3 — `extreme_with(records: list[Record], comparator: Callable[[Record, Record], int]) -> str | None`
`comparator(a, b)` 在 `a` 应被视为比 `b` "更小"时返回负数，"更大"时返回正数，相等时
返回 `0` —— 经典的 C/`qsort` 风格契约（也是 `functools.cmp_to_key` 所期望的）。
`extreme_with` 返回在该排序下**最小**的记录的 `id` —— 通过**线性扫描**找到（`O(n)` 次
比较器调用），而不是排序：维护一个运行中的 `best`，只在严格更优时替换
（`comparator(candidate, best) < 0`），这也顺带免费得到与 Part 1-2 相同的"平局取先出现者"
tie-break。要用比较器表达"最大"，调用方传入一个符号翻转的比较器。`main()` 的 `PART 3`
使用规范比较器 `by_amount_then_created_at`（amount 升序，并列时按 created_at 升序打破）
—— 这是一个真正有用的比较器，Part 2 单一的 `(key, mode)` 接口*无法*表达它，因为它需要
两个字段各自独立的 tie-break 顺序。

### Part 4 — `extreme_all(records: list[Record], key: str, mode: str) -> list[str]`
与 Part 2 相同的 `(key, mode)` 接口，但返回**所有**并列为极值的记录 —— 不只是第一个。
输出是并列的 id，**按 `id` 升序排序**（普通字符串顺序），每行一个。这与 Part 1-3（总是
把并列归结为单一赢家）是一个真正不同的契约 —— 如果被问及如何调和它们，明确点出这一点。
空输入 → `["NONE"]`，与其他每个 part 相同。

## 演示样例
贯穿全文使用的记录（固定顺序，下文按此顺序引用）：
```
r1,100.00,2024-01-10T10:00:00Z,US
r2,50.00,2024-01-05T09:00:00Z,CA
r3,50.00,2024-01-01T08:00:00Z,DE
r4,200.00,2024-02-01T00:00:00Z,US
```

Part 1：`min_by_amount` → **r2**（金额 50.00 与 r3 并列，r2 在输入顺序中排在前面）。

Part 2：
- `extreme(key=amount, mode=max)` → **r4**（200.00，最大金额）
- `extreme(key=created_at, mode=min)` → **r3**（2024-01-01，最早的时间戳）
- `extreme(key=country, mode=min)` → **r2**（字典序 `"CA"` < `"DE"` < `"US"`）
- `extreme(key=country, mode=max)` → **r1**（`"US"` 在 r1 和 r4 之间并列；r1 排在前面）

Part 3：`extreme_with(by_amount_then_created_at)` → **r3**。r2 和 r3 在 amount 上并列
（50.00），所以比较器落入 `created_at` 比较；r3 的 `2024-01-01` 早于 r2 的
`2024-01-05`，所以 r3 胜出 —— **与 Part 1 的 `min_by_amount` 不同的答案**，后者只看
`amount`，因此在同一个并列上选择 r2。这个差异正是 Part 3 的全部意义所在：比较器能表达
单一 `key` 无法表达的排序。

Part 4：
- `extreme_all(key=amount, mode=min)` → **r2, r3**（都是 50.00，按 id 升序排序）
- `extreme_all(key=country, mode=max)` → **r1, r4**（都是 `"US"`，按 id 升序排序）

空输入，任何 part → `NONE`。

## 隐藏测试已知会针对的边界情况
- 空记录列表：每个 part 都恰好打印 `NONE`，绝不是空输出/异常
- 单条记录：它自然既是最小也是最大
- 负数金额（退款）与正数正确比较
- 精确并列的边界：两条记录有完全相同的 `Decimal` 金额、相同的 `created_at`（在解析精度
  内）、或相同的 `country` 字符串
- 两条不同记录之间重复的 `id` —— 如果两者都并列极值，都出现在 Part 4 的并列列表中
  （id 不去重）；如果那个重复 id 本身就是唯一记录，两者都是答案
- Part 4 的 `id` 排序是**普通字符串顺序**，不区分大小写不敏感或数值感知
  （`"B" < "a"`、`"user10" < "user2"`）
- `created_at` 同时接受 `Z` 和显式的 `+00:00`/其他偏移量，并正确地把它们作为同一时刻
  比较（一个 `Z` 时间戳和一个相同时刻的偏移量时间戳在 tie-break 目的上相等）
- 未知的 `key` 或 `mode` 字符串 → `ValueError`，不是静默的错误答案
- 一个只在 `amount` *之外*的字段上区分的比较器（比如只看 `country`）传给 `extreme_with`
  也必须正确运行 —— 函数不能假设一定涉及 `amount`
- 大输入（10^5 条记录）必须靠单次线性扫描在性能预算内轻松完成，而不是在只需要极值时做
  `O(n log n)` 排序

## 见过的变体
- rampatra 的记录没有点名记录 schema 或字段类型 —— 本报告选择了 `amount`/
  `created_at`/`country` 作为"若干可求极值的字段"的一个具体、贴合 Stripe 风格的实例化；
  真实转录可能使用不同的字段名或不同的记录结构（比如纯整数），但保持相同的四段递进。
- 一个不在原始四段中的自然追问：直接扩展 `extreme_with` 本身以支持并列（返回所有被
  比较器认为与赢家相等的记录），而不是新增一个单独的 `extreme_all` —— 见下方
  "面试官会怎么追问"第 7 条。

## 本题考察点
skills: S03 把记录建模为小型有类型结构（不是原始 CSV 行）· S08 带明确、有意在 Part 1-3
和 Part 4 之间改变的 tie-break 的确定性排序 · S12 时间戳解析/比较 · S19 增量式设计
（Part 4 复用 Part 2 的 `(key, mode)` 接口；Part 3 独立作为更通用的机制）· S21 标准库
熟练度（`Decimal`、`datetime.fromisoformat`、`functools.cmp_to_key` 与手写线性扫描的对比）

## 来源
- rampatra，2020-01，都柏林 Stripe 电面记录（`loop/raw/en_forums.md` §3.3 中的 P14）：
  "Part 1：取最小值的记录；Part 2：按参数返回最小或最大；Part 3：使用比较器；
  Part 4：处理并列。"

## 面试官会怎么追问
1. "为什么 `extreme_with` 用线性扫描而不是
   `min(records, key=functools.cmp_to_key(comparator))`？"（答案：找*一个*极值时渐进
   结果相同，线性扫描是 `O(n)` 次比较器调用，CPython 里基于 `cmp_to_key` 的 `min` 实现
   也同样是 `O(n)` —— 这里更倾向手写扫描的真正原因是它把"平局取先出现者"规则明确、可
   审计地放在一个 `if` 条件里，而且不需要把每条记录都包进 `cmp_to_key` 产生的对象；
   如果你还需要*排序后*的顺序用于别的事情，排序才有道理，但对单个极值来说这是不必要的
   额外工作）
2. "`comparator` 需要满足什么不变式，`extreme_with` 才能正确？"（答案：反对称性 ——
   `comparator(a,b)` 和 `comparator(b,a)` 符号必须相反（或都为零）—— 以及传递性；一个
   违反这些性质的比较器（比如按 `id % 3` 以循环方式比较）会让"线性扫描保留最优"的策略
   根据记录顺序返回不确定或干脆错误的答案，排序也会静默犯同样的错）
3. "扩展 `extreme` 接受一个 `(key, mode)` 对的*列表*来实现多键排序，而不用写完整的自定义
   比较器。"（答案：为每条记录构建一个元组 key ——
   `tuple(extract(key, mode) for key, mode in fields)`，`mode="max"` 的字段取反/反转
   —— 然后比较元组；这是 `extreme` 的单一 key 和 `extreme_with` 完全通用比较器之间自然
   的折中）
4. "如果记录以实时流的形式到达而不是批量给出，你怎么在不重新计算的情况下维护当前的
   极值？"（答案：对单个运行中的最小/最大值，维护一个运行中的 `best`，用同样的比较器
   在每条新记录上 `O(1)` 更新；对于 Part 4 "全部并列"的语义在流上，你还需要维护完整的
   并列集合，如果来了一条严格更优的记录可能还要淘汰其中一些成员）
5. "为什么 `amount` 用 `Decimal` 而不是 `float`？"（答案：像 `0.1 + 0.2` 这样的十进制
   字面量在 float 下相等性/顺序不可靠，而且如果这个极值查找器后续被喂进任何做求和或
   舍入的流水线，float 累积会漂移 —— `Decimal` 与本仓库其余部分的金额约定一致（见
   CONVENTIONS.md），尽管本题本身不做任何运算）
6. "你会怎么让 Part 4 支持基于*比较器*而不仅仅是 `(key, mode)` 对的并列，把它和 Part 3
   统一起来？"（答案：在通过 `extreme_with` 的扫描找到 `best` 之后，把相等性检查
   `value == extreme_value` 换成 `comparator(record, best) == 0` —— 函数签名会变成
   `extreme_all_with(records, comparator) -> list[str]`，`extreme_all(records, key,
   mode)` 可以变成它的一个薄包装，就像现在 Part 4 包装 Part 2 的接口一样）

## 未解决点
- 来源中唯一验证过的事实是四段结构本身及其每段一句话的描述；记录 schema、字段名、精确
  的 tie-break 规则，以及所有演示样例数字都是本报告的重构。如果出现带样例 I/O 的转录，
  应据此核对上面的演示样例。
