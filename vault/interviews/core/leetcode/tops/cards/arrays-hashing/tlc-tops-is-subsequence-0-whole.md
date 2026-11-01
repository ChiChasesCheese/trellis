---
id: tlc-tops-is-subsequence-0-whole
node: arrays-hashing.is-subsequence
type: qa
---
## Q
**LC 392 判断子序列**｜Easy · 全公司热度第 288 名 · Top Interview 150、LeetCode 75

给定字符串 `s` 和 `t`，判断 `s` 是否为 `t` 的子序列。子序列是原字符串删除一些（也可以不删除）字符、不改变剩余字符相对位置形成的新字符串（`"ace"` 是 `"abcde"` 的子序列，`"aec"` 不是）。`0 <= s.length <= 100`，`0 <= t.length <= 10^4`，只含小写字母。例：`s = "abc"`, `t = "ahbgdc"` → `true`；`s = "axc"`, `t = "ahbgdc"` → `false`。进阶：有大量输入 `s1, s2, ..., sk`（`k >= 10 亿`）要依次检查是否为 `t` 的子序列，代码怎么改？

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 同向双指针 + 贪心匹配：子序列只关心「顺序」，不关心「连续」。

**一句话。** 指针 `i` 指向 `s` 里正在等待匹配的字符，扫描 `t`，遇到就匹配、`i` 前进，最后看 `i` 是否走完 `s`。

**识别。** 「删除若干字符得到另一个串」= 子序列判定；两个串各一个指针，只往前走，`O(n + m)`。

**推导。** 枚举 `t` 的所有子序列是指数级。但匹配可以贪心：`t` 里每次遇到 `s` 当前需要的字符就立刻用掉，晚匹配只会留给后面更少的字符，不会更好。所以 `t` 只需扫一遍。

```python
def is_subsequence(s: str, t: str) -> bool:
    i = 0  # 不变式：s[:i] 已经在 t 已扫过的部分里按序匹配上
    for ch in t:
        if i < len(s) and ch == s[i]:  # 贪心：t 里一遇到 s 正在找的字符就用掉，越早匹配留给后面的越多
            i += 1
    return i == len(s)
```

运行：`("abc", "ahbgdc")` → `True`；`("axc", "ahbgdc")` → `False`；`("", "ahbgdc")` → `True`；`("a", "")` → `False`。

**复杂度。** 时间 `O(|t|)`，空间 `O(1)`。

**拓展优化。**
- 进阶（海量 `s`，同一个 `t`）：每个 `s` 都扫一遍 `t` 是 `O(k·|t|)`。预处理 `t`：记录每个字符的下标列表，之后每个 `s` 里的字符用二分在列表里找「上一个匹配位置之后」的第一个下标，单个 `s` 是 `O(|s| log |t|)`，与 `|t|` 几乎无关。

```python
from bisect import bisect_left
from collections import defaultdict


class SubsequenceChecker:
    def __init__(self, t: str) -> None:
        self.pos: dict[str, list[int]] = defaultdict(list)  # 字符 -> 它在 t 中的全部下标（升序）
        for i, ch in enumerate(t):
            self.pos[ch].append(i)

    def check(self, s: str) -> bool:
        prev = -1  # 上一个字符匹配到的 t 下标
        for ch in s:
            idx = self.pos.get(ch, [])
            j = bisect_left(idx, prev + 1)  # 二分找 ch 在 prev 之后出现的第一个位置
            if j == len(idx):
                return False
            prev = idx[j]
        return True
```

- 也可以预处理成「下一个出现位置」表 `nxt[i][c]`（`(|t|+1) × 26`），查询 `O(|s|)`，以空间换时间。

**易错点。**
- 把子序列当成「`s` 的每个字符都在 `t` 里出现」：`s = "aec"`, `t = "abcde"` 会错判成 `True`（顺序不对），正确答案是 `False`。
- `s` 为空串应返回 `True`；`i < len(s)` 的判断不能省，否则 `s` 匹配完后继续访问 `s[i]` 会越界。

**同模式。** LC 792 匹配子序列的单词数、LC 524 通过删除字母匹配到字典里最长单词、LC 1143 最长公共子序列、LC 1768 交替合并字符串。
