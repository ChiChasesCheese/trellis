---
id: leetcode-q-buddy-strings-pattern
node: strings.string
type: qa
anki: 1787613694318
tags: [lc::859, leetcode, pattern, recall]
---
## Q
Buddy Strings：如何用 O(n) 判断能否通过一次交换让 s 变成 goal？

## A
先比较 Counter(s) 和 Counter(goal)，字符集不同直接 False。再找出所有 s[i] != goal[i] 的下标存入 diff：若 len(diff) == 2 且这两个位置互为对方字符即可返回 True；若 len(diff) == 0（s 已等于 goal），需要 s 中存在重复字符（len(s) != len(set(s))）才能通过交换任意一对相同字符使结果不变；其他情况均为 False。

**Evidence**

def buddyStrings(self, s, goal): if Counter(s) != Counter(goal): return False; diff = [i for i in range(len(s)) if s[i] != goal[i]]; return len(diff) == 2 or (len(diff) == 0 and len(s) != len(set(s)))

[原文 ↗](obsidian://open?vault=lc&file=questions%2F859%20-%20Buddy%20Strings)
