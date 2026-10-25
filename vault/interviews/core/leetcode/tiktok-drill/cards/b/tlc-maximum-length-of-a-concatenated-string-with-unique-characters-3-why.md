---
id: tlc-maximum-length-of-a-concatenated-string-with-unique-characters-3-why
node: b.maximum-length-of-a-concatenated-string-with-unique-characters
type: qa
step: 3
---
## Q
**LC 1239 串联字符串的最大长度**｜正确性

为什么要先过滤自带重复字母的字符串？为什么遍历 `masks` 时必须先取快照？不这样做会在哪个输入上出错？

## A
**不变量。** 处理完前 `i` 个字符串后，`masks` 恰好是「从前 `i` 个串里选出若干个（按原顺序）、且字母互不重复」能得到的全部字母集合；`best` 是其中的最大位数。

**为什么要过滤。** 掩码只记录「某个字母有没有」，不记录次数。字符串 `"aa"` 的掩码和 `"a"` 一样，只有一位。如果不过滤，它会被当成一个合法的串选进来，实际拼接结果里有两个 `a`，违反规则。

**反例：不过滤。** `arr = ["aa","bb"]`：
- 不过滤时 `"aa"` 的掩码是 `{a}`，`"bb"` 是 `{b}`，两者不相交，合并成 `{a, b}`，位数 `2`。
- 正确答案是 `0`：两个串都不能选。

**为什么要取快照。** 在 `for m in masks` 里执行 `masks.add(...)` 会改变集合大小，Python 抛 `RuntimeError: Set changed size during iteration`。先 `list(masks)` 取快照，遍历的是不变的旧集合，新加入的掩码留到下一个串再参与合并。

**为什么用位数而不是字符串长度。** 过滤之后每个串内部无重复，且合并要求不相交，所以拼接结果的长度恰好等于掩码里 `1` 的个数。
