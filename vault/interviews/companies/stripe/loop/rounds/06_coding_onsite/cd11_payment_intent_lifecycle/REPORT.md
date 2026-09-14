# cd11 PaymentIntent lifecycle — report

## Summary
一道**自建的 onsite class-design 题**：题号来自四个上游镜像文件的标题（"Initializing the
System" → "Change Is Good!" → "Accepting Failure" → "Timing Matters"），规则集则是本仓库依据
`loop/study/20-cards/stripe_api.md` 里转述的真实 Stripe PaymentIntent 状态机自行设计的——因为
上游四个文件**只有标题和一段摘要，正文全部在付费墙后**，读不到任何函数签名、样例或精确规则。
核心是一个 `PaymentIntentEngine` 类：`card`（同步，confirm 立即成功/失败）和 `bank_debit`
（异步，confirm 先进 `processing`，之后才 `settle`/`fail`）两条支付方式分叉、"拒付后退回
`requires_payment_method` 以便重试"这个最容易漏掉的官方细节、"confirm 次数过多自动
`canceled`"的反滥用机制，以及 Part 4 的 `settle_window`/`expire` 时间窗口。

## CONVENTIONS 对照
和 `cd02` 一样，源头（这里是"上游标题暗示的题型"）要求的是一个**类**，不是
`partN(lines) -> list[str]` 流水线：`PaymentIntentEngine` 的九个方法在四个 part 之间累积暴露
（同一个对象，逐步解锁方法），大多数测试直接实例化它、调方法、断言返回值/状态，这是 VO
class-design 轮该有的形状。`run_commands`/`part1..4`/`main()` 是围着同一个类包一层命令流
harness（命令字 → 方法调用 → 文本行），只是为了满足这个仓库对 `impl.partN(lines)` 和
`main(stdin, stdout)` 的统一测试约定；类本身才是产品。

## 与 q10 的区别
**这道题和 `problems/q10_payment_intent_commands` 是同一个域（Stripe PaymentIntent 生命周期），
但规则集完全不同，做题时不要把两套规则混着背**：

| | q10（OA） | cd11（本题，onsite VO） |
|---|---|---|
| 接口形状 | 纯函数 `partN(lines) -> list[str]`，无类 | 一个 `PaymentIntentEngine` 类，方法逐 part 解锁 |
| 状态名 | 自造的 `REQUIRES_ACTION`/`PROCESSING`/`COMPLETED` | 真实 Stripe 状态名 `requires_payment_method`/`processing`/`succeeded`/`canceled` |
| 支付方式分叉 | 没有——所有 payment 走同一条 `CREATE→ATTEMPT→SUCCEED` | `card`（同步，confirm 直接成功）vs. `bank_debit`（异步，confirm 只进 processing，`settle` 才成功）——`change_method` 还能在 confirm 前把一条路径换成另一条 |
| Part 2 "change" | 只有 `UPDATE`（改金额） | `update_amount` **和** `change_method`（改金额 + 改支付方式，且方式变化会重塑之后 confirm 的分支） |
| Part 3 "failure" 目标状态 | `FAIL`: `PROCESSING → REQUIRES_ACTION` | `fail`: `processing → requires_payment_method`——**目标状态名不同，且没有"退款"这个动作**（q10 的 Part 3 核心是 `REFUND`，本题完全没有 `REFUND`） |
| Part 3 独有机制 | 无 | **confirm 次数过多自动 `canceled`**（`max_confirm_attempts`，默认 3；`fail` 不重置计数器）——q10 没有这个规则 |
| Part 4 "timing" 机制 | 商户级 `refund_limit`：`t_refund - t_create <= limit`，`0` = 永不退款，负数 = 强制视为"无限制" | 每个 intent 自己的 `settle_window`：`t - confirmed_at <= window`（从**confirm 时刻**起算，不是 create 时刻），`0` = 仅允许同一 tick（**不是**"永不"），负数 = **整条 CREATE 命令被拒绝**（不是"强制无限制"）——语义和 q10 刻意反着设计，避免"背了 q10 的 0/负数规则就以为 cd11 一样" |
| Part 4 新命令 | 无新命令，只是给已有命令加时间戳 | 新增 `EXPIRE`：显式的"系统收割超时 processing payment"事件，q10 没有对应物 |
| Output | 批量重放完后打印全部商户余额一次 | 每条命令产生一行输出（`OK`/`IGNORED`/具体状态词），额外有 `BALANCE <merchant>` 查询命令按需查余额 |

一句话：**q10 考的是"三态机 + 幂等 + 一种退款窗口"，cd11 考的是"class 设计 + 支付方式分叉 +
拒付重试 + 两种完全不同语义的时间窗口"**——两题的 `0`/负数边界值语义是**故意设计成相反**的，
就是为了防止候选人凭记忆而不是读题作答。

## Sources & confidence
**低置信度**：四个上游文件（`catalog/raw/mirror_1p3a_stripe/coding/146/145/149/148__...txt`）
全部是"Source Type: OJ / More Problems"的 SUMM 转述，每个只有标题 + 一段 3-5 句的 "Question
Summary" 要点列表，**没有正文、没有函数签名、没有输入输出格式、没有样例**——四个指向的
1point3acres URL（`interview/problems/ef09d8a4…`/`3adeb37a…`/`33ee3a0c…`/`0644b8b3…`）本轮均因
付费墙无法直接读取原文。**能从上游拿到、且本题据此保留的信息只有**：(1) 四个 part 的数量、
标题、隐含顺序（建立初始状态 → 状态变更 → 失败路径 → 时间维度）；(2) 摘要提到的关键词
（"merchant"、"state machine"、几个和 q10 相同的状态名/命令名片段）。由于这些关键词描述的规则
集已经和 `q10`（5 个独立来源交叉验证、置信度 high）高度重合，本题**没有**照抄这些细节，而是
用 `loop/study/20-cards/stripe_api.md`（Stripe 官方文档转述，非编造）里的真实状态机另建一套
规则——这一决定和取舍原因见上面"与 q10 的区别"，也写进了 `problem.md` 顶部的警示块。**规则细节
、输入输出格式、全部 4 个 worked example，都是本仓库自拟**，不代表任何候选人转述过的真实面试
规格。

## Part-by-part approach
1. **Part 1**：`PaymentIntent` dataclass（`id`/`merchant_id`/`amount_cents`/`method`/`status`/
   `confirm_attempts`/`confirmed_at`/`settle_window`）+ 两个字典（`_merchants`、`_intents`）。
   `confirm` 是全题的分支点：`card` 直接进 `succeeded` 并记账；`bank_debit` 进 `processing`，
   记账推迟到 `settle`。
2. **Part 2**：`update_amount`/`change_method` 都只检查"当前是不是还在
   `requires_payment_method`"这一个前置条件——因为 `confirm` 在决定同步/异步分支时是"现读现取"
   `method` 字段，`change_method` 天然就能重塑后续行为，不需要额外的状态搬迁逻辑。
3. **Part 3**：`fail` 是 `settle` 的镜像（都只在 `processing` 生效，都过 Part 4 的窗口检查），
   区别只是落点状态和有没有记账。自动取消逻辑**塞进 `confirm` 内部**而不是单独一个方法——
   在写 `confirm_attempts += 1` 之后立刻判断是否超限，这样"计数器不被 `fail` 重置"这条规则
   自然成立（`fail` 根本不碰 `confirm_attempts`）。
4. **Part 4**：`_within_window(pi, ts)` 是唯一的窗口判定逻辑，`settle`/`fail`/
   `cancel`(processing 分支) 三处共用；`settle_window is None` 或 `ts is None` 都视为放行——
   后者保证 Part 1-3 的测试（从不传 `ts`）永远不会被这段新代码影响。`expire` 是唯一"主动检查
   已超时"的方法，用严格 `>` 保证"恰好等于窗口"仍然合法（和 `settle`/`fail` 的 `<=` 边界呼应）。

## Pitfalls hidden tests target
- 把 `fail` 的目标状态写成一个新造的"failed"状态，而不是退回 `requires_payment_method`
  （官方文档明确说的行为，也是 `stripe_api.md` 卡片里标注的"最常被漏掉的失败路径"）。
- `confirm_attempts` 在 `fail` 时被误重置——导致永远触发不了自动取消。
- 自动取消判断用 `>=` 而不是 `>`（或反过来），导致 `max_confirm_attempts` 次巧好合法的
  confirm 被多算/少算一次。
- 把 Part 4 `settle_window=0` 当成"永不允许"（照抄 q10 `refund_limit=0` 的语义）——这里 `0`
  其实允许"同一 tick"的操作。
- 把负数 `settle_window` 强制视为"无限制"（照抄 q10 的负数语义）——这里负数是拒绝整条
  `CREATE` 命令。
- `cancel` 在 `processing` 分支忘记检查 `method == "bank_debit"`，误把 `card` 当作也能在
  processing 里取消（虽然本题的 `card` 正常路径永远不会进 processing，但 `cancel` 方法本身
  必须显式做这个检查，而不是依赖"反正不会发生")。
- `expire` 在 `settle_window is None` 时仍然触发——违反"无限期宽限永不自动过期"的规则。
- `CONFIRM` 的输出词是小写状态词（`succeeded`/`processing`/`canceled`/`ignored`），其余命令
  是大写 `OK`/`IGNORED`——混用两套词表是最容易被 `fmt` 测试抓到的格式坑。
- Part 1-3 没有时间戳前缀，Part 4 每一行都要有；`INIT`/`CREATE`/`UPDATE`/`CHANGE_METHOD`/
  `BALANCE` 在 Part 4 里仍要吃掉时间戳字段（哪怕自己不用），漏解析会导致整行被当成格式错误
  静默丢弃。

## Complexity & measured cost
所有 `PaymentIntentEngine` 方法都是 `O(1)` 摊还（字典查找/赋值）；`balances()` 是 `O(m log m)`
（`m` = 商户数，排序）。`run_commands` 对 `n` 行输入是 `O(n)`。50,000 次 `CREATE+CONFIRM(+SETTLE)`
周期（125,002 行，含 Part 4 时间戳与窗口解析）实测 **0.247 s**，远低于 2 s 预算；
`test_perf_100k_confirm_settle_cycles` 用同规模数据额外断言 `< 2.0 s` 且 `< 256 MB`，均通过。

## Test inventory
37 tests：part1 12 · part2 6 · part3 9 · part4 10；edge 12 · fmt 2 · io 4 · perf 1（marker 有重叠，
比如一个 part4 测试同时是 edge）。
- `python3 -m pytest loop/rounds/06_coding_onsite/cd11_payment_intent_lifecycle --tb=short`
  → **37 passed**（对 `solution.py`）。
- `IMPL=starter python3 -m pytest loop/rounds/06_coding_onsite/cd11_payment_intent_lifecycle --tb=no`
  → **36 failed, 1 passed**（唯一通过的是 `test_empty_stdin`，因为空输入下 starter 的
  `run_commands` 存根直接返回 `[]`，`main()` 什么也不打印，天然满足这条测试）。
- `bash loop/lint.sh loop/rounds/06_coding_onsite/cd11_payment_intent_lifecycle` → 通过
  （black -l 110 + flake8，F 类 0，E203/W503/E501 按仓库约定忽略）。

## Skills exercised
S01 读完四个 part 再设计（尤其是提前想好 `settle_window`/`confirm_attempts` 这两个字段，
第一版就放进 dataclass，不是 Part 4 才现加）· S02 变长时间戳前缀的行解析 · S03 用类
（`PaymentIntentEngine`）+ dataclass（`PaymentIntent`）建模，而不是散落的字典——VO 轮和 OA 的
分水岭 · S10 有真实回退的状态机（`processing → requires_payment_method`）· S11 幂等
（重复 `init_merchant`/`create_intent`、终态 `cancel` 的空操作）· S12 从"confirm 时刻"而不是
"create 时刻"起算的时间窗口 · S17 错误/空操作契约设计（`confirm` 返回四态字符串，其余方法
返回布尔值——两种不同粒度的返回值分别服务于不同调用方需求）· S18 校验与防御式输入处理
（负数窗口拒绝整条命令，而不只是把字段清空）· S19 四个 part 在同一个持久对象上的增量设计 ·
S24 领域知识（Stripe 官方 `requires_payment_method`/`processing` 状态名、拒付重试、
confirm 防滥用两条真实文档细节）。

## 面试官会怎么追问
1. **并发**：如果两个线程同时对同一个 `intent_id` 调 `confirm`，现在的"先加计数器再判断"会不会
   产生竞态（两个线程都读到"未超限"然后都往下走)？你会用锁还是 CAS 风格的乐观重试？
2. **持久化**：如果要把 `PaymentIntentEngine` 的状态存进真实数据库，`confirm`/`settle` 这种
   "读状态 → 判断 → 写状态"的组合操作要怎么变成一个事务，防止两次并发调用都基于同一份旧状态
   做决定？
3. **`settle_window` 到期后没人调 `expire` 怎么办**：现在 `expire` 是被动调用的，如果没有任何
   后续命令，一个超时的 `processing` intent 会永远卡着。真实系统会怎么设计一个后台定时任务
   扫描过期 intent？这个定时任务和"客户端主动查询状态"之间会不会有竞态（客户端查到
   `processing`，定时任务同时把它标成 `canceled`)？
4. **可扩展性**：如果要加第三种支付方式（比如需要用户在手机上做 3D Secure 验证的
   `requires_action` 中间态），现在 `confirm` 里"if method == card / else" 的两分支写法要怎么
   改成不需要改已有分支代码就能加新方式（策略模式/方法注册表）？
5. **审计**：如果要求每一次状态迁移都有不可篡改的历史记录（谁在什么时候把哪个 intent 从什么
   状态变成什么状态），现在的 `PaymentIntent` 只保留"最终状态"，要怎么改成同时维护一条
   事件日志，而不影响 `get_status`/`get_balance` 的 O(1) 读取？

## Open points
- Part 4 的 `settle_window` 目前只挂在 `PaymentIntent` 上（每个 intent 独立配置），而不是像
  q10 那样挂在商户级别——这是刻意选择（一个商户可能同时接入不同结算速度的支付渠道），
  但如果面试官现场要求"改成商户级默认窗口，intent 可以覆盖"，`create_intent` 需要加一个
  "未传时从商户拿默认值"的查找，`PaymentIntentEngine` 需要多存一个
  `_merchant_default_window: dict[str, int | None]`。
- `EXPIRE` 目前是"客户端/测试主动调用"的离散事件，不是真的后台定时任务——这是"面试官会怎么
  追问 #3"里明确留白的部分，本题不实现真的调度器。
