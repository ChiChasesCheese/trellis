# pc07 Anagram Store — report

## Summary
一手报道：PracHub 的 Millennium 题单（Technical Screen，2026-02-12）"Design a data structure to store anagrams"；同一份 StealthCoder 社区标签统计把 Valid Parentheses 也列进 Millennium 报道题目。3-part 设计题，前面接一道 Valid Parentheses 热身：热身 + Part 1 `add/group_of/count`（对照两种分组键）→ Part 2 `remove` + `most_common_group`（一手原题）→ Part 3 大小写/Unicode 策略 + 流式 top-k **(reconstructed)**。

## Sources & confidence
HIGH：PracHub `prachub.com/companies/millennium`（Technical Screen，2026-02-12）"Design a data structure to store anagrams"；StealthCoder Millennium 标签列表收录 Valid Parentheses（Easy）。Part 3（大小写/Unicode 策略、流式 top-k）未见一手报道，标 (reconstructed)：是"存储 + 分组查询"设计题最自然的追问方向。

## Approach by part
1. 热身用栈匹配括号。Part 1 用 `dict[str, list[str]]` 存分组：键统一用排序字符串（`canonical_key_sorted`），另给出 26 位计数向量版本（`canonical_key_counts`）做复杂度对照——两者在随机小写词上产生完全相同的分组划分。
2. `remove` 按字面量身份删除分组内的一个实例（不是同组任意删一个）；`most_common_group` 用 `(-len(group), key)` 排序取最小，保证并列时结果不依赖插入顺序。
3. `case_sensitive=False` 时用 `str.casefold()` 折叠后再排序作为分组键，但分组列表里保留原始大小写；`top_k_groups` 复用 `most_common_group` 的并列规则，对全部分组排序后切片。

## Pitfalls hidden tests target
- `canonical_key_counts` 遇到大写/数字/非 ASCII 字符必须 `ValueError`（固定字母表的代价），`canonical_key_sorted` 对同样的输入不报错——两者的适用边界必须能讲清楚
- `remove` 删除"从未加入"或"已删光"的词 → `ValueError`；同一词被 `add` 两次时 `remove` 只删一个实例，另一个还在
- `most_common_group` / `top_k_groups` 的并列必须按分组键字典序（不是插入顺序、不是词本身的字典序）——用 `["zz","aa"]` 这种"后插入的词字典序更小"的用例专门验证
- `top_k_groups(k)`：`k` 超过现有分组数返回全部而不报错；`k` 非正整数 → `ValueError`
- Unicode 输入（如 `naïve` 与打乱后的 `ïanev`）必须按 code point 排序正确分组；`café` 的 `é`（U+00E9）排在 ASCII 字母之后，不是之前——写测试前先用 `solution.py` 实跑验证，不能凭直觉猜排序结果
- io 测试覆盖 Part 1/2/3 三条完整命令流，Part 3 额外挂 `fmt`（验证 `|` 与空格两级分隔符的精确格式）

## Complexity & measured cost
`add`/`group_of`/`count`：均摊 O(L log L)（`L` 为词长，排序键的开销）。`remove`：O(group 长度)（`list.remove` 的线性查找 + 删除）。`most_common_group`：O(G)（`G` 为分组数）。`top_k_groups`：O(G log G)（对全部分组排序后切片）。perf：2 万次 `ADD`（随机 5 字母词）+ 一次 `TOPK 5`，`solution.py` 作为脚本端到端 < 2 s（编排者验证）。

## Test inventory
25 tests — part1 10（含 1 io）· part2 7（含 1 io）· part3 8（含 1 io/fmt、1 perf）；edge 15 · fmt 1 · perf 1 · io 3。`grep -c "def test" test_pc07.py` = 25。空 `starter.py`（`starter_template.py` 的拷贝）跑同一套测试：25 个里 20 个失败，全部三个 part 都大面积红。

## Skills exercised
哈希分组键的设计权衡（O(L log L) 通用排序键 vs O(L) 但字母表受限的计数向量）· `dict[key, list]` 实现"分组容器"的增删查改，删除按字面量身份而非分组任意成员 · 排序并列的 tie-break 必须显式写死（分组键字典序），不能依赖 `dict`/插入顺序 · Unicode 大小写折叠（`casefold()` 而不是 `lower()`）与 code point 排序的边界直觉 · 从"一次性查询"到"流式 top-k"时复用同一套排序规则而不是另起一套逻辑。
