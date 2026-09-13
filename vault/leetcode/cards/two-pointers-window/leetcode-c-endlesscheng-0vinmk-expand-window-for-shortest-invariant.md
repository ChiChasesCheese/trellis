---
id: leetcode-c-endlesscheng-0vinmk-expand-window-for-shortest-invariant
node: two-pointers-window.expand-window-for-shortest
type: cloze
anki: 1787268626837
tags: [concept-cloze, invariant, leetcode, recall]
---
扩张式滑窗中,内层while是在窗口已经{{c1::合法}}的前提下尝试收缩,以寻找更短的合法窗口。

while循环是在窗口已经合法的前提下尝试收缩,寻找更短解；收缩到窗口刚好不再合法(或left越界)时才停止

**Evidence**

§2.2 越长越合法/求最短/最小

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.03%20-%20%E6%89%A9%E5%BC%A0%E5%BC%8F%E4%B8%8D%E5%AE%9A%E9%95%BF%E6%BB%91%E7%AA%97%EF%BC%88%E6%B1%82%E6%9C%80%E7%9F%AD-%E6%9C%80%E5%B0%8F%EF%BC%89)
