# ps05 · Numeronym validation

**类型：** 电面（技术） · **阶段：** 45 分钟技术电面 · **最近一次出现：** 报告未标注日期，页面 2026 年仍在线（FinalRound）；Exponent 把它列为 coding 轮样题
**出现频率：** 2 处独立提及（FinalRoundAI 题目页面、Exponent 面试指南） · **可信度：** 中等（两个来源都没有公开精确的 I/O 契约 —— 本文基于该术语的标准定义和 Stripe 一贯的"校验 → 展开 → 生成"递进结构重构而成）

## 背景
numeronym（数字缩略词）是一种通过保留单词首尾字母、用被省略的中间字母数量替代的缩写形式：
`internationalization` → `i18n`（省略了 18 个字母）、`accessibility` → `a11y`、
`kubernetes` → `k8s`。Stripe 内部工具（以及大量开源项目）用它们作为长标识符的简短别名。
本题要求你先校验 numeronym 的*形式*，再拿它去比对真实词典，然后反过来为词典生成
numeronym —— 包括处理两个不同单词生成*同一个* numeronym 会怎样。

## 输入（stdin，供 `main()` 使用）
第一行是 `PART 1`、`PART 2` 或 `PART 3`。之后的行因 part 而异（见下文）。空行在任何地方都
会被忽略。

## 输出
每个输出项一行，大小写精确，`main()` 用换行符拼接并在末尾加一个换行（没有输出内容时
不打印任何东西）。

## 规则

### Part 1 — `is_valid(numeronym: str) -> bool`
当且仅当匹配 `^[a-z][1-9][0-9]*[a-z]$` 时 numeronym 合法：
- 开头恰好一个小写字母，结尾恰好一个小写字母；
- 中间是一个或多个 ASCII 数字，解析为被省略字母的数量；
- digit 数量必须 **≥ 1** 且**没有前导零**（`i018n` 非法，即使数值上 `18 == 018` ——
  *字符串*不能以 `0` 开头）；
- 大小写敏感：任何位置出现大写字母都会导致非法。

stdin 主体：每行一个候选字符串。输出：每行一个 `VALID` 或 `INVALID`，按输入顺序。

### Part 2 — 对照词典展开
给定一个 numeronym 和一份词典，找出这个 numeronym 可能是哪些词典单词的缩写。
单词 `w` 匹配 numeronym `n` 当且仅当：
- `w[0] == n[0]` 且 `w[-1] == n[-1]`（首尾字母相同），**且**
- `len(w) == digits(n) + 2`（首字母 + 省略的中间部分 + 尾字母）。

stdin 主体：第 1 行是 numeronym，之后的行是词典单词（每行一个，假定为小写 `[a-z]+`；不是
`[a-z]+` 的行作为格式错误跳过 —— 它永远不可能是真实单词；同一个单词的重复行只算一次，
与 Part 3 相同）。如果 numeronym 本身结构上非法（未通过 Part 1），那它就不可能合法地代表
任何单词：输出 `NONE`。输出所有匹配的单词，**按字典序排序**，每行一个；如果没有匹配，
只输出一行：`NONE`。

### Part 3 — 为词典生成 numeronym，处理冲突
对每个词典单词，生成它的 numeronym：
1. **长度小于 3 个字符的单词**无法有 ≥ 1 的省略字母数，所以映射到**自身**（不可能压缩）——
   例如 `ok -> ok`。
2. **长度 ≥ 3 的单词**：基础形式是 `word[0] + str(len(word) - 2) + word[-1]`。
3. **冲突**：如果两个或更多词典单词生成*相同*的基础形式（首字母相同、尾字母相同、长度
   相同），通过保留更多字面前缀来消歧。尝试前缀长度 2、3、……（形式为
   `word[:p] + str(len(word) - p - 1) + word[-1]`）直到冲突组内每个单词都有不同的形式。
   前缀长度上限为 `len(word) - 2` —— 再多一位就会把 digit 压到 0，Part 1 禁止这样。
4. **不可消解的冲突**：如果两个单词在 digit 被压到 1 之后仍然相同（即它们*仅*在倒数第二个
   字符上不同 —— 例如 `flap`/`flip`），任何合法的 numeronym（digit ≥ 1）都无法区分它们。
   该组内每个单词都回退到**自身**（完整字面拼写），与规则 1 相同。
5. 同一个单词的重复行折叠为一个词典条目（词典中没有重复单词）。

输出：为每个不同的单词输出 `word -> numeronym`，**按单词排序**（普通字符串顺序）。

## 演示样例
```
PART 1
i18n
a11y
k8s
i018n
I18n
i18N
i0n
in
i1
ab12cd
->
VALID
VALID
VALID
INVALID   (leading zero: "018")
INVALID   (uppercase first letter)
INVALID   (uppercase last letter)
INVALID   (digit count is 0)
INVALID   (no digit segment at all)
INVALID   (missing trailing letter)
INVALID   (more than one letter before the digits)
```
```
PART 2
i18n
internationalization
international
interpretation
->
internationalization
```
(`internationalization` has length 20 = 18 + 2, starts `i` ends `n`. `international` ends in
`l`, not `n`. `interpretation` has length 14, not 20.)
```
PART 2
k8s
kilobytes
->
NONE
```
(`kilobytes` has length 9, but `k8s` needs length 10 — `kubernetes` would have matched.)
```
PART 3
cart
cost
cyst
few
internationalization
->
cart -> ca1t
cost -> co1t
cyst -> cy1t
few -> f1w
internationalization -> i18n
```
(`cart`/`cost`/`cyst` all base to `c2t` — length 4, starts `c`, ends `t`. Prefix length 2 gives
`ca`/`co`/`cy`, all distinct, so the disambiguated forms are `ca1t`/`co1t`/`cy1t`.)
```
PART 3
flap
flip
->
flap -> flap
flip -> flip
```
(Both base to `f2p`; the only prefix length available before the digit would hit 0 is 2 (`fl`
for both) — still colliding, so both fall back to their literal spelling.)

## 边界情况
- digit 段的前导零（`i018n`）—— 非法，即使数值本身没问题
- digit 数量恰好为 0（`i0n`）—— 非法，不是"空压缩"
- 任何位置出现大写字母 —— 非法，与 digit 规则无关
- numeronym 完全没有数字，或有数字但缺少某个字母
- Part 2：numeronym 结构上非法 → `NONE`，不是异常
- Part 2：词典单词长度匹配但首/尾字母不匹配
- Part 2：不是 `[a-z]+` 的词典行（数字、标点、大写）—— 跳过
- Part 2：空词典 → `NONE`
- Part 2：同一个匹配单词列出两次 → 只打印一次
- Part 3：单词长度恰好为 3（有 numeronym 的最短长度）
- Part 3：三方冲突（不只是两两冲突）在同一个前缀长度上解决
- Part 3：不可消解的冲突（仅倒数第二个字符不同）→ 两者都回退到自身
- Part 3：词典中的重复单词行 → 一条输出条目
- Part 3：超大词典（10^5 个单词）—— 尽管有分组，算法仍必须接近线性

## 见过的变体
- Exponent 的指南把同样的想法归为"校验一种紧凑编码"的若干练习题之一（没有公开 Part 2/3
  —— 这里的对照词典展开和冲突消解扩展遵循 Stripe 一贯用在其他电面题上的"校验 → 对照真实
  数据应用 → 处理冲突"三段式结构。
- 部分转述只要求反方向（"给定一个单词，生成它的 numeronym"），没有词典 —— 这正是 Part 3
  去掉冲突处理步骤。

## 本题考察点
skills: S02 解析/正则纪律 · S08 带明确 tie-break 的确定性排序 ·
S09 精确字符串格式化（`word -> numeronym`）· S14 字符串归一化/大小写规则 ·
S18 校验与错误路径 · S19 增量式设计（Part 3 复用 Part 1 的合法性判断）

## 来源
- https://www.finalroundai.com/interview-questions/stripe-tech-numeronyms-validation（FinalRound
  AI，Stripe 技术面试题库，页面截取时 2026 年仍在线）
- Exponent 面试指南，"Stripe coding 轮"样题列表（numeronym validation 与"解析交易日志得到
  余额"和"实现限流器"并列，作为 Stripe 电面代表性风格 —— 没有单独捕获 URL，引用自
  `loop/raw/en_forums.md` §3.3 P16 和 skills_matrix.md A 行"Numeronym validation"）

## 面试官会怎么追问
1. Part 1 的正则你会怎么手写一个不用 `re` 模块的版本？（练字符扫描，面试官常见的"别用库"追问）
2. 如果同一个 numeronym 在词典里匹配到多个词，你怎么判断哪个是"正确"的那个？（答案：本题定义为返回全部匹配，追问会引导到"如果必须唯一，你需要什么额外信息"）
3. Part 3 的前缀扩展算法最坏情况复杂度是多少？如果一个组里有 10 万个长度相同、只在最后一个字符前一位不同的词会怎样？（引导到我们定义的"不可消歧退化为字面词"规则，以及它的复杂度上界）
4. 如果词典是流式给的（不能一次性读进内存），Part 2/Part 3 怎么改？
5. 大小写不敏感的版本怎么改？如果 numeronym 允许 Unicode 字母呢（`café` 这种）？
6. 如果要求"生成的 numeronym 必须比原词短"（避免 `ok -> ok` 这种退化），你会加什么约束，对现有 API 影响多大？
7. 你会怎么给 Part 1 的校验写一个模糊测试（property-based test）来自动发现我们手写规则里的漏洞？
