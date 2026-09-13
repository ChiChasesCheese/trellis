# ps05 Numeronym validation — report

## Summary
A three-part "validate → look up → generate with conflicts" string-processing question. Stripe's
phone screens like this shape because it rewards careful spec-reading (leading-zero rule, case
sensitivity) over algorithmic cleverness, and Part 3 forces the candidate to notice — unprompted —
that generation can collide, which is exactly the kind of "what happens when two things map to
the same identifier" question Stripe cares about for real (idempotency keys, short URL slugs).

## Sources & confidence
medium — FinalRoundAI's Stripe question bank names "numeronym validation" directly (page live
2026); Exponent's guide lists it among Stripe coding-round sample questions but without a
published I/O contract. The regex form of Part 1 and the "dictionary + collisions" shape of
Parts 2-3 are this report's reconstruction of the standard numeronym definition, not a verbatim
transcript -- flagged as an open point below.

## Approach by part
1. **Validate**: `^[a-z][1-9][0-9]*[a-z]$` -- one regex, but the two traps (leading zero, digit=0)
   are easy to miss if you write `\d+` without the leading-`[1-9]` anchor.
2. **Expand against a dictionary**: numeronym -> `(first, last, expected_len)`, filter dictionary
   words structurally, sort. O(dictionary size).
3. **Generate + resolve collisions**: group words by `(first, last, length)` (the base numeronym);
   singleton groups are done; colliding groups grow a literal prefix (2, 3, ...) until forms
   diverge, capped so the digit segment never goes below 1; groups that still collide at the cap
   (words differing only in the character right before the last one) fall back to the literal
   word for every member -- this is the one non-obvious design decision in the whole problem and
   is called out explicitly as "面试官会怎么追问" item 3.

## Pitfalls hidden tests target
- `i018n` (leading zero) vs `i18n` -- numerically equal digit value, string-invalid
- `i0n` -- digit count 0 is not a degenerate-but-valid numeronym
- case sensitivity independent of the digit rules
- Part 2 malformed dictionary lines (uppercase, embedded digits) must be skipped, not crash
- Part 2 on a structurally invalid numeronym -> `NONE`, not an exception
- Part 3 words < 3 chars -> map to themselves (never crash on `len(word) - 2 < 0`)
- Part 3 3-way collisions resolved at the *same* prefix length for the whole group
- Part 3 the irreducible-collision fallback (`flap`/`flip`) -- the one case a naive "just grow the
  prefix" implementation gets wrong (infinite loop or a digit of 0, which would itself be invalid
  per Part 1's own rule)
- Part 3 duplicate dictionary lines collapse to one entry, not one output line per line

## Complexity & measured cost
Part 1/2: O(n) in input size. Part 3: O(n) to bucket by base form, plus O(k^2 . g) for each
colliding group of size `g` at up to `k` prefix lengths tried -- negligible in practice since real
dictionaries have few collisions per (first, last, length) bucket. Measured: 100,000 random
3-15 char lowercase words, Part 3 end-to-end (stdin -> stdout) in well under 2 s, ~24 MB RSS
(perf budget is 2 s / 256 MB) -- see `test_perf_100k_words`.

## Test inventory
23 tests -- part1: 8 (incl. 1 io) . part2: 6 . part3: 9 (incl. 1 io, 1 perf); edge 7 . fmt 3 .
io 3 . perf 1.

## Skills exercised
S02 parsing/regex discipline . S08 deterministic sort with stated tie-break . S09 exact string
formatting . S14 string canonicalization/case rules . S18 validation and error paths .
S19 incremental design (Part 3 builds directly on Part 1's `is_valid`)

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

## Open points
- 官方来源没有公开 Part 2/3 的确切 I/O 契约（仅确认"numeronym validation"这个题干存在于 FinalRound 题
  库、Exponent 把它列为 Stripe coding 轮样题）；本题的 Part 2/3 设计是遵循 Stripe 电面一贯的"验证 → 对
  照真实数据 → 处理冲突"三段式模板做的合理重建，如果拿到更精确的原题转录应回来对照修订。

## Review（Fable 5.1，2026-09-01）
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

**遗留**：Part 2/3 的原题 I/O 契约仍是重建（见 Open points）；perf 用例 100k 词约 0.3 s，未做进一步优化。
