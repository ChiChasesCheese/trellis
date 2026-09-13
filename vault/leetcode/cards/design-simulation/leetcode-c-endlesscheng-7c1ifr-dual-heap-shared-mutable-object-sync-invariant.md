---
id: leetcode-c-endlesscheng-7c1ifr-dual-heap-shared-mutable-object-sync-invariant
node: design-simulation.dual-heap-shared-mutable-object-sync
type: cloze
anki: 1787272455279
tags: [concept-cloze, invariant, leetcode, recall]
---
使用双堆共享可变对象方案时，读取或弹出堆顶前必须先 {{c1::循环剔除}} 已被标记为失效（如剩余数量为 0）的懒删除项，否则拿到的不是当前 {{c2::真正有效}} 的最值。

两把堆判断失效的标准必须一致，例如都以 remaining == 0 作为已删除标记。

**Evidence**

银联-4. 设计自动售货机 代码中的 while it.expire ... 和 while it.data ... 清理逻辑

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F17.01%20-%20%E5%8F%8C%E5%A0%86%E5%85%B1%E4%BA%AB%E5%8F%AF%E5%8F%98%E5%AF%B9%E8%B1%A1%E5%90%8C%E6%AD%A5%EF%BC%88%E6%87%92%E5%88%A0%E9%99%A4%EF%BC%89)
