---
id: leetcode-q-lexicographically-smallest-palindromic-permutation-greater-than-target-pattern
node: arrays-hash-prefix.enumeration
type: qa
anki: 1788391211199
tags: [lc::3734, leetcode, pattern, recall]
---
## Q
如何构造「字符可重排」且需满足回文 + 严格大于 target 的最小排列？(如 LC 3734)

## A
先用 Counter 统计字符频次，若奇数频次字符数>1则无解；否则记录唯一奇数字符为 mid，其余频次减半，只需构造前半部分 half，答案为 half+mid+half[::-1]。构造 half 时贪心比较 target 前半 tl：
1) 先尝试「与 tl 完全一致」的候选：若剩余频次能凑出 tl，且 mid+tl反转 > target 后半 tr，则直接返回 tl+mid+tl[::-1]；
2) 否则逐位扫描 target，在位置 i 尝试放入与 target[i] 相同的字符，检查剩余字符能拼出的最大后缀 right_max 是否 > tl[i+1:]（能兜住则可行）；若不行，则在剩余字符里找比 target[i] 大的最小字符 bigger，放入后其余字符降序填充作为最大化后缀，然后立即 break 结束构造。
本质是「逐位贪心 + 相等/更大两条路径」的字符串构造范式，可迁移到其它'排列/重排 + 大于目标 + 字典序最小'的题目。

**Evidence**

for i, c in enumerate(target): if cnt[c] > 0: ... right_max = ...sorted(cnt.elements(), reverse=True)... if right_max > tl[i+1:]: ...continue; else 找 bigger 并 break — 以及前置的 '候选1：左半边跟 target 完全一致' 分支

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3734%20-%20Lexicographically%20Smallest%20Palindromic%20Permutation%20Greater%20Than%20Target)
