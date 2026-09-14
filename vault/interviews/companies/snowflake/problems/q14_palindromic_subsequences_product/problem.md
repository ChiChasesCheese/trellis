# q14 · Maximum Product of the Length of Two Palindromic Subsequences — 两个不相交回文子序列的最大长度积

> 2023 Snowflake OA 候选人索引直接复用的 LeetCode 原题。Part 1 为原题；Part 2 **(reconstructed)**：不仅要长度积，还要给出具体的下标方案。

## 背景

`catalog/raw/coding_oa.md` #12（对应 2023 Canada OA 索引 item #10）："Palindromic Subsequences"，直链 https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/ （LC 2002 "Maximum Product of the Length of Two Palindromic Subsequences"），confidence MED，逐字复用无改编。

这道题的关键约束是 `2 <= s.length <= 12`——长度被卡得极小，就是在暗示"状态压缩/位掩码枚举子集"是预期解法，而不是任何多项式 DP（两个子序列互相"抢"下标，不存在简单的区间/前缀 DP 状态）。

## 输入格式

- `s: str`，`2 <= len(s) <= 12`，仅小写英文字母。

非法输入（长度越界、含非小写字母字符）抛 `ValueError`。

## API 契约

```python
def max_product_two_palindromic_subsequences(s: str) -> int
def max_product_with_subsequences(s: str) -> tuple[list[int], list[int]]
```

## 规则

### Part 1 — LC 2002 原题

从 `s` 中选两个**下标不相交**的子序列，要求两个子序列各自都是回文串，最大化两个子序列长度的乘积。

**解法**：`n <= 12`，枚举每个下标子集（位掩码，`2^n <= 4096` 个），O(n) 判断该子集对应的子序列是否回文，记录长度。然后对每个是回文的 `mask1`，只在它的**补集**里枚举子掩码（经典"枚举子掩码"技巧：`sub = (sub-1) & comp`），若该子掩码也是回文就用两者长度乘积更新答案。整体 O(3ⁿ)（每个下标在三种状态之一：属于 mask1 的子集、属于补集的子集、都不属于——均摊后是子掩码枚举的标准界），`n=12` 时约 5×10⁵ 次判断，远小于 2 秒预算。

### Part 2 — 给出具体下标方案 **(reconstructed)**

不只是返回最大乘积，还要返回一组**具体**达到该乘积的不相交下标列表 `(idx1, idx2)`（各自升序）。因为最优解可能不唯一，测试用一个 checker 校验任意合法方案：下标不重复、两组互斥、每组对应字符串是回文、且长度乘积等于 Part 1 的答案——不要求和某个"标准答案"字面相同。

## Worked examples（全部由 `solution.py` 实际运行得出）

| s | Part 1 | Part 2（一种合法方案） |
|---|---|---|
| `"leetcodecom"` | `9`（LC2002 例 1） | `idx1=[1,2,7]`→`"eee"`，`idx2=[5,8,9]`→`"oco"` |
| `"bb"` | `1`（LC2002 例 2） | `idx1=[0]`→`"b"`，`idx2=[1]`→`"b"` |
| `"accbcaxxcxx"` | `25`（LC2002 例 3） | `idx1=[0,1,2,4,5]`→`"accca"`，`idx2=[6,7,8,9,10]`→`"xxcxx"` |
| `"ab"` | `1` | 两个单字符子序列，乘积恒为 1 |
| `"aaaaaaaaaaaa"`（12 个 a） | `36` | 任意 6/6 切分（任何子集都是回文），`6×6=36` |

## `main()` 命令流

```
PART 1              PART 2
leetcodecom         bb
→ 9                 → 0
                     1
```
（Part 2 输出两行，每行是逗号分隔的下标列表，对应两个子序列。）

## 边界清单

- 最短输入 `len(s) = 2`：两个不同字符时乘积只能是 1
- 全同字符（`"aaaa...a"`，12 个）：任意子集都回文，最优是尽量平均切分
- `s` 本身整体就是回文（如 `"abcba"`），但**不能**把整个串当成一侧——必须真的切成两个不相交部分
- 单侧无法形成长度 ≥1 的回文？不可能：任意单字符都是长度 1 的回文，所以答案下界为切出两个不相交非空回文的乘积（只要 `len(s)>=2` 总能找到，最小是 `1*1=1`）
- 非法输入：空串、长度 13、含大写/数字/非 ASCII 字符 → `ValueError`
- 性能：`n = 12`（题目本身的规模上限）两个 part 都 < 2 s

## 追问

1. **为什么 `n <= 12` 就足够暗示位掩码枚举？** `2^12 = 4096` 个子集，配合子掩码枚举是 `3^12 ≈ 5.3×10^5`，普通位运算判断回文是 O(n)，总量在毫秒级；再大几倍 n 这套解法就会指数爆炸。
2. **能不能用 DP 代替暴力枚举子集？** 两个子序列互相竞争同一份下标资源，没有简单的"前缀/区间"状态能同时描述"哪些下标已经被占用"，除非状态本身就是位掩码——所以最终还是位掩码 DP/枚举，只是本题 n 太小，直接枚举更简单。
3. **如果要三个不相交回文子序列的最大长度积呢？** 需要三重枚举子掩码（O(4ⁿ) 左右），`n<=12` 依然可行，但增长很快——面试官常用这个追问来看候选人是否理解子掩码枚举的复杂度来源，而不是死记模板。
4. **最优解不唯一时，Part 2 该怎么定"哪个是正确答案"？** 显式定义 checker（校验合法性 + 乘积达到上界）而不是要求逐字匹配某个参考实现的下标选择——这是"多解问题"测试设计的通用范式。

## 来源与置信度

- **MED**：`catalog/raw/coding_oa.md` #12，2023 Canada OA 索引 item #10，直链 https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/ （LC 2002，逐字复用）。
- Part 2 为重建（reconstructed），非原题实录。

## 考什么

位掩码枚举子集 + 枚举子掩码的 O(3ⁿ) 技巧（对应 skills_matrix S08 LC 原题+复杂度再压一档的姊妹技能：这里是"利用极小 n 反推预期解法"）· 回文判定 · 多解问题的 checker 式测试设计。
