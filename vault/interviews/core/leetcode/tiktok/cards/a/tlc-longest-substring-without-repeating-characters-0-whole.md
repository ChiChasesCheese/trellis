---
id: tlc-longest-substring-without-repeating-characters-0-whole
node: a.longest-substring-without-repeating-characters
type: qa
---
## Q
**LC 3 无重复字符的最长子串**｜Medium · TikTok 高频

给字符串 `s`，求其中不含重复字符的**最长子串**的长度（子串必须连续）。`0 <= s.length <= 10^5`，字符是英文字母、数字、符号和空格。例：`"abcabcbb"` → `3`（`"abc"`），`"bbbbb"` → `1`，`"pwwkew"` → `3`（`"wke"`；`"pwke"` 是子序列不是子串）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 可变长滑动窗口：右端逐个吃进字符，撞上窗口内的重复字符时，左端**直接跳到**该字符上次出现位置的下一位；每步用窗口长度更新答案。`O(n)`。

**识别。** 「连续子串 + 最长 + 窗口内容有约束」是滑动窗口的标准信号；`n = 10^5` 排除 `O(n^2)`；约束有单调性（有重复的窗口再扩大仍有重复），所以左端只进不退。

**推导。** 暴力枚举子串 `O(n^3)` → 固定起点向右扩 `O(n^2)` → 撞到重复字符 `c` 时，起点在旧起点到 `c` 上次位置之间的都会在同一处撞上 `c`，可整段跳过 → 每个下标进出窗口各一次，`O(n)`。

```python
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}          # 字符 -> 它最近一次出现的下标
    best = left = 0                    # 窗口是 s[left : right + 1]
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:   # ch 在窗口内出现过：左端直接跳过去
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

运行：`"abcabcbb"` → `3`，`"bbbbb"` → `1`，`"pwwkew"` → `3`，`""` → `0`，`"abba"` → `2`。

**复杂度。** 时间 `O(n)`；空间 `O(min(n, Σ))`，`Σ` 为字符集大小。

**易错点。**
- 条件必须是 `last[ch] >= left`：字典里留着已滑出窗口的旧位置，只写 `ch in last` 会让左端后退。`"abba"` 会错成 `3`（正确 `2`）。等价写法 `left = max(left, last[ch] + 1)`。
- 空串返回 `0`；`best` 在循环内更新，别漏掉最后一个窗口。

**追问。**
- 返回子串本身：更新答案时一并记起点，`best, start = right - left + 1, left`。
- 每个字符至多出现 `k` 次：改用 `Counter` 计数窗口，违反时 `while` 收缩左端；这是滑动窗口的通用三步「扩右 → 违规缩左 → 更新答案」。
- 字符集固定为 ASCII：`last = [-1] * 128`，用 `ord(ch)` 当下标，常数更小。

**同模式。** LC 159 / 340 至多 k 种字符、LC 424 替换后的最长重复字符、LC 76 最小覆盖子串。
