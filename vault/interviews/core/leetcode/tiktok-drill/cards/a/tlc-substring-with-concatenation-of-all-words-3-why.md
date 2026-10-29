---
id: tlc-substring-with-concatenation-of-all-words-3-why
node: a.substring-with-concatenation-of-all-words
type: qa
step: 3
---
## Q
**LC 30 串联所有单词的子串**｜正确性

为什么要对 `0..w-1` 每个偏移各扫一遍？为什么"窗口里恰好 `k` 个单词且没有任何单词超额"就等价于"与 `words` 一致"？给出漏掉这些会出错的输入。

## A
**不变量。** 对固定的偏移，处理完 `right` 后，`have` 恰好是 `s[left : right + w]` 按单词切分后的计数，且对每个单词都有 `have[x] <= need[x]`。如果这时窗口恰有 `k` 个单词，而 `need` 的总数也是 `k`，各项又都不超额，那么各项必然都相等，窗口就是 `words` 的一个排列的拼接。

**为什么要所有偏移。** 一个串联子串可以从任意位置开始，不一定在 `0, w, 2w, ...` 上；起点按余数 `mod w` 分成 `w` 类，同一类内才能以 `w` 为步长滑动。

**反例 1：只扫偏移 0。** `s = "xfoobar"`，`words = ["foo","bar"]`：串联子串 `"foobar"` 从下标 1 开始。只扫偏移 0 返回 `[]`，扫全部偏移返回 `[1]`。

**反例 2：只判断单词是否出现过。** `s = "foofoo"`，`words = ["foo","bar"]`：两个单词都是 `words` 里的词，只看"属于不属于"会返回 `[0]`；计数后 `"foo"` 出现 2 次超过 `need["foo"] = 1`，要吐出，窗口始终凑不到 `"bar"`，返回 `[]`。
