# pc05 · Subarray Sums Divisible by K → 和恰为 K → 最长子数组

> 45 分钟第一轮里的编码环节常见题；Part 1、Part 2 是一手报道的原题，Part 3 **(reconstructed)**。

## 背景

一位 Millennium LEaD 候选人在 LeetCode Discuss 帖 7423863（Quant Dev-Python 岗）报道：第一轮 45 min（15 min 背景 + 30 min 编码）第二题就是 **LC 974（Subarray Sums Divisible by K）**；TechPrep 2026 汇总的 Millennium 题单也把它列为高频。这三个 part 都用同一个技巧：**前缀和 + 计数字典**——一旦把"子数组和"问题翻译成"两个前缀和的差"，剩下就是数一数字典。

## API 契约（英文签名）

```python
def count_subarrays_div_k(nums: list[int], k: int) -> int
def count_subarrays_sum_k(nums: list[int], k: int) -> int
def longest_subarray_sum_k(nums: list[int], k: int) -> tuple[int, int, int]
```
- `nums` 必须是 `list[int]`（元素非 `int`，或 `nums` 本身不是 `list`）→ `ValueError`。
- `count_subarrays_div_k` 的 `k` 是模数，必须是正整数（`k < 1`）→ `ValueError`。
- `count_subarrays_sum_k`、`longest_subarray_sum_k` 的 `k` 是目标和，可正可负可为 0，但必须是 `int`（否则 `ValueError`）。
- `longest_subarray_sum_k` 返回 `(length, start, end)`：`start`/`end` 是 0-indexed 闭区间下标；不存在这样的子数组时返回 `(0, -1, -1)`。

## 规则

### Part 1 — LC 974：和能被 K 整除的子数组个数

子数组 `(l, r]`（用前缀和 `P[0..n]`，`P[0] = 0`）的和能被 `K` 整除，当且仅当 `P[r] % K == P[l] % K`——同余的两个前缀凑一对。用一个计数字典边扫边累加：遇到某个余数时，先加上"之前出现过多少次这个余数"，再把当前余数计数 +1。一遍扫描，O(n) 时间、O(min(n, K)) 空间。

Python 的 `%` 对正 `K` 天然返回 `[0, K)` 内的值，负数元素不需要特殊处理——这和 C / Java 里 `%` 可能返回负数是两回事（追问会问到）。

### Part 2 — LC 560：和恰为 K 的子数组个数

同一个前缀和技巧，去掉取模：`(l, r]` 的和恰为 `K`，当且仅当 `P[l] == P[r] - K`。字典记录"每个前缀和出现过几次"，扫到 `r` 时查 `P[r] - K` 出现过几次就累加几。`K` 这里是目标和，不是模数，可以是 0 或负数。

### Part 3 — 最长的、和恰为 K 的子数组 **(reconstructed)**

不再数个数，而是要**最长**的那个 `(l, r]`，`tie` 时取**最左**（起点下标最小）的那个。同样是前缀和，但字典只记录**每个前缀和第一次出现的下标**（更晚的相同前缀和只会让子数组变短，没用）。扫到 `r` 时若 `P[r] - K` 出现过，候选长度是 `r - l`；**只在严格更长时才更新答案**——这一步顺带保证了并列最长时留住最左边那个（两个等长子数组的 `r` 差多少，`l` 也差多少，所以先扫到的那个 `r` 更小，对应的 `l` 也更小）。

## Worked examples（全部由 `solution.py` 实际运行得出）

**Part 1**
- `count_subarrays_div_k([4, 5, 0, -2, -3, 1], 5) = 7`
- `count_subarrays_div_k([5, 0, 0], 5) = 6`
- `count_subarrays_div_k([], 5) = 0`
- `count_subarrays_div_k([5], 5) = 1`，`count_subarrays_div_k([3], 5) = 0`

**Part 2**
- `count_subarrays_sum_k([1, 1, 1], 2) = 2`
- `count_subarrays_sum_k([1, 2, 3], 3) = 2`
- `count_subarrays_sum_k([1, -1, 0], 0) = 3`（`[1,-1]`、`[0]`、`[1,-1,0]` 三个子数组和为 0）

**Part 3**
- `longest_subarray_sum_k([1, -1, 5, -2, 3], 3) = (4, 0, 3)`（子数组 `[1,-1,5,-2]`）
- `longest_subarray_sum_k([-2, -1, 2, 1], 1) = (2, 1, 2)`（子数组 `[-1,2]`；`[1]` 单独也和为 1 但更短）
- `longest_subarray_sum_k([1, 2, 3], 100) = (0, -1, -1)`（不存在）

## `main()` 命令流

输入每两行一组查询：第一行是空格分隔的 `nums`（可为空行），第二行是 `k`。

```
PART 1                    PART 2                PART 3
4 5 0 -2 -3 1              1 1 1                  1 -1 5 -2 3
5                          2                      3
5 0 0                      → 2                    → 4 0 3
5
→ 7
  6
```

## 边界清单

- `nums = []`（空输入）→ 三个 part 都是"没有子数组"，Part 1/2 返回 `0`，Part 3 返回 `(0, -1, -1)`
- 单元素数组（`[5]`，`k=5`）
- 全部重复元素（如 `[1, 1, 1]`）
- `count_subarrays_div_k` 的 `k < 1` → `ValueError`
- `nums` 含非 `int` 元素或不是 `list` → `ValueError`
- Part 2/3 的 `k = 0`（找和为 0 的子数组，`k` 不是模数所以合法）
- Part 3 并列最长时必须取最左（见 Part 2 worked example 里 `[-1,2]` vs `[1]` 的对比）
- 大规模输入（10^4–10^5 元素）验证仍是 O(n)

## 追问

1. **负数取模**：Python 的 `%` 对正 `k` 返回值总落在 `[0, k)`；C / Java 里 `%` 可能返回负数，需要 `((x % k) + k) % k` 修正——这道题在 Python 里不用管，但面试官常追问其他语言怎么办。
2. **为什么是 O(n) 而不是 O(n²)**：暴力枚举所有 `(l, r)` 对是 O(n²)；前缀和把"子数组和"变成两个数的差，配合哈希表把"找配对"从 O(n) 查找降到 O(1) 摊还。
3. **流式版本**：如果 `nums` 是不断到来的流，只关心"目前为止和为 K 的子数组数"，三个 part 的字典都可以边到达边更新，不需要回看历史数组——这正是它们已经写成单遍扫描的原因。
4. **Part 1 的空间为什么是 `O(min(n, K))`**：余数最多只有 `K` 种取值，字典的 key 数不会超过 `min(n+1, K)`。

## 来源与置信度

- **HIGH（一手）**：LeetCode Discuss 7423863（Quant Dev-Python，Millennium LEaD 第一轮 Round 2），题面即 LC 974（`https://leetcode.com/problems/subarray-sums-divisible-by-k/`）；TechPrep 2026 Millennium 题单同列此题。
- Part 2（LC 560，`https://leetcode.com/problems/subarray-sum-equals-k/`）为同一报道帖里被提及的姊妹题，同一前缀和技巧的直接变体。
- Part 3（LC 325 "Maximal Size Subarray Sum Equals k" 的做法）未见于该轮的一手报道，标 **(reconstructed)**：是 Part 2 最自然的追问（"能不能不只数个数，还要最长的那个"）。

## 考什么

前缀和把子数组问题变成两数之差 · 用哈希表把"配对计数"降到 O(1) 摊还 · Part 3 额外练"只记第一次出现的下标"这个子技巧（与"最长无重复子串"里记最后一次出现下标正好相反，容易搞混）。
