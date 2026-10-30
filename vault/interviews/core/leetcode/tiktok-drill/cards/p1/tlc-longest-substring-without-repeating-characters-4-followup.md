---
id: tlc-longest-substring-without-repeating-characters-4-followup
node: p1.longest-substring-without-repeating-characters
type: qa
step: 4
---
## Q
**LC 3 无重复字符的最长子串**｜追问

面试官接着问：（1）如果要返回**子串本身**而不只是长度？（2）如果约束放宽成「每个字符最多出现 `k` 次」？（3）如果字符集固定是 ASCII，能不能不用字典？分别怎么改。

## A
1. **返回子串**：更新答案时同时记下起点，`if right - left + 1 > best: best, start = right - left + 1, left`，最后返回 `s[start : start + best]`。用元组同时赋值，避免先改 `best` 再用旧值的顺序错误。
2. **每个字符至多 `k` 次**：「跳到上次位置的下一位」不再成立，因为窗口里可以合法地有重复。改成**计数窗口**：`count = Counter()`，右端加入后若 `count[ch] > k`，就 `while` 收缩左端、逐个减计数，直到 `count[ch] == k`。左端仍只前进，所以还是 `O(n)`。这是滑动窗口的通用形态：**扩右端 → 违反约束就缩左端 → 更新答案**。
3. **固定字符集**：用长度 128 的列表代替字典，`last = [-1] * 128`，用 `ord(ch)` 当下标。常数更小，空间 `O(1)`；但字符集一旦变成 Unicode 就不能用，字典版更通用。面试里先写字典版，再提这个优化。

**Python 提醒**：`Counter` 里计数减到 0 的键不会自动删除；若要用 `len(count)` 表示「窗口里有几种字符」，减到 0 时要 `del count[ch]`。
