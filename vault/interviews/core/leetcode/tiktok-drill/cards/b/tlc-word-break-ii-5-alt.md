---
id: tlc-word-break-ii-5-alt
node: b.word-break-ii
type: qa
step: 5
---
## Q
**LC 140 单词拆分 II**｜另一种解法

不用缓存句子，先算出「每个后缀能不能拆」，再做回溯，怎么写？它和记忆化返回句子的做法相比，什么时候更合适？

## A
**思路。** 先用自底向上的 DP 得到 `can[i]`：`s[i:]` 能否拆成字典词。再从 `0` 开始回溯，每次只走 `can[j]` 为真的分支，这样回溯里不会进入死胡同，每走一步都至少能产生一个句子，路径上的单词用一个共享列表 `path` 维护，到末尾才拼成字符串。

```python
def word_break_backtrack(s: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)
    n = len(s)
    can = [False] * (n + 1)            # can[i]: s[i:] 能否拆成字典词
    can[n] = True
    for i in range(n - 1, -1, -1):
        can[i] = any(can[j] for j in range(i + 1, n + 1) if s[i:j] in words)
    result: list[str] = []
    path: list[str] = []

    def dfs(i: int) -> None:
        if i == n:
            result.append(' '.join(path))
            return
        for j in range(i + 1, n + 1):
            if can[j] and s[i:j] in words:   # 只走“后面一定拆得完”的分支
                path.append(s[i:j])
                dfs(j)
                path.pop()

    if can[0]:
        dfs(0)
    return result
```

输出与记忆化版一致：示例 1 → `['cat sand dog', 'cats and dog']`，示例 3 → `[]`，`"a" * 20` 加 `"a"` 到 `"a" * 20` 的字典 → `524288` 个句子（`2^19`）。

**取舍。**
- 回溯 + `can[]`：`can[]` 是 `O(n^2)` 的预处理，之后搜索树没有死胡同，额外内存只有 `path` 和 `can`，不存每个位置的中间句子，适合句子很多、内存紧的场景。
- 记忆化返回句子：代码短，天然把「死胡同」缓存成空，但每个位置都保存一份后缀句子列表，内存是输出规模的若干倍。
- 两者复杂度同阶，都由输出规模决定。面试里先写记忆化（最短、最不容易错），被问内存时再给这个。
