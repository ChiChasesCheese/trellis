---
id: tlc-patterns-dp-grid-string-7-wordbreak-parens
node: patterns.dp-grid-string
type: qa
step: 7
---
## Q
**动态规划：网格、双串与区间｜一维字符串 DP：单词拆分（LC 139）与最长有效括号（LC 32）**

"前 `i` 个字符能否拆成词典里的词"怎么转移？括号题的 `dp[i]` 为什么是"以 `i` 结尾"？

## A
**LC 139**：`dp[i]` = `s[:i]` 能否拆分。枚举**最后一个词**的起点 `j`：`dp[j]` 为真且 `s[j:i]` 在词典里。限制 `j` 的范围到最长词长，把 `O(n^2)` 降到 `O(n · L)`。

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)
    max_len = max(map(len, words))
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(max(0, i - max_len), i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[-1]
print(word_break("leetcode", ["leet", "code"]), word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))   # True False
```

**LC 32**：`dp[i]` = 以 `s[i]` **结尾**的最长有效括号长度（只有 `)` 结尾才可能非零）。

```python
def longest_valid_parentheses(s: str) -> int:
    dp = [0] * len(s)
    for i in range(1, len(s)):
        if s[i] == ")":
            if s[i - 1] == "(":
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2          # "...()"
            else:
                j = i - dp[i - 1] - 1                              # 与 s[i] 配对的左括号位置
                if j >= 0 and s[j] == "(":
                    dp[i] = dp[i - 1] + 2 + (dp[j - 1] if j >= 1 else 0)   # 再接上 j 之前的有效段
    return max(dp, default=0)
print(longest_valid_parentheses("(()"), longest_valid_parentheses(")()())"), longest_valid_parentheses("()(())"))   # 2 4 6
```

栈解法同样 `O(n)`：栈底放 `-1`（最后一个无法匹配的位置），遇到 `(` 压下标，遇到 `)` 弹栈，栈空则压入当前下标，否则 `best = max(best, i - 栈顶)`。
