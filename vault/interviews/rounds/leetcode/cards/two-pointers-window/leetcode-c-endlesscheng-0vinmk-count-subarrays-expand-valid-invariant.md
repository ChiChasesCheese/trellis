---
id: leetcode-c-endlesscheng-0vinmk-count-subarrays-expand-valid-invariant
node: two-pointers-window.count-subarrays-expand-valid
type: cloze
anki: 1787268627437
tags: [concept-cloze, invariant, leetcode, recall]
---
该计数法关注的是{{c1::left - 1}}的合法性,而不是left本身,因为内层while收缩后[left, right]恰好不合法。

内层while收缩直到[left, right]变得不合法(或left越界)为止；关注的是left-1的合法性,而不是left本身；固定right时,合法左端点数量等于left

**Evidence**

§2.3.2 越长越合法

[原文 ↗](obsidian://open?vault=lc&amp;file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.05%20-%20%E5%AE%9A%E9%95%BF%E6%89%A9%E5%BC%A0%E8%AE%A1%E6%95%B0%E6%B3%95%EF%BC%88%E8%B6%8A%E9%95%BF%E8%B6%8A%E5%90%88%E6%B3%95%EF%BC%89)
