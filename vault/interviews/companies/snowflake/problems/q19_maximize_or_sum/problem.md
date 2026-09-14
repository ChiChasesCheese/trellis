# q19 · Maximize OR-Sum — 至多 k 次翻倍，让整个数组的按位或最大

> OA 题（2026-05 Snowflake AIML 实习 HackerRank，一手原帖）。Part 1 为原题；Part 2 **(reconstructed)**：k 到 10⁹，结果取模。

## 背景

候选人原帖（Reddit r/cscareerquestions，2026-05-01）：

> "maximize OR-Sum (Greedy + Bit Manipulation) Given an array of n integers, you can perform up to k operations where each operation doubles any element. Return the maximum possible bitwise OR of all elements after operations. Example: arr = [12, 9], k = 1 → 30 … To maximize OR, apply all k operations to the largest element."

**发帖人自己的思路是错的**，评论区当场指出：`[12, 9], k = 1` 把最大的 12 翻倍得 `24 | 9 = 25`，把 9 翻倍得 `12 | 18 = 30`。发帖人回复"考试时没想清楚，只翻倍最大的也过了测试"——说明 HackerRank 的测试用例没覆盖这个反例，但面试官或更严的测试会。**这道题练的就是"一眼贪心"和"正确贪心"的差别。**

## 输入

- `1 ≤ n ≤ 10⁵`，`0 ≤ nums[i] < 2³¹`；
- 每次操作把**任意一个**元素乘 2（左移一位），总共至多 `k` 次，同一个元素可以被多次选中。

非法输入抛 `ValueError`：空数组、`k < 0`、元素越界。

## API 契约（英文签名）

```python
def max_or_sum(nums: list[int], k: int) -> int
def max_or_sum_mod(nums: list[int], k: int) -> int
```

## 规则

### Part 1 — 精确值（`k ≤ 15`）

返回操作后所有元素按位或的最大值。

**关键事实**：k 次操作**全部给同一个元素**一定最优。把某个元素左移 k 位，它的最高位到达 `msb + k`，任何"分给几个元素"的方案都到不了这么高；而 OR 只关心哪些位是 1。所以答案是：对每个 `i`，`(nums[i] << k) | (其余所有元素的 OR)` 取最大。其余元素的 OR 用前缀 OR 和后缀 OR 在 O(1) 内得到，整体 O(n)。

### Part 2 — k 到 10⁹，结果对 `1_000_000_007` 取模 **(reconstructed)**

精确结果有约 10⁹ 位，不能真的算出来再比较。
- `k ≤ 64` 时照 Part 1 精确算再取模；
- `k > 64` 时，被翻倍的元素整体落在第 31 位以上，**和其余元素的位完全不重叠**，候选值是 `nums[i]·2^k + others_i`：先比 `nums[i]`（大者胜），相等再比 `others_i`，选出最优 `i` 后用 `pow(2, k, MOD)` 算取模结果。

**注意**：取模之后的数不能拿来比较大小——必须先在"真实大小"上选出最优下标，再取模。

## Worked examples（全部由 `solution.py` 实际运行得出）

| nums | k | Part 1 | Part 2 |
|---|---|---|---|
| `[12, 9]` | 1 | `30`（翻倍 9：`12 | 18`） | `30` |
| `[8, 1, 2]` | 2 | `35`（`32 | 1 | 2`，LC 2680 例 2） | `35` |
| `[5]` | 3 | `40` | `40` |
| `[1, 2, 4]` | 0 | `7` | `7` |
| `[12, 9]` | 10⁹ | — | `687500014` |
| `[3, 3, 1]` | 100 | — | `929113844` |

## `main()` 命令流

```
PART 1          PART 2
2 1             2 1000000000
12 9            12 9
→ 30            → 687500014
```

## 边界清单

- 翻倍最大元素不是最优（`[12, 9], k = 1`）
- 全 0；只有一个元素；`k = 0`
- 多个相等的最大值（Part 2 要比"其余元素的 OR"）
- `k` 恰在 64 附近（Part 2 的两条路径切换处）
- 非法输入：空数组、负 k、`2³¹`、负数
- 性能：`n = 10⁵` 两个 part 都 < 2 s

## 追问

1. **为什么全给一个元素最优？** 位的最高位置决定大小；`msb(nums[i]) + k` 是任何方案能达到的最高位，只有全给一个元素才能达到。
2. **能不能只试最大的那个元素？** 不能（本题例 1）。能不能只试最高位最大的那些元素？可以缩小候选，但最坏情况下所有元素最高位相同，仍要枚举。
3. **把"翻倍"换成"乘 3"呢？** 乘 3 会产生进位、改变低位，贪心不再成立。
4. **没有前缀后缀数组，O(1) 额外空间怎么做？** 统计每一位被多少个元素占用（31 个计数器），去掉元素 i 时只清掉计数为 1 且属于 i 的位。

## 来源与置信度

- **HIGH（一手，逐字题面 + 样例）**：Reddit r/cscareerquestions `1t0ogu7`（2026-05-01，Snowflake AIML Intern HackerRank，同场另一题为 Student/Result OOP）：https://www.reddit.com/r/cscareerquestions/comments/1t0ogu7/ 。原文与评论见 `../../catalog/discovery/harvest/reddit_posts_2026-09-13.json`，triage 见 `../../catalog/discovery/TRIAGE.md` #4。
- **LOW（聚合站）**：interviewfox 2026 OA 回忆，`../../catalog/raw/coding_oa.md` #44。
- 与 LC 2680 "Maximum OR" 是同一题：https://leetcode.com/problems/maximum-or/
- Part 2 为重建。

## 考什么

S08 贪心的正确性论证（区分"看起来对"和"证明对"）· 位运算 · 前后缀预处理 · 超大数取模时"先比较后取模"。
