---
id: tlc-tops-rotate-string-0-whole
node: arrays-hashing.rotate-string
type: qa
---
## Q
**LC 796 旋转字符串**｜Easy · 全公司热度第 153 名

给定两个字符串 `s` 和 `goal`。`s` 的一次**旋转**是把最左边的字符移到最右边（`"abcde"` 旋转一次得到 `"bcdea"`）。若经过若干次旋转后 `s` 能变成 `goal`，返回 `true`，否则返回 `false`。`1 <= s.length, goal.length <= 100`，`s` 和 `goal` 由小写字母组成。例：`s = "abcde"`, `goal = "cdeab"` → `true`；`s = "abcde"`, `goal = "abced"` → `false`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 循环移位 = 把字符串首尾相接（`s + s`）后取子串；子串查找。

**一句话。** `s` 的所有旋转都是 `s + s` 里长度为 `n` 的子串，所以长度相等且 `goal` 在 `s + s` 里就是答案。

**识别。** 「旋转 / 循环位移 / 环形」想到把序列**复制一份接在后面**，把环形问题变成线性的子串问题；`n <= 100`，任何做法都够，这题考的是这个转换。

**推导。** 暴力：旋转 `n` 次，每次与 `goal` 比较，`O(n^2)`。旋转 `k` 次得到的串，正好是 `s + s` 里从下标 `k` 开始、长 `n` 的那一段，`k = 0..n-1` 全部枚举完，一次子串查找就覆盖了所有旋转。

```python
def rotate_string(s: str, goal: str) -> bool:
    if len(s) != len(goal):  # 长度不同，goal 可能是 s+s 的子串（比如更短的重复串）却不是旋转
        return False
    return goal in s + s  # 旋转 k 次 = s+s 中下标 k 起长 n 的子串，所有旋转都藏在 s+s 里
```

运行：`("abcde", "cdeab")` → `True`；`("abcde", "abced")` → `False`；`("abc", "abc")` → `True`；`("a", "aa")` → `False`。

**复杂度。** 时间 `O(n)` 到 `O(n^2)`（取决于 `in` 的子串查找实现，`n <= 100` 无影响；要保证线性见下面的 KMP），空间 `O(n)`（拼接）。

**拓展优化。**
- 面试官可能要求不拼接、保证线性：手写 KMP，在 `s` 的两遍循环里匹配 `goal`：

```python
def rotate_string_kmp(s: str, goal: str) -> bool:
    n = len(s)
    if n != len(goal):
        return False
    nxt = [0] * n  # nxt[i]：goal[:i + 1] 最长的「既是前缀又是后缀」的真前缀长度
    k = 0
    for i in range(1, n):
        while k and goal[i] != goal[k]:
            k = nxt[k - 1]
        if goal[i] == goal[k]:
            k += 1
        nxt[i] = k
    k = 0
    for c in s + s:  # 把 s 走两遍（用 s+s 的字符流，不另存）
        while k and c != goal[k]:
            k = nxt[k - 1]
        if c == goal[k]:
            k += 1
        if k == n:  # goal 整个匹配上
            return True
    return False
```

**易错点。**
- 漏掉长度判断：`s = "a"`, `goal = "aa"` 时 `"aa" in "aa"` 为 `True`，正确答案是 `False`。
- 把「零次旋转」排除掉：`s == goal` 时应返回 `true`（`goal in s + s` 自然成立）。
- 只检查 `goal in s`：`s = "abcde"`, `goal = "cdeab"` 返回 `False`，正确是 `True`；必须在拼接后的 `s + s` 里找。

**同模式。** LC 459 重复的子字符串、LC 28 找出字符串中第一个匹配项的下标、LC 686 重复叠加字符串匹配、LC 189 轮转数组。
