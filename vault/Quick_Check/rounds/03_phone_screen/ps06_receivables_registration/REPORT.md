# ps06 Receivables registration — 报告

## 概述
一道包装成真实 Stripe 巴西合规流程（向央行登记应收款）的 CSV 聚合题。Part 1 是纯粹的
分组 + 整数分求和；Part 2 才是真正区分候选人水平的地方 —— 处理格式错误行时要跳过并
*计数*（而不是静默丢弃），带符号金额（退款），以及一条日期归一化规则（周末的支付日期
顺延到下一个工作日）必须在构建聚合 key *之前*运行，而不是之后 —— 这是常见的顺序颠倒
bug。

## 来源与可信度
中等 —— csoahelp.com 2024-10-04 的转录给出了场景（巴西应收款）、函数名
（`register_receivables`）、精确的 CSV 字段列表
（`customer_id,merchant_id,payout_date,card_type,amount`）、聚合 key
（`merchant_id + card_type + payout_date`），以及 4 段面试结构（澄清 → 方案讲解 →
追问 → 行为面）。它**没有**公开精确的输出格式或 Part 2 的业务规则 —— 周末顺延规则、
具体的坏行分类、以及 `SKIPPED n` 尾行都是本报告的重构，写成一个合理、常见的追问方向，
而非逐字转录。已在 problem.md 的"见过的变体"一节明确标注。

## 各部分思路
1. **Part 1**：解析 `customer_id,merchant_id,payout_date,card_type,amount`，把
   `amount` 转换为整数分（`_amount_to_cents`），累加进以
   `(merchant_id, card_type, payout_date)` 为 key 的 `defaultdict(int)`，按
   `(merchant_id, payout_date, card_type)` 排序渲染 —— 注意*输出*列顺序
   （`merchant_id,card_type,payout_date,total`）与*排序 key*顺序不同，这正是隐藏测试
   会针对的细节。
2. **Part 2**：同样的聚合，外加每行的校验门（字段数 == 5，金额匹配
   `-?\d+\.\d{2}`，日期匹配 `YYYY-MM-DD`**且**通过 `datetime.strptime` 解析为真实
   日历日期），任何一项失败就递增跳过计数；只有通过校验的行才会在用作分组 key *之前*
   把 `payout_date` 顺延（周六 +2，周日 +1），这样同一个 merchant/card_type 的周六
   行和周日行才能正确合并进同一个周一组。

## 隐藏测试针对的坑点
- 输出列顺序与排序 key 顺序是两个不同的元组 —— 容易混淆
- `2026-02-30`（不存在的日期）vs `2026/08/03`（分隔符错误）—— 两者都非法，但原因不同；
  只做形状正则校验的方案会漏掉日历合法性这一情况
- `150.5` / `150` / 空字符串金额 —— 一位小数、没有小数、空字符串都非法，与仅仅是负数但
  格式正确的 `-15.50` 不同
- 在构建 key *之前*而不是之后顺延日期 —— 分组后再顺延会产生两个独立的组（顺延前的周六
  组和原本的周一组），而不是一个合并组（`test_saturday_and_sunday_both_roll_to_same_monday`
  正是针对这一点）
  净额恰好为 `0.00` 的组仍必须打印为一条真实的登记行
- 没有任何行被跳过时 `SKIPPED 0` 仍必须是最后一行（不能走"只有 n > 0 才打印 SKIPPED"
  的捷径）
- 跨月/跨年边界的周末顺延（`2026-01-31` 周六 -> `2026-02-02` 周一）

## 复杂度与实测开销
解析+聚合 O(n)，排序 O(g log g)，其中 `g` = 不同组的数量（对任何现实批次 g << n）。
实测：10 万行（穿插约 1/5000 比例的格式错误行）端到端经 stdin -> stdout 远低于 2 秒，
在 256 MB 预算内绰绰有余 —— 见 `test_perf_100k_rows`。

## 测试清单
21 个测试 —— part1: 6（含 1 个 io）· part2: 12（含 1 个 io、1 个 perf）；edge 11 ·
fmt 1 · io 3 · perf 1。

## 涉及技能
S02 解析/格式错误行处理 · S04 分组/聚合 · S06 整数货币（BRL 分，绝不用浮点累加）· S08
确定性多键排序 · S09 精确格式化（无货币符号，带符号总额）· S12 日期处理（日历合法性 +
工作日顺延）· S18 校验与错误路径（跳过并计数，绝不因坏输入崩溃）

## 电面话术：边写边说什么
1. **澄清阶段** (面试第①段)：主动问三件事——`amount` 到底是分还是两位小数字符串（本题定死两位小数，
   但真实面试里这是第一个该问的问题）；输出要不要带货币符号（登记到央行的内部文件通常不带）；聚合
   总额如果是负数（退款超过消费）该怎么办，是报错还是照实输出。不要默认，直接问。
2. **写 Part 1 时**：边写边强调"金额我用整数分累加，绝不用 float"，并且提前说明输出列顺序
   (`merchant_id,card_type,payout_date,total`) 和排序 key 顺序
   (`merchant_id,payout_date,card_type`) 是两回事——这是本题最容易在口头描述里被自己绕晕的地方，主动
   讲清楚等于提前排掉一个追问。
3. **过渡到 Part 2 时** (面试第②段思路讨论)：先列出"哪些行是坏行"的分类（字段数、金额格式、日期格式/
   日期合法性），再决定"skip + count"而不是"skip 但不计数"或"直接抛异常"——说明这个选择是因为央行提交
   场景下，静默丢弃数据是不可接受的，必须有审计痕迹（`SKIPPED n`）。
4. **写周末顺延规则时**：显式说"我要在这行数据进入聚合字典**之前**做日期归一化，不然周六和周一的同一
   商户流水会被分成两组"——这是本题唯一真正容易挖坑的地方，主动指出比等面试官问出来更加分。
5. **追问阶段** (面试第③段)：参考 problem.md 末尾"面试官会怎么追问"列表——幂等重复提交、10^7 行流式处理、
   多币种、时区/夏令时、节假日日历接入、更正/冲正记录设计，任选 2-3 条主动展开讨论，展示系统设计视角
   而不仅仅是把题做对。
6. **收尾**：跑一遍 worked examples 手算核对，再补一句"如果给我历史提交批次的哈希/幂等键，我可以把
   `SKIPPED` 之外再加一个 `DUPLICATE` 计数，防止重试导致重复登记"——呼应第④段行为面试常问的"你怎么考虑
   生产环境的鲁棒性"。

## 未解决点
- csoahelp 的转录没有公开 Part 2 的具体业务规则（本 REPORT 已在 problem.md 的 Variants 一节明确标注：
  周末顺延、坏行分类、`SKIPPED n` 尾行都是本套件按 Stripe 电面惯用"happy path -> robustness/business
  rules"模板做的合理重建，不是逐字转录）；如果后续拿到更精确的原题转录（尤其是官方 Part 2 措辞），应
  回来核对本文件的规则定义是否需要调整。
- 未确认真实面试是否要求处理带引号/嵌入逗号的 CSV 字段（本题假设简单 split(",") 足够，字段本身不含
  逗号），如果拿到反例应补充 RFC4180 引号解析。

## 复盘（Fable 5.1，2026-09-01）
**改了什么**
- `solution.py` 重构为同一条流水线 `_data_lines → 解析成 Row → _aggregate → _render`：Part 1 用
  `_parse_row_trusted`，Part 2 用 `_parse_row_checked`（返回 `None` 即坏行）+ `_roll_weekend(row)`，两个
  part 共用 `_aggregate/_render`，不再各自维护一份聚合循环（原来 Part 2 是 Part 1 的复制粘贴版）。
- 规则集中为常量：`FIELD_COUNT`、`AMOUNT_RE`、`DATE_RE`、`ROLL_FORWARD_DAYS = {SAT: 2, SUN: 1}`；`Row`
  用 `NamedTuple` 命名字段；日期合法性改用 `date.fromisoformat`（正则先定形状）；`AMOUNT_RE.match` →
  `fullmatch`；`main` 用 `PARTS` 表分发（starter_template/starter 同步）。
- problem.md 补两句定死：字段两侧空格容忍（实现一直如此，题面没写）；Part 1 不做周末顺延。
- 测试 +2：Part 1 周六日期不顺延（区分两个 part）；格式化 `1234567.89` 无千分位、`-0.05` 保留前导 0。
  21 → 23。lint：black 110 + flake8 通过（此前 4 个文件 black 未格式化）。

**为什么**：checklist S 项"后 part 复用前 part / 规则用表不用散 if / 解析-逻辑-格式化分离"；原实现
Part 2 里"归一化在入 key 之前"这条关键规则埋在 12 行循环中间，现在是 `rows.append(_roll_weekend(row))`
一行加注释，面试官 60 秒能看到。

**遗留**：Part 2 规则仍是重建（见 未解决点）；带引号/嵌入逗号的 CSV 未处理（题面明确假设简单 split）。
