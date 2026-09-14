# q14 Maximum Product of the Length of Two Palindromic Subsequences — report

## Summary
2023 Snowflake OA 候选人索引直接复用的 LC 2002 原题：`n <= 12` 的极小规模直接暗示位掩码枚举子集解法。Part 1 求两个不相交回文子序列的最大长度积；Part 2 **(reconstructed)** 追加要求给出一组具体达到该乘积的下标方案（多解问题，用 checker 校验而非逐字比对）。

## Sources & confidence
MED——`catalog/raw/coding_oa.md` #12，2023 Canada OA 索引 item #10，直链 LC 2002 https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/ （逐字复用）。Part 2 为重建。

## Approach by part
1. 枚举所有 `2^n` 个下标子集，O(n) 判断该子集对应字符序列是否回文并记录长度；对每个回文 mask，枚举其补集的所有子掩码（`sub=(sub-1)&comp`），若子掩码也回文则更新最大乘积。整体 O(3ⁿ)。
2. 同一次枚举里额外记住取得最大乘积的 `(mask1, mask2)` 对，转换成升序下标列表返回；因为最优解不唯一，测试用 checker（不相交、下标合法、各自回文、乘积达标）校验，不要求和参考实现的下标字面相同。

## Pitfalls hidden tests target
- 整串本身是回文（如 `"abcba"`）但必须真正切成两个不相交部分，不能整体当一侧
- 全同字符时最优是尽量平均切分（`n=12` 时 `6×6=36`）
- 最短输入 `len(s)=2` 两个不同字符时乘积恒为 1
- 非法输入：长度越界（<2 或 >12）、非小写字母（大写/数字/非 ASCII）→ `ValueError`
- Part 2 多解：checker 只校验合法性与乘积，不比对具体下标

## Complexity & measured cost
O(3ⁿ) 时间、O(2ⁿ) 空间，n<=12 时约 5×10⁵ 次判断。编排者验证：Part 1 与"每个下标分配到 {跳过, 子序列1, 子序列2} 的递归枚举"（另一条 O(3ⁿ) 路径但实现完全独立）在 120 组随机小输入（n<=8）上 0 不一致；Part 2 同样用 checker 在 60 组随机输入上验证。perf：n=12（题目规模上限本身）两个 part 均 < 2 s。

## Test inventory
20 tests — part1 11（含 3 参数化 worked examples、6 参数化非法输入、1 随机 brute-force、1 perf、1 io）· part2 5（含 6 参数化最优性校验、随机 brute-force、非法输入、1 perf、1 io/fmt）；edge 12 · fmt 1 · perf 2 · io 2。

## Skills exercised
位掩码枚举子集 + 枚举子掩码的 O(3ⁿ) 技巧（从极小 n 反推预期解法）· 回文判定 · 多解问题的 checker 式测试设计。
