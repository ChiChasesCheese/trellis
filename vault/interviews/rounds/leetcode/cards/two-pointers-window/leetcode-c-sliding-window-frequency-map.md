---
id: leetcode-c-sliding-window-frequency-map
node: two-pointers-window.sliding-window-frequency-map
type: cloze
anki: 1787102263859
tags: [concept-cloze, leetcode, recall]
---
在 Sliding Window With Frequency Map 模板中，right 右移时先 {{c1::freq[s[right]] += 1}}，一旦窗口不满足条件就用 while 循环收缩 left；这是因为频率条件具有单调性——{{c2::left 前进只会让条件更满足，不会变得更不满足}}，所以可以用 while 而不用担心收缩过头后条件又被破坏。

该单调性保证了双指针每次只需要单向移动即可维护窗口合法性，是滑动窗口能用 O(n) 而非暴力 O(n^2) 的关键前提。

**Evidence**

Invariants: 频率条件单调性：left前进时只会使条件更满足（不会违反）；Template 中 for right 先更新 freq，再 while 收缩 left。

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%E9%A2%91%E6%AC%A1%E8%A1%A8)
