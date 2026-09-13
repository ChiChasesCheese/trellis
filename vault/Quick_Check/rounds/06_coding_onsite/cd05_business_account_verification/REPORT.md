# cd05 Business Account Data Verification — 报告

## 概述
一个作用于嵌套 `account` JSON 树的可配置规则引擎：`requires`（必须非空）、`when`（全部匹配才
生效）、`one_of`（至少一个满足即可的分组）、以及 `owners[].first_name` 数组通配。Stripe 真实的
入驻流程正是这样运作的——表单字段不是写死的，而是由一张规则表驱动，这样合规团队可以在不发版的
情况下增改要求。全部难点都在路径解析语义上（缺失 vs 空 vs 类型不对），而不在算法本身。

## 来源与可信度
规则 schema 部分可信度高（源材料给出接近逐字的 JSON schema 级别描述：`when`/`requires`/
`one_of`、路径语法、"非空"定义、输出格式、全部四项数值约束）。2 处独立提及：
`1point3acres interview/problems/ad817329-...`（完整规格）和 `interview/thread/1155516`
（VO 挂经提到同一任务名，无技术细节）。Worked examples 以及少数未文档化的行为（通配基础缺失时的
回退、`one_of` 与通配的交互）是本仓库自己的重构补全——已在 problem.md 的 Clarifications
小节里明确标注，因为源文本从未逐字给出自己的 worked example。

## 分 Part 的思路
1. Part 1：`_expand()` 用 `.` 拆分路径后对 account 字典逐段解析；不含 `[]` 的普通 `requires`
   列表每条规则最多只产生一个 (path, value) 对。把所有规则里缺失的 token 收集进一个 `set`
   （去重），输出前 `sorted()`。
2. Part 2：同一个 `_expand()` 现在还处理 `owners[]` 这类通配段——遍历数组，对每个元素递归，
   把下标烙进解析出的路径字符串（`owners[2].first_name`）；基础值缺失或不是列表时回退成
   *未展开的* 字面路径，作为单个 token 输出，而不是默默什么都不做。`_when_matches()` 是另一个
   独立的、不做通配的单值解析器（`equals`/`present`），因为本题范围内 `when` 条件从不需要
   数组展开。`one_of` 复用同一个单值解析器：第一个解析到非空值的路径就短路判定为"满足"，否则
   按声明顺序输出 `one_of(f1|f2|...)`（内部不排序——只有整段 token 参与最终排序）。

## 隐藏测试瞄准的坑
- `equals` 对类型敏感（字符串 `"true"` != 布尔 `True`）——朴素地用 `str(value) == v` 会错误地
  通过这个判断。
- `present: false` 匹配的是"路径不存在"（不是"值为假值"）——很容易和别处用的"非空"定义混淆。
- 空的通配数组（`"owners": []`）视为 vacuously 满足——朴素实现可能把"没有 owner"本身当成违规。
- 通配基础整体缺失（`owners` key 不存在）绝不能默默产生零输出（那样会掩盖真实的缺口）；应回退
  输出未展开的字面路径。
- 不同规则要求同一字段时要去重——朴素的列表 append 实现会重复打印。
- 排序必须是对全部 token 一次性显式 `sorted()`（普通 requires 路径和 `one_of(...)` 字符串混排），
  而不是分别排序两组再拼接——worked 的 Part 2 示例特意构造成 `one_of(...)` 排在 `owners[1]...`
  之前（因为 `'n' < 'w'`），这在"requires 先、one_of 后"的拼接顺序下会悄悄出错。
- `when` 是整个条件列表的 AND——只要有一个条件不满足就跳过整条规则，即便列表里更早的条件匹配了
  也一样。

## 复杂度与实测开销
O(实际解析出的路径展开总数)，上界为 `rules × requires_per_rule × 平均数组长度`——线性于实际
访问到的 JSON 叶子数，最坏病态情况下也不超过 `account` 节点数上限（10^4）乘以规则数上限
（200），实践中远低于此，因为大多数规则只涉及少量叶子。性能测试：3000 个 owner 的账户、200
条规则，其中一条对全部 3000 个 owner 展开——远在 2 秒 / 256 MB 的预算之内（CPython 3.12 上通常
< 0.1 秒，占用几 MB）。

## 测试清单
21 个测试——part1: 8（含 1 个 io）· part2: 13（含 1 个 io、1 个 perf）；edge: 8 · fmt: 2 ·
io: 2 · perf: 1。

## 涉及的技能
S02 解析（JSON 而非 CSV）· S03 树形路径解析 · S04 分组去重 · S08 确定性排序（混合格式 token）·
S09 精确格式化（`one_of(...)`、带下标路径）· S18 校验规则引擎设计 · S19 渐进式设计
（Part 1 → 2 增加 `when`/`one_of`/通配）

## 复盘（2026-09-02）
逐条对照 `loop/tasks/review_checklist.md` 复核，结论：solution.py 在 review 前已经完全正确——21
个测试全绿（含全部 worked examples 手工逐字核对：Part 1 缺失列表、`VERIFIED` 分支、Part 2 的
`one_of(...)`/通配下标输出都精确匹配 problem.md），`IMPL=starter` 下 21 个测试全部按预期失败，
`starter.py`/`starter_template.py` 内容一致。**没有发现 F 级 bug**——路径解析、`when` 的 AND 短路、
`one_of` 的短路满足、通配数组的 vacuous-true 与缺失回退、排序去重全部与 problem.md 逐条一致。

改动（均为 S 级打磨，不改变任何输出行为）：
- `solution.py`：给 `_split`/`_when_matches`/`_missing_for_requires`/`_missing_for_one_of`/
  `part1`/`part2` 补了一句话 docstring（此前只有 `_is_nonempty`/`_expand`/`_resolve_one` 有），
  满足 checklist "docstring 一句话说清做什么"。
- `test_cd05.py`：`test_perf_large_account_and_ruleset` 里 `rng = random.Random(0)` 被创建但从未
  使用（`knocked_out` 原来是固定的 `range(0, 3000, 7)` 步长模式，flake8 F841 报未用变量）——改成
  `rng.sample(range(3000), 429)`（429 是原步长模式的元素个数，保持断言 `len(lines) ==
  len(knocked_out)` 不变），既修了 lint 又让这条 perf 用例真正符合 CONVENTIONS "perf 用
  `random.Random(0)`" 的要求，而不是名义上创建了 rng 却不用。
- `black --fix` 在 `solution.py`/`starter.py`/`starter_template.py`/`test_cd05.py` 四个文件的
  module docstring 后各加了一个空行（新版 black 风格），纯格式改动。

回归：`rtk proxy python3 -m pytest loop/rounds/06_coding_onsite/cd05_business_account_verification
--tb=short` 21 passed；`IMPL=starter` 同目录 21 failed；`loop/lint.sh
loop/rounds/06_coding_onsite/cd05_business_account_verification` 通过（black 无需改动，flake8 无
输出）。

遗留：无。这题的三处"本仓库补全"细节（数组整体缺失回退、`one_of` 不支持通配、`present` 的精确
语义）在 problem.md 的 Clarifications 里已经写清楚，solution.py 与之完全对齐，不需要进一步调整。
