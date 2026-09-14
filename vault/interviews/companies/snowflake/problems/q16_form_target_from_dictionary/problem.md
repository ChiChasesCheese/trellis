# q16 · Number of Ways to Form a Target String Given a Dictionary — 从词典拼出目标串的方案数

> 2023 Snowflake OA 候选人索引直接复用的 LeetCode 原题。Part 1 为原题；Part 2 **(reconstructed)**：不关心具体是哪个单词提供字符，只问"能否拼出来，最小字典序的列选择是什么"。

## 背景

`catalog/raw/coding_oa.md` #15（对应 2023 Canada OA 索引 item #13）："String Formation via dictionary (LC-exact)"，直链 LC 1639 "Number of Ways to Form a Target String Given a Dictionary"，confidence MED，逐字复用。

**命名冲突提醒（来自 catalog）**：2025 夏季 Infrastructure Automation Intern OA 里也有一道叫"String Formation"的题（1point3acres thread-1120493），但那是完全不同的一道题（页面 403，只有 WebSearch 摘要），不要与本题（LC 1639）混淆——本题的来源锚定在 2023 Canada 索引的直链 LC URL，置信度更高。

## 输入格式

- `words: list[str]`，非空，所有单词**等长**（记这个长度为 `m`），仅小写字母；
- `target: str`，非空，仅小写字母，`len(target) <= m`。

把 `words` 想象成堆叠成一个 `len(words) × m` 的网格。非法输入（`words`/`target` 为空、单词长度不一致、`target` 比单词还长、含非小写字符）抛 `ValueError`。

## API 契约

```python
def num_ways_to_form_target(words: list[str], target: str) -> int
def smallest_column_assignment(words: list[str], target: str) -> list[int]
```

## 规则

### Part 1 — LC 1639 原题

从左到右拼出 `target`：对 `target[i]`，选一个**列下标 `c`**（必须严格大于上一次选的列）和**某一行（某个单词）**，要求该单词在列 `c` 处的字符等于 `target[i]`。**每一列在整个拼出过程中最多只能被使用一次**（不管是哪个单词提供的字符，用过的列号不能再选）。统计不同的 `(列, 单词)` 选择组合数，对 `1e9+7` 取模——同一列被不同单词满足算不同方案。

**解法**：预处理 `cnt[j][ch]` = 有多少个单词在列 `j` 处的字符是 `ch`。一维 DP（0/1 背包式）：`dp[i]` = 用当前已处理的列拼出 `target` 前 `i` 个字符的方案数；按列从左到右遍历，每列内部 `i` **从大到小**更新 `dp[i+1] += dp[i] * cnt[j][target[i]]`（倒序保证同一列在本次遍历里不会被用两次）。最终答案 `dp[len(target)]`。O(n·m) 时间。

### Part 2 — 列下标的最小字典序方案 **(reconstructed)**

不关心方案数、也不关心具体是哪个单词提供字符，只问：**是否存在**一组严格递增的列下标能拼出 `target`（只要求"该列上至少有某个单词的字符匹配"），如果存在，返回**字典序最小**的那组列下标；不存在则返回空列表。

**解法**：贪心从左到右扫描列。对 `target` 的每个字符，取"大于上一次选择"的**最小**列下标中含有该字符的列。这个贪心和"判断 `target` 是否是某个多重集合序列的子序列"完全同构（类似判断子序列的双指针），正确性来自：如果当前字符能在更靠左的列被满足却选了更靠右的列，会严格劣于（或至少不优于）选最靠左的那个，因为选更靠左的列给后续字符留下了更大的可选空间。

## Worked examples（全部由 `solution.py` 实际运行得出）

| words | target | Part 1 | Part 2 |
|---|---|---|---|
| `["acca","bbbb","caca"]` | `"aba"` | `6`（LC1639 例 1） | `[0, 1, 3]` |
| `["abba","baab"]` | `"bab"` | `4`（LC1639 例 2） | `[0, 1, 2]` |
| `["abcd"]` | `"abcd"` | `1`（LC1639 例 3） | `[0, 1, 2, 3]` |
| `["abab","baba","abba","baab"]` | `"abba"` | `16`（LC1639 例 4） | — |
| `["aaa"]` | `"aa"` | `3`（3 列全是 `a`，选 2 个不同列 `C(3,2)=3`，验证"每列只能用一次"） | — |
| `["aaa"]` | `"aab"` | — | `[]`（没有列含 `b`，不可能拼出） |

## `main()` 命令流

```
PART 1              PART 2
3                    3
acca                 acca
bbbb                 bbbb
caca                 caca
aba                  aba
→ 6                  → 0,1,3
```

## 边界清单

- `target` 比 `words` 短（任意一列都能贡献单个字符）
- 无法拼出（某个字符在所有列都凑不出来）→ Part1 返回 `0`，Part2 返回 `[]`
- 单词/目标长度为 1 的极小情形
- "每列只能用一次"的验证（同一列不能重复满足 target 的两个不同位置）
- 非法输入：空 `words`/`target`、单词长度不一致、`target` 比单词长、含非小写字符 → `ValueError`
- 性能：`words` 和 `target` 长度均到 1000 时两个 part 都 < 2 s

## 追问

1. **为什么 DP 里 `i` 要倒序遍历？** 这是标准 0/1 背包"每个物品只能用一次"的技巧：如果正序更新 `dp[i+1]`，会用到本轮已经被同一列更新过的 `dp[i]`，导致同一列被同一次遍历里使用两次。
2. **空间能不能进一步压缩？** 已经是 O(n) 的一维数组（相对于 O(n·m) 的二维 DP 表），如果 `n` 也很大可以考虑滚动，但对本题的约束已经足够。
3. **Part 2 的贪心为什么不需要回溯？** 因为目标是"字典序最小"而不是"存在性最优的其它指标"，局部贪心（尽量早满足每个字符）在字典序意义下天然全局最优——这和"判断字符串是否为子序列"的双指针写法是同一个证明思路。
4. **如果还要统计"最小字典序方案"对应的具体单词组合数呢？** 需要在贪心确定列之后，对每个选定列统计有多少个单词在该列匹配该字符，再把这些计数相乘——相当于把 Part 1 的计数逻辑限制在 Part 2 选出的那组列上。

## 来源与置信度

- **MED**：`catalog/raw/coding_oa.md` #15，2023 Canada OA 索引 item #13，直链 https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/ （LC 1639，逐字复用）。
- Part 2 为重建（reconstructed），非原题实录。
- 命名冲突警示：2025 Infra Automation Intern OA 的同名"String Formation"是不同的题，见 `catalog/raw/coding_oa.md` #15 原文说明。

## 考什么

0/1 背包式一维 DP（列不可重复使用的资源约束建模）· 子序列匹配的贪心/双指针范式（对应 skills_matrix S08 的复杂度压一档思路，这里是"从计数 DP 退化为存在性贪心"）· 精确的输入契约定义（`target` 长度约束、非法字符）。
