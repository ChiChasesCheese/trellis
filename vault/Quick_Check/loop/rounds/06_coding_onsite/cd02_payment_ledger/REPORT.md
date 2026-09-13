# cd02 PaymentLedger — 报告

## 概述
2026 夏季实习 VO coding 轮的一道小型类设计记账题：实现一个 `PaymentLedger`，支持支付、部分退款、
营收统计、按日期范围查询，分三个面试阶段逐步揭示。真正的难点不在算法，而在于选定并贯彻始终一套一致
的错误契约：幂等无操作（`False`）vs. `KeyError` vs. `ValueError`，分别对应三种本质不同的失败情形；
再加上持久化的往返读写必须保留足够的状态（包括*哪些*退款 id 已经处理过），才能在重新加载后继续执行
同样的规则。

## CONVENTIONS 对照
本题的源材料要求的是一个**类**，而不是 `partN(lines) -> list[str]` 流水线——方法集合
（`add_payment`、`add_refund`、`get_total_revenue`、`get_payments_by_date`）是在*同一个*对象上，
跨三个面试阶段累积起来的，就像真实面试官揭示题目的方式一样（不存在"Part 1 的类"和"Part 2 的类"之
分）。为了让类始终是主要、自然的接口，同时仍满足本仓库测试框架的约定：
- 大多数测试直接实例化 `impl.PaymentLedger()` 并调用方法——这是 OOP 题目的自然形态，并且由于整个
  模块（类 + 函数）作为一个整体加载，依然可以通过 `IMPL=starter` 完全替换。
- `part1(lines)` / `part2(lines)` / `part3(lines)` 是围绕同一个 `run_commands(lines)` 命令流引擎
  （`PAY`/`REFUND`/`REVENUE`/`RANGE`）的薄、**完全相同**的包装，其存在纯粹是为了让本仓库其他题目
  依赖的 `impl.partN(...)` 与 `main(stdin, stdout)` 接口在这里也存在。它们之间的区别只在于哪些测试
  会用到它们（按功能划分），而不是实现能力上的差异——这一点在 solution.py 的 docstring 和本文档里都
  明确写出，以免被误读为疏漏。

## 来源与置信度
中高——`loop/raw/cn_forums.md` 第 104 行（programhelp.net 对 2026 夏季实习 VO 的记录）逐字给出了方法
名（`Add_payment`、`Add_refund`、`Get_total_revenue`、`Get_payments_by_date`）、payment_id 去重规
则、部分退款支持，以及全部五条追问方向。它**没有**给出确切的参数名/类型、时间戳格式、哪些失败是异
常还是返回 `False`，也没有给出持久化方法的签名（`export_json`/`load_json`）——这些都是本
problem.md 自己做出的、具体且可测试的还原，在"Variants"一节中已明确标注。

## 分部分思路
1. **Part 1**：用一个以 `payment_id` 为 key 的字典；`add_payment` 遇到重复 id 时返回 `False`，且不
   修改任何状态。`get_total_revenue` 是对 `amount - refunded` 的生成器求和（在 Part 2 出现之前
   refunded 始终为 `0`，所以此阶段就是普通求和）。
2. **Part 2**：`add_refund` 按照如下确切顺序检查：时间戳有效性 -> 重复 `refund_id`（幂等
   `False`）-> 未知 `payment_id`（`KeyError`）-> 超额退款（`ValueError`）-> 成功（累加
   `refunded`，记录 `refund_id`）。顺序很关键：`test_refund_invalid_timestamp_raises_before_other_checks`
   和 `test_duplicate_refund_id_is_idempotent_before_amount_check` 分别锁定了两处候选人容易搞反
   的顺序。
3. **Part 3**：`get_payments_by_date` 先校验两个边界，然后直接对存储的*字符串*做过滤——固定宽度
   的 `YYYY-MM-DDTHH:MM:SS` profile 使得字符串顺序等价于时间顺序，因此每次查询都不需要重新解析。
   线性扫描，不建索引：性能预算（10^5 笔支付，单次查询）根本用不到索引；追问列表把 bisect/索引化的
   扩展方式作为讨论点提出，而不是硬性要求。`export_json`/`load_json` 需要同时往返序列化支付记录*和*
   `refund_ids` 集合——丢掉后者会让重新加载后的 ledger 接受一次重放的重复退款，
   `test_loaded_ledger_still_enforces_refund_rules` 直接捕获这一点。

## 隐藏测试针对的坑
- 三种截然不同的失败形态对应三种不同情形（幂等 `False` / `KeyError` / `ValueError`）——把任意两种
  混为一谈是最容易犯的错误。
- 退款校验顺序：错误时间戳的优先级高于"未知支付"；重复 `refund_id` 的优先级高于超额检查（因此重
  放一个已经成功的退款永远不会抛异常，即便该支付此后已被其他退款全额退完）。
- 恰好在边界上的退款（正好退掉剩余余额）必须成功；多一分钱必须抛异常——`>` 与 `>=` 的 off-by-one
  是这里的经典 bug。
- `get_payments_by_date` 的边界两端都是闭区间；排序的 tie-break 是 `payment_id`，而不是插入顺序。
- `export_json`/`load_json` 必须保留退款 id 集合，而不只是运行中的累计值——一个常见的偷懒做法（每
  笔支付只持久化 `refunded_cents`）会在重新加载后悄悄破坏幂等性。
- 重复的 `payment_id` 不能覆盖原始的 amount/ts/customer——只能通过布尔返回值来告知调用方这是一次
  无操作。

## 复杂度与实测开销
`add_payment`/`add_refund`（字典操作）均摊 O(1)；`get_total_revenue` 和 `get_payments_by_date` 为
O(n)（n 为支付笔数）——在题目给定的 10^5 规模下可以接受，且按追问列表自身的定位，特意没有过度设计成
索引结构（那是讨论型的扩展）。10 万笔支付 + 一次区间查询，远低于 2 秒 / 256 MB 的预算（见
`test_perf_100k_payments_and_range_query`）。

## 测试清单
24 个测试——part1: 6 · part2: 6 · part3: 12（含 1 个格式、3 个 io、1 个性能）；edge 9 · fmt 1 ·
io 3 · perf 1。

## 涉及技能点
S02 固定时间戳 profile 下的解析/校验 . S03 分阶段揭示的类 API . S06 整数分金额 . S08 确定性多键排
序 . S09 精确的输出格式 . S17 错误契约设计（三种不同的失败形态） . S18 校验与防御性输入处理 . S20
序列化往返正确性

## 边写边说什么
1. **拿到题面先问三件事**：金额是分还是浮点美元（本题定死整数分，但真实面试要主动问）；时间戳格式
   是不是统一的 ISO 8601（本题定死一种 profile，说明理由：字符串排序要和时间排序一致）；
   `payment_id`/`refund_id` 重复算错误还是算幂等重试——这直接决定返回值设计。
2. **写 Part 1 时**：先讲清楚"存字典、`payment_id` 查重返回 `False` 而不是抛异常"这个设计选择的原
   因——重试是分布式系统里最常见的场景，接口应该对"重复提交同一个请求"宽容，而不是让调用方每次都要
   `try/except`。
3. **过渡到 Part 2 时**：主动列出退款可能失败的三种情况（时间戳格式错、payment 不存在、金额超额），
   并且现场说明"我打算用哪种异常类型区分它们"——`KeyError` vs `ValueError` 是一个值得展示"API 设计
   思考"的地方，不要三种情况都用一个笼统的 `Exception`。
4. **写部分退款累加时**：现场举一个"退两次刚好用完额度"和"退第二次超一分钱"的边界例子，证明自己想
   到了 `>` vs `>=` 的坑。
5. **Part 3 讲区间查询时**：主动说"现在是线性扫描，10^5 量级没问题；如果要支撑 10^7 级别的高频查
   询，我会按 `ts` 排序维护一个索引，用 `bisect` 定位区间边界"——即使不写代码，口头提到这一点也是加
   分项（对应追问②）。
6. **持久化**：解释为什么 `export_json` 必须连 `refund_ids` 集合一起序列化，而不是只存
   `refunded_cents` 累计值——因为幂等性依赖"这个 refund_id 是否已经处理过"，光有累计金额恢复不出这
   个信息。
7. **收尾**：跑一遍 worked examples 手算核对，再挑 1-2 条"面试官会怎么追问"（时区、并发写入竞态、
   审计日志）主动展开，呼应源材料里明确列出的 5 条追问方向。

## 遗留问题
- 时间戳 profile（`YYYY-MM-DDTHH:MM:SS`，naive，无 offset）是本题自己做出的范围界定，目的是让字
  符串排序 == 时间顺序这一点天然成立，避免 aware/naive `datetime` 比较的坑。时区感知的变体作为
  "Variants"/追问项（#4）列出，未实现。
- 确切的命令流协议（`PAY`/`REFUND`/`REVENUE`/`RANGE` 动词，`OK`/`DUP`/`ERROR` token）是为本题的
  io 测试框架发明的；programhelp.net 的源材料只描述了类 API，没有 CLI 协议。

## 复盘（2026-09-02）
**改了什么**
- `test_cd02.py`：problem.md 的 worked examples 1–3 原来只被"拆散"覆盖（各测试用不同金额），没有逐字
  进测试（checklist F 项）。新增 `_example_ledger` / `_example2_ledger` 两个 helper 复现例子状态，加
  `test_example1_verbatim`（revenue 1500）、`test_example2_verbatim`（800 / r3 ValueError / r1 dup /
  ghost KeyError，且三次失败都不改状态）、`test_example3_verbatim`（区间查询 dict 逐字 + round-trip）。
  现在 24 tests：part1 6 · part2 6 · part3 12；edge 9 · fmt 1 · io 3 · perf 1。`IMPL=starter` 23
  failed / 1 passed（只有 `test_empty_stdin` 天然通过）。
- `solution.py` 重构为范本（公共 API 不变）：`Payment` dataclass 取代魔法字符串 key 的 dict
  （`p["amount"]`→`p.amount_cents`，字段名与 `get_payments_by_date` 的输出 dict 一致，`asdict` 直接
  出结果）；`net_cents` property 把"剩余可退额度"和"贡献的 revenue"收成一个定义，`add_refund` 的超额
  判断变成 `amount_cents > payment.net_cents`；`_parse_ts` 改为 `_validate_ts`（返回原串），
  `get_payments_by_date` 不再对每条记录 `strptime` 两次——固定宽度 profile 下已校验字符串的序 == 时间
  序，直接比字符串（这条本来就写在 REPORT 的遗留问题里，代码现在和说法一致；perf 测试 0.58 s）；
  命令流 harness 从一个 40 行 if/elif 改为 `COMMANDS` 分发表 + 每个动词一个 `_cmd_*` 函数，错误到文本
  的映射只在 harness 层，类本身不知道 CLI 协议；`PaymentLedger` / `__init__` / `get_total_revenue` /
  `export_json` / `load_json` 补一句话 docstring，类 docstring 列出两个状态字段及"为什么要持久化
  refund_ids"。
- `problem.md` Part 1："including the no-op duplicate path's own timestamp is still checked…"
  一句语法不通，改写为"the check runs before the duplicate check — an invalid timestamp on a
  duplicate call still raises `ValueError` rather than returning `False`"，语义不变。
- black 格式化 4 个文件（docstring 后空行等），`loop/lint.sh` 通过（flake8 原本就是 0）。
**为什么**：worked examples 逐字进测试与 lint 通过是 F 项；其余是 S 项（记录用 dataclass、规则表取代
散落 if、docstring、不重复解析）。4 个 worked examples 已用 `python3 solution.py` / 直接调类逐个核
对，输出逐字不变；`IMPL=starter` 失败集合与之前一致（多出的 3 个 example 测试也失败）。
**遗留**：无。`get_total_revenue` 保持 O(n) 求和而不维护 running total（避免第二份真相），O(1) 版本
与按 `ts` 的 bisect 索引仍只作为追问 #2/#6 口头讨论，不实现。
