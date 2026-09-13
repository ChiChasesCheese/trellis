# ps05 Numeronym validation — 报告

## 概述
"校验 → 查找 → 带冲突生成"三段式字符串处理题。Stripe 电面喜欢这种形状，因为它奖励仔细
读题（前导零规则、大小写敏感）而不是算法技巧，而且 Part 3 逼迫候选人自己发现（没人提醒）
生成过程可能撞车 —— 这正是 Stripe 真正关心的那类"两个东西映射到同一个标识符会怎样"的
问题（幂等键、短 URL slug）。

## 来源与可信度
中等 —— FinalRoundAI 的 Stripe 题库直接点名"numeronym validation"（页面 2026 年仍在线）；
Exponent 的指南把它列为 Stripe coding 轮样题之一，但没有公开 I/O 契约。Part 1 的正则形式
和 Part 2-3 的"词典 + 冲突"结构是本报告对标准 numeronym 定义的重构，不是逐字面经 —— 在
下方 未解决点 中标出。

## 各部分思路
1. **校验**：`^[a-z][1-9][0-9]*[a-z]$` —— 一个正则，但两个坑（前导零、digit=0）如果写
   `\d+` 而不加 `[1-9]` 开头锚点，很容易漏掉。
2. **对照词典展开**：numeronym -> `(first, last, expected_len)`，结构化过滤词典单词，
   排序。O(词典规模)。
3. **生成 + 解决冲突**：按 `(first, last, length)`（base numeronym）给单词分组；单例组
   直接完成；冲突组逐步扩展字面前缀（2、3、...）直到各形式分道扬镳，上限确保 digit 段
   永不低于 1；到达上限仍冲突的组（只在倒数第二个字符不同的单词）为组内每个成员都回退到
   字面单词 —— 这是全题唯一不显而易见的设计决策，在"面试官会怎么追问"第 3 条中明确点出。

## 隐藏测试针对的坑点
- `i018n`（前导零）vs `i18n` —— 数值上的 digit 相等，字符串上非法
- `i0n` —— digit count 为 0 不是"退化但合法"的 numeronym
- 大小写敏感独立于 digit 规则
- Part 2 格式错误的词典行（大写、内嵌数字）必须跳过，不能崩溃
- Part 2 遇到结构性非法的 numeronym -> `NONE`，不是异常
- Part 3 长度 < 3 的单词 -> 映射到自身（绝不因 `len(word) - 2 < 0` 崩溃）
- Part 3 三方冲突要在*同一个*前缀长度上为整组解决
- Part 3 不可消歧退化（`flap`/`flip`）—— 朴素的"只管扩展前缀"实现最容易在此出错（死循环，
  或产生一个本身就违反 Part 1 规则的 0 digit）
- Part 3 重复的词典行折叠为一个条目，不是每行输出一次

## 复杂度与实测开销
Part 1/2：输入规模上 O(n)。Part 3：按 base 形式分桶 O(n)，每个大小为 `g` 的冲突组在最多
`k` 个前缀长度上尝试，开销 O(k^2 . g) —— 实践中可忽略不计，因为真实词典里每个
(first, last, length) 桶的冲突很少。实测：10 万个随机 3-15 字符小写单词，Part 3
端到端（stdin -> stdout）远低于 2 秒，约 24 MB RSS（性能预算 2 秒 / 256 MB）—— 见
`test_perf_100k_words`。

## 测试清单
23 个测试 —— part1: 8（含 1 个 io）· part2: 6 · part3: 9（含 1 个 io、1 个 perf）；
edge 7 · fmt 3 · io 3 · perf 1。

## 涉及技能
S02 解析/正则纪律 · S08 带明确 tie-break 的确定性排序 · S09 精确字符串格式化 · S14
字符串归一化/大小写规则 · S18 校验与错误路径 · S19 增量式设计（Part 3 直接建立在
Part 1 的 `is_valid` 之上）

## 电面话术：边写边说什么
1. **读题时**：先大声确认三件事——numeronym 的形式规则（尤其"前导零"和"大小写"这两条容易被面试官
   当口头补充规则临时加）、Part 2 的"匹配"到底是长度精确相等还是"至少"、Part 3 冲突时期望的输出是
   报错、去重、还是像本题一样"扩展前缀消歧"。不要默认最常见的解释，直接问。
2. **写 Part 1 时**：先写规则再写正则，边写边说"我要防两个坑：leading zero 和 digit=0"，显式在代码
   里放一行注释解释为什么用 `[1-9][0-9]*` 而不是 `\d+`——这是面试官最容易追问的点，提前说等于免费分。
3. **写 Part 2 时**：说明"我复用 Part 1 的 is_valid 来防御式处理坏输入"，体现 S19 增量设计；顺带提一句
   "如果要支持大小写不敏感，我只需要在比较前 `.lower()`，不改数据结构"，展示可扩展性意识。
4. **写 Part 3 时**：这是全场唯一有难度的地方——先说清楚朴素算法（每个词独立生成 base 形式）会撞车，
   再引出"按 (first,last,length) 分组"这个关键 insight，最后主动抛出"如果前缀长到 digit=0 还是撞车怎么
   办"这个边界，自己给出退化方案（回退到全词），不要等面试官问出这个坑再补救——主动暴露边界比防御性
   代码更加分。
5. **收尾**：跑一遍 worked examples 手算结果对一遍，再问一句"要不要我写一个 property-based test 来验证
   is_valid 和我手写的正则完全等价"，展示测试意识（S20）。

## 未解决点
- 官方来源没有公开 Part 2/3 的确切 I/O 契约（仅确认"numeronym validation"这个题干存在于 FinalRound 题
  库、Exponent 把它列为 Stripe coding 轮样题）；本题的 Part 2/3 设计是遵循 Stripe 电面一贯的"验证 → 对
  照真实数据 → 处理冲突"三段式模板做的合理重建，如果拿到更精确的原题转录应回来对照修订。

## 复盘（Fable 5.1，2026-09-01）
**改了什么**
- `solution.py` 重构为"规则常量 → 解析 helper → 三个 part → I/O 分发"四段：新增 `_parse_dictionary`
  （去重 + 过滤坏行，Part 2/3 共用）、`_expands_to`（Part 2 的匹配谓词单独一个函数）、`numeronym_for(word,
  prefix_len=1)`（prefix 1 就是 base 形式，Part 3 里不再手写两遍公式）；`_resolve_group` 的循环改为
  `range(2, max_prefix + 1)`，删掉原来"cap 单独再试一次"的重复分支；`main` 用 `PARTS` 表分发。
- **F（题面歧义）**：Part 2 词典含重复词时原实现会把同一个词打印两遍，题面没定义。现统一为"重复词只算一
  个"（与 Part 3 规则 5 一致），problem.md Part 2 + Edge cases 已补一句。starter_template/starter 的
  `part2` docstring 与 `main` 分发同步更新。
- 测试：`test_output_sorted_by_word_not_input_order` 从"只断言有序"改为精确串；新增 Part 2 去重、Part 3
  三路冲突需要前缀 3、不可消歧退化是"整组"三个用例。23 → 26。
- lint：black 110 + flake8 通过（此前 4 个文件 black 未格式化）。

**为什么**：checklist S 项"后 part 复用前 part / 规则集中一处 / 一个函数一件事"；原 `_resolve_group` 的
cap 分支是可读性负担而非必要；"只断言有序"的测试对 starter 也可能空过。

**遗留**：Part 2/3 的原题 I/O 契约仍是重建（见 未解决点）；perf 用例 100k 词约 0.3 s，未做进一步优化。
