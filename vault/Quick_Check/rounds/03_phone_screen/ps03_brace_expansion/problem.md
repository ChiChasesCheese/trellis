# ps03 · Brace Expansion — 类 glob 的 `{a,b,c}` 模板展开、健壮性、嵌套

**类型：** 技术电面（"Team Screen"） · **阶段：** 60 分钟（45 分钟写代码 + 15 分钟问答），3 个部分 · **最近一次出现：** 2026-08（InterviewDB "Expansion — Phone"，抓取时距发布仅 5 天）
**出现频率：** 逐字的 LeetCode Discuss 面经报告（班加罗尔后端，2024-06）；interviewdb.io 显示"Expansion"在 2026 年仍活跃；hackerprep.io 将其归类为"Bracket Expansion (Stack)" · **可信度：** Part 1 高（来源中有三个独立的演示样例）；Part 2/3 的规则是根据来源自身的追问描述重构的（"不完整/不匹配的括号、少于 2 个 token、无括号 —— 原样返回；嵌套括号"）—— 见来源部分。

## 背景
Stripe 电面版本的这道题读起来像 shell：`"/2022/{jan,feb,march}/report"` 展开成三个
report 路径；`"read.txt{,.bak}"` 展开成一个文件和它的备份。这是文件名模板、webhook 端点
模式或 price-ID 模板的 glob 式展开 —— 一次处理一个逗号分隔的组。面试官接下来会追问畸形
输入，如果时间允许，还会问单个模式中的嵌套组和多组（笛卡尔积）。

**这道题刻意不同于 `problems/qA03_lc1087_brace_expansion`**（本仓库中已有的、打了
LeetCode 标签的算法版本）：qA03 返回 `sorted(set(...))`（字典序，去重），因为那是 LC 1087
要求的。这个电面版本要求相反的契约 —— **保留顺序**（先列出的 token 排前面）且**保留
重复项** —— 因为来源报告中的样例就是这样展示的，这也是真实 shell-glob / 模板展开的行为。
如果你发现自己下意识想写 `sorted(set(...))`，停下来：它会同时破坏下面的顺序要求和
重复计数要求。

## 输入（stdin）
第一行 `PART n`（n ∈ 1..3）。之后每行一个**模式**（pattern）—— 混合了字面字符和花括号组
的模板字符串。每一行都是独立的（自成一个测试用例）；空行忽略。每行在解析前都会去除
首尾空白。

## 输出
每个输入模式一行，**按输入顺序**：该模式的所有展开结果用 `,` 连接（不含空格），顺序按
下方规则定义。畸形模式（Part 2-3）或完全没有组的模式（任何 part）恰好产生一个"展开
结果"—— 原字符串，不变。

## 规则
### Part 1 — 单组展开 `expand_braces(pattern: str) -> list[str]`
`pattern` 至多包含**一个** `{tok1,tok2,...}` 组（逗号分隔的 token；token 可以为空或
多字符；不嵌套）。组前后的所有内容都是字面前缀/后缀，在每个输出中原样保留。结果：每个
token 一个字符串，**token 按书写顺序**，格式为 `prefix + token + suffix`。完全没有组的
模式返回 `[pattern]`（一个"展开结果"：它自己）。假定输入是良构的 —— Part 1 不测试畸形
输入；那是 Part 2 的事。

### Part 2 — 畸形输入 `expand_braces_safe(pattern: str) -> list[str]`
与 Part 1 范围相同（至多一个组，不嵌套），但现在输入可能是畸形的：不匹配的花括号
（`{` 没有对应的 `}`，或多余的 `}`），**第二个组**（超出这一部分的范围 —— 该能力在
Part 3 才加入），组内**嵌套**的 `{`（同样原因），或者一个组的逗号分隔 token 数**少于 2 个**
（`{single}`、`{}`）。以上任何一种情况，都**原样返回该模式** —— `[pattern]` —— 不抛
异常，不打印错误字符串。良构的单组模式仍然照 Part 1 的方式展开。

### Part 3 — 嵌套与多组 `expand_braces_nested(pattern: str) -> list[str]`
两项新能力，都是笛卡尔积风格，**从左到右，外层组优先**：
* **多个顶层组**：`{a,b}{1,2}` → `a1, a2, b1, b2`（最左边的组是外层循环，与 bash 花括号
  展开完全一致：`echo {a,b}{1,2}`）。
* **嵌套组**：组内每个逗号分隔的备选项本身也可以包含组。`{a,{b,c}}d` → 备选项 `a`
  （字面量）然后备选项 `{b,c}`（展开为 `b`、`c`），按书写顺序排列，每个后面都跟着外层
  后缀 `d` → `ad, bd, cd`。

畸形输入处理规则依然适用，并泛化到任意深度：任意位置不匹配的花括号，或**任何**组
（顶层或嵌套）备选项少于 2 个，都会使**整个模式**畸形 → 原样返回 `[pattern]`（即使
畸形的组埋在三层深处）。任何一个 part 中顺序都不会被排序，重复的展开结果也不会被去除。

## 演示样例
Part 1（良构，单组）：
```
PART 1
/2022/{jan,feb,march}/report
over{crowd,eager,bold,fond}ness
read.txt{,.bak}
{z,a,z}
no braces here
```
→
```
/2022/jan/report,/2022/feb/report,/2022/march/report
overcrowdness,overeagerness,overboldness,overfondness
read.txt,read.txt.bak
z,a,z
no braces here
```
（`{z,a,z}` 既没有排序也没有去重 —— `z` 按书写顺序出现两次；对比 qA03 中在 LC 1087
规则下的 `{z,a,z}`，会得到 `["a", "z"]`。）

Part 2（畸形 → 原样回显；最后一行仍正常展开）：
```
PART 2
over{crowd,eager
over}crowd
{onlyone}
{}
a{b,{c,d}}e
{a,b}x{1,2}
read.txt{,.bak}
```
→
```
over{crowd,eager
over}crowd
{onlyone}
{}
a{b,{c,d}}e
{a,b}x{1,2}
read.txt,read.txt.bak
```
（第 5 行和第 6 行**在 Part 2 的范围内**是畸形的 —— 分别是嵌套组和第二个组 —— 尽管
它们在 Part 3 中都是完全良构的。）

Part 3（嵌套 + 多组现在合法；仍然畸形的 → 原样回显）：
```
PART 3
{a,{b,c}}d
{a,b}{1,2}
a{b,{c,d}}e
{a,{single}}
x{a,b}y{1,2}z
over{crowd
```
→
```
ad,bd,cd
a1,a2,b1,b2
abe,ace,ade
{a,{single}}
xay1z,xay2z,xby1z,xby2z
over{crowd
```
（`{a,{single}}` 是畸形的，因为其内部备选项 `{single}` 只有 1 个 token —— 整个模式，
而不仅仅是那个备选项，都会被原样回显。）

## 隐藏测试已知会针对的边界情况
- 组内的空 token（`read.txt{,.bak}`、`{,x}`）—— 空字符串是合法 token
- 组位于模式的最前面（`{a,b}suffix`）、最后面（`prefix{a,b}`）或整个模式
  （`{a,b,c}`，完全没有字面量）
- 重复 token 保留且不重新排序（`{z,a,z}` → `z,a,z`，不是 `a,z,z`）
- 完全没有花括号的模式在每个 part 下都返回 `[pattern]`，不是错误
- Part 2：未匹配的开括号、未匹配的闭括号、`{}`（0 个真实 token）、`{single}`（1 个
  token）、第二个顶层组、一个嵌套组 —— 这六种情况都原样回显模式
- Part 3：畸形检测是递归的 —— 埋在三层深处 `< 2` token 的组仍会使整个模式失效
- Part 3 笛卡尔积顺序：`{a,b}{1,2}` 是 `a1,a2,b1,b2`（左边的组在外层），不是
  `a1,b1,a2,b2`
- 很长的模式 / 每次运行很多模式（性能：10,000 行，每行一个中等大小的组）

## 见过的变体
- **字典序、去重输出**（LeetCode 1087 标签数据，本仓库的
  `problems/qA03_lc1087_brace_expansion`）—— 一种不同的、排序+去重的契约；不要与本题混淆。
- **"有多少个词，不需要列出来"** 和 **"给我第 k 个词"** 追问（同一 LC Discuss 面经系列）——
  在 qA03 Part 4 中实现为 `count_expansions` / `kth_expansion`，本题不重复实现，因为本题
  集的 Part 3 已经覆盖了嵌套的追问。
- Stripe 电面版本明确允许多字符 token（`{jan,feb,march}`、`{crowd,eager,bold,fond}`）——
  LC 1087 限制 token 为单个小写字母。

## 本题考察点
skills: S02 解析（segment/花括号扫描）· S14 不做归一化的保序输出 · S18 无异常的输入校验 ·
S19 增量式设计（Part 1 范围刻意收窄，使 Part 2 的畸形回显规则和 Part 3 的能力扩展各自都是
真实、可测试的一步）· S21 递归 / 笛卡尔积

## 来源
- https://leetcode.com/discuss/interview-experience/5341224/Stripe-or-Backend-Engineer-or-Bangalore-or-Jun-2024-or-Reject/ （逐字："Part 1 — 解析括号并生成所有组合... 例如 `/2022/{jan,feb,march}/report`... `over{crowd,eager,bold,fond}ness`... `read.txt{,.bak}`"；追问："处理不完整/不匹配的括号、少于 2 个逗号分隔值、或完全没有括号（原样返回字符串）"；"候选人只通过了第一个追问... 通常会有 2-3 个追问"）
- https://www.interviewdb.io/question/stripe ("Expansion — Phone"，标记为最近出现，2026)
- https://hackerprep.io/company/stripe/bracket-expansion （归类为"Bracket Expansion (Stack)"；付费墙，仅有标题/标签）
- `loop/raw/en_forums.md` §3.3 P4 "Bracket / Brace Expansion"（本仓库对上述内容的自行整理）

## 说明（作者本人添加，非来源内容 —— 原始报告未给出输出格式）
- 输出格式（逗号连接，每个模式一行）是本仓库自己的约定，为了让每次运行多个独立模式时
  stdin/stdout 保持确定性；来源只描述了返回的列表，没有描述序列化方式。
- Part 2 的"第二个组"和"嵌套组"情况被视为畸形（原样回显）而不是部分展开，因为 Part 1/2
  声明的范围是"至多一个、不嵌套的组"—— Part 3 才明确解除了这个限制，与来源自身
  "嵌套括号"追问的描述一致。
