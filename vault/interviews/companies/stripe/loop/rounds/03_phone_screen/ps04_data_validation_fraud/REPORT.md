# ps04 Transaction Data Validation / Fraud Report — 报告

## 概述
四阶段交易分诊：记录是否完整、是否违反硬性规则（金额范围、被封禁的支付方式）、是否符合
用户自身历史行为，以及 —— 当多项都出错时 —— 打印哪两项、按什么顺序。全部难点在于跨分节
stdin 协议（rules/blocklist/profiles/transactions）的状态管理，以及在 Part 4 中把
"优先级 + 截断"规则做得完全正确，而不在于任何单一算法。

## 来源与可信度
四部分结构的可信度高：一篇 2025-11-30 的 LeetCode Discuss 面经（经 programhelp 转载）
逐一点名了全部四个部分，每个部分附一句话规则，包括关键短语"至少 50% 的行为属性"（Part 3）
和"最多两个错误码...保持列对齐"（Part 4）。interviewdb.io 证实这道题（作为两个分别追踪
的条目"Data Validation"和"Fraud Reports"）在 2026 年仍然活跃。精确的输入协议
（分节名称/顺序）、profile schema 和优先级顺序都是本仓库自行重构的 —— 不同于 q03/q05
那种有仓库自带样例的题目，本题没有逐字的 I/O 样例可参考。

## 各部分思路
1. `check_row(fields, checks=1, ...)`：7 个 trim 后的字段中任意一个为空（包括补齐的缺失
   末尾列）-> `MISSING_FIELD`。
2. `checks=2` 增加：`Decimal` 金额相对 `RULES` 的闭区间范围检查，以及对 `payment_method`
   不区分大小写的 `BLOCKLIST` 成员检查。两者互相独立评估，也独立于 `MISSING_FIELD`。
3. `checks=3` 增加对用户 `PROFILES` 行的 3 属性比较（国家归属、一天中的小时范围、
   profile 专属的金额范围）；`< 2` 项匹配 -> `SUSPICIOUS`。用户没有 profile ->
   该检查完全跳过（永不标记）。
4. `part4` 复用 `checks=3` 的完整评估，然后截断为 `codes[:2]`（构造时已按优先级顺序，
   无需重新排序），并将 `txn_id` 按本次调用中实际出现的最长 id 做列对齐。

## 隐藏测试针对的坑点
- 用固定常量而不是本批次实际最长的 `txn_id` 计算列宽
- 把"3 项中匹配 2 项"当成可疑（">= 2" 和 "> 2" 的差一错误 —— 3 的 50% 四舍五入是 2，
  不是"超过一半"，超过一半其实也是 2，所以这个坑只在代码层面隐蔽，数学上并不模糊）
- 在评估 `SUSPICIOUS` 时，对没有 profile 行的 `user_id` 崩溃（或错误地标记
  `AMOUNT_OUT_OF_RANGE`）
- 在 Part 4 截断前对代码列表重新排序或去重，而不是依赖插入顺序本身已经是优先级顺序
- 在 `PART 1`/`PART 2` 下评估了 Part 3/4 的规则（`checks` 门控必须真正生效）
- 金额上使用浮点累加 —— 本方案全程不接触 `float`，只用 `Decimal`

## 复杂度与实测开销
交易数量上 O(n)，profile 数量上 O(u)，都是单次遍历配合 dict 查找（没有嵌套扫描）。
10 万条交易 / 2000 个 profile（Part 4，完整评估）：约 0.4 秒，约 15 MB RSS（预算
2 秒 / 256 MB）。

## 测试清单
17 个测试 —— part1: 3 · part2: 3 · part3: 3 · part4: 5（含 1 个 io、1 个 perf、1 个
fmt）· 另有 1 个 io 测试归在 part1 下（空 stdin）。edge: 6 · fmt: 1 · io: 2 · perf: 1。

## 涉及技能
S02 分节 stdin 解析 · S05 闭区间检查 · S06 `Decimal` 货币 · S08 确定性排序 · S09 精确
列对齐格式化 · S18 校验与优先级错误码 · S19 增量式规则类别（`checks` 门控）· S24 领域知识
（风控分诊，与 q15 的 KYC 不同）

## 电面话术：边写边说什么
- 先把优先级和"最多两个错误码"复述给面试官确认："如果一笔交易同时命中三四条规则，Part 4 只保留优先级最高
  的两个，对吗？其余的丢弃，不是合并展示。"——这类"最多 N 个"的截断规则最容易漏测，先确认能省后面返工。
- 设计 `check_row` 时说明为什么用一个 `checks` 整数而不是四个布尔开关："这样 Part n 的语义就是'评估类别
  1..n'，Part 4 复用 Part 3 的判定逻辑，只是输出格式不同——不用为每个 part 重写一遍规则。"
- 讲 SUSPICIOUS 规则时用具体数字过一遍："3 个属性里 ≥2 个匹配才算 OK，也就是 0 或 1 个匹配才 SUSPICIOUS——
  这是'at least 50%'在整数属性个数下的直接写法，不需要算百分比再四舍五入。"
- 遇到"用户没有历史画像怎么办"的追问，主动给出默认假设并说明理由："没有画像就没法比较，我选择不标记
  suspicious——如果面试官希望反过来（没画像更可疑），改一行判断就行，我先按更保守的假设写。"
- 收尾如果还有时间：主动提出加一个 `--part 4` 的列宽在流式场景下如何处理（要不要固定宽度而不是动态计算，
  因为流式场景取不到"最长 id"）——展示对边界条件的延伸思考。

## 复盘（2026-09-02）
- 逐条对照 `loop/tasks/review_checklist.md` 复核：problem.md 四个 Part 的 worked examples 已用
  `solution.py` 逐字重跑核对（直接喂 stdin，对比 stdout），四段输出与文档字符级一致，未发现规则歧义或
  文档-代码不一致。
- `solution.py` 逻辑复核：`check_row` 的四类规则相互独立判断（不用 `elif`）、`checks` 等级正确门控
  Part n 只评估类别 1..n、`SUSPICIOUS` 的插入顺序天然等于 `PRIORITY` 常量顺序（Part 4 截断 `codes[:2]`
  无需重排）、无画像用户正确跳过 `SUSPICIOUS`、金额缺失不会额外触发 `AMOUNT_OUT_OF_RANGE`、金额区间/
  黑名单大小写不敏感/列宽动态计算均按题面实现，未发现功能性 bug（F 项 0 处需修）。
  `starter.py`/`starter_template.py` 内容仍完全一致，公共 API（`partN(lines) -> list[str]`）与
  `solution.py` 一致。
- 修复：`loop/lint.sh --fix` 对 `solution.py`/`starter.py`/`starter_template.py`/`test_ps04.py` 做了
  纯格式化（模块 docstring 后补一行空行、超长字面量列表按 black 的 magic-trailing-comma 规则逐行展开），
  无语义变化；`loop/lint.sh` 复检通过（black 110 列 + flake8 F 类 0）。
- 回归：`rtk proxy python3 -m pytest loop/rounds/03_phone_screen/ps04_data_validation_fraud --tb=short`
  17 passed；`IMPL=starter` 同目录 15 failed / 2 passed（余下 2 处是空输入的平凡用例，starter 的默认
  `return []` 恰好也满足，不构成"空洞测试"）。
- 遗留：无功能性遗留项。`PRIORITY` 常量当前只用于文档/注释说明（`check_row` 内 append 顺序需要人工保持
  与其一致），代码里已有显式注释标注这一不变量（"insertion order below IS priority order -- do not
  re-sort"）；若未来规则类别继续增多，可考虑改成显式按 `PRIORITY` 顺序迭代的规则表以消除该隐式耦合，
  当前 4 类规模下不值得为此增加抽象层。
- 文章：`loop/study/30-articles/ps04_data_validation_fraud.md`（138 行）。
