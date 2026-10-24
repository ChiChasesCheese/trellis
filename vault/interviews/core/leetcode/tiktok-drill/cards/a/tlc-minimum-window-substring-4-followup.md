---
id: tlc-minimum-window-substring-4-followup
node: a.minimum-window-substring
type: qa
step: 4
---
## Q
**LC 76 最小覆盖子串**｜追问

面试官接着问：（1）`t` 的字符必须**按顺序**出现在窗口里（子序列，LC 727）怎么做？（2）并列最短时要返回所有窗口？（3）`s` 是不断到来的数据流，内存放不下全部时呢？

## A
1. **按顺序（最小窗口子序列）**：计数不再够用，因为顺序也要对。做法是找到一个能匹配完 `t` 的右端后，再**反向**从右往左匹配一次，把左端收紧到最大可能的位置；记录窗口后，从该窗口起点的下一格继续往右找。最坏 `O(mn)`。

```python
def min_window_subsequence(s: str, t: str) -> str:
    n, m = len(s), len(t)
    best_l, best_len = 0, n + 1
    i = 0
    while i < n:
        j = 0
        while i < n:                               # 正向：贪心匹配 t，停在最后一个字符匹配的位置
            if s[i] == t[j]:
                j += 1
                if j == m:
                    break
            i += 1
        if j < m:
            break
        end, j = i, m - 1
        while j >= 0:                              # 反向：从 end 往回贪心匹配，收紧起点
            if s[i] == t[j]:
                j -= 1
            i -= 1
        i += 1                                     # i 回到窗口起点
        if end - i + 1 < best_len:
            best_l, best_len = i, end - i + 1
        i += 1
    return "" if best_len > n else s[best_l : best_l + best_len]
```

`min_window_subsequence("abcdebdde", "bde")` → `"bcde"`，`min_window_subsequence("ab", "c")` → `""`。
2. **并列时返回全部**：记录最短长度 `best_len`，遇到相同长度就把窗口追加进列表，遇到更短就清空重来；上面的主解法只在严格更短时更新，所以返回的是最靠左的一个。
3. **数据流**：滑动窗口只需要窗口内的字符和计数表，不需要保留已经滑出窗口的部分。窗口内容用 `deque` 保存，右端到来时入队，覆盖后从队头弹出；内存取决于窗口的长度。覆盖 `t` 之前窗口会一直变长，最坏要保存到目前为止的所有字符，所以内存上界仍是 `O(m)`，只是不必把整个 `s` 一次性读入。

**Python 提醒**：`Counter` 读取不存在的键不会插入，但 `need[ch] -= 1` 会插入新键（值为负）；`Counter` 的减法运算符 `-` 会丢掉非正数项，`Counter(t) - Counter(window)` 为空表示窗口覆盖 `t`，但每次要 `O(Σ)`，不适合放进 `O(1)` 的热路径。
