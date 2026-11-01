---
id: tlc-tops-longest-substring-without-repeating-characters-0-whole
node: sliding-window.longest-substring-without-repeating-characters
type: qa
---
## Q
**LC 3 无重复字符的最长子串**｜Medium · 全公司热度第 3 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给定字符串 `s`，找出其中不含重复字符的**最长子串**的长度（子串必须连续）。`0 <= s.length <= 10^5`，`s` 由英文字母、数字、符号和空格组成。例：`"abcabcbb"` → `3`（`"abc"`）；`"bbbbb"` → `1`；`"pwwkew"` → `3`（`"wke"`；`"pwke"` 是子序列，不是子串）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 可变长滑动窗口（variable-size sliding window）+ 哈希表记录字符最近位置。

**一句话。** 右端逐个吃进字符，撞上窗口内的重复字符时，左端**直接跳到**该字符上次出现位置的后一格，每步用窗口长度更新答案。

**识别。** 「连续子串 + 最长 + 窗口内容有约束」是滑动窗口的标准信号；`n = 10^5` 排除 `O(n^2)`；约束具有单调性（有重复的窗口继续扩大仍有重复），所以左端只进不退。

**推导。** 暴力枚举所有子串并检查，`O(n^3)`；固定起点向右扩，撞到重复就停，`O(n^2)`。撞到的重复字符 `c`，其上次位置之前的所有起点都会在同一个 `c` 上撞车，可以整段跳过。每个下标进出窗口各一次，`O(n)`。

```python
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}  # 字符 -> 它最近一次出现的下标
    best = left = 0  # 窗口是 s[left : right + 1]，不变式：窗口内没有重复字符
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:  # ch 在窗口内出现过：左端直接跳到它上次位置的后一格
            left = last[ch] + 1  # 条件里的 >= left 不能省：字典里还留着已滑出窗口的旧位置
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

运行：`"abcabcbb"` → `3`；`"bbbbb"` → `1`；`"pwwkew"` → `3`；`""` → `0`；`"abba"` → `2`。

**复杂度。** 时间 `O(n)`，空间 `O(min(n, Σ))`，`Σ` 是字符集大小。

**拓展优化。**
- 返回子串本身：更新答案时一并记下起点。
- 字符集固定为 ASCII：把字典换成 `[-1] * 128` 数组，用 `ord(ch)` 当下标，常数更小。

**易错点。**
- 条件必须是 `last[ch] >= left`：字典里留着已滑出窗口的旧位置，只判断「出现过」会让左端后退，`"abba"` 会得到 `3`，正确是 `2`。
- 空串返回 `0`；`best` 要在循环里每步更新，别漏掉最后一个窗口。

**同模式。** LC 340 至多包含 K 个不同字符的最长子串、LC 424 替换后的最长重复字符、LC 76 最小覆盖子串、LC 1004 最大连续1的个数 III。
