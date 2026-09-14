---
id: leetcode-q-isomorphic-strings-pattern
node: strings.string
type: qa
anki: 1787613691837
tags: [lc::205, leetcode, pattern, recall]
---
## Q
如何判断两个字符串是否同构（isomorphic）？核心技巧是什么？

## A
同构要求字符是双射映射（一一对应），不能只检查单方向映射。两种写法：
1. 集合法：`len(set(zip(s,t))) == len(set(s)) == len(set(t))`，即字符对种类数、s 的字符种类数、t 的字符种类数三者相等，天然保证双射。
2. 哈希表法：遍历时用 `cvt[ch1]=ch2` 记录映射，若已存在且映射值不同则返回 False；最后再检查 `len(cvt.values()) == len(set(cvt.values()))` 确保没有多个 key 映射到同一个 value（防止非双射）。

**Evidence**

return len(set(zip(s, t))) == len(set(s)) == len(set(t)) ... return len(cvt.values()) == len(set(cvt.values()))

[原文 ↗](obsidian://open?vault=lc&file=questions%2F205%20-%20Isomorphic%20Strings)
