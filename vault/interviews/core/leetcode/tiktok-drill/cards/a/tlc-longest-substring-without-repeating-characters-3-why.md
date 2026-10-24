---
id: tlc-longest-substring-without-repeating-characters-3-why
node: a.longest-substring-without-repeating-characters
type: qa
step: 3
---
## Q
**LC 3 无重复字符的最长子串**｜正确性

滑动窗口解法里，判断条件为什么必须是 `last[ch] >= left`，而不能只写 `ch in last`？给出一个只写 `ch in last` 会出错的输入，并说明窗口应保持的不变量。

## A
**不变量。** 每一步结束时，`s[left : right + 1]` 里没有重复字符，而且以 `right` 结尾的无重复子串里，它是最长的那个。

**为什么要 `>= left`。** 字典 `last` 不会随左端移动而清理，里面留着**已经滑出窗口**的旧位置。只写 `ch in last` 时，一个在窗口外出现过的字符也会触发跳转，而 `left = last[ch] + 1` 可能让左端**往回退**，窗口里就混进了重复字符。

**反例 `"abba"`。** 正确答案是 `2`（`"ab"` 或 `"ba"`）。
- 读到第二个 `b`（下标 2）：左端跳到 2。
- 读到第二个 `a`（下标 3）：`a` 上次在下标 0，已不在窗口 `[2, 3]` 里。只写 `ch in last` 会把左端设成 `0 + 1 = 1`，窗口变成 `"bba"`，长度 3，答案错成 `3`。
- 加上 `>= left` 判断后不跳转，窗口是 `"ba"`，长度 2。

另一种等价写法是 `left = max(left, last[ch] + 1)`：左端只前进不后退，同样守住不变量。
