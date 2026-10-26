# hc17 · 解法与原理

通配匹配是一道「同一个问题两种写法」的题：动态规划稳，贪心省空间，面试官真正想听的是你能不能说清楚贪心为什么不会漏掉答案。下面先说开场 3 分钟，然后每个 Part 给出思路、原理和两种语言的完整代码，最后是口头追问的答案。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "So `*` matches any sequence including empty, and the pattern has to match the whole text, not just a part of it. Can either string be empty? And are letters the only other characters — no `?`, no escaping?"

面试官通常会说：要匹配整个 text，可以为空，只有小写字母和 `*`。先把「整个」问清楚很重要：`("abc","*a")` 是假的。

## Part 1 · 动态规划

**思路**：先写二维表。`dp[i][j]` 表示 pattern 前 i 个字符匹配 text 前 j 个字符。`dp[0][0] = true`，其余第 0 行为假。

- pattern 第 i 个字符是普通字母：`dp[i][j] = dp[i-1][j-1] && text[j-1] == pattern[i-1]`。
- 是 `*`：`dp[i][j] = dp[i-1][j] || dp[i][j-1]`。前者是「`*` 匹配空」，后者是「`*` 多吃掉 text[j-1]」。

答案是 `dp[m][n]`。写完二维表后你会发现第 i 行只依赖第 i-1 行和本行左边，所以一行就够了。

**原理：一维滚动怎么不串行**

- 遇到 `*`：新的 `dp[j]` 要用旧的 `dp[j]`（匹配空）和新的 `dp[j-1]`（多吃一个字符）。从左往右更新正好满足：`dp[j] = dp[j] || dp[j-1]`，此时 `dp[j-1]` 已经是新值。`dp[0]` 不变，因为 `*` 匹配空时 `dp[0]` 保持原值。
- 遇到普通字母：新的 `dp[j]` 要用旧的 `dp[j-1]`，所以必须从右往左更新，否则 `dp[j-1]` 先被改掉。最后 `dp[0] = false`，因为一个字母不可能匹配空串。

**Java**

```java
public static boolean matchDp(String text, String pattern) {
    int n = text.length();
    boolean[] dp = new boolean[n + 1];  // dp[j]：当前已读的 pattern 前缀能否匹配 text[0..j)
    dp[0] = true;
    for (char c : pattern.toCharArray()) {
        if (c == '*') {
            for (int j = 1; j <= n; j++) dp[j] = dp[j] || dp[j - 1];
        } else {
            for (int j = n; j >= 1; j--) dp[j] = dp[j - 1] && text.charAt(j - 1) == c;
            dp[0] = false;
        }
    }
    return dp[n];
}
```

**C++**

```cpp
inline bool match_dp(const std::string& text, const std::string& pattern) {
    const std::size_t n = text.size();
    std::vector<char> dp(n + 1, 0);
    dp[0] = 1;
    for (char c : pattern) {
        if (c == '*') {
            for (std::size_t j = 1; j <= n; ++j) dp[j] = dp[j] || dp[j - 1];
        } else {
            for (std::size_t j = n; j >= 1; --j) dp[j] = dp[j - 1] && text[j - 1] == c;
            dp[0] = 0;
        }
    }
    return dp[n];
}
```

复杂度：时间 O(n·m)，空间 O(n)（二维表是 O(n·m)）。C++ 用 `vector<char>` 而不是 `vector<bool>`，后者按位压缩，慢，也不是真正的容器。

## Part 2 · 双指针 + 回溯到最近的 `*`

**思路**：用 `i` 走 pattern，`j` 走 text。

1. 两边字符相同：一起前进。
2. pattern[i] 是 `*`：先让它匹配空。记下 `star = i`（`*` 的位置）和 `mark = j`（这时 text 走到哪），然后 `i` 前进一格。
3. 失配，但之前见过 `*`：回到 `star` 后面一格，让 `*` 多吃一个字符，`j = ++mark`。
4. 失配，没有 `*` 可回：返回假。
5. text 走完后，pattern 剩下的必须全是 `*`。

**原理：为什么只回到最近的一个 `*`**

把 pattern 按 `*` 切成若干段普通字符串，例如 `m*iss*pi` 是 `m`、`iss`、`pi`。匹配成功意味着这些段按顺序、不重叠地出现在 text 里，第一段贴着开头，最后一段贴着结尾。

关键是：每一段取**最靠左**的出现位置，永远不会比取靠右的差，因为靠左留给后面的段的空间更大。贪心就是在做这件事：`*` 先匹配空，段失配了就让 `*` 多吃一个字符、把这一段往右挪一格。前面的段一旦匹配上，就不再动它，因为它已经是最靠左的了。

这条论证只在 `*` 是唯一通配符、而且每段是定长的普通字符串时成立。如果有「`a*` 表示任意个 a」这种能改变长度的写法，前面的段位置就会影响后面能不能匹配，贪心会漏掉答案，只能用 DP 或自动机。

**Java**

```java
public static boolean matchGreedy(String text, String pattern) {
    int n = text.length(), m = pattern.length();
    int i = 0, j = 0, star = -1, mark = 0;
    while (j < n) {
        if (i < m && pattern.charAt(i) == '*') { star = i++; mark = j; }
        else if (i < m && pattern.charAt(i) == text.charAt(j)) { i++; j++; }
        else if (star >= 0) { i = star + 1; j = ++mark; }
        else return false;
    }
    while (i < m && pattern.charAt(i) == '*') i++;
    return i == m;
}
```

**C++**

```cpp
inline bool match_greedy(const std::string& text, const std::string& pattern) {
    const std::size_t n = text.size(), m = pattern.size();
    std::size_t i = 0, j = 0, mark = 0;
    long long star = -1;
    while (j < n) {
        if (i < m && pattern[i] == '*') { star = static_cast<long long>(i++); mark = j; }
        else if (i < m && pattern[i] == text[j]) { ++i; ++j; }
        else if (star >= 0) { i = static_cast<std::size_t>(star) + 1; j = ++mark; }
        else return false;
    }
    while (i < m && pattern[i] == '*') ++i;
    return i == m;
}
```

注意判断顺序：先看 `pattern[i] == '*'`，再比字符。这样即使 text 里将来出现字符 `*` 也不会被当成普通字母匹配（题目保证 text 只有小写字母，但顺序对了更稳）。

复杂度：额外空间 O(1)。时间见下面第 3 问。

## Part 3 · 口头追问和回答

**1. 为什么只回到最近的 `*`？为什么只在 `*` 是唯一通配符时才对？**

见 Part 2 的原理。pattern 切成的每一段取最靠左的位置，剩给后面的空间最大，所以更早的 `*` 不用再重新分配。如果通配符能匹配「变长的东西」而且和前文有关系（比如正则里的 `a*` 表示任意个 a，或者有分组和反向引用），一段的位置不同会让后面可匹配的范围不同，贪心就不再安全。

**2. 加上 `?`（恰好匹配一个字符）会怎样？**

DP 只多一个分支：遇到 `?` 和普通字母一样处理，只是不比较字符，`dp[j] = dp[j-1]`。贪心也只改一处比较：`pattern[i] == '?' || pattern[i] == text[j]`。原因是 `?` 不改变段的长度，每一段仍是定长的，「取最靠左的出现」的论证还成立。

**3. 贪心的最坏时间是多少？怎样做到线性？**

O(n·m)。例如 text 是 n 个 `a`，pattern 是 `*` 加 k 个 `a` 再加一个 `b`：`*` 每右挪一格，就要把 k 个 `a` 重新比一遍，最后在 `b` 上失配。n = 1000、k = 500 时指针共走 251001 步，约等于 (n-k)·k。要做到 O(n+m)，把 pattern 按 `*` 切段，每一段用 KMP（Knuth-Morris-Pratt）在 text 里找最靠左的出现位置，下一段接着往后找。

**4. 灾难性回溯是什么？为什么这里的贪心不会？**

回溯式正则引擎遇到 `(a*)*b` 这类嵌套重复，对 `aaaa…ac` 这样的输入，要尝试把 a 的个数拆成每一种分法，路径数随长度指数增长。这里的贪心每次失配只回到**最近的一个** `*`，`mark` 只增不减，总步数有 O(n·m) 的上界，不会指数增长。工程上的做法是不回溯：把正则编译成自动机（Thompson 构造的 NFA 同时跟踪所有状态，或者转成 DFA），时间和输入长度成正比，这是 RE2 一类引擎的思路。

**5. 一个 pattern 要匹配很多单词怎么办？**

pattern 只处理一次：按 `*` 切成段，记下开头段和结尾段。对每个单词，先检查长度不小于各段长度之和、开头和结尾对得上，再用 `find` 依次找中间的段。这样每个单词只需要扫一遍，不用每次重新解析 pattern。如果单词很多且前缀重复多，可以把单词放进字典树（trie），沿树往下走，遇到 `*` 就同时尝试「匹配空」和「吃掉一个孩子」，用「当前在 pattern 的哪一位」做状态去重。

## 常见错误

1. 把 `*` 当成「匹配一个任意字符」：`("ac","a*c")` 返回假。
2. 一维滚动时对普通字母从左往右更新：`dp[j-1]` 已经是新值，结果串行。
3. 只判断 pattern 走完，不要求 text 走完（或反过来）：`("abc","*a")` 返回真。
4. 贪心里遇到 `*` 后忘记记下 `mark`，回溯时从头开始，漏掉或重复。
5. text 走完后直接返回 `i == m`，不跳过 pattern 末尾的 `*`：`("abc","abc*")` 返回假。
