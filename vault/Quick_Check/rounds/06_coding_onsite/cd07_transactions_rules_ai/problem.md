# cd07 · Transactions + Rules (AI Programming Exercise) — 关键字匹配 → 比较运算 → AND/OR/NOT

**类型：** 现场面试 "AI Programming Exercise"（2026 新增轮，HackerRank 内嵌 AI 聊天窗口）· **阶段：**
有 AI 辅助约 30 分钟（"有点像轻量版 Cursor"）/ 本仓库也把它当作 60 分钟手写轮来演练，共 3 个 Part ·
**最近一次出现：** 2026-06-09 的写作（滚动更新，截至该日期属于"新近加入"）· **出现频率：** 2 个独立
提及（interviewdb.io 的 AI-exercise 指南；interviewfox.ai 的 OA/HackerRank 指南），加上
`en_forums.md` §9 自己的整理（C11）· **可信度：** 中等——递进关系（"关键字/字符串匹配 → AND/OR
布尔逻辑，多阶段"）和评分标准（能否指挥/验证/调试 AI，是否自己写测试）都被两个独立来源明确点名；
确切的输入协议、字段列表和实测数字是本仓库的重建（没有公开的逐字 I/O 样例）。

## 背景
Stripe 在 2026 年新增的 "AI Programming Exercise" 轮，把候选人放进一个带内嵌 AI 聊天面板的
HackerRank 环境，评分点在于**你怎么指挥它**，而不是你打字快不快。题目本身刻意做得很普通——一个基于
规则的交易过滤器，结构上和 Radar 真实的规则引擎同形（生产版本见 `problems/q12_platform_balance_radar_rules`
的 `ACCEPT`/`BLOCK if (:field: = "const")`），但更小：没有带引号的常量、没有 `:field:` 标记、没有
`API:`/`BAL:` 余额账本——只是针对一批交易求值的 `ALLOW|BLOCK if <condition>` 规则，共三个 Part，
每个 Part 增加一层表达能力。本目录刻意**不**重复 q12 的语法或它带余额账本的 Part 1——把这两题当作
在不同的"AI 辅助 vs. 手写"节奏下考察同一个规则引擎技能的姊妹题。

## 输入（stdin）
第一行是 `PART n`（n ∈ 1..3）。然后是两个 section，顺序固定，各自的 header 独占一行；空行处处忽略：
```
RULES
ALLOW|BLOCK if <condition>          one rule per line, in registration order
TRANSACTIONS
id,amount,currency,country,card_brand,merchant
```
`amount` 是非负整数（单位为分）；`currency`、`country`、`card_brand`、`merchant` 都是裸的
字母数字/下划线 token（不含逗号、不含空格——这个协议没有 CSV 引号转义）。交易行如果列数少于 6 列，
缺的尾部列一律当作空字符串处理。规则行最多 10^5 条，交易行最多 10^5 行。

## 输出
每笔交易一行，**按输入顺序**：`id ALLOW (rule k)` 或 `id BLOCK (rule k)`，其中 `k` 是**该匹配规则在
`RULES` 块内的 1-索引行号**（计入每一条规则行，包括 Part 3 里后来被判定无效而跳过的行——不管文件里
还有什么解析失败，编号都保持稳定）。如果没有规则匹配，这一行就只是 `id ALLOW`——没有 `(rule k)`
后缀；因为没有可引用的规则。（Part 3 还会打印 `ERROR line k: <reason>` 行，每条无效规则在解析时
打印一次，全部先于任何交易输出——见 Part 3。）

## 规则
### Part 1 — 关键字相等
`<condition> := <field> == <value>`，仅此一种形式。`<field> ∈ {id, amount, currency, country,
card_brand, merchant}`；`<value>` 是一个裸 token，按去空格后的字符串比较（所以即使 `amount` 是数值，
`amount == 10000` 依然有效——数字位当字符串比较也相等）。规则按**注册顺序**求值；**第一条条件为真的
规则生效**。无匹配 → 默认 `ALLOW`。

### Part 2 — 比较运算符和 `in`
`<condition>` 新增五个运算符——`!=`、`>`、`<`、`>=`、`<=`——外加一个成员判断形式：
`<field> in [v1, v2, v3]`（逗号后和方括号周围的空格可选）。每条规则依然只能有一个比较（还没有布尔
组合，那是 Part 3 的事）。运算符两侧的空白始终可选（`amount>=5000`、`amount >= 5000`、
`amount>= 5000` 解析结果相同）。比较语义（Part 3 也复用）：对 `==`/`!=`，如果**两边**都能解析成
整数，就按数字比较（`amount==0100` 匹配 `100`）；否则比较去空格后的字符串。排序运算符
（`>`、`<`、`>=`、`<=`）只针对 `amount`（唯一的数值字段）——把两边都解析成整数。`in [...]` 是把该
字段的字符串形式与列表中每个字面量比较（`country in [US, CA, MX]`）。

### Part 3 — AND / OR / NOT / 括号
递归下降语法，**`not` 比 `and` 绑得紧，`and` 又比 `or` 绑得紧**（关键字 `and`/`or`/`not`/`in`
大小写不敏感；字段名、`ALLOW`/`BLOCK`、以及值都大小写敏感）：
```
expr        := or_expr
or_expr     := and_expr ("or" and_expr)*
and_expr    := unary ("and" unary)*
unary       := "not" unary | primary
primary     := "(" expr ")" | comparison
comparison  := field OP value | field "in" "[" value ("," value)* "]"   # OP as in Part 2
```
`field` token 是 `{id, amount, currency, country, card_brand, merchant}` 中的任意一个名字；操作数
位置上任何其它裸 token 都是字面量值（这就是该语法怎么区分"和交易的 `country` 比较"和"和字面量字符串
`country` 比较"而不需要引号的关键所在）。`not` 只作用于紧跟着的那一个 `unary`（所以 `not a and b` 是
`(not a) and b`，而不是 `not (a and b)`）。一条规则的条件解析失败——运算符写错、括号不匹配、末尾有
多余内容、该填操作数的地方用了关键字等等——会产生 **`ERROR line k: <reason>`**（k 是该规则在 `RULES`
中的 1-索引行号），该规则**被跳过**（永远不会用于匹配任何交易，且不影响后面规则的行号）。`<reason>`
文本的具体措辞由实现自定；隐藏测试只检查 `ERROR line k:` 前缀和行号，不检查具体措辞。

## 实测示例
### Part 1
```
RULES
ALLOW if country == US
BLOCK if amount == 10000
TRANSACTIONS
t1,500,USD,US,visa,acme
t2,10000,USD,CA,visa,acme
t3,700,USD,FR,visa,acme
```
→
```
t1 ALLOW (rule 1)
t2 BLOCK (rule 2)
t3 ALLOW
```

### Part 2
```
RULES
BLOCK if amount > 5000
ALLOW if country in [US, CA]
BLOCK if currency != USD
TRANSACTIONS
t1,6000,USD,US,visa,acme
t2,3000,USD,MX,visa,acme
t3,3000,EUR,FR,visa,acme
t4,3000,USD,CA,visa,acme
```
→
```
t1 BLOCK (rule 1)
t2 ALLOW
t3 BLOCK (rule 3)
t4 ALLOW (rule 2)
```
（`t2`：金额没超过 5000，国家 MX 不在列表里，货币 USD 不满足 `!= USD`——没有规则命中，默认 ALLOW。）

### Part 3
```
RULES
BLOCK if country == US and amount > 5000
ALLOW if (country == CA or country == MX) and not currency == EUR
BLOCK if amount >
TRANSACTIONS
t1,6000,USD,US,visa,acme
t2,3000,USD,CA,visa,acme
t3,3000,EUR,CA,visa,acme
t4,100,USD,FR,visa,acme
```
→
```
ERROR line 3: expected a field or value
t1 BLOCK (rule 1)
t2 ALLOW (rule 2)
t3 ALLOW
t4 ALLOW
```
（`t3`：规则 1 为假（country 不是 US）；规则 2 的 `not currency == EUR` 为假，因为 currency
*正是* `EUR`，所以整个 `and` 为假；规则 3 因无效被丢弃——没有规则匹配，默认 ALLOW。`t4`：什么都不
匹配——FR 既不是 CA 也不是 MX——默认 ALLOW。）

```python
part3(["RULES", 'BLOCK if not country == US', "TRANSACTIONS", "t1,0,USD,CA,visa,acme"]) == ["t1 BLOCK (rule 1)"]
part3(["RULES", "ALLOW if a or b and c", "TRANSACTIONS"]) == []   # a/b/c aren't real fields — see edge cases
```

## 隐藏测试已知瞄准的边界情况
- 默认-ALLOW **没有** `(rule k)` 后缀；任何匹配到的规则都一定有，哪怕是 `(rule 1)`
- `(rule k)` 的编号计入*每一条* `RULES` 行，包括后来被报 `ERROR` 的行（Part 3）——被跳过的规则之后
  的规则保留其真实行号，不会往前移
- 运算符空白：`amount>=5000`、`amount >=5000`、`amount>= 5000`、`amount >= 5000` 解析结果完全相同
  （Part 2 及以后）
- `==`/`!=` 的数值/字符串兜底：`amount == 0100` 匹配 `amount == 100`（两边都能解析成整数，按数字
  比较）；`country == us` **不**匹配 `country == US`（字符串，不做大小写折叠——字段名/值大小写敏感，
  只有布尔关键字不敏感）
- `in [...]` 分别测零个、一个、多个元素；逗号后的空格可选；元素不存在 → 不匹配（不是错误）
- `not` 优先级：`not a and b` 是 `(not a) and b`；`a or b and c` 是 `a or (b and c)`（`and` 比
  `or` 紧）；嵌套括号 `(a and (b or not c))`
- 即使输入交易*也可能*匹配后面的规则，第一条匹配的规则依然获胜——一旦有规则命中，后面的规则永远不会
  被求值
- 一条规则把字段名当作*值*来引用是可以的，只要比较的另一边是真实字段（`country == country` 恒真，
  两边都解析成同一个交易字段）——这不是作为"陷阱"来考的，只是确认字段 vs. 字面量的判定是按操作数
  逐个进行，而不是按规则整体
- Part 3 中能正常分词、但结构有问题的畸形规则：括号不匹配、比较缺右操作数、`and`/`or` 缺操作数、
  该填字段/值的地方出现裸关键字（`and`/`or`/`not`/`in`）——每种都恰好产生一条 `ERROR line k:`，
  而不是崩溃
- 空的 `RULES` 块（每笔交易都默认 `ALLOW`）；空的 `TRANSACTIONS` 块（没有输出行，若有则只有
  `RULES` 相关的 `ERROR` 行）；列数少于 6 列的交易行（缺的尾部字段当作 `""`，针对它们的比较只是不
  匹配，而不会崩溃）
- 最多 10^5 条规则 × 10^5 笔交易，针对每笔交易不能是二次方复杂度（每条规则的 AST 只编译一次，在
  所有交易间复用）

## 现实中见过的变体
- 描述这一轮的两个来源都认可其形态（"关键字/字符串匹配，升级为 AND/OR 布尔逻辑，多个渐进阶段"），但
  都没有公布逐字的 I/O 样例或字段列表——本仓库的 `RULES`/`TRANSACTIONS` stdin 协议、六字段交易
  schema，以及确切的语法产生式都是为了可测试性而做的重建，参照了本题库自己的
  `problems/q12_platform_balance_radar_rules`（同一个"规则字符串 → AST → 求值"技能的生产级姊妹题，
  它还记录了真实的 Radar 语法：https://docs.stripe.com/radar/rules/reference）。
- 本仓库用两种方式演练这道题：`loop/mock.py start cd07` 给你完整的 60 分钟手写预算（本演练环境没有
  AI 面板）；下面"用 AI 做这题的流程"一节说的是如果*允许*使用编码助手时会有什么不同，依据来源里的
  评分说明。

## 用 AI 做这题的流程
这一轮评分的是**你怎么驾驭助手**，而不是打字速度——两个来源都明确点名"能否有效使用 AI 而不关掉自己
的脑子"（interviewdb）和"从架构、测试、优化几个维度打分你怎么用它"（interviewfox）作为明确的评分
标准。推荐流程（interviewdb 自己的总结）：**AI 总结题面 → 你和它一起敲定实现方案 → AI 生成代码 →
你自己写测试 → 你调试并确认自己理解生成出来的东西**，而不是"复制提示词、复制输出、直接提交"。

**AI 生成的这道题解法常犯的五个错误**——接受 diff 之前逐条检查：
1. **把 `in [US, CA]` 当成子串测试而不是集合成员判断**——写成 `value in raw_condition_text` 或
   `field_value in "US,CA"`，而不是拆分方括号内容再逐个精确比较。症状：`country == USA` 会错误地
   满足 `country in [US]`，因为 `"US"` 是 `"USA"` 的子串。
2. **`and`/`or` 优先级写反或拍平**——把它们实现成同一优先级从左到右（`a or b and c` →
   `(a or b) and c`，错误），而不是 `and` 绑得更紧；或者自底向上搭建解析器，导致 `or` 最终嵌套在
   `and` 内部而不是相反。
3. **跳过短路求值**——无条件地对 `and`/`or` 两边都求值。这本身不算致命（这里没有任何场景会因为
   良构交易而在两种做法下给出不同*结果*——每个字段都存在），但要留意 AI 用防御性
   `try/except` 把每次比较都包一层来"修复"这个不存在的问题，这样反而会悄悄吞掉真正的 bug（真的
   缺字段、运算符打错字），而不是把它按 Part 3 真正想要的方式呈现成 `ERROR line k`。
4. **默认方向写反**——把未匹配的交易默认成 `BLOCK` 而不是 `ALLOW`，或者打印一个占位符比如
   `(rule None)`/`(rule -1)`，而不是完全省掉后缀。这是候选人之后让 AI "加上 Part 3 支持"时，
   AI 顺手悄悄重写了 Part 1/2 默认处理逻辑，最常见的一种回归。
5. **tokenizer 要么欠造要么过造**——欠造：对原始文本做 `condition.split(" ")`，一旦间距不是精确
   一个空格就会崩（`amount>=5000` 完全没有空格）；过造：同一口气生成了一个带算术运算符、带引号字符串
   常量、带可插拔函数注册表的通用表达式引擎，而题面根本没要求这些，白白烧掉 30 分钟的 AI 预算
   （或 60 分钟的手写预算）在评分者从没要求的范围上。这两种极端的错误都源于接受生成代码之前没有
   重新对照题面的语法。

## 面试官会怎么追问
1. "这是 AI 轮，评分标准是'你怎么指挥 AI'——如果面试官现在问你'你让 AI 生成的第一版代码有什么问题、
   你怎么发现的'，你会怎么回答?" — 逼你能具体说出一条真实的 review 发现（比如 `in [...]` 被 AI
   写成了子串匹配），而不是空泛地说"我 review 过了"。
2. "为什么 `not` 比 `and` 优先级高、`and` 又比 `or` 优先级高？这个优先级关系在你的递归下降解析器里
   体现在哪一行？" — 期望候选人直接指着 `_or` 调 `_and`、`_and` 调 `_not` 的调用链解释：**优先级
   越高的运算符，对应的解析函数离"叶子"越近**，而不是背一个优先级表却说不出代码里怎么实现的。
3. "如果要加一个新的运算符 `xor`，绑定优先级介于 `and` 和 `or` 之间，你会改哪几个函数？" — 检验
   候选人是否真的理解这个语法糖表结构是可扩展的：只需要在 `_or`/`_and` 之间插入一层新的 `_xor`
   方法，其余分支不用动。
4. "为什么 `ERROR line k` 只在 Part 3 出现，Part 1/2 遇到写错的规则就直接静默跳过？这是题面明确要求
   还是你自己的选择？如果面试官现在说'Part 2 也要报错'，你需要改哪里？" — 检验候选人能不能区分
   "题面写死的行为"和"没写清楚、自己做的合理选择"，并现场说出只需要把 `_evaluate` 里 `if part == 3`
   的判断放宽。
5. "10 万条规则、10 万笔交易，最坏情况下每笔交易都要扫到最后一条规则才 default ALLOW，复杂度是
   多少？有没有办法优化？" — 期望候选人先诚实指出这是 `O(rules × txns)` 最坏情况、当前实现无法避免
   （规则是任意布尔表达式，没有通用的索引结构能跳过不相关规则），再提一个受限场景下的优化思路，比如
   "如果大多数规则只判断单个字段的等值条件，可以按字段建索引、只对该字段值可能命中的规则做全量求值"。
6. "`country == country` 这种写法你选择让它按字段解析、恒真——为什么不是直接报错？换个角度，如果
   一个用户传进来的字段值本身就叫 `country`（比如商户名就是 `country`），你的语法怎么区分"这是字段"
   还是"这是值"？" — 检验候选人是否理解这套语法的核心设计取舍：**字段 vs. 字面量的判定是按 token
   的拼写、不是按值的语义**，这是省掉引号语法（不像 q12 需要 `:field:` 标记）所必须付出的代价。

## 本题考察什么
技能：S02 条件字符串的分词/解析 · S06 数值/字符串比较兜底 · S10 first-match-wins 的有序规则求值 ·
S18 校验（Part 3 按规则报 `ERROR` 而不崩溃整批）· S19 渐进式语法（Part n 是 Part n+1 的严格语法
子集）· S24 Radar 规则引擎词汇（与 q12 共用，在 AI 辅助轮的规模上）· S25 指挥/审查 AI 生成代码
（理解题面、自己写测试、抓过度工程——这一轮真正的评分轴，依据 Sources）

## 来源
- https://www.interviewdb.io/guides/stripe-ai-programming-exercise（2026-06-09："给一份交易列表和
  一份规则列表，每条规则说明是否接受或拦截一笔交易，后面跟一个 if 条件"；评分标准："能否有效使用 AI
  而不关掉自己的脑子"；流程："AI 总结 README，你们一起敲定实现方案，AI 生成代码，你自己写测试，
  你调试并确认自己理解"）
- https://interviewfox.ai/interview-questions/stripe-oa-hackerrank-guide/（2026："从架构、测试、
  优化几个维度打分你怎么用它"；约 30 分钟，HackerRank 内嵌 AI 聊天，"有点像轻量版 Cursor"）
- `loop/raw/en_forums.md` §9 "2026 新增：AI Programming Exercise 轮" 和 §6.2 C11（本仓库对上述
  两个来源的自行整理）
- `problems/q12_platform_balance_radar_rules/problem.md`（本仓库的生产级姊妹题；这里的
  RULES/比较运算符/布尔语法设计刻意做成那道题技能的更小、不重叠子集，而不是照搬它的
  `API:`/`BAL:`/`:field:` 语法）

## 澄清说明（作者自加，非来源内容）
- 两个来源都没有给出输入输出协议、交易字段列表或确切语法——本仓库的 `RULES`/`TRANSACTIONS` stdin
  分节、六字段交易 schema、`(rule k)` 输出后缀，以及 Part 3 的 `ERROR line k:` 报告都是为可测试性
  而做的重建，选择向 `problems/q12` 自身的 house style 靠拢（parse → model → evaluate、
  first-match-wins、默认接受），而不是为同一个底层技能再发明第四种约定。
- "默认 ALLOW 不带后缀"（而不是例如 `(default)`）是本仓库自己的选择，之所以在这里写明，是因为来源
  的一句话描述完全没有指定输出格式。
