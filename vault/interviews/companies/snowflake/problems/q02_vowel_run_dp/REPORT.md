# q02 Vowel-Run DP — report

## 摘要

同一个"数连续元音游程"的 DP 状态机，在 Snowflake OA 题库里出现三次：一次要精确大整数
（part1）、一次要取模且要求大 n 下高效（part2，FastPrep 官方题），一次把同样的"游程"概念用在
具体字符串的子串计数上（part3）。三个 part 共享同一个心智模型（`dp[j]` = 结尾游程长度恰为 j 的
方案数），但落地成三种不同的工程约束：大整数精度、取模 + 性能、字符串扫描 + O(1) 增量判定。

## 来源与置信度

- high：https://leetcode.com/discuss/interview-question/2550834/ （2022-09-08，Core/Data
  Engineering Intern OA，part1/part3 均逐字引用）。
- medium-high：https://www.fastprep.io/problems/calculate-ways （2024-10，part2 官方样例，
  三个样例全部用于测试且全部通过）。
- medium：2022-11-17 LeetCode discuss 图片帖 + 2026 linkjob 面经复盘，交叉印证同一题族反复出现。
- medium：https://www.fastprep.io/problems/snowflake-vowel-substring，part3 交叉引用。

## 逐 part 思路

1. **part1**：状态向量 `dp[0..k]`，`dp[0]` 是"以辅音结尾/空串"桶，`dp[j]` 是"恰好 j 个连续元音
   结尾"桶。每步转移：`new_dp[0] = 21 * sum(dp)`（追加辅音，任何状态都能到达），
   `new_dp[j] = 5 * dp[j-1]`（追加元音，把游程延长 1）。答案是长度 n 后 `sum(dp)`，用 Python 原
   生大整数，不取模。用 `cap = min(k, n)` 裁剪状态向量长度，避免为用不到的状态分配空间。
2. **part2**：与 part1 完全相同的转移，只是每步都对 `1_000_000_007` 取模。为了在
   `word_len<=2500` 时稳定 <2s，用内置 `sum(dp)`（C 级别实现）而不是 Python for 循环求和，实测
   `word_len=k=2500`（最坏情形，`O(n·k)`≈625 万次基本运算）约 0.3s。
3. **part3**：先按"任何辅音都打断游程"切出所有最大元音游程，游程内用一个 5-key 的 `last` 字典
   增量维护每个元音最后出现的下标；一旦 5 个 key 全部出现，当前右端点的贡献是
   `min(last.values()) + 1`（游程局部下标，起点为 0）。整体 `O(len(s))`，因为每步只做 O(1)（最多
   5 个 key）的字典更新和 min 计算。

## 隐藏测试针对的坑

- **part1 精度**：容易在实现时顺手加个 mod（复制 part2 代码时忘记去掉），加了一个专门测试
  `test_no_mod_stays_exact_big_int` 用 n=30 无约束场景断言结果精确等于 `26**30`（远超 1e9+7），
  能抓住这个坑。
- **part2 性能**：naive 的 O(n·k) 双重 Python for 循环（不用内置 `sum`）在 n=k=2500 时可能逼近
  甚至超过 2s 预算；用内置 `sum()` 规避。
- **part3 游程边界**：辅音紧跟在"刚好凑齐 5 元音"之后不应该产生额外贡献（`"aeioub"` == 1，不是
  2）；辅音把一个本可能凑齐的游程斩断在中途也不能被误算（`"aeiobu"` == 0）。这两个都在样例里
  显式覆盖。
- **part3 重复元音**：同一元音在"凑齐 5 个"前后重复出现时，`min(last.values())` 必须用**最新**
  的 `last` 更新之后再取 min，用暴力法（`test_matches_brute_force_random_short_strings` +
  `test_repeated_vowels_before_and_after_completion`）交叉验证。
- **k>=n / max_vowels>=word_len 退化**：容易在状态向量裁剪逻辑（`cap = min(k, n)`）写错导致越界
  或漏算，用显式的 `26**n` 断言覆盖。

## 复杂度与实测

- part1 / part2：`O(n * min(k, n))` 时间，`O(min(k, n))` 空间。实测 `word_len=k=2500`：约
  0.25–0.3s（预算 2s）。
- part3：`O(len(s))` 时间，`O(1)` 额外空间（游程内 last 字典最多 5 个 key）。实测长度 1e6 的
  元音密集随机字符串：远小于 2s。

## 测试清单

29 个测试 — part1: 6（含 1 大整数精度校验）· part2: 8（含 2 perf）· part3: 10（含 1 perf）·
io: 5。标记分布：edge 11 · perf 3 · io 5。`IMPL=starter` 下全部 18 个断言型测试失败（真实断言
失败，非 collection error），`solution.py` 下全绿。

## 技能 ids

S02 计数 DP（状态 = 位置 × 游程/剩余长度，取模）· S06 整数取模运算 · S07 大 n 下的 DP 效率优化
（避免 O(n^2) 在边界规模超时）· S09 精确格式化输出（stdin/stdout 单行整数协议）。
