---
id: tlc-permutation-in-string-4-followup
node: a.permutation-in-string
type: qa
step: 4
---
## Q
**LC 567 字符串的排列**｜追问

面试官接着问：（1）返回 `s2` 里所有排列窗口的起点（LC 438）？（2）字符集是 Unicode，不是 26 个小写字母？（3）`s2` 是流式输入，读不进内存？分别怎么改。

## A
1. **所有起点**：同一个窗口，把 `return True` 改成记录起点。窗口 `[i - m, i - 1]` 在循环体开头检查，匹配就 `res.append(i - m)`；循环结束后再检查最后一个窗口，起点是 `len(s2) - m`。时间仍是 `O(n)`。
2. **大字符集**：`cnt` 换成 `dict[str, int]`（或 `defaultdict(int)`），用字符本身当键；`diff` 的更新逻辑完全不变，只是 `ord(c) - 97` 换成 `c`。空间 `O(|s1| 中的不同字符数)`，因为窗口外的键计数回到 `0` 也可以保留。
3. **流式**：算法只需要「最近 `m` 个字符」。用 `collections.deque(maxlen=m)` 保存窗口：新字符 `append` 时，`deque` 自动挤出最旧的字符，需要在 `append` 前先取 `window[0]` 作为要移出的字符。空间 `O(m)`，不依赖流的总长度。

**Python 提醒**：比较计数时不要写 `Counter(window) == Counter(s1)` 套在循环里，那是每步 `O(m)` 的重建；`collections.Counter` 在 3.10 之后相等比较会忽略值为 `0` 的键，但仍要遍历所有键，不如自己维护 `diff`。
