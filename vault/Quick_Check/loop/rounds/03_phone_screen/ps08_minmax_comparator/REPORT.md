# ps08 Min/Max with comparator — 报告

## 概述
一道四段式递进题：从"取最小值"到"按任意字段取最小或最大值"到"在调用方任意指定的顺序
下取极值"到"如果有多条记录并列该怎么办"。它精炼地展示了 Stripe 工程师经常要做的一个真实
API 设计决策：什么时候单独一个 `key`/`mode` 参数不够用了，需要一个完整的比较器？Part 3
的演示样例专门设计成能把这一点具体化 —— 在同一个平局上，规范比较器选出的赢家与 Part 1
更简单规则选出的赢家*不同*，因为它能表达一个（先 amount 后 created_at 的）复合排序，而
单个字段做不到。

## 来源与可信度
中等 —— rampatra 2020-01 都柏林电面记录（`loop/raw/en_forums.md` 第 3.3 节，P14）逐字
验证了这四段结构（"Part 1：取最小值的记录；Part 2：按参数返回最小或最大；Part 3：使用
比较器；Part 4：处理并列"），但没有包含记录 schema 或样例 I/O。本报告的记录结构
（`id, amount, created_at, country`）、所有演示样例数字，以及精确的 tie-break 规则都是
重构 —— 选择贴合 Stripe 风格，并让 Part 3 在一个可手算的例子上真正偏离 Part 1 的结果 ——
见"未解决点"。

## 各部分思路
1. `min_by_amount`：一次线性扫描，只在严格更优时替换 `best` —— 这既能找到最小值，也顺带
   免费得到"平局取先出现者"的规则，不需要单独的 tie-break 步骤。
2. `extreme(records, key, mode)`：同样的扫描结构，通过一个小的 `_key_extractor(key)`
   分发泛化（amount -> Decimal 比较，created_at -> datetime 比较，country -> 字符串
   比较）加上一个 `mode` 开关；未知的 key/mode 抛 `ValueError`，而不是静默返回错误答案。
3. `extreme_with(records, comparator)`：同样是线性扫描结构，但比较本身委托给调用方的
   `comparator(a, b) -> int`。有意用扫描而不是
   `min(records, key=functools.cmp_to_key(comparator))` —— 在下面的电面话术中讨论。
   `main()` 的 `PART 3` 使用一个规范的 `by_amount_then_created_at` 比较器，正是因为它
   需要两个字段各自独立的 tie-break 顺序，这是 Part 2 的接口无法表达的。
4. `extreme_all(records, key, mode)`：在与 Part 2 相同的 `(key, mode)` 接口上做两次
   扫描 —— 先找到极值，再收集所有提取值等于该极值的记录，按 `id` 排序。这是唯一一处
   tie-break*契约*被有意改变的地方（返回所有并列的记录而不是第一个），这个改动被明确
   点出，而不是隐含不说。

## 隐藏测试针对的坑点
- 空输入 -> 每个 part 都是 `NONE`，绝不是异常或空打印
- `Decimal` 金额比较，绝不用 `float`（包括负数金额/退款）
- `created_at` 同时解析 `Z` 和显式数字偏移量，并把它们当作同一时刻比较
- Part 4 的 `id` 排序是普通字符串顺序（`"B" < "a"`、`"user10" < "user2"`），不区分大小写
  不敏感或数值感知 —— 与 q03 的 user-id 排序规则相同，有意复用
- 重复的 `id` 不会被去重 —— 如果一对重复 id 的两个成员都并列极值，两者都出现在 Part 4
  的输出中
- Part 3 比较器参数顺序和符号约定与 C/`qsort`/`cmp_to_key` 一致（`negative` = a 排在 b
  前面）；一个只检查非 `amount` 字段的比较器也必须正常工作，因为 `extreme_with` 不对
  比较器使用哪些字段做任何假设
- Part 1/2/3 与 Part 4 的 tie-break 差异：Part 1-3 始终归结为恰好一个 id（输入顺序中第
  一个）；Part 4 是唯一返回多行的 part，且仅在并列时才会
- Part 3 的规范比较器 `by_amount_then_created_at` 在同一对并列记录上选出与 Part 1 的
  `min_by_amount` 不同的赢家 —— 两者在各自规则下都是正确的，测试专门锁定这一差异，而不
  把它当作 bug
- 未知的 `key`/`mode` 字符串抛 `ValueError`

## 复杂度与实测开销
Part 1-3：`O(n)` —— 一次线性扫描，不排序。Part 4：`O(n)` 找到极值，加上 `O(k log k)`
排序 `k` 个并列 id（`k <= n`），只要只需要极值（或并列集合），绝不对全部记录做完整的
`O(n log n)` 排序。实测：10 万条记录，金额区间较窄（构造上有大量并列），Part 4 端到端
（stdin -> stdout）远低于 2 秒，远在 256 MB 预算之内 —— 见 `test_perf_100k_records`。

## 测试清单
33 个测试 —— part1: 9 · part2: 8 · part3: 7 · part4: 9（含 6 个 io、1 个 perf）；edge 11
· fmt 1 · io 6 · perf 1。

## 涉及技能
S03 把记录建模为小型有类型结构（NamedTuple），而不是原始 CSV 行 · S08 带明确 tie-break
的确定性排序，在 Part 4 中有意改变 · S12 时间戳解析/比较（Z 与显式偏移量）· S19 增量式
设计（Part 4 包装 Part 2 的接口；Part 3 独立作为更通用的机制）· S21 标准库熟练度
（Decimal、datetime.fromisoformat、讨论但未使用 functools.cmp_to_key，转而用线性扫描）

## 电面话术：边写边说什么
1. **读题时**：在写代码前确认每个 part 的 tie-break 规则 —— Part 1-3 是"输入顺序中第一个"，
   Part 4 是"返回所有" —— 并明确说这是两个不同的契约，不是需要掩盖的不一致。
2. **写 Part 1 时**：大声指出一次 `if val < best_val: best = val` 扫描能同时给你最小值
   和"平局取先出现者"规则，不需要单独的 tie-break 步骤 —— 说起来很便宜，而且能提前堵住
   "你怎么处理并列"这个追问。
3. **写 Part 2 时**：提到对未知 key/mode 抛 `ValueError` 是有意选择 —— "我宁愿在打错 key
   时大声失败，也不要静默地什么都不比较然后返回错误答案。"
4. **写 Part 3 时**：这是应该放慢速度的地方。说明为什么用手写线性扫描而不是
   `min(records, key=functools.cmp_to_key(comparator))`：两者在这里实际上都是 `O(n)`，
   但扫描把 tie-break 规则保留在一个可见的 `if` 条件里，不需要把每条记录都包进一个
   `cmp_to_key` 对象；如果你还需要完整的排序结果用于别的地方，`cmp_to_key` 才是正确
   选择，但对于单个极值来说它做了题目不需要的额外工作。然后手动过一遍 r2/r3 的平局，
   证明比较器确实选出了与 Part 1 不同（且正确）的答案。
5. **写 Part 4 时**：指出这是唯一一个契约本身发生改变的 part —— "我不是在 Part 1-3 的
   单赢家函数上硬塞并列处理；Part 4 是一个新函数，有新的返回类型，我直接建立在 Part 2
   的 key/mode 提取逻辑之上，让两者保持同步。"
6. **收尾**：手动跑一遍演示样例，然后主动提出自然的追问 —— "如果你想要基于比较器而不是
   key/mode 的并列，我会把 extreme_all 里的相等性检查换成
   `comparator(record, best) == 0`，勾勒一下而不必真的写出来" —— 这正是面试官会加分的
   那种主动暴露边界的做法。

## 未解决点
- 只有四段结构本身和其一句话描述来自来源验证；记录 schema、字段名，以及本 problem.md
  中的每一个演示样例数字都是重构，选择保持内部一致且可手算验证。如果出现带真实样例 I/O
  的转录，应据此核对 schema 和数字。

## 复盘（2026-09-02）
- 逐条对照 `loop/tasks/review_checklist.md` 复核：problem.md 四个 Part 的全部 worked examples（Part 1
  单值、Part 2 四组 key/mode、Part 3 比较器、Part 4 两组并列、空输入 `NONE`）已用 `solution.py` 逐字
  重跑核对（stdin → stdout），全部与文档一致，未发现规则歧义。
- `solution.py` 逻辑复核：`min_by_amount`/`extreme`/`extreme_with` 三者都是同一个"严格更优才替换"的
  单趟扫描骨架，平局天然保留输入序中先出现的记录，无需额外 tie-break 分支；`extreme_with` 未对
  comparator 做任何字段假设（`test_extreme_with_custom_comparator_ignores_amount` 覆盖）；`extreme_all`
  两趟扫描复用 `_key_extractor`，不复用单赢家函数（返回类型不同，独立实现是对的）；未知 `key`/`mode`
  均正确抛 `ValueError`；`created_at` 的 `Z`/显式偏移量归一化正确比较为同一时刻；未发现功能性 bug
  （F 项 0 处需修）。`starter.py`/`starter_template.py` 内容仍完全一致，公共 API 与 `solution.py` 一致。
- 修复：`loop/lint.sh --fix` 对 `solution.py`/`starter.py`/`starter_template.py` 做了纯格式化（模块
  docstring 后补一行空行，本地 black 版本差异导致），无语义变化；`loop/lint.sh` 复检通过（black 110 列
  + flake8 F 类 0，flake8 单独核实无任何警告）。
- 回归：`rtk proxy python3 -m pytest loop/rounds/03_phone_screen/ps08_minmax_comparator --tb=short`
  33 passed；`IMPL=starter` 同目录 26 failed / 7 passed（余下 7 处全部是"空输入 → None/NONE"的平凡
  用例，starter 桩代码的默认返回值恰好满足，不构成空洞测试）。
- 遗留：无功能性遗留项。问题面来源置信度为 medium（仅四段的一句话描述可验证，具体字段名/schema/worked
  numbers 为本仓库重构），problem.md 的 未解决点 已如实标注，不需要在代码侧处理。
- 文章：`loop/study/30-articles/ps08_minmax_comparator.md`（152 行）。
