---
id: leetcode-c-endlesscheng-7c1ifr-dual-heap-shared-mutable-object-sync-template
node: design-simulation.dual-heap-shared-mutable-object-sync
type: cloze
anki: 1787272455379
tags: [concept-cloze, leetcode, recall, template]
---
在共享可变对象的双堆实现中，过期或消耗某个元素时应直接修改该 {{c1::共享 list/对象}} 的字段（如把剩余数量设为 0），而不是新建对象，这样另一把堆通过引用能立即感知，这种技术称为 {{c2::懒删除}}（lazy deletion）。

对应模板中的 record[2] = 0 / wrapper.data[2] = 0 写法。

**Evidence**

银联-4. 设计自动售货机 代码中的 lst[2] = 0 # 懒删除 注释

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F17.01%20-%20%E5%8F%8C%E5%A0%86%E5%85%B1%E4%BA%AB%E5%8F%AF%E5%8F%98%E5%AF%B9%E8%B1%A1%E5%90%8C%E6%AD%A5%EF%BC%88%E6%87%92%E5%88%A0%E9%99%A4%EF%BC%89)
