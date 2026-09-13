# cd05 · Business Account Data Verification — when/requires/one_of 规则引擎

**Type:** onsite Programming Exercise · **Stage:** virtual onsite "general coding" (60 min, 2 part + follow-ups) · **Last asked:** 日期未知 (1point3acres 题库)
**Frequency:** 2 independent mentions (1point3acres oj 题库 `interview/problems/ad817329-...` 给出完整规则语义+约束+示例的转述；1point3acres `interview/thread/1155516` VO 挂经提及同名 "Business Account Data Verification" 任务，反馈延迟+完成问卷后被拒） · **Confidence:** high for the rule schema/semantics（源材料给出接近逐字的 JSON schema 级别描述：`when`/`requires`/`one_of`、路径语法、"非空"定义、输出格式、约束数字全部齐全）；worked examples 与部分行为细节（数组整体缺失时的回退格式、`one_of` 是否允许通配、`present` 条件的精确含义）本仓库重构补全——`cn_forums.md` 只转述了"附完整示例输入输出"这句话，没有把示例原文抄进来，因此 worked examples 全部改写自源描述，而非逐字复制。

## Context
Stripe 需要在放行一个企业账户之前校验它的资料是否齐全：法定名称、经营类型、受益所有人（owner）
列表、代表人联系方式等。校验规则不是写死在代码里的，而是一份可配置的规则列表——每条规则说"在什么
条件下（`when`）、哪些字段必须非空（`requires`），或者哪一组字段里至少要有一个非空（`one_of`）"。
这道题考的不是复杂算法，而是**干净的路径解析 + 规则引擎设计**：处理 `.` 嵌套、数组通配
`owners[].first_name`、条件短路、结果去重与稳定排序。

## Input (stdin)
第一行 `PART n`（n ∈ {1,2}）。其余整个输入是**一个 JSON 文档**（可能跨多行/带缩进）：
```json
{
  "account": { "...任意深度的嵌套对象..." : "..." },
  "rules": [ { "...": "..." } ]
}
```

## API
`part1(doc: dict) -> list[str]`、`part2(doc: dict) -> list[str]`（`doc` 就是上面整份反序列化后的
JSON：`{"account": ..., "rules": [...]}`）。`main()` 读取首行 `PART n`，对剩余文本 `json.loads`
得到 `doc`，按 `n` 分发，逐行打印返回值。

## Output
全部规则满足 → 打印单行 `VERIFIED`。否则按**字典序（Python 默认字符串比较）**逐行打印缺失项，
去重后每个缺失 token 只打印一次：
- 普通字段路径直接打印，如 `business_profile.url`
- 通配路径按元素展开、带具体下标，如 `owners[2].first_name`
- `one_of` 组失败打印整段 `one_of(field1|field2|...)`（字段顺序 = 规则里声明的顺序，不重排），
  这一整段字符串参与最终排序

## Rules

### 字段路径语法（两个 Part 通用）
`.` 分隔的段序列，如 `business_profile.url`；`owners[].first_name` 中 `owners[]` 表示"对
`owners` 数组的每个元素分别解析剩余路径"。本题只支持**每条路径最多一个 `[]` 通配段**，且必须
整段出现（`owners[]`，不是 `owners[0]` 这种具体下标）。

### "非空"定义（两个 Part 通用）
路径能够解析到值，且该值：不是 `null`；不是空字符串 `""`；不是空列表 `[]`。**其余类型
（数字、布尔、空字典 `{}`）一律视为非空**——这是本仓库对源材料未覆盖细节的显式补全（见
Clarifications）。路径解析不到（中间某段不存在，或类型不对，比如对字符串取子字段）视为"缺失"，
效果等同"非空判定失败"。

### Part 1 — `requires` only
规则形如 `{"requires": ["path1", "path2", ...]}`，**没有 `when`，没有 `one_of`，路径不含 `[]`
通配**（Part 1 的规则永远生效）。对规则里列出的每个路径分别判断非空；全部规则的所有路径合并、
去重、排序后输出；全部满足则只输出 `VERIFIED`。

### Part 2 — `when` + `one_of` + 数组通配
规则形如：
```json
{
  "when": [ {"path": "business_type", "equals": "company"},
            {"path": "legal_name",   "present": true} ],
  "requires": ["owners[].first_name"],
  "one_of":   ["representative.email", "representative.phone"]
}
```
- `when`（可选，条件列表，**全部满足**规则才生效，AND 语义；省略或空列表 = 恒生效）。条件两种
  形式：`{"path": p, "equals": v}`（路径能解析到值 **且** 该值与 `v` 相等，Python `==` 语义，
  类型敏感——字符串 `"true"` 不等于布尔 `true`）；`{"path": p, "present": true|false}`
  （路径是否能解析到任意值，包含 `null`——"存在" ≠ "非空"，`present` 只看 key 链是否走得通）。
  一条 `when` 不满足即整条规则**跳过**（它声明的 `requires`/`one_of` 都不检查，不产生任何缺失
  项）。
- `requires`（可选）：同 Part 1，但路径**允许** `owners[].first_name` 式通配——对数组每个现存
  元素分别检查，缺失的按下标输出 `owners[2].first_name`；数组本身为空列表 `[]` 时**没有元素可
  检查，视为整条 vacuously 满足，不产生缺失项**；数组本身不存在或不是列表时，退化为输出**未
  展开的字面路径** `owners[].first_name`（见 Clarifications）。
- `one_of`（可选，**不支持通配**，本题范围内路径均为普通 `.` 路径）：列表内至少一个路径非空即
  满足；全部为空/缺失才失败，失败时输出整段 `one_of(field1|field2|...)`（原始声明顺序）。
  一条规则可以同时有 `requires` 和 `one_of`（`when` 匹配时两者都要检查）。

## Worked examples

**Part 1**（无 `when`）：
```json
PART 1
{
  "account": {
    "business_name": "Acme Inc",
    "business_profile": {"url": "", "mcc": "5734"},
    "representative": {"email": "rep@acme.com"}
  },
  "rules": [
    {"requires": ["business_name", "business_profile.url", "business_profile.mcc"]},
    {"requires": ["representative.email", "representative.phone"]}
  ]
}
```
输出：
```
business_profile.url
representative.phone
```
（`business_profile.url` 是空字符串；`representative.phone` 整条路径不存在；`business_name` /
`business_profile.mcc` / `representative.email` 都非空，不出现。）

若把 `business_profile.url` 改成 `"https://acme.example"`、补上
`"representative": {"email": "rep@acme.com", "phone": "555-0100"}`，则输出单行 `VERIFIED`。

**Part 2**（`when` + `one_of` + 通配）：
```json
PART 2
{
  "account": {
    "business_name": "Acme Inc",
    "business_type": "company",
    "representative": {"email": "", "phone": ""},
    "owners": [
      {"first_name": "Alice"},
      {"first_name": ""},
      {"last_name": "Kim"}
    ]
  },
  "rules": [
    {"requires": ["business_name"]},
    {"when": [{"path": "business_type", "equals": "company"}],
     "requires": ["owners[].first_name"]},
    {"when": [{"path": "business_type", "equals": "individual"}],
     "requires": ["ssn_last4"]},
    {"one_of": ["representative.email", "representative.phone"]}
  ]
}
```
输出：
```
one_of(representative.email|representative.phone)
owners[1].first_name
owners[2].first_name
```
（第 3 条规则 `when` 不匹配 `business_type=company`，整条跳过——`ssn_last4` 完全不出现在输出里；
`owners[0].first_name` = `"Alice"` 非空，不出现；排序上 `"one_of("` 的 `n` < `"owners["` 的
`w`，所以 `one_of(...)` 排在最前。）

## Edge cases hidden tests are known to target
- `rules` 为空列表 → 直接 `VERIFIED`
- 缺失路径的中间段整个不存在（不是叶子字段为空，而是父对象本身没有这个 key）→ 照样输出这段
  完整路径字符串
- `when` 里 `present: false`：期望路径**不存在**才算匹配（比如"没有填 `dba_name` 的账户才需要
  额外的 `requires`"这种反向门控）
- `when` 有多个条件，其中一个不满足 → 整条规则跳过（AND 语义，不是"至少一个满足就生效"）
- `one_of` 全部字段"存在但为空字符串"（不是完全不存在）依然触发失败
- `one_of` 里至少一个非空即可，不要求"哪一个"，只要有一个满足就不输出
- 通配数组为空列表 `[]` → 视为满足（vacuous truth），不是"数组必须非空"
- 通配的基础路径整个不存在（`owners` key 缺失，或类型不是列表）→ 回退输出未展开的字面路径
  `owners[].first_name`（不产生带下标的多行）
- 两条不同规则要求同一个字段，且都缺失 → 输出去重，只打印一次
- `equals` 比较类型敏感：`"equals": "company"` 不匹配值为 `true`/`1`/`"Company"`（大小写敏感）
- `rules` ≤ 200 条，单条 `requires` ≤ 50 项、`one_of` ≤ 20 项，字段路径长度 ≤ 100 字符，
  `account` 总 JSON 节点数 ≤ 10^4 —— 必须能在预算内跑完（无嵌套指数级展开）

## Variants seen in the wild
- 源材料标注该题在两条独立渠道出现：一次是完整规格题库条目（`interview/problems/ad817329`），
  一次是 VO 挂经帖只提到任务名和"反馈延迟+问卷后被拒"的负面流程体验，没有技术细节——后者只作为
  "这题真实出现在 VO 阶段"的旁证，不贡献规则细节。
- 源材料原题不分 Part（一次性给出完整规则语义）；本仓库按仓库惯例拆成 Part 1（仅 `requires`）→
  Part 2（加 `when`/`one_of`/通配）两级递进，便于 45–60 分钟内分阶段验收。

## What this tests
skills: S02 parsing（JSON 而非 CSV）· S03 树形数据的路径解析 · S04 分组去重 · S08 确定性排序
（含拼接字符串排序）· S09 精确格式化（`one_of(...)`/带下标路径）· S18 校验规则引擎设计 ·
S19 incremental design（Part 1 → 2 逐步加规则语义）

## Sources
- https://www.1point3acres.com/interview/problems/ad817329-a95b-50ec-9860-f453c5fa0a1b
  （"Business Account Data Verification"，完整规则语义+约束+示例的转述，见 `loop/raw/cn_forums.md`
  第 266 行）
- https://www.1point3acres.com/interview/thread/1155516（VO 挂经，任务同名，无技术细节，见
  `loop/raw/cn_forums.md` 第 61/157 行）

## Clarifications（本仓库的显式补全，源材料未覆盖）
- "非空"定义只提到 `null`/空串/空列表三种否定情形；数字 `0`、布尔 `false`、空字典 `{}` 一律按
  "非空"处理（因为它们都不是这三种情形之一），本题不做"falsy 即空"的隐式推广。
- 通配基础数组整体缺失或类型不对时的行为，源材料未指定；本仓库定义为回退输出未展开的字面路径
  （`owners[].first_name`），而不是静默跳过或报"整条规则缺失"——这样候选人在两种失败模式
  （元素缺字段 vs 数组本身缺失）之间的输出可以区分开。
- `one_of` 是否支持通配路径，源材料未提及；本仓库范围内 `one_of` 只允许普通 `.` 路径，通配放进
  `one_of` 是未定义行为（面试官追问方向之一，见下）。

## 面试官会怎么追问
1. "如果一条规则的 `when` 引用了一个整个 `account` 里都不存在、任何账户都不可能有的字段路径，
   这条规则就永远不会生效——你怎么在部署前发现这种'死规则'?" —— 期望候选人提出对规则集做静态
   分析（相对 `account` 的 JSON Schema 走一遍 `when` 路径是否可达），而不是等运行时才发现。
2. `owners[].first_name` 缺失和 `owners[].email` 缺失应该分别输出成什么样的**用户可读**错误
   信息（本地化到中文/日文）？—— 期望候选人提出"机器 token（路径）与展示文案分离"，用一张
   `path -> i18n key` 的映射表，而不是把路径字符串直接怼给终端用户。
3. 如果要一次校验 10^5 个账户（同一份 `rules`，不同 `account`），当前实现每次都要重新遍历/
   解析路径字符串——怎么优化？—— 期望候选人提出"预编译"：规则加载时把每条路径的 `.`/`[]` 语法
   一次性切好段（`split_path` 结果缓存），复用于所有账户，避免字符串解析在热路径里重复发生。
4. 如果要扩展 DSL 支持 `not`（取反一个 `when` 条件）和 `any`（`requires` 的"或"版本，等价于
   `one_of` 但可以嵌套在别的组合子里），你会怎么设计这套语法的抽象表示？—— 期望候选人画出一棵
   小型表达式树（`AllOf`/`AnyOf`/`Not`/`Present`/`Equals` 节点），而不是继续往扁平字典里加
   特殊 key。
5. 两条规则语义上互相矛盾——一条 `requires` 某字段非空、另一条的 `when` 恰好只在该字段**不存在**
   时生效并 `requires` 同一个字段——这种"永远无法同时满足"的规则集，你怎么在规则录入阶段就
   拦下来，而不是留到跑测试才发现？—— 期望候选人提出针对每条规则的 `when`/`requires` 做一次
   "自反性"检查（规则是否要求它自己 `when` 条件所排除的状态），或者退一步说"这是运行时数据
   相关的矛盾，静态分析代价过高，改用规则评审 + 单元测试覆盖"也是可接受答案，只要讲清楚权衡。
6. 同一份 `(account, rules)` 重复跑两次，输出必须完全一致（幂等）——当前实现里哪些地方可能
   意外引入非确定性？—— 期望候选人指出"用集合收集缺失项后必须显式 `sorted()` 再输出，不能依赖
   集合/字典的迭代顺序"、以及"输入 JSON 里字段的书写顺序变化不应该改变输出"两点。
7. 如果 `account` 允许多层嵌套数组（`owners[].addresses[].city` 这种连续两个通配段），当前
   "每条路径最多一个 `[]`"的限制怎么放开，复杂度会怎样变化？—— 期望候选人认识到这是笛卡尔积
   展开（`owners` 数组 × 每个 owner 的 `addresses` 数组），仍然是线性于展开后的叶子总数，只要
   `account` 总节点数 ≤ 10^4 的约束还在，就不会失控，但递归 `_expand()` 需要支持多段通配而不是
   写死一段。
