---
id: leetcode-c-endlesscheng-7c1ifr-dual-heap-shared-mutable-object-sync-recognition
node: design-simulation.dual-heap-shared-mutable-object-sync
type: cloze
anki: 1787272455180
tags: [concept-cloze, leetcode, recall, recognition]
---
当需要用两把按 {{c1::不同键}} 排序的堆维护同一批会被部分消耗或过期的元素时，应考虑让两把堆共享同一个 {{c2::可变对象}} 的引用，而不是各自存值的副本。

典型场景：一把堆按（价格,过期时间）排序取最优购买顺序，另一把堆单独按过期时间排序判断是否过期。

**Evidence**

银联-4. 设计自动售货机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F17.01%20-%20%E5%8F%8C%E5%A0%86%E5%85%B1%E4%BA%AB%E5%8F%AF%E5%8F%98%E5%AF%B9%E8%B1%A1%E5%90%8C%E6%AD%A5%EF%BC%88%E6%87%92%E5%88%A0%E9%99%A4%EF%BC%89)
