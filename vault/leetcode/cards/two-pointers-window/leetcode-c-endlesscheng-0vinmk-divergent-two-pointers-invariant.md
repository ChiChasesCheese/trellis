---
id: leetcode-c-endlesscheng-0vinmk-divergent-two-pointers-invariant
node: two-pointers-window.divergent-two-pointers
type: cloze
anki: 1787268628638
tags: [concept-cloze, invariant, leetcode, recall]
---
背向双指针的不变量是:两指针从同一起点出发后,左右间距{{c1::单调增大且永不相遇}}。

左指针只减小,右指针只增大,二者的间距单调增大,不会相遇；每一步先检查左右是否越界,再检查条件是否继续成立

**Evidence**

§3.4 背向双指针

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.09%20-%20%E8%83%8C%E5%90%91%E5%8F%8C%E6%8C%87%E9%92%88)
