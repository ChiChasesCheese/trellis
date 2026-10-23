---
id: hl-cx-hashmap-worst
node: foundations.complexity
type: qa
step: 15
---
## Q
`HashMap.get` 的平均和最坏复杂度分别是多少？最坏情况怎么来的？面试怎么答？

## A
平均 O(1)：键散到桶里，每个桶平均常数个元素。

最坏：所有键哈希到同一个桶。JDK 7 以前是链表，查找 O(n)；JDK 8 起桶太长（≥ 8 个且表够大）转成红黑树，最坏 **O(log n)**（前提键实现 `Comparable`，否则退化更厉害）。

这不只是理论：对外服务若用用户输入当键，攻击者可构造大量哈希冲突的键（hash flooding）。

面试答法：「`HashMap.get` 平均 O(1)，最坏 O(log n)（JDK 8+，冲突桶树化）。」两个都说。
