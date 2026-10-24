---
id: tlc-edit-distance-2-code
node: a.edit-distance
type: qa
step: 2
---
## Q
**LC 72 编辑距离**｜写出 Python 实现

两个小写字母字符串 `word1`、`word2`（长度都在 `[0, 500]`），可以对 `word1` 做插入、删除、替换一个字符的操作。返回把 `word1` 变成 `word2` 的最少操作数，用 `O(n)` 额外空间。

## A
**思路。** `dp[i][j]` 是 `word1[:i]` 到 `word2[:j]` 的最少操作数。逐行计算：第 0 行是 `0..n`（全部插入）。第 `i` 行第 0 列是 `i`（全部删除）。其他格子：两个末尾字符相同，取左上角；不同，取左上（替换）、上（删除）、左（插入）三者最小值加 `1`。只保留上一行 `prev` 和当前行 `cur`。

```python
def min_distance(word1: str, word2: str) -> int:
    n = len(word2)
    prev = list(range(n + 1))           # prev[j]：word1 空前缀 -> word2[:j]，要插入 j 个字符
    for i, a in enumerate(word1, 1):
        cur = [i] + [0] * n             # cur[0]：word1[:i] -> 空串，要删 i 个字符
        for j, b in enumerate(word2, 1):
            if a == b:
                cur[j] = prev[j - 1]    # 末尾相同，不花操作
            else:
                cur[j] = 1 + min(prev[j - 1],   # 替换
                                 prev[j],       # 删除 word1 的 a
                                 cur[j - 1])    # 插入 word2 的 b
        prev = cur                      # 只留上一行：空间 O(n)
    return prev[n]
```

运行：`("horse", "ros")` → `3`，`("intention", "execution")` → `5`，`("", "abc")` → `3`，`("abc", "")` → `3`，`("", "")` → `0`，`("a", "a")` → `0`，两个 500 个字符的随机串也瞬间算完。

**复杂度。** 时间 `O(m · n)`：两层循环；空间 `O(n)`：`prev` 和 `cur` 两个长度 `n + 1` 的列表。

**写法要点。** `list(range(n + 1))` 一步生成第 0 行；`enumerate(word1, 1)` 让下标从 1 开始，`i`、`j` 就是前缀长度，不需要 `i - 1` 去取字符；直接迭代字符 `a`、`b`，不写 `word1[i-1]`；`cur = [i] + [0] * n` 每行新建一个列表，`prev = cur` 只是换引用，没有拷贝；自底向上的写法没有递归，`m + n` 到 `1000` 时也不会像 `@cache` 的自顶向下那样触到递归上限。
