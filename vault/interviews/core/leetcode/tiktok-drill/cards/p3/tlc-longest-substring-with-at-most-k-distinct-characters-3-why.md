---
id: tlc-longest-substring-with-at-most-k-distinct-characters-3-why
node: p3.longest-substring-with-at-most-k-distinct-characters
type: qa
step: 3
---
## Q
**LC 340 至多包含 K 个不同字符的最长子串**｜正确性

为什么缩左端时计数减到 `0` 必须删键？如果只写 `count[out] -= 1` 而不删除，会出什么错？滑动窗口为什么不会漏掉最长的合法子串？

## A
**不变量。** 每个右端处理完后，`count` 恰好是窗口 `s[left : right + 1]` 里每种字符的出现次数（只含次数大于 `0` 的字符），`len(count)` 就是窗口里的不同字符数，并且 `len(count) <= k`。

**为什么必须删键。** `Counter` 中计数减到 `0` 的键仍然留在字典里，`len(count)` 会把已经不在窗口里的字符也算一种。种类数就此“虚高”，`while len(count) > k` 永远不会变成假，左端一直推进。
- `s = "eceba"`，`k = 2`：窗口走到 `"eceb"` 时，`count` 里有 `e, c, b`（3 种），缩左端把 `e` 减到 `1`、`c` 减到 `0`，不删 `c` 的话 `len(count)` 仍是 `3`，继续缩到 `left` 越过字符串末尾，抛 `IndexError: string index out of range`。
- 删键之后 `c` 消失，`len(count) = 2`，循环正确停止。

**为什么不漏。** 窗口合法时，以 `right` 结尾的最长合法子串的起点就是当前 `left`：`left` 之前的任何起点都会使窗口更宽，种类数不会更少（单调性），它们在更早的某一步已经被证明不合法。所以每个右端处理后，`right - left + 1` 就是以 `right` 结尾的最长合法子串，对所有右端取最大即答案。

**边界：`k = 0`。** 每加入一个字符，种类数变成 `1 > 0`，缩到窗口为空，`right - left + 1 = 0`，答案 `0`，不需要特判。
