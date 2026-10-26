# hc17 · 带 * 的通配匹配

给你一个只含小写字母的字符串 text，和一个由小写字母与 `*` 组成的 pattern，`*` 可以匹配任意长度（包括 0）的任意字符。问 pattern 能不能匹配整个 text。面试官先要动态规划，再要不用额外数组的双指针写法，最后追问「为什么贪心是对的」「加一个 `?` 会怎样」「正则引擎为什么会卡死」。Java 和 C++ 的签名都在下面，选面试官要的那种语言。

## 面试官会怎么说

> "You are given a lowercase string `text` and a pattern containing lowercase letters and `*`, where `*` matches any sequence of characters, including the empty one. Does the pattern match the whole text?"
> 接着会问："Can you do it in O(1) extra space?" "Why is the greedy correct?" "What if we add `?`?" "What is the worst case of your greedy?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：要匹配整个 text 还是只要包含？`*` 能匹配空吗？text 和 pattern 可以为空吗？ |
| 3–15 分钟 | **Part 1**：动态规划，一维滚动数组 |
| 15–30 分钟 | **Part 2**：双指针 + 回溯到最近的 `*` |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 动态规划（约 13 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static boolean matchDp(String text, String pattern)` |
| C++ | `bool match_dp(const std::string& text, const std::string& pattern)` |

- `dp[i][j]` 表示 pattern 的前 i 个字符能否匹配 text 的前 j 个字符。时间 O(n·m)，n、m 是两个串的长度。
- 写完二维表以后，改成只留一行的滚动数组。
- 例子：`("abc","a*c")` 为真，`("ac","a*c")` 为真（`*` 匹配空），`("abc","*a")` 为假（必须匹配整个 text），`("","**")` 为真，`("","a")` 为假，`("mississippi","m*iss*pi")` 为真，`("mississippi","m*iss*pa")` 为假。

## Part 2 · 双指针 + 回溯（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static boolean matchGreedy(String text, String pattern)` |
| C++ | `bool match_greedy(const std::string& text, const std::string& pattern)` |

- 额外空间 O(1)，结果必须和 Part 1 一致。
- 遇到 `*` 先让它匹配空，只记下它的位置和 text 当时的位置；后面失配了，就回到最近的那个 `*`，让它多吃一个字符再试。
- 例子：`("aaaaab","*aaab")` 为真，`("aaabaaab","*aab")` 为真，`("aaaaa","*aaab")` 为假，`("abcabcabd","*abc*abd")` 为真，`("abc","*abc*abc*")` 为假。
- 十万个 `a` 的 text 对 `*a*a*a` 要能立刻跑完。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 为什么贪心只需要回到**最近**的一个 `*`，不用回到更早的？为什么这只在 `*` 是唯一通配符时才对？
2. pattern 里再加 `?`（匹配恰好一个字符），DP 和贪心各要改什么？
3. 贪心的最坏时间是多少？怎样做到线性？
4. 正则引擎里的灾难性回溯（catastrophic backtracking）是什么？为什么这里的贪心不会？
5. 一个 pattern 要去匹配很多个单词，怎么做？

## 边界

- text 或 pattern 为空，pattern 全是 `*`
- `*` 在开头、结尾、连续出现
- pattern 比 text 长但全是 `*` 之外的字符
- 十万个相同字符

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc17_text_pattern_stars       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc17_text_pattern_stars --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc17_text_pattern_stars       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc17_text_pattern_stars --tag part1
```
