# ps04 · Transaction Data Validation / Fraud Report — 范围 + 黑名单 + 行为匹配 + 优先级报告

**类型：** 技术电面（"Team Screen"） · **阶段：** 60 分钟（45 分钟写代码 + 15 分钟问答），4 个部分 · **最近一次出现：** 2025-11-30（programhelp，转载至 LeetCode Discuss）
**出现频率：** LeetCode Discuss 面经（programhelp 记录，2025-11-30）；interviewdb.io 分别列出"Data Validation"（发布 2 周）和"Fraud Reports"（发布 1 个月）两个独立追踪、截至 2026-07 仍活跃的条目 · **可信度：** 四部分结构和每部分的一句话规则概要可信度高（来源明确点名全部四个部分）；精确的输入协议、"最多两个码"之外的优先级顺序、以及演示数字都是本仓库的重构 —— 见来源部分。

## 背景
Stripe Radar 分阶段筛查交易：记录是否完整、是否违反硬性业务规则（金额范围、被封禁的支付
方式）、是否符合用户自身历史行为，以及 —— 如果同时出错多项 —— 哪两项最重要需要打印出来。
本题刻意**不是** `problems/q15_kyc_verification`（KYC：入驻 CSV、账单描述符规则、带引号
的逗号、重构的循环依赖检查）。ps04 是入驻之后的**风控分诊**：数字范围检查、黑名单，以及
对每用户行为画像的 3 属性匹配 —— 没有 CSV 引号，没有描述符规则。

## 输入（stdin）
第一行 `PART n`（n ∈ 1..4）。之后是固定顺序的四个分节，各自的标题独占一行；空行在任何
地方都忽略。四个分节始终全部存在（其内容对更早的 part 可能无关紧要 —— 照样解析；这样
协议在各个 part 之间保持一致，只有*被评估*的规则会变化）。
```
RULES
min_amount,max_amount                                    十进制美元，闭区间边界
BLOCKLIST
method1,method2,...                                      可能是空行（没有被封禁的方式）
PROFILES
user_id,countries,hour_min,hour_max,amount_min,amount_max
                                                           countries 用 ';' 连接（例如 US;CA）；
                                                           hour_min/hour_max 是 0-23 闭区间的整数；
                                                           amount_min/amount_max 是十进制美元
TRANSACTIONS
txn_id,user_id,amount,currency,payment_method,country,timestamp
                                                           标题行始终存在，始终跳过；
                                                           timestamp 是 ISO-8601 'YYYY-MM-DDTHH:MM:SS'
```
字段按 `,` 分割（不做引号处理 —— 这些字段都不含内嵌逗号）；每个值都会 trim。少于 7 列的
交易行，缺失的末尾列视为空字符串；多余的列忽略。最多 10^5 条交易行。

## 输出
API：`partN(lines: list[str]) -> list[str]`，每条交易一行输出，**按输入顺序**。
Part 1–3：`txn_id: CODE1,CODE2,...` 或 `txn_id: OK`。Part 4：列对齐的报告（见下文）。

## 规则（累积式 —— Part n 评估类别 1..n；每个激活的类别都独立检查，所以一行可能触发多个码）
### Part 1 — 完整性 → `MISSING_FIELD`
7 个字段（`txn_id,user_id,amount,currency,payment_method,country,timestamp`）中任意一个
trim 后为空（包括缺失的末尾列）→ `MISSING_FIELD`。

### Part 2 — 范围 + 黑名单 → `AMOUNT_OUT_OF_RANGE`, `BLOCKED_METHOD`
`amount` 必须能解析为数字**且**落在 `RULES` 分节的 `[min_amount, max_amount]`**闭区间**内
（金额缺失/为空这里不额外标记 —— `MISSING_FIELD` 已经覆盖）。`payment_method`
（不区分大小写，已 trim）不能出现在 `BLOCKLIST` 中。违反任一条即触发对应的码；两者可以
在同一行同时触发。

### Part 3 — 行为匹配 → `SUSPICIOUS`
将交易与其用户的 `PROFILES` 行在**3 个属性**上比较：`country` 是否在 profile 的国家集合中；
timestamp 的小时是否落在 `[hour_min, hour_max]`；`amount` 是否落在 `[amount_min,
amount_max]`（*profile 自身*的范围 —— 独立于 Part 2 的全局 `RULES` 范围）。统计 3 个属性中
匹配了多少个。**匹配数少于 2（即 0 或 1 —— "至少 50%" 四舍五入为"至少 3 项中的 2 项"）→
`SUSPICIOUS`。** 没有 profile 行的用户永远不会被标记为可疑（没有比较对象 —— 这条规则对
该用户直接跳过）。

### Part 4 — 优先级报告
与 Part 3 相同的规则集，但输出变成一份报告：按优先级最多保留**前 2 个**码（其余丢弃），
格式化为一个对齐的代码块。优先级从高到低：
`MISSING_FIELD > BLOCKED_METHOD > AMOUNT_OUT_OF_RANGE > SUSPICIOUS`。每行格式为
`txn_id`**左对齐，宽度为本次运行中最长 `txn_id` 的宽度**，之后恰好**两个空格**，然后是
（≤2 个）码用 `,` 连接，如果没有触发任何码则是 `OK`。

## 演示样例
以下每个样例共享同一个设置：
```
RULES
10.00,5000.00
BLOCKLIST
prepaid_card,gift_card
PROFILES
u1,US;CA,8,20,10.00,500.00
u2,GB,0,23,5.00,10000.00
TRANSACTIONS
txn_id,user_id,amount,currency,payment_method,country,timestamp
t1,u1,150.00,USD,credit_card,US,2026-08-01T14:30:00
t2,u1,150.00,USD,prepaid_card,US,2026-08-01T14:30:00
t3,u1,6000.00,USD,credit_card,US,2026-08-01T14:30:00
t4,u1,150.00,USD,credit_card,,2026-08-01T14:30:00
t5,u1,150.00,,credit_card,FR,2026-08-01T03:00:00
t6,u3,150.00,USD,credit_card,US,2026-08-01T14:30:00
t7,u1,9000.00,USD,gift_card,DE,2026-08-01T02:00:00
,u1,150.00,USD,credit_card,US,2026-08-01T14:30:00
```
`PART 1` →
```
t1: OK
t2: OK
t3: OK
t4: MISSING_FIELD          (country 为空)
t5: MISSING_FIELD          (currency 为空)
t6: OK
t7: OK
: MISSING_FIELD            (txn_id 本身为空 -- 显示为空字符串)
```
`PART 2`（加入范围 + 黑名单）→
```
t1: OK
t2: BLOCKED_METHOD                       (prepaid_card 被封禁)
t3: AMOUNT_OUT_OF_RANGE                  (6000.00 > 5000.00)
t4: MISSING_FIELD
t5: MISSING_FIELD
t6: OK
t7: BLOCKED_METHOD,AMOUNT_OUT_OF_RANGE   (gift_card 被封禁 且 9000.00 > 5000.00)
: MISSING_FIELD
```
`PART 3`（加入行为匹配；u1 的 profile：国家在 {US,CA} 内，小时 8-20，金额 10.00-500.00）→
```
t1: OK                                                  (国家 US、小时 14、金额 150 -- 3/3 匹配)
t2: BLOCKED_METHOD                                      (同样 3/3 匹配，所以不可疑)
t3: AMOUNT_OUT_OF_RANGE                                 (国家+小时匹配，金额 6000 不匹配 -- 2/3，仍是 OK)
t4: MISSING_FIELD                                       (国家 '' 不匹配，小时+金额匹配 -- 2/3，仍是 OK)
t5: MISSING_FIELD,SUSPICIOUS                            (国家 FR 不匹配，小时 3 不匹配，金额 150 匹配 -- 1/3 < 2)
t6: OK                                                  (u3 没有 profile -- SUSPICIOUS 从不评估)
t7: BLOCKED_METHOD,AMOUNT_OUT_OF_RANGE,SUSPICIOUS       (国家 DE 不匹配，小时 2 不匹配，金额 9000 不匹配 -- 0/3)
: MISSING_FIELD
```
`PART 4`（按优先级取前 2 个，列对齐；这里最长 txn_id 是 `t1`..`t7`，宽度 2）→
```
t1  OK
t2  BLOCKED_METHOD
t3  AMOUNT_OUT_OF_RANGE
t4  MISSING_FIELD
t5  MISSING_FIELD,SUSPICIOUS
t6  OK
t7  BLOCKED_METHOD,AMOUNT_OUT_OF_RANGE
    MISSING_FIELD
```
（`t7` 的第 3 个码 `SUSPICIOUS` 因为前 2 规则被丢弃。空 `txn_id` 行的 id 列是 2 个空格
（填充宽度），后面跟着必须的 2 个空格分隔符，所以 `MISSING_FIELD` 前面共 4 个空格。）

## 隐藏测试已知会针对的边界情况
- 只有空白字符的值 trim 后为空（`"  "` → `MISSING_FIELD`）
- 金额恰好等于 `min_amount` / `max_amount`（闭区间边界，两端都测）→ 不算超出范围
- 少于 7 列的行（缺失末尾列）→ 那些列为空 → `MISSING_FIELD`
- `BLOCKLIST` 比较不区分大小写（如果 `prepaid_card` 在列表中，`Prepaid_Card` 也被封禁）；
  空的 `BLOCKLIST` 行不封禁任何东西
- 3 个行为属性中恰好匹配 2 个**不算**可疑（">= 2" 边界，不是 "> 2"）
- 3 个中恰好匹配 1 个**算**可疑；0 个匹配也算可疑
- 没有 `PROFILES` 行的用户永远不是 `SUSPICIOUS`，无论交易看起来多异常 —— 没有比较对象
- 触发了 3 个以上码的一行：Part 1–3 全部打印（按优先级顺序）；Part 4 只保留前 2 个，
  丢弃其余，绝不重新排序
- 全部通过的行打印 `OK`，不是空码列表或空字符串
- `PART n` 真正门控评估：`BLOCKED_METHOD`/`AMOUNT_OUT_OF_RANGE`/`SUSPICIOUS` 违规在
  `PART 1` 下不可见（行打印 `OK`）
- txn_id 本身为空（仍触发 `MISSING_FIELD`；显示为空字符串，在 Part 4 对齐列中也是纯填充 ——
  见演示样例）
- Part 4 的列宽是本次运行按实际出现的最长 `txn_id` 重新计算的，不是固定常量
- 无法解析为数字的金额（非数字、非空）超出文档规定范围，隐藏测试不会触及（该字段要么为空，
  要么是合法十进制数）
- 最多 10^5 条交易行，最多 10^5 个 profile —— 不能是平方级复杂度（用 dict 查找，不能扫描）

## 见过的变体
- 来源的 Part 2 说"金额必须在业务定义的范围内"和"支付方式不在被封禁列表中"，但没有说明
  两者是放在一个规则块还是两个；本版本为了便于解析把它们分成独立的 `RULES` / `BLOCKLIST`
  分节。
- "至少 50% 的行为属性匹配"（来源原话）在这里实现为字面意义的 3 项中 `>= 2` 项，即向上取整
  到多数，不是分数阈值 —— 恰好 3 个属性的情况下没有歧义（2/3 = 66.7% >= 50%，
  1/3 = 33.3% < 50%），但本仓库显式定义了整数阈值，而不是每次都从百分比重新推导。
- 来源没有明确 Part 4 保留的输出码数量，只说"最多两个"，也没有指定平局优先级；本仓库
  确定了两者（`MISSING_FIELD > BLOCKED_METHOD > AMOUNT_OUT_OF_RANGE > SUSPICIOUS`），
  因为电面评分标准需要一个确定的顺序。

## 本题考察点
skills: S02 解析（分节 stdin）· S05 闭区间检查 · S06 `Decimal` 货币，绝不用浮点 · S08
确定性排序（全程保留输入顺序）· S09 精确格式化（列对齐）· S18 校验与优先级错误路径 ·
S19 增量式规则（Part n 评估类别 1..n）· S24 领域知识（Radar 式风控分诊，与 q15 的
KYC 领域不同）

## 来源
- https://leetcode.com/discuss/post/7384225/stripe-phone-screen-4-part-interview-exp-dhoy/ （programhelp 记录，2025-11-30："Part 1：读取一份 6 字段的 CSV [原文如此 —— 本仓库使用 7 字段，见说明部分]，校验所有字段非空。Part 2：金额必须在业务定义的范围内，支付方式不能在被封禁列表中，否则标记为可疑。Part 3：与历史行为比较（消费国家、时间范围、金额范围）—— 至少 50% 的行为属性必须匹配，否则 SUSPICIOUS。Part 4：输出一份错误报告，每笔交易最多两个错误码，按优先级排列，保持列对齐以便阅读。"）
- https://www.interviewdb.io/question/stripe （"Data Validation" — 发布 2 周；"Fraud Reports" — 发布 1 个月，截至 2026-07 抓取）
- `loop/raw/en_forums.md` §3.3 P6 "交易风控四段题（Data Validation / Fraud Reports）"（本仓库对上述内容的自行整理）

## 说明（作者本人添加，非来源内容）
- 来源在完整性检查部分说的是"6 字段"，但领域描述（金额、货币、支付方式、国家、timestamp
  用于行为匹配）需要 7 个命名列（`txn_id,user_id,amount,currency,payment_method,
  country,timestamp`）才能让 Part 2–4 有明确定义；本仓库使用 7 字段，把"6"视为来源自身的
  转述误差（这是一份二手记录，不是逐字的原始题面）。
- 来源转述中 Part 2 的"标记为可疑"，一旦 Part 4 的"错误码，按优先级排列"这句话表明到
  Part 4 时存在多个不同的码，就被更具体的 `AMOUNT_OUT_OF_RANGE` / `BLOCKED_METHOD`
  取代 —— `SUSPICIOUS` 专门保留给 Part 3 的行为匹配失败，依据来源自身 Part 3 的措辞。
- 精确的分节名称（`RULES`/`BLOCKLIST`/`PROFILES`/`TRANSACTIONS`）、profile schema 和
  优先级顺序都是本仓库的重构（没有逐字的 I/O 样例可参考），参照本题集自身
  `problems/q02_merchant_fraud_score` 的分节 stdin 惯例建模。
