---
id: tlc-word-pattern-ii-0-whole
node: c.word-pattern-ii
type: qa
---
## Q
**LC 291 单词规律 II**｜Medium · LC TikTok 全时段热度 26/100

给定模式 `pattern` 和字符串 `s`，判断 `s` 是否与 `pattern` 匹配：存在从模式字符到**非空**字符串的双射映射，使得把 `pattern` 中每个字符替换成它的映射后恰好得到 `s`。双射意味着不会有两个字符映射到同一个字符串，也不会有一个字符映射到两个不同字符串。`1 <= pattern.length, s.length <= 20`，二者由小写英文字母组成。例：`pattern = "abab", s = "redblueredblue"` → `true`（`a -> "red"`，`b -> "blue"`）；`pattern = "aaaa", s = "asdasdasdasd"` → `true`（`a -> "asd"`）；`pattern = "aabb", s = "xyzabcxzyabc"` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 回溯：按模式逐个字符走，已有映射就检查 `s` 对应位置是否匹配，没有映射就枚举它对应 `s` 的哪一段，用 `used` 集合保证双射，失败就撤销。

**识别。** 长度只有 20 且要求「存在一种划分」：搜索 + 回溯；与 LC 290 的区别是 `s` 没有分隔符，每个字符对应的子串要自己枚举。

**推导。** 状态是 `(i, j)`：模式走到第 `i` 个字符、`s` 走到位置 `j`，加上当前的映射表。已映射的字符没有选择，只有新字符才分叉，分叉数最多是剩余长度，所以总量远小于所有划分数。回溯时同步撤销 `mapping` 和 `used`。

```python
def word_pattern_match(pattern: str, s: str) -> bool:
    mapping: dict[str, str] = {}                 # 模式字符 -> 它对应的子串
    used: set[str] = set()                       # 已被占用的子串，保证双射（不同字符不能映射到同一子串）

    def dfs(i: int, j: int) -> bool:             # pattern[i:] 要匹配 s[j:]
        if i == len(pattern):
            return j == len(s)                   # 模式用完时，s 也必须刚好用完
        ch = pattern[i]
        if ch in mapping:                        # 已有映射：s 从 j 开始必须恰好是这个子串
            word = mapping[ch]
            return s.startswith(word, j) and dfs(i + 1, j + len(word))
        for end in range(j + 1, len(s) + 1):     # 新字符：枚举它对应 s[j:end]（非空）
            word = s[j:end]
            if word in used:                     # 已被别的字符占用，违反双射
                continue
            mapping[ch] = word
            used.add(word)
            if dfs(i + 1, end):
                return True
            del mapping[ch]                      # 回溯：撤销这次尝试
            used.remove(word)
        return False

    return dfs(0, 0)
```

运行：三个示例依次得到 `True`、`True`、`False`；`"ab"`, `"aa"` → `False`（两字符不能映射到同一子串）；`"a"`, `"ab"` → `True`；`"abc"`, `"aaa"` → `False`。

**复杂度。** 时间最坏指数级，约 `O(C(n - 1, m - 1))`（`m` 个互不相同的模式字符把长 `n` 的串切成 `m` 段，`n, m <= 20`），空间 `O(m)`。

**拓展优化。**
- 剪枝：新字符的结束位置不能让后面的字符没字可用（每个至少 1 个字符），只改循环上界：

```python
def word_pattern_match_pruned(pattern: str, s: str) -> bool:
    mapping: dict[str, str] = {}
    used: set[str] = set()

    def dfs(i: int, j: int) -> bool:
        if i == len(pattern):
            return j == len(s)
        ch = pattern[i]
        if ch in mapping:
            word = mapping[ch]
            return s.startswith(word, j) and dfs(i + 1, j + len(word))
        later = len(pattern) - i - 1             # 之后还有 later 个模式字符，每个至少需要 1 个字符
        for end in range(j + 1, len(s) - later + 1):   # 剪枝：end 不能让后面的字符没字可用
            word = s[j:end]
            if word in used:
                continue
            mapping[ch] = word
            used.add(word)
            if dfs(i + 1, end):
                return True
            del mapping[ch]
            used.remove(word)
        return False

    return dfs(0, 0)
```

- 先检查 `len(s)` 是否至少等于 `len(pattern)`，并统计每个字符的出现次数做长度可行性判断，可以提前返回 `False`。

**易错点。**
- 忘记 `used`：`"ab"`, `"aa"` 会让 `a -> "a"`、`b -> "a"` 通过，得到 `True`，应为 `False`。
- 回溯时只撤销 `mapping` 不撤销 `used`（或相反）：之后的分支会误以为某个子串已被占用或某个字符已有映射。
- 允许空映射：`end` 从 `j` 开始会让字符映射到空串，题目要求非空，应从 `j + 1` 开始。

**追问。**
- 只判断不要求双射（单向映射）：去掉 `used`。
- 返回一种可行的映射：成功时 `mapping` 就是答案，复制出来返回。

**同模式。** LC 290 单词规律、LC 205 同构字符串、LC 22 括号生成、LC 46 全排列、LC 93 复原 IP 地址。
