# q16 Number of Ways to Form a Target String Given a Dictionary — report

## Summary
2023 Snowflake OA 候选人索引直接复用的 LC 1639 原题：从等长单词词典里按严格递增的列选择拼出 target，统计方案数。Part 1 是标准的 0/1 背包式一维 DP；Part 2 **(reconstructed)** 退化成存在性问题——不关心哪个单词提供字符，只求字典序最小的可行列序列，用贪心/子序列匹配思路解决。

## Sources & confidence
MED——`catalog/raw/coding_oa.md` #15，2023 Canada OA 索引 item #13，直链 LC 1639 https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/ （逐字复用）。Part 2 为重建。命名冲突警示：2025 Infra Automation Intern OA 的同名题是不同问题，已在 problem.md 注明。

## Approach by part
1. 预处理每列每个字符出现的单词数 `cnt[j][ch]`；一维 DP `dp[i]` = 用当前列拼出 target 前 i 个字符的方案数，按列从左到右遍历、每列内部 i 倒序更新（0/1 背包技巧，保证同一列不会在一次遍历里被用两次），答案 `dp[n] mod 1e9+7`。
2. 贪心扫描列：对 target 每个字符，在"大于上一次选择"的列里找最小的、含该字符的列；等价于经典的"判断子序列"双指针，局部贪心即全局字典序最优。

## Pitfalls hidden tests target
- 同一列不能被复用满足两个不同位置（`["aaa"], "aa"` 必须是 `C(3,2)=3` 而非把同一列算两次）
- target 比单词短的一般情形
- 完全无法拼出的情况（Part1 返回 0，Part2 返回 `[]`）
- 非法输入：单词长度不一致、target 比单词长、非小写字符、空输入 → `ValueError`
- 命名冲突：不要把这题和 2025 Infra OA 同名题混淆（problem.md 已标注）

## Complexity & measured cost
O(n·m) 时间（n=target 长度，m=单词长度）、O(n) 额外空间。编排者验证：Part 1 与 `itertools.combinations` 枚举所有严格递增列组合的纯组合数暴力在 150 组随机小输入上 0 不一致；Part 2 与"combinations 按字典序枚举、取第一个可行组合"的独立暴力在 150 组随机小输入上 0 不一致。perf：words 与 target 长度均到 1000 时两个 part 端到端均 < 2 s。

## Test inventory
22 tests — part1 12（含 4 参数化 worked examples、6 参数化非法输入、1 随机 brute-force、1 perf、1 io）· part2 7（含 3 参数化 worked examples、随机 brute-force、1 perf、1 io/fmt）；edge 12 · fmt 1 · perf 2 · io 2。

## Skills exercised
0/1 背包式一维 DP（资源不可重复使用的建模）· 子序列匹配贪心/双指针 · 精确输入契约（长度约束、字符集）的显式校验。
