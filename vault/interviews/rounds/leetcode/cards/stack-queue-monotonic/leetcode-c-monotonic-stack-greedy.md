---
id: leetcode-c-monotonic-stack-greedy
node: stack-queue-monotonic.monotonic-stack-greedy
type: cloze
anki: 1787102263662
tags: [concept-cloze, leetcode, recall]
---
在单调栈贪心构造字典序最小子序列时，只有当栈顶元素 {{c1::大于当前字符 ch 且 remainings[栈顶元素] {{c2::> 0}}}} 时才能弹出栈顶。

remainings[ch] 表示该字符在后续（当前位置之后）还会出现的次数；若栈顶字符后续不再出现（remainings==0），弹出它会导致该字符永久丢失，因此必须保留。

**Evidence**

栈顶元素 > ch 且后续还会出现，可安全弹出

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E5%8D%95%E8%B0%83%E6%A0%88%E8%B4%AA%E5%BF%83%E5%AD%90%E5%BA%8F%E5%88%97)
