# q02 · Vowel-Run DP — counting strings and substrings by consecutive-vowel runs

**Type:** bespoke OA · **Stage:** Online Assessment · **Last asked:** 2024-10 (FastPrep) /
2022-09-08 (LeetCode discuss) · **Frequency:** 3 independent sources across 2022→2026 ·
**Confidence:** high (part1/part3 verbatim quotes), medium-high (part2 FastPrep + cross-refs)

## 背景

Snowflake 的 OA 题库里反复出现同一个 DP 家族："计数满足元音游程约束的字符串"。字母表固定为 26 个
小写字母，元音 `{a, e, i, o, u}` 5 个，辅音 21 个。三个 part 都围绕同一个状态设计：
`dp[i][j]` = 长度为 i、且当前结尾正好是长度为 j 的连续元音游程的字符串数（j=0 表示结尾是辅音，或
字符串为空）。part1/part2 是同一 DP 的两个变体（无 mod / 有 mod + 大 n 要求效率），part3 是同一
"元音游程" 概念在具体字符串上的应用（数子串而不是数抽象字符串）。

## 输入格式

`main()` 的 stdin 格式：第一行 `PART n`（n ∈ {1,2,3}）；第二行是该 part 的 payload：
- PART 1 / PART 2：一行 `n k`（两个非负整数，空格分隔，对应 `part1`/`part2` 的位置参数）
- PART 3：一行原始字符串 `s`（可以是空行，表示空字符串）

输出：一行单个整数（十进制，无多余空格/调试输出）。

## 规则 Part 1..3

### Part 1 — count strings, no mod

> "You are given two integers n and k. Return the number of strings of length n you can form
> where there are no more than k consecutive vowels in the string."
>
> — Snowflake Core/Data Engineering Intern OA, 2022-09-08, LeetCode discuss

`part1(n: int, k: int) -> int` — 恰好返回长度为 n、字母表为 26 个小写字母、任意连续元音游程长度都
不超过 k 的字符串个数，**精确整数**（Python 大整数，不取模）。

DP：`dp[j]`（0<=j<=k）= 到目前为止以恰好 j 个连续元音结尾的方案数（j=0 桶同时代表"以辅音结尾"和
"空串"）。转移：从任意状态追加 1 个辅音（21 种）都会把游程清零 → 新的 `dp[0] = 21 * sum(dp)`；从
状态 j-1 追加 1 个元音（5 种）把游程延长到 j → 新的 `dp[j] = 5 * dp[j-1]`（j=1..k）。长度 n=0 的
基准：空串，`dp = [1, 0, ..., 0]`。最终答案是长度 n 后所有桶求和。

手算校验（务必先用小 n 验证再信任实现）：n=1, k=0（完全不允许元音）→ 21（只能选辅音）；
n=1, k>=1 → 26（任意字母都行，因为单字符游程最长是 1）。

### Part 2 — calculateWays with modulus, large n

> "Given a word length and maximum consecutive vowels allowed, calculate how many unique words
> can be generated... no more than `maxVowels` consecutive vowels."
>
> — FastPrep "Calculate Ways", `calculateWays(wordLen, maxVowels) -> int mod 1e9+7`,
>   `wordLen` up to 2500

`part2(word_len: int, max_vowels: int) -> int` — 和 part1 同一个 DP，但结果对 `1_000_000_007`
取模，并且 `word_len` 最大到 2500 时必须高效（`O(word_len * max_vowels)` 或更好；因为
`max_vowels <= word_len`，最坏 O(n^2)（n=2500）约 625 万次基本运算，纯 Python 用内置 `sum()` /
列表操作实测 <0.5s，足够快）。

**已验证的样例（FastPrep 原题，必须精确匹配）：** `calculateWays(1,1) == 26`；
`calculateWays(4,1) == 412776`；`calculateWays(4,2) == 451101`。这些 n 很小，所以
`part1(4,1)` 不取模也应该等于 412776，`part1(4,2)` 等于 451101 —— 加一个交叉验证测试断言
`part1` 和 `part2` 在这些小样例上一致（`part1(4,1) == part2(4,1)`）。

### Part 3 — vowel-only substrings containing every vowel

> "You are given a string s. Return the number of substrings within s that contain at least one
> of each vowel, and do not contain any consonants."
>
> — 同 part1 来源，2022-09-08

也有交叉引用：LeetCode 1987/2062 同族题（2023 Canada 题库索引），
`https://www.fastprep.io/problems/snowflake-vowel-substring`。

`part3(s: str) -> int` — 统计 `s` 中满足以下两个条件的子串数量：(a) 子串**完全**由元音字符组成
（a/e/i/o/u，不含任何辅音）；(b) 子串包含全部 5 个不同的元音各至少一次。

**算法（已手工验证正确）：** 把 `s` 按"任何辅音都会打断游程"的规则切成若干个最大元音游程。对每个
长度为 L 的游程 `r`（游程内部下标从 0 开始），从 `j=0` 扫到 `L-1`，维护 `last[v]` = 游程内到目前
为止元音 `v` 最后出现的下标。一旦 5 个元音都出现过（`last` 里凑齐 5 个 key），当前 `j` 对答案的
贡献是 `min(last.values()) + 1`（因为下标是游程局部的，游程起点是 0）。把每个 `j` 的贡献和每个
游程的贡献都累加起来就是最终答案。

## 3+ Worked Examples

```
part1(1, 0)  == 21        # 完全不允许元音，只能选 21 个辅音之一
part1(1, 5)  == 26        # k >= n，无约束，任意字母
part1(0, 0)  == 1         # 空串，vacuous true
part1(3, 3)  == 26 ** 3   # k >= n，无约束

part2(1, 1)  == 26
part2(4, 1)  == 412776    # FastPrep 官方样例
part2(4, 2)  == 451101    # FastPrep 官方样例
part1(4, 1)  == part2(4, 1)  == 412776   # 交叉验证：part1 不取模应与 part2 取模前数值一致

part3("aeiou")        == 1   # 恰好一个游程，恰好用完 5 个元音各 1 次
part3("aeiouu")       == 2   # 游程 "aeiouu"：j=4 时全 5 元音齐 → +1；j=5 时依然齐 → +1，共 2
part3("aeioub")       == 1   # 'b' 结束游程，不增加贡献
part3("aeioubaeiou")  == 2   # 两个独立游程 "aeiou" + "aeiou"，各贡献 1
part3("xyz")          == 0   # 完全没有元音游程
part3("aeiobu")       == 0   # 'b' 把 "aeio" 和 "u" 拆成两段，谁都凑不齐 5 个元音
```

## 隐藏测试边界清单

- `n=0` / `word_len=0`：空字符串，恰好 1 种方案（空字符串对"任何游程都不超过 k"是 vacuously true）
- `k=0` / `max_vowels=0`：完全不允许元音，答案退化为 `21^n`（part2 取模）
- `k >= n` / `max_vowels >= word_len`：约束形同虚设，答案是 `26^n`（或取模）
- part1 的结果必须是**精确大整数**，不能悄悄取模（用 n=30 左右、无约束的场景验证结果远大于
  `1e9+7` 且等于 `26**n` 精确值）
- `s=""`（part3）：答案 0
- 完全没有元音的字符串（part3）：答案 0
- part2 用 `word_len=2500`（`max_vowels` 从 1 到 2500 各种取值）做性能测试，必须远小于 2s
- part3 用一个长度 ~1e6、由 `random.Random(0)` 生成的元音密集字符串做性能测试，同样必须远小于 2s
- part3 中一个元音在游程内重复出现、且在"凑齐 5 个"之前或之后都重复出现的情况（用暴力法交叉验证）

## 变体

- 把"最多连续 k 个元音"换成"最少连续 k 个元音"（同一 DP 状态机，只是转移条件反过来）。
- part3 变体：不要求"完全由元音组成"，只要求"包含全部 5 个元音"（不排除辅音）——这是完全不同的
  滑窗题（LC 1987/2062 精确形态），本题特意保留"纯元音子串"这个更强的约束。
- word_len 上限从 2500 提到 10^5+，需要把 DP 换成 O(n) 的滑动窗口线性递推（本题的 O(n·k) 实现在
  这个规模下会超时，属于已知的"下一步优化"追问）。

## 来源与置信度

- https://leetcode.com/discuss/interview-question/2550834/Snowflake-OA-(CoreData-Engineering-Intern)
  — 2022-09-08, Core/Data Engineering Intern OA, HIGH confidence，part1/part3 均为原题逐字引用。
- https://www.fastprep.io/problems/calculate-ways — 2024-10, MEDIUM，part2 的官方样例
  （`calculateWays(1,1)=26`, `calculateWays(4,1)=412776`, `calculateWays(4,2)=451101`）。
- https://leetcode.com/discuss/interview-question/2825744 — 2022-11-17 图片帖，交叉引用同一
  DP 题族。
- 2026 linkjob 面经复盘（同一 DP 题族，MEDIUM，与 FastPrep 合并计入置信度）。
- https://www.fastprep.io/problems/snowflake-vowel-substring — part3 的交叉引用来源。

## 考什么

skills: **S02** 计数 DP（状态 = 位置 × 游程/剩余长度，取模）· S06 整数取模运算 · S07 大 n 下的
DP 效率优化（避免 O(n^2) 在边界规模超时）· S09 精确格式化输出（stdin/stdout 单行整数协议）。
