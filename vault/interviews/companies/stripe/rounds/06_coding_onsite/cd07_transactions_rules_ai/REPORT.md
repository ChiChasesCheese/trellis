# cd07 Transactions + rules（AI Programming Exercise）— 报告

## 概述
一个针对一批交易的三阶段规则引擎（`ALLOW|BLOCK if <condition>`）：先是关键字相等，然后是比较运算符
加 `in [...]`，最后是完整的 `and`/`or`/`not`/括号递归下降语法，并带每条规则的错误报告。它是
`problems/q12_platform_balance_radar_rules` 的 Radar 语法在 AI 辅助轮的姊妹题，特意做得更小（没有
带引号的常量、没有 `:field:` 标记、没有余额账本），因为真实轮次的预算是有 AI 助手约 30 分钟，而不是
手写的 75 分钟。

## 来源与可信度
中等。两个独立来源（interviewdb.io 的 AI-programming-exercise 指南，2026-06-09；interviewfox.ai 的
HackerRank OA 指南，2026）都认可这一轮的存在、形式（HackerRank + 内嵌 AI 聊天，约 30 分钟）、评分
维度（"你能不能指挥/验证/调试 AI，是否自己写测试"），以及题目形态（"交易 + 规则，ALLOW/BLOCK if
条件，从关键字匹配递进到 AND/OR 布尔逻辑"）。两者都没有公布逐字的输入输出样例、字段列表或确切语法——
`RULES`/`TRANSACTIONS` 的 stdin 协议、六字段交易 schema、`(rule k)` 输出后缀，以及 Part 3 的
`ERROR line k:` 报告都是本仓库的重建，目的是与 `problems/q12` 自身的 parse→model→evaluate house
style 保持一致，而不是为同一技能再发明第四种约定。

## 分 Part 的思路
1. `RULE_RE` 把每一行 `ALLOW|BLOCK if <condition>` 拆开；Part 1 的语法通过贯穿解析器的 `part` 参数，
   把 `<condition>` 限制为单个 `field == value` 比较。
2. 同一套 tokenizer/parser，`part=2` 解锁 `!=`、`>`、`<`、`>=`、`<=`，以及 `field in [v1, v2, ...]`。
   `_compare` 复用了 q12 自身的数值/字符串兜底规则（两边都能解析成整数就按数字比较，否则比较去空格后
   的字符串），因此 `amount == 0100` 能匹配 `amount == 100`。
3. `part=3` 解锁布尔语法（`_or` → `_and` → `_not` → `_primary`），`not` > `and` > `or` 的优先级
   直接由递归结构本身天然保证，括号子表达式通过 `_primary` 的 `LP` 分支处理。tokenize 或 parse 失败
   的规则会抛出 `RuleError`，按规则逐条捕获，这样一行坏规则不会拖垮整批；只有 Part 3 会把它呈现为
   `ERROR line k: <reason>`（Part 1/2 静默跳过，因为题面的错误处理要求只限定在 Part 3）。
   字段 vs. 字面量的判定（`_resolve`）是按操作数逐个判断，而不是按规则整体判断：一个裸 token 如果
   命中已知的交易列名（`id`、`amount`、`currency`、`country`、`card_brand`、`merchant`）就去交易里
   查值，其余一律当作字面量字符串。这正是该语法能完全省掉引号（不像 q12 需要 `:field:`/`"const"`
   标记）的同时，还能支持字段对字段的比较（`country == country`）而不用特殊处理的原因。

## 隐藏测试瞄准的坑
- `(rule k)` 的行号必须计入 `RULES` 里的每一行，包括之后被 `ERROR` 掉的行——被跳过的规则之后的规则
  不会往前重新编号
- 默认（无匹配）**完全没有** `(rule k)` 后缀，与命中某个 k 的规则区分开
- 运算符两侧空白的容忍度（`amount>=5000` vs `amount >= 5000`）——一个朴素的 `line.split(" ")` 解析器
  （题面自己的"常见错误"一节点名的 AI 生成失败模式）在无空格形式下会崩
- `and` 优先级比 `or` 紧，`not` 只作用于紧跟着的单个 unary/primary，而不是整个 `and`/`or` 链——两者
  都有专门设计成"优先级读错就会得出不同答案"的测试用例，而不只是恰好殊途同归
- `in [...]` 是真正的集合成员判断，而不是意外的子串匹配（`USA` 不能满足 `country in [US]`）
- 畸形的 Part 3 规则（括号不匹配、缺操作数、关键字当操作数、动作关键字写错）各产生恰好一条
  `ERROR line k:`，并被跳过，不会导致整个运行失败
- 2,000 条编译后的规则 × 20,000 笔交易，不能对每笔交易重新解析规则文本（规则只编译成 AST 一次，
  之后在整批交易中复用）

## 复杂度与实测开销
编译一次是 O(rules)，求值是 O(transactions × matched-rule-position)（每笔交易在第一条匹配的规则处
停止）。2,000 条规则 / 20,000 笔交易（Part 3，最坏情况：很多规则永远不匹配，导致大多数交易要扫得
很深）：约 0.3 秒，远低于 5 秒 / 256 MB 的预算。

## 测试清单
23 个测试——part1: 6（含 1 个 io）· part2: 5 · part3: 12（含 1 个 io、1 个 perf）。edge: 14 · fmt: 1 ·
io: 3 · perf: 1。

## 涉及的技能
S02 条件字符串的分词/解析 · S06 数值/字符串比较兜底 · S10 first-match-wins 的有序规则求值 ·
S18 校验（按规则报 `ERROR` 而不崩溃整批）· S19 渐进式语法（每个 part 都是下一个 part 的严格子集）·
S24 Radar 规则引擎词汇（与 q12 共用，在 AI 辅助轮的规模上）· S25 指挥/审查 AI 生成代码
## 电面话术：边写边说什么
1. **读题时**：先大声确认协议边界——"`RULES` 和 `TRANSACTIONS` 两个 section 靠一行独立的 header
   区分，行数不定长；一行交易少于 6 列时，缺的列我当空字符串处理，不报错"——把隐含契约说出来。
2. **写 Part 1 前**：一句话说明分层——"我打算把条件文本的解析和对交易求值分开，这样后面加运算符、
   加布尔逻辑都只是扩展解析这一层，求值和主循环不用大改"。
3. **写 Part 2 时**：主动点出数值/字符串双轨比较——"`==`/`!=` 我先看两边是不是都能转成整数，能就按
   数字比，不能就按去空格后的字符串比，这样 `amount == 0100` 才能匹配 `amount == 100`"。
4. **写 Part 3 前**：先口头画出优先级——"`not` 最紧，然后 `and`，最后 `or`，我用递归下降实现，
   `or_expr` 调 `and_expr`、`and_expr` 调 `unary`，优先级天然由函数调用顺序保证，不用额外维护
   优先级表"。
5. **写错误处理时**：说明设计选择而不是默认行为——"题面只要求 Part 3 报 `ERROR line k`，Part 1/2
   我选择静默跳过写错的规则；如果你们希望 Part 1/2 也报错，我现在就能把这个判断放宽一行"。
6. **收尾**：主动提一句关于 AI 轮的自我审查——"如果是用 AI 生成的版本，我会重点检查三处：`in [...]`
   是不是被写成了子串匹配、`and`/`or` 优先级有没有被拍平、默认方向是不是写反成了 BLOCK"——呼应
   problem.md 里"AI 生成代码常见的五个坑"，证明这不是背答案而是真的理解每个坑背后的原因。
7. **被追问复杂度时**：「规则先编译成 AST 一次，之后对每笔交易只做树遍历，不重新解析文本；最坏情况
   是每笔交易都要扫到最后一条规则，`O(rules × transactions)`，如果规则以单字段等值判断为主，可以
   按字段建索引进一步剪枝。」
## 复盘（2026-09-02）
- **发现（F）**：REPORT.md 缺少 CONVENTIONS/checklist 要求的"电面话术/边写边说"节——已补上。检查
  未发现半成品痕迹（无遗留 TODO/调试 print/未完成分支），LEDGER 里"代理撞 limit 前已完成"这条记录
  与实际代码状态一致：`solution.py`/tests/starter 三件套完整、lint 干净、23 个测试全绿。
- **发现（S）**：`test_in_list_empty_single_and_several_items` 的名字承诺测了"empty"（零元素）的
  `in []` 情况，但原测试体只覆盖了 3 元素和单元素两种，没有真正测零元素——已补一条 `country in []`
  永不匹配的断言。problem.md 缺少本仓库其它题目都有的"面试官会怎么追问"节——已补 6 条，覆盖 AI 轮
  评分标准、优先级实现位置、语法扩展性、错误处理的题面 vs. 自选边界、最坏复杂度、字段/字面量判定
  依据这几个方向。
- **未改动**：`solution.py` 本身未发现 F 级问题——tokenizer/parser/evaluator 三层分离清晰，
  worked examples 逐字核对全部通过，lint（black -l 110 + flake8 F 类）一次性通过，无需 `--fix`。
- **遗留**：无。`_compare` 对 `==`/`!=` 的数值兜底目前对 Part 1/2/3 统一生效，problem.md 的 Part 1
  措辞（"值按去空格字符串比较"）与 Part 2 措辞（"两边都能转成整数就按数字比"）在字面上略有张力，
  但两种解释在所有 worked examples 和当前测试上给出相同结果，本次未改动此行为，仅在这里记录供后续
  如需收紧 Part 1 语义时参考。
