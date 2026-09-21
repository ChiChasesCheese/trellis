# pc05 Subarray Sums Divisible by K — report

## Summary
一手报道：Millennium LEaD 第一轮 45 min 编码里的一题就是 LC 974（Subarray Sums Divisible by K）。3-part：Part 1 数能被 K 整除的子数组个数（一手原题）→ Part 2 数和恰为 K 的子数组个数（同贴提及的姊妹题 LC 560）→ Part 3 最长的、和恰为 K 的子数组，并列取最左 **(reconstructed)**。三个 part 都是前缀和 + 哈希表这一个技巧的变形。

## Sources & confidence
HIGH（一手）：LeetCode Discuss 7423863（Quant Dev-Python，Round 2）+ TechPrep 2026 Millennium 题单，两者都列 LC 974；Part 2（LC 560）同贴提及为姊妹题；Part 3（等价于 LC 325 的做法）未见一手报道，标 (reconstructed)。

## Approach by part
1. 前缀和取模：`P[r] % K == P[l] % K` 即整除，用计数字典边扫边累加同余对数，O(n) 时间、O(min(n, K)) 空间。
2. 去掉取模，字典改记"每个前缀和出现次数"，查 `P[r] - K` 出现几次即累加几次。
3. 字典只记"每个前缀和第一次出现的下标"（更晚出现只会让子数组更短），查到 `P[r] - K` 就算长度，**严格更长才更新**——顺带保证了并列最长时留住最左边那个（`r` 更小则对应 `l` 也更小）。

## Pitfalls hidden tests target
- Part 1：`k <= 0`（模数非法）、`nums` 含非 `int` 元素、空数组、全部重复元素（`[0,0,0]` 应数出全部 6 个子数组）
- Part 2：目标和为负数、为 0（`[1,-1,0]` 有 3 个子数组和为 0）、单元素恰好命中/不命中
- Part 3：并列最长必须取最左（`[-2,-1,2,1], k=1` 里 `[-1,2]` 长 2 比 `[1]` 长 1 更优）、无解要返回 `(0, -1, -1)`、全部重复元素时的最左并列（`[1,1,1,1], k=2` → `(2, 0, 1)`）
- 所有三个 part 都用暴力 O(n²) 枚举做了 400 组随机数组的交叉验证

## Complexity & measured cost
三个 part 都是 O(n) 时间、O(n) 空间（Part 1 的空间上界是 `min(n, K)`）。编排者验证：Part 1/2/3 与暴力枚举在 400 组随机数组（长度 0–14，元素 [-9,9]）上均 0 处不一致。perf：10 万元素的数组、`k=5`，`solution.py` 作为脚本端到端 < 2 s（实测远小于 2 s，见 `test_perf_100k_elements`）。

## Test inventory
27 tests — part1 10（含 1 perf、1 io）· part2 8（含 1 io）· part3 9（含 1 io/fmt）；edge 15 · fmt 1 · perf 1 · io 3。`grep -c "def test" test_pc05.py` = 27。

## Skills exercised
前缀和把子数组和问题变成两数之差 · 用哈希表把"配对计数/配对查找"降到 O(1) 摊还 · "只记第一次出现的下标"这个子技巧（与最长无重复子串"记最后一次出现下标"相反）· 并列答案的确定性 tie-break。
